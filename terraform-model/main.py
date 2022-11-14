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


if os.stat(".auto.tfvars.json").st_size == 0 or os.stat(".auto.tfvars.json").st_size == 53:
    dict_variables = {"security_groups" : {}, "instances" : {}}
    contador = 0
else:
    dict_variables = json.load(open(".auto.tfvars.json"))
    contador = len(dict_variables["security_groups"])

@click.group()
def mycommands():
    pass

@click.command()
@click.option('--decision', prompt = '\033[1;32m\n-------------------------------------------------------------\nWelcome to the Terraform Application, what do you want to do?\n-------------------------------------------------------------\n\n 1. Create a new instance\n 2. Delete an instance\n 3. List all instances\n 4. List security groups\n 5. Delete security group \n 6. Apply all changes\n 7. Create user \n 8. Delete user \n 9. List all users \n 10. Exit \n\n', 
type=click.Choice(['1', '2', '3', '4', '5', '6','7','8','9','10'], case_sensitive=False), help = 'The option you choose.')

def write_json(decision):
    global contador

    # ---------------------------------- CREATE INSTANCE ---------------------------------- #
    if decision == "1":
        contador += 1
        dict_instance_key = 'instance_' + str(contador)
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

            if security_name in dict_variables["security_groups"]:
                print("Security group already exists, adding this new instance to it\n")
                time.sleep(0.8)
                dict_variables["security_groups"][security_name]["instances_applied"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "aws-region" : region}})
                dict_variables["instances"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "aws-region" : region}})
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

            security_description = input("Description: \n")
            security_ingress = input("Ingress description: \n")
            security_from_port = input("From port: \n")
            security_to_port = input("To port: \n")
            security_protocol = input("Protocol: \n")
            security_cidr_blocks = input("CIDR blocks: \n")


            if security_name not in dict_variables["security_groups"]:
                dict_variables["instances"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "aws-region" : region, "security_name" : security_name}})
                dict_variables["security_groups"].update({security_name : {"security_name": security_name, "security_description" : security_description, "security_ingress" : security_ingress, "security_from_port" : security_from_port, "security_to_port" : security_to_port, "security_protocol" : security_protocol, "security_cidr_blocks" : [security_cidr_blocks], "instances_applied": {dict_instance_key: {"instance_name" : name, "instance_type" : type, "aws-region" : region}}}})
            else:
                dict_variables["instances"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "aws-region" : region, "security_name" : security_name}})
                dict_variables["security_groups"][security_name]["instances_applied"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "aws-region" : region}})


        if security == "n":
            print("Applying default security group\n")
            time.sleep(0.5)

            if "standard" not in dict_variables["security_groups"]:
                dict_variables["instances"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "aws-region" : region, "security_name" : "standard"}})
                dict_variables["security_groups"].update({"standard" : {"security_name" : "standard", "security_description" : "Default security group", "security_ingress" : "Default ingress", "security_from_port" : "22", "security_to_port" : "22", "security_protocol" : "tcp", "security_cidr_blocks" : ["1.0.0.0/16"], "instances_applied": {dict_instance_key : {"instance_name": name, "instance_type": type, "aws-region": region}}}})
            else:
                dict_variables["instances"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "aws-region" : region, "security_name" : "standard"}})
                dict_variables["security_groups"]["standard"]["instances_applied"].update({dict_instance_key : {"instance_name": name, "instance_type": type, "aws-region": region}})
   
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
        for key in dict_variables["instances"]:
            print(key)

        time.sleep(0.8)
        instance_id = input("Enter the instance number to delete: \n")

        dict_key = "instance_" + str(instance_id)

        instances_aws =[]

        for each in ec2re.instances.all():
            instances_aws.append(each.tags[0]["Value"])
        
        if instance_id == "":
            print("No instance ID entered. Please try again.")
            time.sleep(0.8)
            mycommands()
        else:
            for key in dict_variables["instances"]:
                if dict_key not in dict_variables["instances"]:
                    print("Invalid instance ID. Please try again.\n")
                    time.sleep(0.8)
                    mycommands()

                if dict_variables["instances"][dict_key]["instance_name"] in instances_aws:
                    dict_variables["security_groups"][dict_variables["instances"][dict_key]["security_name"]]["instances_applied"].pop(dict_key)
                    dict_variables["instances"].pop(dict_key)
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
                        for key in dict_variables["security_groups"]: 
                            dict_variables["security_groups"][dict_variables["instances"][dict_key]["security_name"]]["instances_applied"].pop(dict_key)
                            dict_variables["instances"].pop(dict_key)
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
        if dict_variables["instances"] == {}:
            print("No instances created yet. \n")
        else:
            for key in dict_variables["instances"]:
                print("ID: " + key + "| Name: " + dict_variables["instances"][key]["instance_name"] + "| Type: " + dict_variables["instances"][key]["instance_type"] + "| Region: " + dict_variables["instances"][key]["aws-region"] + "\n")
    
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
        for key in dict_variables["security_groups"]:
            print(dict_variables["security_groups"][key]["security_name"])
        print("\n")

        
        print("Existing security groups in AWS: \n")
        time.sleep(0.4)
        groups = []

        for each in ec2re.security_groups.all():
            groups.append(each.group_name)
            print("ID: " + each.id + " " + "| Name: " + each.group_name + "\n")
         
        sg = input("Enter the security group name to list the rules: \n")

        if sg == "":
            print("Returning to main menu...")
            time.sleep(0.8)
            mycommands()
        
        if sg in groups:
            print("Showing rules... \n")
            time.sleep(0.4)
            for rule in each.ip_permissions:
                print("Rule: " + str(rule) + "\n")
            print("-------------------------------------------------------------\n")
            time.sleep(0.8)
            mycommands()
        else:
            print("\nSecurity group not found in AWS!")
            time.sleep(0.4)
            mycommands()

        time.sleep(0.8)
        print("\n")
        mycommands()

    # ---------------------------------- DELETE SECURITY GROUP ---------------------------------- #
    if decision == "5":
        print("Existing security groups in Terraform file: \n")
        for key in dict_variables["security_groups"]:
            print(dict_variables["security_groups"][key]["security_name"])
        print("\n")

        sgs = []

        for each in ec2re.security_groups.all():
            sgs.append(each.group_name)

        print("WARNING: All instances attached to the security group will be deleted. \n")
        sg = input("Enter the security group name to delete OR nothing to come back: \n")

        if sg == "":
            print("Returning to main menu...")
            time.sleep(0.8)
            mycommands()
        
        if sg in dict_variables["security_groups"]:
            if sg in sgs:
                dict_variables["security_groups"].pop(sg)
                for key in list(dict_variables["instances"]):
                    if dict_variables["instances"][key]["security_name"] == sg:
                        dict_variables["instances"].pop(key)
                json_object = json.dumps(dict_variables, indent = 4)

                time.sleep(0.4)

                print("Deleting the security group from JSON file: " + sg + "\n")

                for i in tqdm(range(10)):
                    time.sleep(0.2)

                with open('.auto.tfvars.json', 'w') as f:
                    f.write(json_object)
                
                print("\nSecurity group deleted from the JSON successfully. \n")

                aws = input("Do you want to delete it from AWS? (y/n) \n")
                
                if aws == "y":
                    print("Deleting the security group from AWS...\n")
                    os.system('terraform apply -var-file=secret.tfvars')
                    print("Security group deleted from AWS successfully!\n")
                    time.sleep(0.8)
                    mycommands()

                elif aws == "n":
                    print("Returning to main menu...")
                    time.sleep(0.8)
                    mycommands()

                time.sleep(0.8)
                mycommands()

            else:
                print("Security group not found in AWS, it could not exist or it was already deleted.\n")
                mycommands()
        else:
            print("\nSecurity group not found in Terraform file!")
            time.sleep(0.4)
            mycommands()

        time.sleep(0.8)
        print("\n")
        mycommands()

    # ---------------------------------- APPLY CHANGES ---------------------------------- #
    if decision == "6":
        print("Applying all changes...")
        time.sleep(0.8)
        os.system('terraform init')
        os.system('terraform plan -var-file=secret.tfvars')
        os.system('terraform apply -var-file=secret.tfvars')
        mycommands()

    # ---------------------------------- CREATE USER ---------------------------------- #
    if decision == "7":
        
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
    
    if decision == "8":
        print("Deleting user...")
        time.sleep(0.8)
        #os.system('terraform
        mycommands()
    
    # ---------------------------------- LIST ALL USERS ---------------------------------- #
    if decision == "9":
        print("Listing all users...")
        time.sleep(0.8)
        #os.system('terraform

    # ---------------------------------- EXIT ---------------------------------- #
    if decision == "10":
        print("Exiting...")
        time.sleep(0.5)
        exit()

mycommands.add_command(write_json)

if __name__ == '__main__':
    mycommands()



