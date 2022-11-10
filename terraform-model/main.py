import click
import json
import os
import time

contador = 0
dict_variables = {"instance_variables" : {}}

@click.group()
def mycommands():
    pass

@click.command()
@click.option('--decision', prompt = 'Welcome to the Terraform Application, what do you want to do?\n\n 1. Create a new instance\n 2. Delete an instance\n 3. List all instances\n 4. Exit\n\n', 
type=click.Choice(['1', '2', '3', '4'], case_sensitive=False), help = 'The option you choose.')

def write_json(decision):
    global contador
    contador += 1

    if decision == "1":
        name = input("Enter the name of the instance: \n")
        type = input("Enter the instance type [t2.micro, t2.nano]: \n")
        dict_variables["instance_variables"].update({'instance_' + str(contador): {'instance_name': name, 'instance_type': type}})

        json_object = json.dumps(dict_variables, indent = 4)

        with open('.auto.tfvars.json', 'w') as f:
            f.write(json_object)

        value = input('\nDo you want to create another VM? (y/n):  ')

        if value == 'y':
            print('\nCreating another VM...\n')
            mycommands()

        elif value == 'n':
            click.echo('\nFinishing VM creation...')

        os.system('terraform init')
        os.system('terraform plan -var-file=secret.tfvars')
        #os.system('terraform apply -var-file=secret.tfvars')
    
    if decision == "2":
        print("Deleting an instance...")
        os.system('terraform destroy -var-file=secret.tfvars')
    
    if decision == "3":
        print("Creating a new security group...")
        os.system('terraform apply -var-file=secret.tfvars')
    
    if decision == "4":
        print("Exiting...")
        time.sleep(0.5)
        exit()

mycommands.add_command(write_json)

if __name__ == '__main__':
    mycommands()



