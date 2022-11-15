import click
import json
import os
import time
from tqdm import tqdm
import boto3

contador = 0
session = boto3.Session(profile_name='default', region_name='us-east-1')
ec2client = session.client('ec2')
ec2iam = session.client('iam')
ec2re = session.resource('ec2')

if os.stat(".auto.tfvars.json").st_size == 0 or os.stat(".auto.tfvars.json").st_size == 71:
    dict_variables = {"security_groups" : {}, "instances" : {}, "users" : []}
    contador = 0
else:
    dict_variables = json.load(open(".auto.tfvars.json"))
    contador = len(dict_variables["security_groups"])

@click.group()
def mycommands():
    pass

@click.command()
@click.option('--decision', prompt = '\033[1;32m\n-------------------------------------------------------------\nWelcome to the Terraform Application, what do you want to do?\n-------------------------------------------------------------\n\n 1. Create a new instance\n 2. Delete an instance\n 3. List all instances\n 4. Add rules to Security Group \n 5. List security groups\n 6. Delete security group \n 7. Apply all changes\n 8. Create user \n 9. Delete user \n 10. List all users \n 11. Exit \n\n', 
type=click.Choice(['1', '2', '3', '4', '5', '6','7','8','9','10','11'], case_sensitive=False), help = 'The option you choose.')

