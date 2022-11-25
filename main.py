import click
import json
import os
import time
from tqdm import tqdm
import boto3

contador = 0

os.system('cls')
path = input("\033[1;32m\n" + "-"*80 + "\n" + " "*30 + "SELECT THE REGION" + " "*30 + "\n" + "-"*80 + "\033[0m" + "\n\n\033[1;32m1.\033[0m us-east-1 (North Virginia)\n\033[1;32m2.\033[0m us-east-2 (Ohio): \n\n")
os.system("cls")

while path != "1" and path != "2":
    print("\033[31mInvalid option, please try again\033[00m\n")
    time.sleep(0.8)
    os.system("cls")
    path = input("\033[1;32m\n" + "-"*80 + "\n" + " "*30 + "SELECT THE REGION" + " "*30 + "\n" + "-"*80 + "\033[0m" + "\n\n\033[1;32m1.\033[0m us-east-1 (North Virginia)\n\033[1;32m2.\033[0m us-east-2 (Ohio): \n\n")
    os.system("cls")
if path == "1":
    os.chdir('terraform-east-1')
    session = boto3.Session(profile_name='default', region_name='us-east-1')
elif path == "2":
    os.chdir('terraform-east-2')
    session = boto3.Session(profile_name='default', region_name='us-east-2')

ec2client = session.client('ec2')
ec2iam = session.client('iam')
ec2re = session.resource('ec2')

@click.group()
def mycommands():
    pass

@click.command()
@click.option('--decision', prompt = "\033[1;32m\n" + "-"*80 + "\n" + " "*10 + "Welcome to the Terraform Application, what do you want to do?" + " "*10 + "\n" + "-"*80 + "\033[0m\n\n \033[1;32m1.\033[00m Create a new instance\n \033[1;32m2.\033[00m Delete an instance\n \033[1;32m3.\033[00m List all instances\n \033[1;32m4.\033[00m Add rules to Security Group \n \033[1;32m5.\033[00m List security groups\n \033[1;32m6.\033[00m Delete security group \n \033[1;32m7.\033[00m Apply all changes\n \033[1;32m8.\033[00m Create user \n \033[1;32m9.\033[00m Delete user \n \033[1;32m10.\033[00m List all users \n \033[1;32m11.\033[00m Exit \n\n", 
type=click.Choice(['1', '2', '3', '4', '5', '6','7','8','9','10','11'], case_sensitive=False), help = 'The option you choose.')

