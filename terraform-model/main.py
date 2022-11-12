import click
import json
import os
import time
from tqdm import tqdm
import boto3

contador = 0
session = boto3.Session(profile_name='default', region_name='us-east-1')
ec2client = session.client('ec2')
ec2re = session.resource('ec2')


if os.stat(".auto.tfvars.json").st_size == 0:
    dict_variables = {"instance_variables" : {}}
    dict_security_groups = {"security_group" : {}}
    contador = 0
else:
    dict_variables = json.load(open(".auto.tfvars.json"))
    contador = len(dict_variables["instance_variables"])

@click.group()
def mycommands():
    pass

@click.command()
@click.option('--decision', prompt = '\n-------------------------------------------------------------\nWelcome to the Terraform Application, what do you want to do?\n-------------------------------------------------------------\n\n 1. Create a new instance\n 2. Delete an instance\n 3. List all instances\n 4. List security groups\n 5. Apply all changes\n 6. Create user \n 7. Exit \n\n', 
type=click.Choice(['1', '2', '3', '4', '5', '6','7'], case_sensitive=False), help = 'The option you choose.')

def write_json(decision):
    global contador

    # ---------------------------------- CREATE INSTANCE ---------------------------------- #
    if decision == "1":
        contador += 1
        name = input("Enter the name of the instance: \n")
        type = input("Enter the instance type [t2.micro, t2.nano]: \n")
        if type != "t2.micro" and type != "t2.nano":
            print("Invalid instance type, please try again")
            mycommands()

        security = input("Do you want to create a security group? (y/n) \n")
        if security == "y":
            security_name = input("Name of the security group: \n")
            security_description = input("Description: \n")
            security_ingress = input("Ingress description: \n")
            security_from_port = input("From port: \n")
            security_to_port = input("To port: \n")
            security_protocol = input("Protocol: \n")
            security_cidr_blocks = input("CIDR blocks: \n")

            dict_security_groups = {"security_name" : security_name, "security_description" : security_description, "security_ingress" : security_ingress, "security_from_port" : security_from_port, "security_to_port" : security_to_port, "security_protocol" : security_protocol, "security_cidr_blocks" : [security_cidr_blocks]}
            dict_variables["instance_variables"].update({'instance_' + str(contador) : {"instance_name" : name, "instance_type" : type, "security_group" : dict_security_groups}})

        if security == "n":
            print("Applying default security group\n")
            time.sleep(0.5)
            dict_security_groups = {"security_name": "standard", "security_description": "Allow inbound traffic", "security_ingress": "SSH", "security_from_port": 22, "security_to_port": 22, "security_protocol": "tcp", "security_cidr_blocks": ["20.0.0.0/16"]}
            dict_variables["instance_variables"].update({'instance_' + str(contador): {'instance_name': name, 'instance_type': type, 'security_group': dict_security_groups}})

        json_object = json.dumps(dict_variables, indent = 4)

        time.sleep(0.4)
        print("Creating instance...\n")

        for i in tqdm(range(10)):
            time.sleep(0.2)

        with open('.auto.tfvars.json', 'w') as f:
            f.write(json_object)
        
        print("Instance created successfully!\n")
        time.sleep(0.2)
        
        apply = input('\nDo you want to apply the changes right now? (y/n):  ')
        if apply == 'y':
            os.system('terraform init')
            os.system('terraform plan -var-file=secret.tfvars')
            os.system('terraform apply -var-file=secret.tfvars')
        else:
            mycommands()
    
    # ---------------------------------- DELETE INSTANCE ---------------------------------- #
    if decision == "2":
        
        print('\n-------------------------------------------------------------\n')
        print('List of instances: \n')
        for key in dict_variables["instance_variables"]:
            print(key)

        time.sleep(0.8)
        instance_id = input("Enter the instance ID to delete: \n")

        dict_key = "instance_" + str(instance_id)
        
        if instance_id == "":
            print("No instance ID entered. Please try again.")
            time.sleep(0.8)
            mycommands()

        else:

            if  dict_key in dict_variables["instance_variables"].keys():

                delete = input('\nDo you want to delete the instance from AWS? (y/n): ')

                if delete == 'y':
                    
                    if ec2re.instances.all().tags[0]["Value"] == dict_variables["instance_variables"][dict_key]["instance_name"]:
                        if ec2re.instances.all().state['Name'] != 'terminated':
                            dict_variables["instance_variables"].pop(dict_key)
                            json_object = json.dumps(dict_variables, indent = 4)

                            time.sleep(0.4)

                            print("Deleting the instance with ID: " + instance_id + "\n")

                            for i in tqdm(range(10)):
                                time.sleep(0.2)

                            with open('.auto.tfvars.json', 'w') as f:
                                f.write(json_object)
                            
                            print("\nInstance deleted from the JSON successfully. \n")
                            
                            os.system('terraform apply -var-file=secret.tfvars')
                            print("Instance deleted from AWS successfully!")
                            time.sleep(0.8)
                            mycommands()
                        else:
                            print("Instance already deleted from AWS!")
                            time.sleep(0.4)
                            mycommands()
                    else:
                        print("Instance not found in AWS!")
                        time.sleep(0.4)
                        mycommands()
                elif delete == 'n':
                    print("Deleting the instance with ID: " + instance_id + "\n")

                    for i in tqdm(range(10)):
                        time.sleep(0.2)

                    with open('.auto.tfvars.json', 'w') as f:
                        f.write(json_object)
                    
                    print("\nInstance deleted from the JSON successfully. \n")

                    mycommands()
            
            else:
                if ec2re.instances.all().state['Name'] == 'terminated' and dict_variables["instance_variables"][dict_key]["instance_name"]:
                    print("Instances already deleted from AWS!")
                    time.sleep(0.4)
                    mycommands()
                else:
                    print("Instance not found in AWS!")
                    time.sleep(0.4)
                    mycommands()

        mycommands()

    # ---------------------------------- LIST INSTANCES ---------------------------------- #
    if decision == "3":
        print("\n-------------------------------------------------------------\n")
        print("List of instances in Terraform file: \n")

        time.sleep(0.8)
        if dict_variables["instance_variables"] == {}:
            print("No instances created yet. \n")
        else:
            for key in dict_variables["instance_variables"]:
                print(key)
    
        print("-------------------------------------------------------------\n")
        print("List of instances in AWS: \n")
        time.sleep(0.4)

        for each in ec2re.instances.all():
            print("ID: " + each.id + " " + "| Name: " + each.tags[0]["Value"] + " " + "| State: " + each.state["Name"] + " " +
            "| Type: " + each.instance_type + "\n")

        print("-------------------------------------------------------------\n")
        time.sleep(0.8)
        mycommands()

    # ---------------------------------- LIST SECURITY GROUPS ---------------------------------- #
    if decision == "4":
        print("Existing security groups in Terraform file: \n")
        for key in dict_variables["instance_variables"]:
            print(dict_variables["instance_variables"][key]["security_group"]["security_name"])
        print("\n")

        print("Existing security groups in AWS: \n")
        time.sleep(0.4)
        response_sec = ec2client.describe_security_groups()
        for i in response_sec.get('SecurityGroups'):
            print(i.get('GroupName'))
        time.sleep(0.8)
        print("\n")
        mycommands()

    # ---------------------------------- APPLY CHANGES ---------------------------------- #
    if decision == "5":
        print("Applying all changes...")
        time.sleep(0.8)
        os.system('terraform init')
        os.system('terraform plan -var-file=secret.tfvars')
        os.system('terraform apply -var-file=secret.tfvars')
        mycommands()

    # ---------------------------------- CREATE USER ---------------------------------- #
    if decision == "6":
        print("Creating user...")
        time.sleep(0.8)
        #os.system('terraform apply -var-file=secret.tfvars')
        mycommands()
    
    # ---------------------------------- EXIT ---------------------------------- #
    if decision == "7":
        print("Exiting...")
        time.sleep(0.5)
        exit()

mycommands.add_command(write_json)

if __name__ == '__main__':
    mycommands()