def program(decision):
    global contador

    # ---------------------------------- CREATE INSTANCE ---------------------------------- #
    if decision == "1":
        contador += 1
        dict_instance_key = 'instance_' + str(contador)
        print("Avaiable zones to use: \n")
        a_zones = []
        for zone in ec2client.describe_availability_zones()['AvailabilityZones']:
            a_zones.append(zone['ZoneName'])
            print(zone['ZoneName'])
        region = input("Enter the region you want to create your instance: \n")
        name = input("Enter the name of the instance: \n")
        type = input("Enter the instance type [t2.micro, t2.nano]: \n")
        if type != "t2.micro" and type != "t2.nano":
            print("Invalid instance type, please try again")
            mycommands()
        
        if region not in a_zones:
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
                dict_variables["instances"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "aws-region" : region, "security_name" : security_name}})

                time.sleep(0.4)
                print("Creating instance in the JSON file\n")
                write_json(dict_variables)
                
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
                dict_variables["security_groups"].update({security_name : {"security_name": security_name, 
                "security_description" : security_description, "security_ingress" : [{"rules": {"description": security_ingress, 
                "from_port" : security_from_port, "to_port" : security_to_port, "protocol" : security_protocol, 
                "ipv6_cidr_blocks": None, "prefix_list_id": None, "self": None,"security_groups": None, 
                "cidr_blocks" : [security_cidr_blocks]}}]}})
            else:
                dict_variables["instances"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "aws-region" : region, "security_name" : security_name}})

        if security == "n":
            print("Applying default security group\n")
            time.sleep(0.5)

            if "standard" not in dict_variables["security_groups"]:
                dict_variables["instances"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "aws-region" : region, "security_name" : "standard"}})
                dict_variables["security_groups"].update({"standard" : {"security_name": "standard", 
                "security_description" : "Allow 22", "security_ingress" : [{"rules": {"description": "Allow 22", 
                "from_port" : "22", "to_port" : "22", "protocol" : "tcp", 
                "ipv6_cidr_blocks": None, "prefix_list_id": None, "self": None,"security_groups": None, 
                "cidr_blocks" : ["0.0.0.0/16"]}}]}})
            else:
                dict_variables["instances"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "aws-region" : region, "security_name" : "standard"}})

        time.sleep(0.4)
        print("Creating instance in the JSON file\n")

        write_json(dict_variables)
        
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
                    dict_variables["instances"].pop(dict_key)

                    time.sleep(0.4)

                    print("Deleting the instance with ID from JSON file: " + instance_id + "\n")

                    write_json(dict_variables)
                    
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
                        dict_variables["instances"].pop(dict_key)   
                        time.sleep(0.4)

                        print("Deleting the instance with ID from JSON file: " + instance_id + "\n")
                        write_json(dict_variables)
                        
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
    
    # ---------------------------------- ADD RULES TO SECURITY GROUP ---------------------------------- #
    if decision == "4":
        print("\n-------------------------------------------------------------\n")
        print("List of security groups in Terraform file: \n")
        time.sleep(0.8)
        if dict_variables["security_groups"] == {}:
            print("No security groups created yet. \n")
        else:
            for key in dict_variables["security_groups"]:
                print("Nome: " + key)
        
        print("\n-------------------------------------------------------------\n")
        print("List of security groups in AWS: \n")
        time.sleep(0.4)

        for each in ec2re.security_groups.all():
            print("Name: " + each.group_name + "\n")
        
        print("-------------------------------------------------------------\n")
        sg_rule = input("Enter the security group name to add rules: \n")
        while sg_rule == "":
            print("No security group name entered. Please try again.")
            sg_rule = input("Enter the security group name to add rules: \n")
        
        while sg_rule not in dict_variables["security_groups"]:
            print("Invalid security group name. Please try again.")
            sg_rule = input("Enter the security group name to add rules: \n")
    
        else:
            new_security_ingress = input("Enter the ingress description: \n")
            new_security_from_port = input("Enter the from port: \n")
            new_security_to_port = input("Enter the to port: \n")
            new_security_protocol = input("Enter the protocol: \n")
            new_security_cidr_blocks = input("Enter the CIDR blocks: \n") 
            dict_variables["security_groups"][sg_rule]["security_ingress"].append({"rules": {"description": new_security_ingress, 
                "from_port" : new_security_from_port, "to_port" : new_security_to_port, "protocol" : new_security_protocol, 
                "ipv6_cidr_blocks": None, "prefix_list_id": None, "self": None,"security_groups": None, 
                "cidr_blocks" : [new_security_cidr_blocks]}})


            time.sleep(0.4)

            print("Adding the new rule to the security group: " + sg_rule + "\n")
            write_json(dict_variables)

            print("\nRule added to the security group successfully. \n")
            time.sleep(0.8)
            mycommands()

    # ---------------------------------- LIST SECURITY GROUPS ---------------------------------- #
    if decision == "5":
        print("Existing security groups in Terraform file: \n")
        for key in dict_variables["security_groups"]:
            print("Name: " + key)
        print("-------------------------------------------------------------\n")

        print("Existing security groups in AWS: \n")
        time.sleep(0.4)
        groups = []

        for each in ec2re.security_groups.all():
            groups.append(each.group_name)
            print("ID: " + each.id + " " + "| Name: " + each.group_name + "\n")
         
        sg = input("Enter the security group name to list the rules OR nothing to return to menu: \n")

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
    if decision == "6":
        print("Existing security groups in Terraform file: \n")
        for key in dict_variables["security_groups"]:
            print(key)
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
                    if dict_variables["instances"][key] == sg:
                        dict_variables["instances"].pop(key)

                time.sleep(0.4)

                print("Deleting the security group from JSON file: " + sg + "\n")
                write_json(dict_variables)
                
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
    if decision == "7":
        print("Applying all changes...")
        time.sleep(0.8)
        os.system('terraform init')
        os.system('terraform plan -var-file=secret.tfvars')
        os.system('terraform apply -var-file=secret.tfvars')
        mycommands()

    # ---------------------------------- CREATE USER ---------------------------------- #
    if decision == "8":
        
        print('\n-------------------------------------------------------------\n')
        username = input("Enter the username: \n")

        while username == "":
            print("No username entered. Please try again.")
            time.sleep(0.8)
            username = input("Enter the username: \n")
        
        print('\n-------------------------------------------------------------\n')
        rules = input("Do you want to apply restrictions to this user? (y | n)\n")
        if rules == "y":
            list_actions = []
            list_resources = []
            restrictions = input("Enter the restriction name: \n")
            while restrictions == "":
                print("No restrictions entered. Please try again.\n")
                time.sleep(0.5)
                restrictions = input("Enter the restriction name: \n")
            action = input("Enter actions you want to restrict separated by commas (e.g. ec2:DescribeInstances, ec2:DescribeRegions): \n")
            resource = input("Enter resources you want to restrict separated by commas (e.g. arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0, arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef1): \n")
            list_actions = action.split(",")
            list_resources = resource.split(",")
            dict_variables["users"].append({"username": username, "restrictions": {"restriction_name": restrictions, "actions": list_actions, "resources": list_resources}})
            print('\n-------------------------------------------------------------\n')
            
        elif rules == "n": 
            restrictions = "user_full_access"
            action = "*"
            resource = "*"
            dict_variables["users"].append({"username": username, "restrictions": {"restriction_name": restrictions, "actions": [action], "resources": [resource]}})

        else:
            print("Invalid option. Please try again.")
            time.sleep(0.5)
            mycommands()

    
        print("Creating user " + username + "...\n")
        write_json(dict_variables)

        user_decision = input("Do you want to create the user in AWS? (y/n) \n")

        if user_decision == "y":
            os.system('terraform apply -var-file=secret.tfvars')
            print("User created successfully!\n")
            time.sleep(0.5)
            mycommands()
        elif user_decision == "n":
            print("Returning to main menu...")
            time.sleep(0.8)
            mycommands()
        else:
            print("Invalid option. Please try again.")
            time.sleep(0.5)
            mycommands()

    # ---------------------------------- DELETE USER ---------------------------------- #
    
    if decision == "9":
        print("Existing users in Terraform file: \n")
        for key in dict_variables["users"]:
            print(key["username"])
        print('\n-------------------------------------------------------------\n')
        print("Existing users in AWS: \n")
        for user in ec2iam.list_users()['Users']:
            print("User: {0}\nUserID: {1}\n\n".format(
                user['UserName'],
                user['UserId']
                )
            )
        print('\n-------------------------------------------------------------\n')
        user = input("Enter the user name to delete OR nothing to come back: \n")
        if user == "":
            print("Returning to main menu...")
            time.sleep(0.8)
            mycommands()
        for key in list(dict_variables["users"]):
            if key["username"] == user:
                dict_variables["users"].remove(key)

        time.sleep(0.4)
        print("Deleting the user from JSON file: " + user + "\n")

        write_json(dict_variables)

        print("\nUser deleted from the JSON successfully. \n")

        aws = input("Do you want to delete it from AWS? (y/n) \n")

        if aws == "y":
            print("Deleting the user from AWS...\n")
            os.system('terraform apply -var-file=secret.tfvars')
            print("User deleted from AWS successfully!\n")
            time.sleep(0.8)
            mycommands()

        elif aws == "n":
            print("Returning to main menu...")
            time.sleep(0.8)
            mycommands()
    
    # ---------------------------------- LIST ALL USERS ---------------------------------- #
    if decision == "10":
        print("Listing all users in AWS...\n")
        time.sleep(0.5)
        for user in ec2iam.list_users()['Users']:
            print("User: {0}\nUserID: {1}\nARN: {2}\nCreated on: {3}\n".format(
                user['UserName'],
                user['UserId'],
                user['Arn'],
                user['CreateDate']
                )
            )
        
        print("Listing all users in Terraform file...\n")
        time.sleep(0.5)

        for user in dict_variables["users"]:
            for key in user:
                print("User: {0}\nRestrictions: {1}\n".format(
                    user[key]["username"],
                    user[key]["restrictions"]["restriction_name"]
                    )
                )

        time.sleep(0.8)
        mycommands()

    # ---------------------------------- EXIT ---------------------------------- #
    if decision == "11":
        print("Exiting...")
        time.sleep(0.5)
        exit()

def write_json(dict_variables):
    json_object = json.dumps(dict_variables, indent = 4)

    for i in tqdm(range(10)):
        time.sleep(0.2)

    with open('.auto.tfvars.json', 'w') as f:
        f.write(json_object)

mycommands.add_command(program)

if __name__ == '__main__':
    mycommands()



