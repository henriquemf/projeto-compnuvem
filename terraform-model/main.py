import click
import json
import os
import time
from tqdm import tqdm

contador = 0

if os.stat(".auto.tfvars.json").st_size == 0:
    dict_variables = {"instance_variables" : {}}
else:
    dict_variables = json.load(open(".auto.tfvars.json"))

@click.group()
def mycommands():
    pass

@click.command()
@click.option('--decision', prompt = '\n-------------------------------------------------------------\nWelcome to the Terraform Application, what do you want to do?\n-------------------------------------------------------------\n\n 1. Create a new instance\n 2. Delete an instance\n 3. List all instances\n 4. Create new security group\n 5. Apply all changes\n 6. Exit \n\n', 
type=click.Choice(['1', '2', '3', '4', '5', '6'], case_sensitive=False), help = 'The option you choose.')

def write_json(decision):
    global contador
    contador += 1

    # ---------------------------------- CREATE INSTANCE ---------------------------------- #
    if decision == "1":
        name = input("Enter the name of the instance: \n")
        type = input("Enter the instance type [t2.micro, t2.nano]: \n")
        #security = input("Enter the security group name: \n")
        dict_variables["instance_variables"].update({'instance_' + str(contador): {'instance_name': name, 'instance_type': type}})

        json_object = json.dumps(dict_variables, indent = 4)

        with open('.auto.tfvars.json', 'w') as f:
            f.write(json_object)
        
        apply = input('\nDo you want to apply the changes right now? (y/n):  ')
        if apply == 'y':
            os.system('terraform init')
            os.system('terraform plan -var-file=secret.tfvars')
            #os.system('terraform apply -var-file=secret.tfvars')
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
                dict_variables["instance_variables"].pop(dict_key)
                json_object = json.dumps(dict_variables, indent = 4)

                time.sleep(0.4)

                print("Deleting the instance with ID: " + instance_id + "\n")

                for i in tqdm(range(10)):
                    time.sleep(0.4)

                with open('.auto.tfvars.json', 'w') as f:
                    f.write(json_object)
                
                print("\nInstance deleted successfully. \n")

                #os.system('terraform apply -var-file=secret.tfvars')
            
            else:
                print("\nInstance ID not found. Please try again.")
                time.sleep(0.8)
                mycommands()


        mycommands()

    # ---------------------------------- LIST INSTANCES ---------------------------------- #
    if decision == "3":
        print("\n-------------------------------------------------------------\n")
        print("List of instances not applied yet: \n")
        for key in dict_variables["instance_variables"]:
            print(key + "\n")
    
        print("-------------------------------------------------------------\n")
        #pegar as instancias que ja deram apply
        time.sleep(1.0)
        mycommands()

    # ---------------------------------- CREATE SECURITY GROUP ---------------------------------- #
    if decision == "4":
        print("Those are the existing security groups: \n")
        
        security = input("Enter the security group id: \n")
        dict_variables["instance_variables"].update({'instance_' + str(contador): {'security_group': security}})
        print("Creating a new security group with the ID " + security + "...\n")
        #os.system('terraform apply -var-file=secret.tfvars')
        mycommands()

    # ---------------------------------- APPLY CHANGES ---------------------------------- #
    if decision == "5":
        print("Applying all changes...")
        time.sleep(0.8)
        os.system('terraform init')
        os.system('terraform plan -var-file=secret.tfvars')
        #os.system('terraform apply -var-file=secret.tfvars')
        mycommands()
    
    # ---------------------------------- EXIT ---------------------------------- #
    if decision == "6":
        print("Exiting...")
        time.sleep(0.5)
        exit()

mycommands.add_command(write_json)

if __name__ == '__main__':
    mycommands()