def program(decision):
    global contador

    if os.stat('.auto.tfvars.json').st_size == 0 or os.stat('.auto.tfvars.json').st_size == 71:
        dict_variables = {"security_groups" : {}, "instances" : {}, "users" : []}
        contador = 0
    else:
        dict_variables = json.load(open(".auto.tfvars.json"))
        contador = len(dict_variables["instances"])

    # ---------------------------------- CREATE INSTANCE ---------------------------------- #
    if decision == "1":
        os.system("cls")
        print("\033[95m" + "-"*80 + "\033[0m")
        print("\033[95m" + " "*30 + "CREATING INSTANCE\033[0m" + " "*30)
        print("\033[95m" + "-"*80 + "\033[0m")
        contador += 1
        dict_instance_key = 'instance_' + str(contador)
        name = input("\033[1;32mINSTANCE NAME\033[00m: ")
        print("\033[1;32m" + "-"*40 + "\033[0m")
        type = input("\n\033[1;32mINSTANCE TYPE\033[00m\n\n\033[1;32m1.\033[00mt2.micro\n\033[1;32m2.\033[00mt2.nano\n\n")
        while type != "1" and type != "2":
            print("\033[31mInvalid instance type, please try again\033[00m\n")
            time.sleep(0.8)
            print("\033[1;32m" + "-"*40 + "\033[0m")
            type = input("\n\033[1;32mINSTANCE TYPE\033[00m\n\n\033[1;32m1.\033[00mt2.micro\n\033[1;32m2.\033[00mt2.nano\n\n")
        print("\033[1;32m" + "-"*40 + "\033[0m")

        if type == "1":
            type = "t2.micro"
        elif type == "2":
            type = "t2.nano"

        security = input("Do you want to create a security group?\n\n\033[1;32my\033[00m = YES\n\033[1;32mn\033[00m = NO\n\n")
        if security == "y":
            os.system("cls")
            print("\033[95m" + "-"*80 + "\033[0m")
            print("\033[95m" + " "*30 + "CREATING SECURITY GROUP\033[0m" + " "*30)
            print("\033[95m" + "-"*80 + "\033[0m")
            security_name = input("\033[1;32mSECURITY GROUP NAME:\033[00m ")

            while security_name == "standard" or security_name == "default":
                print("\033[31mInvalid name, please try again\033[00m\n")
                security_name = input("\033[1;32mSECURITY GROUP NAME:\033[00m ")

            if security_name in dict_variables["security_groups"]:
                print("Security group already exists, adding this new instance to it...\n")
                time.sleep(0.8)
                dict_variables["instances"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "security_name" : security_name}})

                time.sleep(0.4)
                print("Creating instance in the JSON file\n")
                write_json(dict_variables)
                
                print("Instance created successfully!\n")
                time.sleep(0.2)
                
                apply = input("Do you want to apply the changes?\n\n\033[1;32my\033[00m = YES\n\033[1;32mn\033[00m = NO\n\n")
                os.system("cls")
                if apply == 'y':
                    os.system('terraform init')
                    os.system('terraform plan -var-file=secret.tfvars')
                    os.system('terraform apply -var-file=secret.tfvars')
                    print("Changes applied \033[1;32msuccessfully!\033[00m\n")
                    time.sleep(0.2)
                    print("Returning to the main menu...\n")
                    time.sleep(0.8)
                    os.system("cls")
                    mycommands()
                else:
                    print("Returning to the main menu...\n")
                    time.sleep(0.8)
                    os.system("cls")
                    mycommands()

            security_description = input("\033[1;32mDESCRIPTION:\033[00m ")
            security_ingress = input("\033[1;32mINGRESS DESCRIPTION:\033[00m ")
            while security_ingress == "":
                print("\033[31mInvalid description, please try again\033[00m\n")
                security_ingress = input("\033[1;32mINGRESS DESCRIPTION:\033[00m ")
            security_from_port = input("\033[1;32mFROM PORT:\033[00m ")
            while security_from_port == "" and security_from_port.isdigit() == False:
                print("\033[31mInvalid port, please try again\033[00m\n")
                security_from_port = input("\033[1;32mFROM PORT:\033[00m ")
            security_to_port = input("\033[1;32mTO PORT:\033[00m ")
            while security_to_port == "" and security_to_port.isdigit() == False:
                print("\033[31mInvalid port, please try again\033[00m\n")
                security_to_port = input("\033[1;32mTO PORT:\033[00m ")
            security_protocol = input("\033[1;32mPROTOCOL:\033[00m ")
            while security_protocol == "":
                print("\033[31mInvalid protocol, please try again\033[00m\n")
                security_protocol = input("\033[1;32mPROTOCOL:\033[00m ")
            security_cidr_blocks = input("\033[1;32mCIDR BLOCKS:\033[00m ")
            while security_cidr_blocks == "":
                print("\033[31mInvalid CIDR block, please try again\033[00m\n")
                security_cidr_blocks = input("\033[1;32mCIDR BLOCKS:\033[00m ")

            egress_decision = input("\nDo you want to add an egress rule?\n\n\033[1;32my\033[00m = YES\n\033[1;32mn\033[00m = NO\n\n")
            os.system("cls")
            if egress_decision == "y":
                security_egress = input("\033[1;32mEGRESS DESCRIPTION:\033[00m ")
                while security_egress == "":
                    print("\033[31mInvalid description, please try again\033[00m\n")
                    security_egress = input("\033[1;32mEGRESS DESCRIPTION:\033[00m ")
                security_egress_from_port = input("\033[1;32mFROM PORT:\033[00m ")
                while security_egress_from_port == "" and security_egress_from_port.isdigit() == False:
                    print("\033[31mInvalid port, please try again\033[00m\n")
                    security_egress_from_port = input("\033[1;32mFROM PORT:\033[00m ")
                security_egress_to_port = input("\033[1;32mTO PORT:\033[00m ")
                while security_egress_to_port == "" and security_egress_to_port.isdigit() == False:
                    print("\033[31mInvalid port, please try again\033[00m\n")
                    security_egress_to_port = input("\033[1;32mTO PORT:\033[00m ")
                security_egress_protocol = input("\033[1;32mPROTOCOL:\033[00m ")
                while security_egress_protocol == "":
                    print("\033[31mInvalid protocol, please try again\033[00m\n")
                    security_egress_protocol = input("\033[1;32mPROTOCOL:\033[00m ")
                security_egress_cidr_blocks = input("\033[1;32mCIDR BLOCKS:\033[00m ")
                while security_egress_cidr_blocks == "":
                    print("\033[31mInvalid CIDR blocks, please try again\033[00m\n")
                    security_egress_cidr_blocks = input("\033[1;32mCIDR BLOCKS:\033[00m ")
            
            elif egress_decision == "n":
                print("Adding default egress rules...\n")
                security_egress = "Allow all outbound"
                security_egress_from_port = "0"
                security_egress_to_port = "0"
                security_egress_protocol = "-1"
                security_egress_cidr_blocks = "0.0.0.0/0"

            if security_name not in dict_variables["security_groups"]:
                dict_variables["instances"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "security_name" : security_name}})
                dict_variables["security_groups"].update({security_name : {"security_name": security_name, 
                "security_description" : security_description, "security_ingress" : [{"rules": {"description": security_ingress, 
                "from_port" : security_from_port, "to_port" : security_to_port, "protocol" : security_protocol, 
                "ipv6_cidr_blocks": None, "prefix_list_ids": None, "self": None,"security_groups": None, 
                "cidr_blocks" : [security_cidr_blocks]}}], "security_egress" : [{"rules": {"description": security_egress, "from_port" : security_egress_from_port,
                "to_port" : security_egress_to_port, "protocol" : security_egress_protocol, "ipv6_cidr_blocks": None, "prefix_list_ids": None, "self": None,
                "security_groups": None, "cidr_blocks" : [security_egress_cidr_blocks]}}]}})
            else:
                dict_variables["instances"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "security_name" : security_name}})

        if security == "n":
            print("Applying default security group\n")
            time.sleep(0.5)

            if "standard" not in dict_variables["security_groups"]:
                dict_variables["instances"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "security_name" : "standard"}})
                dict_variables["security_groups"].update({"standard" : {"security_name": "standard", 
                "security_description" : "Allow 22", "security_ingress" : [{"rules": {"description": "Allow 22", 
                "from_port" : "22", "to_port" : "22", "protocol" : "tcp", 
                "ipv6_cidr_blocks": None, "prefix_list_ids": None, "self": None,"security_groups": None, 
                "cidr_blocks" : ["0.0.0.0/16"]}}],"security_egress" : [{"rules": {"description": "Allow all outbound", "from_port" : "0",
                "to_port" : "0", "protocol" : "-1", "ipv6_cidr_blocks": None, "prefix_list_ids": None, "self": None,
                "security_groups": None, "cidr_blocks" : ["0.0.0.0/0"]}}]}})
            else:
                dict_variables["instances"].update({dict_instance_key: {"instance_name" : name, "instance_type" : type, "security_name" : "standard"}})

        time.sleep(0.4)
        os.system("cls")
        print("Creating instance in the JSON file\n")

        write_json(dict_variables)
        
        print("\n\033[1;32mInstance created successfully!\033[00m\n")
        time.sleep(0.2)
        
        apply = input("Do you want to apply the changes?\n\n\033[1;32my\033[00m = YES\n\033[1;32mn\033[00m = NO\n\n")
        if apply == 'y':
            os.system('terraform init')
            os.system('terraform plan -var-file=secret.tfvars')
            os.system('terraform apply -var-file=secret.tfvars')
            print("\nInstances deployed in AWS\n")
            time.sleep(0.2)
            print("Returning to the main menu...\n")
            time.sleep(0.8)
            os.system("cls")
            mycommands()
        else:
            print("\nReturning to the main menu...\n")
            time.sleep(0.8)
            os.system("cls")
            mycommands()
    
    # ---------------------------------- DELETE INSTANCE ---------------------------------- #
    if decision == "2":
        
        os.system("cls")
        print("\033[95m" + "-"*80 + "\033[0m")
        print("\033[95m" + " "*30 + "DELETING INSTANCE\033[0m" + " "*30)
        print("\033[95m" + "-"*80 + "\033[0m")
        print('ALL INSTANCES LOCALLY: \n')
        for key in dict_variables["instances"]:
            print(key)

        time.sleep(0.8)
        instance_id = input("Instance number to delete: \n")

        dict_key = "instance_" + str(instance_id)

        instances_aws =[]

        for each in ec2re.instances.all():
            instances_aws.append(each.tags[0]["Value"])
        
        while instance_id == "":
            print("\033[31mNo instance ID entered. Please try again.\033[00m")
            time.sleep(0.8)
            os.system("cls")
            instance_id = input("Instance number to delete: \n")

        else:
            for key in dict_variables["instances"]:
                if dict_key not in dict_variables["instances"]:
                    print("\033[31mInvalid instance ID. Please try again.\033[00m\n")
                    time.sleep(0.8)
                    os.system("cls")
                    mycommands()

                if dict_variables["instances"][dict_key]["instance_name"] in instances_aws:
                    dict_variables["instances"].pop(dict_key)

                    time.sleep(0.4)

                    print("Deleting the instance with ID from JSON file: " + instance_id + "\n")

                    write_json(dict_variables)
                    
                    print("\n\033[1;32mInstance deleted from the JSON successfully.\033[00m\n")
                    os.system("cls")
                    
                    print("Deleting the instance from AWS...\n")
                    os.system('terraform apply -var-file=secret.tfvars')
                    
                    print("\033[1;32mInstance deleted from AWS successfully!\033[00m\n")
                    time.sleep(0.2)
                    print("Returning to the main menu...\n")
                    time.sleep(0.8)
                    os.system("cls")
                    mycommands()
                
                else:
                    os.system("cls")
                    print("\033[93mInstance not found in AWS, it could not exist or it was already deleted.\033[00m\n")
                    final_decision = input("Do you want to delete it from the JSON file? (y/n) \n")
                    if final_decision == "y":
                        dict_variables["instances"].pop(dict_key)   
                        time.sleep(0.4)

                        print("Deleting the instance with ID from JSON file: " + instance_id + "\n")
                        write_json(dict_variables)
                        
                        print("\n\033[1;32mInstance deleted from the JSON successfully.\033[00m\n")
                        time.sleep(0.2)
                        print("Returning to the main menu...\n")
                        time.sleep(0.8)
                        os.system("cls")
                        mycommands()
                    else:
                        time.sleep(0.2)
                        print("Returning to the main menu...\n")
                        time.sleep(0.8)
                        os.system("cls")
                        mycommands()

        mycommands()

    # ---------------------------------- LIST INSTANCES ---------------------------------- #
    if decision == "3":
        os.system("cls")
        print("\033[95m" + "-"*80 + "\033[0m")
        print("\033[95m" + " "*30 + "LISTING INSTANCES\033[0m" + " "*30)
        print("\033[95m" + "-"*80 + "\033[0m")
        print('ALL INSTANCES LOCALLY: \n')

        time.sleep(0.8)
        if dict_variables["instances"] == {}:
            print("No instances created yet. \n")
        else:
            for key in dict_variables["instances"]:
                print("\033[34mID:\033[00m " + key + "\033[34m| Name:\033[00m " + dict_variables["instances"][key]["instance_name"] + "\033[34m| Type:\033[00m " + dict_variables["instances"][key]["instance_type"] + "\n")
    
        print("\033[95m" + "-"*80 + "\033[0m")
        print('ALL INSTANCES IN AWS: \n')
        time.sleep(0.4)

        for each in ec2re.instances.all():
            print("\033[34mID:\033[00m " + each.id + " " + "\033[34m| Name:\033[00m " + each.tags[0]["Value"] + " " + "\033[34m| State:\033[00m " 
            + each.state["Name"] + " " + "\033[34m| Type:\033[00m " + each.instance_type +  "\033[34m| Region:\033[00m " + 
            each.placement['AvailabilityZone'] + "\n")

        print("\033[95m" + "-"*80 + "\033[0m")
        back = input("\nPress ENTER to return to main menu...")

        while back != "":
            print("\033[31mInvalid option. Please try again.\033[00m")
            time.sleep(0.2)
            back = input("\nPress ENTER to return to main menu...")

        if back == "":
            print("Returning to main menu...")
            time.sleep(0.8)
            os.system("cls")
            mycommands()
    
    # ---------------------------------- ADD RULES TO SECURITY GROUP ---------------------------------- #
    if decision == "4":
        os.system("cls")
        print("\033[95m" + "-"*80 + "\033[0m")
        print("\033[95m" + " "*25 + "ADDING RULES TO SECURITY GROUP\033[0m" + " "*35)
        print("\033[95m" + "-"*80 + "\033[0m")
        print('ALL SECURITY GROUPS LOCALLY: \n')
        time.sleep(0.8)
        if dict_variables["security_groups"] == {}:
            print("No security groups created yet. \n")
        else:
            for key in dict_variables["security_groups"]:
                print("\033[34mName:\033[00m " + key)
        
        print("\033[95m" + "-"*80 + "\033[0m")
        print('ALL SECURITY GROUPS IN AWS: \n')
        time.sleep(0.4)

        for each in ec2re.security_groups.all():
            print("\033[34mName:\033[00m " + each.group_name + "\n")
        
        print("\033[95m" + "-"*80 + "\033[0m")
        sg_rule = input("\nEnter the security group name to add rules: ")
        while sg_rule == "":
            print("\033[31mNo security group name entered. Please try again.\033[00m")
            time.sleep(0.5)
            sg_rule = input("\nEnter the security group name to add rules: ")
        
        while sg_rule not in dict_variables["security_groups"]:
            print("\033[31mInvalid security group name. Please try again.\033[00m")
            sg_rule = input("\nEnter the security group name to add rules: ")
    
        else:
            os.system("cls")
            print("\033[95m" + "-"*80 + "\033[0m")
            print("\033[95m" + " "*25 + "ADDING RULES TO SECURITY GROUP " + sg_rule +"\033[0m" + " "*25)
            print("\033[95m" + "-"*80 + "\033[0m")

            new_ingress = input("\nDo you want to add a new ingress rule? (y/n) ")
            while new_ingress != "y" and new_ingress != "n" or new_ingress == "":
                print("\033[31mInvalid option. Please try again.\033[00m")
                time.sleep(0.2)
                os.system("cls")
                new_ingress = input("Do you want to add a new ingress rule? (y/n) \n")

            if new_ingress == "y":
                new_security_ingress = input("Ingress description: \n")
                while new_security_ingress == "":
                    print("\033[31mNo ingress description entered. Please try again.\033[00m")
                    time.sleep(0.2)
                    new_security_ingress = input("Ingress description: \n")
                new_security_from_port = input("From port: \n")
                while new_security_from_port == "":
                    print("\033[31mNo from port entered. Please try again.\033[00m")
                    time.sleep(0.2)
                    new_security_from_port = input("From port: \n")
                new_security_to_port = input("To port: \n")
                while new_security_to_port == "":
                    print("\033[31mNo to port entered. Please try again.\033[00m")
                    time.sleep(0.2)
                    new_security_to_port = input("To port: \n")
                new_security_protocol = input("Protocol: \n")
                while new_security_protocol == "":
                    print("\033[31mNo protocol entered. Please try again.\033[00m")
                    time.sleep(0.2)
                    new_security_protocol = input("Protocol: \n")
                new_security_cidr_blocks = input("CIDR blocks: \n")
                while new_security_cidr_blocks == "":
                    print("\033[31mNo CIDR blocks entered. Please try again.\033[00m")
                    time.sleep(0.2)
                    new_security_cidr_blocks = input("CIDR blocks: \n")
                dict_variables["security_groups"][sg_rule]["security_ingress"].append({"rules": {"description": new_security_ingress, 
                    "from_port" : new_security_from_port, "to_port" : new_security_to_port, "protocol" : new_security_protocol, 
                    "ipv6_cidr_blocks": None, "prefix_list_ids": None, "self": None,"security_groups": None, 
                    "cidr_blocks" : [new_security_cidr_blocks]}})
            
            elif new_ingress == "n":
                print("No ingress rules added. \n")
                time.sleep(0.5)
                os.system("cls")
                pass

            new_egress = input("Do you want to add egress rules? (y/n): \n")
            while new_egress != "y" and new_egress != "n" or new_egress == "":
                print("\033[31mInvalid option. Please try again.\033[00m")
                time.sleep(0.2)
                os.system("cls")
                new_egress = input("Do you want to add egress rules? (y/n): \n")

            if new_egress == "y":
                new_security_egress = input("Egress description: \n")
                while new_security_egress == "":
                    print("\033[31mNo egress description entered. Please try again.\033[00m")
                    time.sleep(0.2)
                    new_security_egress = input("Egress description: \n")
                new_security_from_port = input("From port: \n")
                while new_security_from_port == "":
                    print("\033[31mNo from port entered. Please try again.\033[00m")
                    time.sleep(0.2)
                    new_security_from_port = input("From port: \n")
                new_security_to_port = input("To port: \n")
                while new_security_to_port == "":
                    print("\033[31mNo to port entered. Please try again.\033[00m")
                    time.sleep(0.2)
                    new_security_to_port = input("To port: \n")
                new_security_protocol = input("Protocol: \n")
                while new_security_protocol == "":
                    print("\033[31mNo protocol entered. Please try again.\033[00m")
                    time.sleep(0.2)
                    new_security_protocol = input("Protocol: \n")
                new_security_cidr_blocks = input("CIDR blocks: \n") 
                while new_security_cidr_blocks == "":
                    print("\033[31mNo CIDR blocks entered. Please try again.\033[00m")
                    time.sleep(0.2)
                    new_security_cidr_blocks = input("CIDR blocks: \n")
                dict_variables["security_groups"][sg_rule]["security_egress"].append({"rules": {"description": new_security_egress, 
                    "from_port" : new_security_from_port, "to_port" : new_security_to_port, "protocol" : new_security_protocol, 
                    "ipv6_cidr_blocks": None, "prefix_list_ids": None, "self": None,"security_groups": None, 
                    "cidr_blocks" : [new_security_cidr_blocks]}})
            
            elif new_egress == "n":
                print("No egress rules added. \n")
                time.sleep(0.5)
                os.system("cls")
                pass

            time.sleep(0.4)

            print("Adding the new rule to the security group: " + sg_rule + "\n")
            write_json(dict_variables)

            print("\033[1;32mRules added successfully!\033[00m\n")
            time.sleep(0.2)
            print("Returning to the main menu...\n")
            time.sleep(0.8)
            os.system("cls")
            mycommands()

    # ---------------------------------- LIST SECURITY GROUPS ---------------------------------- #
    if decision == "5":
        os.system("cls")
        print("\033[95m" + "-"*80 + "\033[0m")
        print("\033[95m" + " "*30 + "LIST SECURITY GROUPS\033[0m" + " "*30)
        print("\033[95m" + "-"*80 + "\033[0m")
        print('ALL SECURITY GROUPS LOCALLY: \n')

        for key in dict_variables["security_groups"]:
            print("\033[34mName:\033[00m " + key)

        print("\033[95m" + "-"*80 + "\033[0m")
        print('ALL SECURITY GROUPS IN AWS: \n')
        time.sleep(0.4)
        groups = []
        sg_ids = []

        for each in ec2re.security_groups.all():
            groups.append(each.group_name)
            sg_ids.append(each.id)
            print("\033[34mID:\033[00m " + each.id + " " + "\033[34m| Name:\033[00m " + each.group_name + "\n")
         
        sg = input("Security Group NAME or ID to list the rules" + "\033[33m OR \033[00m" + "press ENTER to come back: \n")

        if sg == "":
            print("Returning to main menu...")
            time.sleep(0.8)
            os.system("cls")
            mycommands()
        
        list_decision = input("Do you want to list locally or from AWS?\n\n\033[1;32m1.\033[00m Locally\n\033[1;32m2.\033[00m AWS\n\n")

        while list_decision != "1" and list_decision != "2" or list_decision == "":
            print("\033[31mInvalid option. Please try again.\033[00m")
            time.sleep(0.8)
            os.system("cls")
            list_decision = input("Do you want to list locally or from AWS?\n\n\033[1;32m1.\033[00m Locally\n\033[1;32m2.\033[00m AWS\n\n")

        if list_decision == "1":
            while sg not in groups or sg not in sg_ids:
                print("\n\033[31mSecurity group not found in AWS!\033[00m")
                time.sleep(0.2)
                print("Please try again.\n")
                os.system("cls")
                sg = input("Security Group NAME or ID to list the rules \n\033[1;32mPress ENTER to return to menu:\033[00m \n")
            
            if sg in groups or sg in sg_ids:
                os.system("cls")
                print("\033[95m" + "-"*80 + "\033[0m")
                print("\033[95m" + " "*30 + "SECURITY GROUP RULES\033[0m" + " "*30)
                print("\033[95m" + "-"*80 + "\033[0m")
                print("\033[34mName:\033[00m " + sg + "\n")
                print("\033[34mIngress rules:\033[00m \n")
                for ingress in dict_variables["security_groups"][sg]["security_ingress"]:
                    time.sleep(0.2)
                    print("\033[95mDescription:\033[00m " + ingress["rules"]["description"] + "\033[95m | From port:\033[00m " + 
                    ingress["rules"]["from_port"] + "\033[95m | To port:\033[00m " + ingress["rules"]["to_port"] + 
                    "\033[95m | Protocol:\033[00m " + ingress["rules"]["protocol"] 
                    + "\033[95m | CIDR:\033[00m " + str(ingress["rules"]["cidr_blocks"]) + "\n")
                print("\033[34mEgress rules:\033[00m \n")
                for egress in dict_variables["security_groups"][sg]["security_egress"]:
                    time.sleep(0.2)
                    print("\033[95mDescription:\033[00m " + egress["rules"]["description"] + "\033[95m | From port:\033[00m " + 
                    egress["rules"]["from_port"] + "\033[95m | To port:\033[00m " + egress["rules"]["to_port"] + 
                    "\033[95m | Protocol:\033[00m " + egress["rules"]["protocol"] 
                    + "\033[95m | CIDR:\033[00m " + str(egress["rules"]["cidr_blocks"]) + "\n")
                print("\033[95m" + "-"*80 + "\033[0m") 
                back = input("\nPress ENTER to return to main menu...")

                while back != "":
                    print("\033[31mInvalid option. Please try again.\033[00m")
                    time.sleep(0.2)
                    back = input("\nPress ENTER to return to main menu...")

                if back == "":
                    print("Returning to main menu...")
                    time.sleep(0.8)
                    os.system("cls")
                    mycommands()

        elif list_decision == "2":
            if sg in dict_variables["security_groups"]:
                os.system("cls")
                print("\033[95m" + "-"*80 + "\033[0m")
                print("\033[95m" + " "*30 + "SECURITY GROUP RULES\033[0m" + " "*30)
                print("\033[95m" + "-"*80 + "\033[0m")
                print("\033[34mName:\033[00m " + sg + "\n")
                print("\033[34mIngress rules:\033[00m \n")
                for ingress in dict_variables["security_groups"][sg]["security_ingress"]:
                    time.sleep(0.2)
                    print("\033[95mDescription:\033[00m " + ingress["rules"]["description"] + "\033[95m | From port:\033[00m " + 
                    ingress["rules"]["from_port"] + "\033[95m | To port:\033[00m " + ingress["rules"]["to_port"] + 
                    "\033[95m | Protocol:\033[00m " + ingress["rules"]["protocol"] 
                    + "\033[95m | CIDR:\033[00m " + str(ingress["rules"]["cidr_blocks"]) + "\n")
                print("\033[34mEgress rules:\033[00m \n")
                for egress in dict_variables["security_groups"][sg]["security_egress"]:
                    time.sleep(0.2)
                    print("\033[95mDescription:\033[00m " + egress["rules"]["description"] + "\033[95m | From port:\033[00m " + 
                    egress["rules"]["from_port"] + "\033[95m | To port:\033[00m " + egress["rules"]["to_port"] + 
                    "\033[95m | Protocol:\033[00m " + egress["rules"]["protocol"] 
                    + "\033[95m | CIDR:\033[00m " + str(egress["rules"]["cidr_blocks"]) + "\n")
                print("\033[95m" + "-"*80 + "\033[0m") 
                back = input("\nPress ENTER to return to main menu...")
                while back != "":
                    print("\033[31mInvalid option. Please try again.\033[00m")
                    time.sleep(0.2)
                    back = input("\nPress ENTER to return to main menu...")
                if back == "":
                    print("Returning to main menu...")
                    time.sleep(0.8)
                    os.system("cls")
                    mycommands()
            else:
                print("\n\033[31mSecurity group not found in Terraform file!\033[00m")
                time.sleep(0.2)
                print("Please try again.\n")
                os.system("cls")
                print("Returning to main menu...")
                time.sleep(0.8)
                os.system("cls")

    # ---------------------------------- DELETE SECURITY GROUP ---------------------------------- #
    if decision == "6":
        os.system("cls")
        print("\033[95m" + "-"*80 + "\033[0m")
        print("\033[95m" + " "*30 + "DELETE SECURITY GROUP\033[0m" + " "*30)
        print("\033[95m" + "-"*80 + "\033[0m")
        print('ALL SECURITY GROUPS LOCALLY: \n')
        for key in dict_variables["security_groups"]:
            print("\033[34mName:\033[00m " + key)
        print("\n")

        sgs = []

        for each in ec2re.security_groups.all():
            sgs.append(each.group_name)

        rule_or_all = input("Do you want to delete a security group (1) or one rule (2)? (1/2): \n")
        while rule_or_all != "1" and rule_or_all != "2":
            print("\033[31mInvalid option. Please try again.\033[00m")
            time.sleep(0.2)
            os.system("cls")
            rule_or_all = input("Do you want to delete a security group (1) or one rule (2)? (1/2): \n")
        
        if rule_or_all == "1":

            print("\033[31mWARNING: All instances attached to the security group will be deleted.\033[00m \n")
            sg = input("Enter the security group name to delete" + "\033[33m OR \033[00m" + "press ENTER to come back: \n")

            if sg == "":
                print("Returning to main menu...")
                time.sleep(0.8)
                os.system("cls")
                mycommands()

            while sg not in dict_variables["security_groups"]:
                print("\n\033[31mSecurity group not found in the JSON!\033[00m")
                time.sleep(0.2)
                print("Please try again.\n")
                os.system("cls")
                sg = input("Enter the security group name to delete" + "\033[33mOR\033[00m" + "press ENTER to come back: \n")

                if sg == "":
                    print("Returning to main menu...")
                    time.sleep(0.8)
                    os.system("cls")
                    mycommands()
            
            if sg in dict_variables["security_groups"]:
                dict_variables["security_groups"].pop(sg)
                for key in list(dict_variables["instances"]):
                    if dict_variables["instances"][key]["security_name"] == sg:
                        dict_variables["instances"].pop(key)

                time.sleep(0.4)

                print("Deleting the security group from JSON file: " + sg + "\n")
                write_json(dict_variables)
                
                print("\n\033[1;32mSecurity group deleted from the JSON successfully.\033[00m \n")
                time.sleep(0.2)
                os.system("cls")
                aws = input("Do you want to delete it from AWS? (y/n) \n")

                while aws not in ["y", "n"]:
                    print("\n\033[31mInvalid option!\033[00m")
                    time.sleep(0.2)
                    print("Please try again.\n")
                    os.system("cls")
                    aws = input("Do you want to delete it from AWS? (y/n) \n")
                
                if aws == "y":
                    if sg not in sgs:
                        print("\n\033[31mSecurity group not found in AWS!\033[00m")
                        time.sleep(0.2)
                        print("Please try again.\n")
                        os.system("cls")
                        mycommands()
                    print("Deleting " + sg + " from AWS...\n")
                    os.system('terraform apply -var-file=secret.tfvars')
                    os.system("cls")
                    print("\n\033[1;32mSecurity group deleted from AWS successfully.\033[00m \n")
                    time.sleep(0.2)
                    print("Returning to main menu...\n")
                    time.sleep(0.8)
                    os.system("cls")
                    mycommands()

                elif aws == "n":
                    print("Returning to main menu...")
                    time.sleep(0.8)
                    os.system("cls")
                    mycommands()
        
        elif rule_or_all == "2":
            sg = input("Enter the security group name to delete a rule" + "\033[33m OR \033[00m" + "press ENTER to come back: \n")

            if sg == "":
                print("Returning to main menu...")
                time.sleep(0.8)
                os.system("cls")
                mycommands()

            while sg not in dict_variables["security_groups"]:
                print("\n\033[31mSecurity group not found in the JSON!\033[00m")
                time.sleep(0.2)
                print("Please try again.\n")
                os.system("cls")
                sg = input("Enter the security group name to delete a rule" + "\033[33mOR\033[00m" + "press ENTER to come back: \n")
                if sg == "":
                    print("Returning to main menu...")
                    time.sleep(0.8)
                    os.system("cls")
                    mycommands()

            if sg in dict_variables["security_groups"]:
                os.system("cls")
                print("\033[95m" + "-"*80 + "\033[0m")
                print("\033[95m" + " "*30 + "SECURITY GROUP RULES\033[0m" + " "*30)
                print("\033[95m" + "-"*80 + "\033[0m")
                print("\033[34mName:\033[00m " + sg + "\n")
                print("\033[34mIngress rules:\033[00m \n")
                for ingress in dict_variables["security_groups"][sg]["security_ingress"]:
                    time.sleep(0.2)
                    print("\033[95mDescription:\033[00m " + ingress["rules"]["description"] + "\033[95m | From port:\033[00m " + 
                    ingress["rules"]["from_port"] + "\033[95m | To port:\033[00m " + ingress["rules"]["to_port"] + 
                    "\033[95m | Protocol:\033[00m " + ingress["rules"]["protocol"] 
                    + "\033[95m | CIDR:\033[00m " + str(ingress["rules"]["cidr_blocks"]) + "\n")
                print("\033[34mEgress rules:\033[00m \n")
                for egress in dict_variables["security_groups"][sg]["security_egress"]:
                    time.sleep(0.2)
                    print("\033[95mDescription:\033[00m " + egress["rules"]["description"] + "\033[95m | From port:\033[00m " + 
                    egress["rules"]["from_port"] + "\033[95m | To port:\033[00m " + egress["rules"]["to_port"] + 
                    "\033[95m | Protocol:\033[00m " + egress["rules"]["protocol"] 
                    + "\033[95m | CIDR:\033[00m " + str(egress["rules"]["cidr_blocks"]) + "\n")
                print("\033[95m" + "-"*80 + "\033[0m") 

                i_or_e = input("Is it an ingress (1) or egress (2) rule? (1/2): \n")

                if i_or_e == "1":
                    i_rule = int(input("Enter the rule number to delete" + "\033[33m OR \033[00m" + "press ENTER to come back: \n"))

                    if i_rule == "":
                        print("Returning to main menu...")
                        time.sleep(0.8)
                        os.system("cls")
                        mycommands()

                    while dict_variables["security_groups"][sg]["security_ingress"][i_rule-1] not in dict_variables["security_groups"][sg]["security_ingress"] or i_rule == 0:
                        print("\n\033[31mRule not found in the JSON!\033[00m")
                        time.sleep(0.5)
                        print("Please try again.\n")
                        time.sleep(0.8)
                        os.system("cls")
                        i_rule = int(input("Enter the rule number to delete" + "\033[33m OR \033[00m" + "press ENTER to come back: \n"))
                        if i_rule == "":
                            print("Returning to main menu...")
                            time.sleep(0.8)
                            os.system("cls")
                            mycommands()

                    dict_variables["security_groups"][sg]["security_ingress"].pop(i_rule-1)
                    time.sleep(0.4)

                    print("Deleting the rule from JSON file \n")
                    write_json(dict_variables)

                    print("\n\033[1;32mRule deleted from the JSON successfully.\033[00m \n")
                    time.sleep(0.2)
                    os.system("cls")
                
                elif i_or_e == "2":
                    e_rule = int(input("Enter the rule number to delete" + "\033[33m OR \033[00m" + "press ENTER to come back: \n"))

                    if e_rule == "":
                        print("Returning to main menu...")
                        time.sleep(0.8)
                        os.system("cls")
                        mycommands()

                    while dict_variables["security_groups"][sg]["security_egress"][e_rule-1] not in dict_variables["security_groups"][sg]["security_egress"] or e_rule == 0:
                        print("\n\033[31mRule not found in the JSON!\033[00m")
                        time.sleep(0.5)
                        print("Please try again.\n")
                        time.sleep(0.8)
                        os.system("cls")
                        e_rule = int(input("Enter the rule number to delete" + "\033[33m OR \033[00m" + "press ENTER to come back: \n"))
                        if e_rule == "":
                            print("Returning to main menu...")
                            time.sleep(0.8)
                            os.system("cls")
                            mycommands()

                    dict_variables["security_groups"][sg]["security_egress"].pop(e_rule-1)
                    time.sleep(0.4)

                    print("Deleting the rule from JSON file \n")
                    write_json(dict_variables)

                    print("\n\033[1;32mRule deleted from the JSON successfully.\033[00m \n")
                    time.sleep(0.2)
                    os.system("cls")

                aws = input("Do you want to delete it from AWS? (y/n) \n")

                while aws not in ["y", "n"]:
                    print("\n\033[31mInvalid option!\033[00m")
                    time.sleep(0.2)
                    print("Please try again.\n")
                    os.system("cls")
                    aws = input("Do you want to delete it from AWS? (y/n) \n")
                
                if aws == "y":
                    print("Deleting rule from AWS...\n")
                    os.system("cls")
                    os.system('terraform apply -var-file=secret.tfvars')
                    os.system("cls")
                    print("\n\033[1;32mRule deleted from AWS successfully.\033[00m \n")
                    time.sleep(0.2)
                    print("Returning to main menu...\n")
                    time.sleep(0.8)
                    os.system("cls")
                    mycommands()
                
                elif aws == "n":
                    print("Returning to main menu...")
                    time.sleep(0.8)
                    os.system("cls")
                    mycommands()

    # ---------------------------------- APPLY CHANGES ---------------------------------- #
    if decision == "7":
        os.system("cls")
        print("\033[95m" + "-"*80 + "\033[0m")
        print("\033[95m" + " "*30 + "APPLY CHANGES\033[0m" + " "*30)
        print("\033[95m" + "-"*80 + "\033[0m")

        print("\nApplying all changes...\n")
        time.sleep(0.8)
        
        if os.path.exists(".terraform.lock.hcl"):
            os.system('terraform plan -var-file=secret.tfvars')
            os.system('terraform apply -var-file=secret.tfvars')
        else:
            os.system('terraform init')
            os.system('terraform plan -var-file=secret.tfvars')
            os.system('terraform apply -var-file=secret.tfvars')

        print("\n\033[1;32mChanges applied successfully.\033[00m \n")
        time.sleep(0.2)
        back = input("\nPress ENTER to return to main menu...")

        while back != "":
            print("\033[31mInvalid option. Please try again.\033[00m")
            time.sleep(0.2)
            back = input("\nPress ENTER to return to main menu...")

        if back == "":
            print("Returning to main menu...")
            time.sleep(0.8)
            os.system("cls")
            mycommands()

    # ---------------------------------- CREATE USER ---------------------------------- #
    if decision == "8":
        os.system("cls")
        print("\033[95m" + "-"*80 + "\033[0m")
        print("\033[95m" + " "*30 + "CREATE USER\033[0m" + " "*30)
        print("\033[95m" + "-"*80 + "\033[0m")
        username = input("Enter the username: \n")

        while username == "":
            print("\n\033[31mUsername cannot be empty!\033[00m")
            time.sleep(0.2)
            print("Please try again.\n")
            time.sleep(0.8)
            os.system("cls")
            username = input("Enter the username: \n")
        
        print("\033[95m" + "-"*80 + "\033[0m")
        rules = input("Do you want to apply restrictions to this user? (y | n)\n")

        while rules not in ["y", "n"]:
            print("\n\033[31mInvalid option!\033[00m")
            time.sleep(0.2)
            print("Please try again.\n")
            time.sleep(0.8)
            os.system("cls")
            rules = input("Do you want to apply restrictions to this user? (y | n)\n")

        if rules == "y":
            os.system("cls")
            print("\033[95m" + "-"*80 + "\033[0m")
            print("\033[95m" + " "*30 + "APPLYING RESTRICTIONS TO USER" + username + "\033[0m" + " "*30)
            print("\033[95m" + "-"*80 + "\033[0m")
            list_actions = []
            list_resources = []
            restrictions = input("Enter the restriction name: \n")
            while restrictions == "":
                print("\n\033[31mRestriction name cannot be empty!\033[00m")
                time.sleep(0.5)
                restrictions = input("Enter the restriction name: \n")
            action = input("Enter actions you want to restrict separated by commas (e.g. ec2:DescribeInstances, ec2:DescribeRegions): \n")
            resource = input("Enter resources you want to restrict separated by commas (e.g. arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0, arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef1): \n")
            list_actions = action.split(",")
            list_resources = resource.split(",")
            dict_variables["users"].append({"username": username, "restrictions": {"restriction_name": restrictions, "actions": list_actions, "resources": list_resources}})
            print("\033[95m" + "-"*80 + "\033[0m")
            
        elif rules == "n": 
            print("Applying no restrictions to user " + username + "\n")
            restrictions = "user_full_access"
            action = "*"
            resource = "*"
            dict_variables["users"].append({"username": username, "restrictions": {"restriction_name": restrictions, "actions": [action], "resources": [resource]}})
    
        print("Creating user " + username + "...\n")
        write_json(dict_variables)

        user_decision = input("Do you want to create the user in AWS? (y/n) \n")

        while user_decision not in ["y", "n"]:
            print("\n\033[31mInvalid option!\033[00m")
            time.sleep(0.2)
            print("Please try again.\n")
            os.system("cls")
            user_decision = input("Do you want to create the user in AWS? (y/n) \n")

        if user_decision == "y":
            os.system('cls')
            list_users = []
            for user in ec2iam.list_users()['Users']:
                list_users.append(user['UserName'])
            if username not in list_users:
                os.system('terraform apply -var-file=secret.tfvars')
                print("\n\033[1;32mUser created successfully.\033[00m \n")
                time.sleep(0.2)
                back = input("\nPress ENTER to return to main menu...")

                while back != "":
                    print("\033[31mInvalid option. Please try again.\033[00m")
                    time.sleep(0.2)
                    back = input("\nPress ENTER to return to main menu...")

                if back == "":
                    print("Returning to main menu...")
                    time.sleep(0.8)
                    os.system("cls")
                    mycommands()
            else:
                print("\n\033[31mUser already exists in AWS!\033[00m \n")
                time.sleep(0.8)
                print("Returning to main menu...")
                time.sleep(0.8)
                os.system("cls")
                mycommands()

        elif user_decision == "n":
            print("Returning to main menu...")
            time.sleep(0.8)
            os.system("cls")
            mycommands()

    # ---------------------------------- DELETE USER ---------------------------------- #
    
    if decision == "9":
        os.system("cls")
        print("\033[95m" + "-"*80 + "\033[0m")
        print("\033[95m" + " "*30 + "DELETE USER\033[0m" + " "*30)
        print("\033[95m" + "-"*80 + "\033[0m")
        print("Existing users in Terraform file: \n")
        for key in dict_variables["users"]:
            print(key["username"])
        print("\033[95m" + "-"*80 + "\033[0m")
        print("Existing users in AWS: \n")

        list_users_del = []

        for user in ec2iam.list_users()['Users']:
            list_users_del.append(user['UserName'])
            print("\033[34mUser:\033[0m {0}\n\033[34mUserID:\033[0m {1}\n\n".format(
                user['UserName'],
                user['UserId']
                )
            )
        print("\033[95m" + "-"*80 + "\033[0m")
        user = input("Enter the user to delete" + "\033[33m OR \033[00m" + "press ENTER to come back: \n")
        if user == "":
            print("Returning to main menu...")
            time.sleep(0.8)
            os.system("cls")
            mycommands()
        
        if user not in [key["username"] for key in dict_variables["users"]] and user in list_users_del:
            print("\n\033[31mUser does not exist in Terraform file!\033[00m\n")
            print("But it exists in AWS. Deleting user from AWS...\n")
            os.system('terraform apply -var-file=secret.tfvars')
            print("\n\033[1;32mUser deleted from AWS successfully.\033[00m \n")
            time.sleep(0.2)
            print("Returning to main menu...\n")
            time.sleep(0.8)
            os.system("cls")
            mycommands()
            
        for key in dict_variables["users"]:
            if key["username"] == user:
                dict_variables["users"].remove(key)
        
        time.sleep(0.4)
        print("Deleting user " + user + "from JSON file\n")

        write_json(dict_variables)

        print("\n\033[1;32mUser deleted from the JSON successfully.\033[00m \n")

        aws = input("Do you want to delete it from AWS? (y/n) \n")

        if aws == "y":
            os.system('cls')
            print("Deleting the user from AWS...\n")
            os.system('terraform apply -var-file=secret.tfvars')
            print("\n\033[1;32mUser deleted from AWS successfully.\033[00m \n")
            time.sleep(0.2)
            print("Returning to main menu...\n")
            time.sleep(0.8)
            os.system("cls")
            mycommands()

        elif aws == "n":
            print("Returning to main menu...")
            time.sleep(0.8)
            os.system("cls")
            mycommands()
    
    # ---------------------------------- LIST ALL USERS ---------------------------------- #
    if decision == "10":
        os.system("cls")
        print("\033[95m" + "-"*80 + "\033[0m")
        print("\033[95m" + " "*30 + "LIST ALL USERS\033[0m" + " "*30)
        print("\033[95m" + "-"*80 + "\033[0m")
        print("Listing all users in AWS...\n")
        time.sleep(0.5)
        for user in ec2iam.list_users()['Users']:
            print("\033[34mUser:\033[00m {0}\n\033[34mUserID:\033[00m {1}\n\033[34mARN:\033[00m {2}\n\033[34mCreated on:\033[00m {3}\n".format(
                user['UserName'],
                user['UserId'],
                user['Arn'],
                user['CreateDate']
                )
            )
        
        print("\033[95m" + "-"*80 + "\033[0m")
        print("Listing all users in Terraform file...\n")
        time.sleep(0.5)

        if len(dict_variables["users"]) == 0:
            print("No users in Terraform file.\n")
            print("\033[95m" + "-"*80 + "\033[0m")
            print("Returning to main menu...\n")
            time.sleep(0.8)
            os.system("cls")
            mycommands()

        for key in dict_variables["users"]:
            print("\033[34mUser:\033[00m " + key["username"])

        print("\033[95m" + "-"*80 + "\033[0m")
        back = input("\nPress ENTER to return to main menu...")

        while back != "":
            print("\033[31mInvalid option. Please try again.\033[00m")
            time.sleep(0.2)
            back = input("\nPress ENTER to return to main menu...")

        if back == "":
            print("Returning to main menu...")
            time.sleep(0.8)
            os.system("cls")
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



