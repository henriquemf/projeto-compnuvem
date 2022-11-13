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


if os.stat(".auto.tfvars.json").st_size == 0 or os.stat(".auto.tfvars.json").st_size == 34:
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
@click.option('--decision', prompt = '\033[1;32m\n-------------------------------------------------------------\nWelcome to the Terraform Application, what do you want to do?\n-------------------------------------------------------------\n\n 1. Create a new instance\n 2. Delete an instance\n 3. List all instances\n 4. List security groups\n 5. Apply all changes\n 6. Create user \n 7. Delete user \n 8. List all users \n 9. Exit \n\n', 
type=click.Choice(['1', '2', '3', '4', '5', '6','7','8','9'], case_sensitive=False), help = 'The option you choose.')

def write_json(decision):
    global contador

    # ---------------------------------- CREATE INSTANCE ---------------------------------- #
    if decision == "1":
        contador += 1
        print("Avaiable regions to use: \n\n  1 - us-east-1 \n  2 - us-east-2 \n")
        region = input("Enter the region you want to create your instance: \n")
        name = input("Enter the name of the instance: \n")
        type = input("Enter the instance type [t2.micro, t2.nano]: \n")
        if type != "t2.micro" and type != "t2.nano":
            print("Invalid instance type, please try again")
            mycommands()
        
        if region == "1":
            region = 'us-east-1'
        elif region == "2":
            region = 'us-east-2'
        else:
            print("Invalid region, please try again")
            mycommands()

        security = input("Do you want to create a security group? (y/n) \n")
        if security == "y":
            security_name = input("Name of the security group: \n")

            if security_name == "standard" or security_name == "default":
                print("Invalid name, please try again\n")
                mycommands()

            security_groups = ec2re.security_groups.all()
            for security_group in security_groups:
                if security_group.group_name == security_name:
                    print("Security group already exists, please try again")
                    mycommands()
            
            for key in range(1, len(dict_variables["instance_variables"])):
                if dict_variables["instance_variables"]["instance_" + str(key)]["security_group"]["security_name"] == security_name:
                    print("Security group already exists, please try again")
                    mycommands()

            security_description = input("Description: \n")
            security_ingress = input("Ingress description: \n")
            security_from_port = input("From port: \n")
            security_to_port = input("To port: \n")
            security_protocol = input("Protocol: \n")
            security_cidr_blocks = input("CIDR blocks: \n")

            dict_security_groups = {"security_name" : security_name, "security_description" : security_description, "security_ingress" : security_ingress, "security_from_port" : security_from_port, "security_to_port" : security_to_port, "security_protocol" : security_protocol, "security_cidr_blocks" : [security_cidr_blocks]}
            dict_variables["instance_variables"].update({'instance_' + str(contador) : {"instance_name" : name, "instance_type" : type, "aws-region": region, "security_group" : dict_security_groups}})

        if security == "n":
            print("Applying default security group\n")
            time.sleep(0.5)
            
            dict_security_groups = {"security_name": "standard", "security_description": "Allow inbound traffic", "security_ingress": "SSH", "security_from_port": 22, "security_to_port": 22, "security_protocol": "tcp", "security_cidr_blocks": ["20.0.0.0/16"]}
            dict_variables["instance_variables"].update({'instance_' + str(contador): {'instance_name': name, 'instance_type': type, "aws-region": region, 'security_group': dict_security_groups}})

        json_object = json.dumps(dict_variables, indent = 4)

        time.sleep(0.4)
        print("Creating instance in the JSON file\n")

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
        instance_id = input("Enter the instance number to delete: \n")

        dict_key = "instance_" + str(instance_id)
        
        if instance_id == "":
            print("No instance ID entered. Please try again.")
            time.sleep(0.8)
            mycommands()
        
        elif dict_key not in dict_variables["instance_variables"]:
            print("Invalid instance ID. Please try again.\n")
            time.sleep(0.8)
            mycommands()

        for each in ec2re.instances.all():
            print("ID: " + each.id + " " + "| Name: " + each.tags[0]["Value"] + " " + "| State: " + each.state["Name"] + " " +
            "| Type: " + each.instance_type +  "| Region: "+  each.placement['AvailabilityZone'] + "\n")
            if each.tags[0]['Value'] == dict_variables["instance_variables"][dict_key]["instance_name"]:
                dict_variables["instance_variables"].pop(dict_key)
                json_object = json.dumps(dict_variables, indent = 4)

                time.sleep(0.4)

                print("Deleting the instance with ID from JSON file: " + instance_id + "\n")

                for i in tqdm(range(10)):
                    time.sleep(0.2)

                with open('.auto.tfvars.json', 'w') as f:
                    f.write(json_object)
                
                print("\nInstance deleted from the JSON successfully. \n")
                
                print("Deleting the instance from AWS...\n")
                os.system('terraform apply -var-file=secret.tfvars')
                
                print("Instance deleted from AWS successfully!")
                time.sleep(0.8)
                mycommands()
            
            else:
                print("Instance not found in AWS, it could not exist or it was already deleted.\n")
                final_decision = input("Do you want to delete it from the JSON file? (y/n) \n")
                if final_decision == "y":
                    dict_variables["instance_variables"].pop(dict_key)
                    json_object = json.dumps(dict_variables, indent = 4)

                    time.sleep(0.4)

                    print("Deleting the instance with ID from JSON file: " + instance_id + "\n")

                    for i in tqdm(range(10)):
                        time.sleep(0.2)

                    with open('.auto.tfvars.json', 'w') as f:
                        f.write(json_object)
                    
                    print("\nInstance deleted from the JSON successfully. \n")
                    time.sleep(0.8)
                    mycommands()
                else:
                    time.sleep(0.8)
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
            "| Type: " + each.instance_type +  "| Region: "+  each.placement['AvailabilityZone'] + "\n")

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

        for each in ec2re.security_groups.all():
            print("| Name: " + each.group_name + "\n")
         
        sg = input("Enter the security group name to list the rules: \n")

        if sg == "":
            print("Returning to main menu...")
            time.sleep(0.8)
            mycommands()
        else:
            for each in ec2re.security_groups.all():
                if each.group_name == sg:
                    print("ID: " + each.id + " " + "| Name: " + each.group_name + "\n")
                    for rule in each.ip_permissions:
                        print("Rule: " + str(rule) + "\n")
                else:
                    print("\nSecurity group not found in AWS!")
                    time.sleep(0.4)
                    mycommands()

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
        
        print('\n-------------------------------------------------------------\n')
        username = input("Enter the username: \n")

        if username == "":
            print("No username entered. Please try again.")
            time.sleep(0.8)
            mycommands()
        
        else:
            dict_variables["user_variables"] = {}
            dict_variables["user_variables"].update({username: {}})
            print("Creating user " + username + "...\n")
            
            print("User created successfully!")
            time.sleep(0.8)
            mycommands()


        #os.system('terraform apply -var-file=secret.tfvars')
        mycommands()

    # ---------------------------------- DELETE USER ---------------------------------- #
    
    if decision == "7":
        print("Deleting user...")
        time.sleep(0.8)
        #os.system('terraform
        mycommands()
    
    # ---------------------------------- LIST ALL USERS ---------------------------------- #
    if decision == "8":
        print("Listing all users...")
        time.sleep(0.8)
        #os.system('terraform

    # ---------------------------------- EXIT ---------------------------------- #
    if decision == "9":
        print("Exiting...")
        time.sleep(0.5)
        exit()

mycommands.add_command(write_json)

if __name__ == '__main__':
    mycommands()



