# Projeto de Computação em Nuvem

## Feito por :people_holding_hands::

- Henrique Martinelli Frezzatti

## Bibliotecas e Linguagens:

- ![Terraform](https://img.shields.io/badge/-Terraform-333333?style=flat&logo=terraform&logoColor=white&labelColor=purple)
- ![Python](https://img.shields.io/badge/-Python-333333?style=flat&logo=python&logoColor=white&labelColor=purple)

## Conceito C - :writing_hand: Criação simples <img src="https://img.shields.io/static/v1?label=ConceitoC&message=Finalizado&color=success&style=flat-square&logo=ghost"/>

- Implementar criação automática de VPC e sub-rede :heavy_check_mark:
- Criação de instâncias e pelo menos 2 tipos de hosts :heavy_check_mark:
- Listar instâncias e regiões, usuários e security_groups com regras :heavy_check_mark:
- Criação de security groups padrões e associação a instâncias :heavy_check_mark:
- Criação de usuário no IAM :heavy_check_mark:
- Deletar usuários, instâncias e security groups :heavy_check_mark:

## Conceito B - :writing_hand: Criação detalhada <img src="https://img.shields.io/static/v1?label=ConceitoB&message=Finalizado&color=success&style=flat-square&logo=ghost"/>

- Regras personalizadas em security groups (ingress e egress) :heavy_check_mark:
- Instâncias em mais de uma região (us-east-1 e us-east-2) :heavy_check_mark:
- Associar restrições a usuários :heavy_check_mark:
- Deletar regras em security groups :heavy_check_mark:

## Conceito A - :writing_hand: Escalabilidade <img src="https://img.shields.io/static/v1?label=ConceitoB&message=Finalizado&color=success&style=flat-square&logo=ghost"/>

- Implementar _High Availability_ :heavy_check_mark:
- Configurar e criar Load Balancer :heavy_check_mark:
- Configurar e criar Auto Scaling Group :heavy_check_mark:
- Criação de 3 sub-redes, uma para cada instância do auto-scaling :heavy_check_mark:
- Testes na AWS, funcionando apenas na região 2 (Ohio) :heavy_check_mark:

# Tutorial de criação :hammer_and_wrench::

## Objetivo :bow_and_arrow:

O principal objetivo que foi estabelecido para esse projeto foi automatizar e facilitar os processos de criação de instâncias, grupos de segurança, VPC (Virtual Private Cloud), sub-redes e usuários na plataforma da AWS (Amazon) utilizando a infraestrutura do `Terraform`. Porém, antes disso, precisamos entender e saber do que se trata o `Terraform`, certo?

## Terraform :man_technologist:

O Terraform se trata de uma ferramenta _open source_ para criar e estabelecer Infraestrutura como código, ou seja, criar e manipular infraestruturas por meio de programação em código (IaC), em uma linguagem declarativa e de fácil uso/acesso.

## Começando os trabalhos...:computer:

Primeiro, é necessário instalar o Terraform em seu computador para que seja possível usar seus recursos para a programação. Para isso, acesse o site a seguir: https://developer.hashicorp.com/terraform/downloads. Para esse projeto, foi utilizado o sistema operacional Windows 11, logo, na página acessada, abra a aba de downloads em Windows e baixe o arquivo 386. Feito isso, extraia a pasta .zip que foi instalada para o local desejado e execute o arquivo de instalação. 

Agora, é necessário setar e configurar o ambiente de desenvolvimento na própria AWS e, utilizando as informações de usuário, ID e senha fornecidas durante a criação pela IAM na AWS, como pode ser visto na imagem abaixo, acessamos o console e estamos prontos para continuar e iniciar:

![image](https://user-images.githubusercontent.com/62613979/203536092-1e885770-4856-4a8e-874d-90b4c7afa4d0.png)

***IMPORTANTE*** :stop_sign:: ao criar seu usuário na AWS, guarde as informações em um .csv conforme pode ser feito durante a própria criação e ***JAMAIS*** forneça essas informações ou as publique em nenhum lugar, ***PRINCIPALMENTE*** a ACCESS_KEY e SECRET_KEY. Essas informações são de alta importância e podem ser utilizadas para abuso do sistema, gerando altos custos ao provedor. 

## Iniciando o ambiente de trabalho :man_factory_worker:

Agora, com o Terraform instalado e o sistema configurado, podemos começar a criar os arquivos. Para isso, na pasta selecionada, foi criado um arquivo `main.tf`. Nele, serão executadas as funções principais de execução e configuração do seu software. Após isso, também foi criado um `provider.tf`, onde será fornecido, justamente, o provedor dos serviços utilizados que, nesse caso, é a AWS. Contudo, nesse projeto em questão, foi tudo colocado em apenas um único arquivo, o `main.tf`.

`main.tf`
```Terraform
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-east-1"
  access_key = var.access_key
  secret_key = var.secret_key
}
```

Você deve estar se perguntando agora, "mas o que é var.access_key e var.secret_key". Bom, lembrando o aviso dado acima sobre não compartilhar as chaves de acesso à sua conta da AWS, é necessário, ainda, utilizá-las para que seja possível que o programa funcione e, de fato, aplique as mudanças na AWS. Para isso, há diversos caminhos que podem ser considerados para tratar esse problema, um deles é usar variáveis de ambiente com o `set` no Windows ou `export` no Linux. Porém, nesse projeto, foi utilizado um arquivo do próprio Terraform denominado `secret.tfvars`. Nele, basta colocar os valores das variáveis que deseja manter em segredo para o uso do projeto e, depois disso, ***NÃO ESQUECER*** de adicionar o arquivo `secret.tfvars` ao `.gitignore`. Além disso, para que o programa saiba quais são cada uma das variáveis, é preciso declarar sua estrutura básica em um arquivo separado e exclusivo para isso denominado `variables.tf`.

`variables.tf`
```Terraform
variable "access_key" {
  description = "AWS access key"
  type        = string
  sensitive = true
}

variable "secret_key" {
  description = "AWS secret key"
  type        = string
  sensitive = true
}
```

`secret.tfvars` (Deve ser criado pelo usuário ao utilizar o programa, já que se encontra no .gitignore).
```Terraform
access_key = ""
secret_key = ""
```

Agora, algumas outras explicações devem ser fornecidas para compreensão completa do funcionamento do programa do Terraform. Sendo assim, ainda no `main.tf`, foram aplicadas os resources para a criação de *instâncias*, *security groups*, *vpc* e *subnet*. Neles, ao analisar o arquivo desse repositório, é possível observar que foram utilizdos uma função denominada `for_each`, a qual é capaz de percorrer listas e objetos para definir múltiplas variáveis de uma vez e, nesse projeto, isso é de extrema importância já que deve ser possível a criação de múltiplas instâncias e security_groups de uma vez, além de regras múltiplas para os SGs. 

## Trabalhando com as variáveis :traffic_light:

No entanto, a pergunta principal é: como fazer com que o Terraform altere as variáveis desejadas de acordo com a vontade e o input do usuário no terminal?. Para isso, foi utilizado um arquivo .json chamado `.auto.tfvars.json`, o qual o próprio Terraform é capaz de lê-lo automaticamente em toda execução, checando quais variáveis que foram declaradas nos arquivos `main.tf` e `variables.tf` estão presentes nesse JSON e, caso esteja presente, irá alterar *automaticamente* os valores de cada uma das variáveis presentes. Abaixo, há um exemplo do arquivo JSON completo para melhor compreensão:


```JSON
{
    "security_groups": {
        "standard": {
            "security_name": "standard",
            "security_description": "Allow 22",
            "security_ingress": [
                {
                    "rules": {
                        "description": "Allow 22",
                        "from_port": "22",
                        "to_port": "22",
                        "protocol": "tcp",
                        "ipv6_cidr_blocks": null,
                        "prefix_list_ids": null,
                        "self": null,
                        "security_groups": null,
                        "cidr_blocks": [
                            "0.0.0.0/16"
                        ]
                    }
                }
            ],
            "security_egress": [
                {
                    "rules": {
                        "description": "quero",
                        "from_port": "0",
                        "to_port": "0",
                        "protocol": "tcp",
                        "ipv6_cidr_blocks": null,
                        "prefix_list_ids": null,
                        "self": null,
                        "security_groups": null,
                        "cidr_blocks": [
                            "10.0.0.0/20"
                        ]
                    }
                }
            ]
        }
    },
    "instances": {
        "instance_2": {
            "instance_name": "henri1",
            "instance_type": "t2.micro",
            "security_name": "standard"
        }
    },
    "users": [
        {
            "username": "henricao",
            "restrictions": {
                "restriction_name": "user_full_access",
                "actions": [
                    "*"
                ],
                "resources": [
                    "*"
                ]
            }
        }
    ]
}
```

Ou seja, como um exemplo, no arquivo `main.tf`, há no `resource "aws_instance" "app_server"` um `for_each = var.instances`. Nele, o Terraform percorre cada uma das chaves do _object_ de instances, pegando cada um dos valores necessários para a implementação da instância desejada. Dessa forma, caso o usuário deseje um tipo específico de instância a ser utilizado (t2.micro, t2.nano, etc.), ao digitar no terminal a opção desejada, o JSON é preenchido e, o Terraform, obtém esse valor com o `each.value.instance_type`, percorrendo o _object_ e adicionando cada um dos instance_type vinculados a instância em questão (nesse caso a instance_2, com nome henri1). 

Muito complicado? Tome um café e pense novamente no que acabou de ler :coffee: :clock130:.

Bom, agora ficou mais fácil e possível realizar operações com múltiplos valores de instâncais, SGs, etc.. Com isso, foram criados de maneira similar/análoga a isso os security groups, sendo que, nesse projeto, cada security group pode estar atrelado a mais de uma instância, mas uma instância está atrelada apenas a um único SG. 

## VPC's e Subnets :construction:

No projeto, foi criado apenas uma única VPC e Subnet por região da AWS, sendo esse um resource fixo e sem possibilidade de alteração pelo usuário no terminal de uso:

```Terraform
resource "aws_vpc" "vpc_east_1" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "vpc_east_1"
  }
}

resource "aws_subnet" "vpc_east_1_subnet" {
  vpc_id     = aws_vpc.vpc_east_1.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "subnet_east_1"
  }
}
```

## Criando usuários :bust_in_silhouette:

Agora, é necessário que sejam criados usuários com nome e permissões específicas que podem ser declaradas pelo próprio criador. Para isso, foi utilizado o arquivo `user.tf`, onde foram criadas as _policies_ de cada usuário, o usuário em si e os _attachments_ entre eles. Além disso, também foi criado um `output.tf` para que, ao final da execução do programa do Terraform, seja mostrado no terminal a senha de acesso ao console da AWS do novo usuário criado.

## Trabalhando com regiões :globe_with_meridians:

Para que seja possível o usuário escolher a região na qual vai trabalhar e dar _deploy_ nas funcionalidades desejadas, sem que interfira em outra região, foi necessário utilizar pastas diferentes para cada uma das regiões. Nesse projeto, foi utilizado apenas 2 regiões: us-east-1 (no arquivo `terraform-east-1`) e us-east-2 (no arquivo `terraform-east-2`). Com isso, no Python, ao executar os comandos abaixo para a execução do Terraform e a aplicação na AWS, foi trocado o diretório de trabalho de acordo com a decisão do usuário da região que deseja trabalhar tendo, nessas pastas, todos os arquivos necessários para as funcionalidades.

## High Availability :recycle:

Para o final do projeto, foi implementado a funcionalidade de high availability, permitindo que uma máquina seja criada automaticamente, por meio de um auto-scaling group, sempre que uma máquina criada seja destruída ou atinja um limite de % de uso. Isso foi configurado em um arquivo denominado `autoscaling.tf` e, para acessar o WebServer criado, é possível acessar o link disponível no output após a execução do programa. 

Para uma mais profunda explicação, primeiramente foi criada uma imagem de uma instância personalizada, a qual teve o NodeJS instalado e um `server.js` criado, o qual é responsável por rodar uma página na internet comum, apenas printando uma frase e outras informações. Feito isso, por meio de uma acesso com **SSH** à essa máquina, é aplicado o crontab, o qual ficará responsável por fazer que esse servidor rode sempre que a máquina é iniciada ou reiniciada, sendo possível acessar esse link por meio do que foi disponibilizado no output do terminal. 

Crontab command
```
echo ‘@reboot ./server.js’ | crontab
```

Feito isso, foi gerada uma imagem AMI dessa instância e aplicada como um _launch template_ para o Auto-Scaling group, fazendo com que toda máquina que seja realizada o _deploy_ por meio dele seja igual à anterior, ou seja, com um WebServer rodando, permitindo uma alta escalabilidade e balanceamento de cargas, fazendo com que nenhuma máquina seja usada excessivamente ou perca a funcionalidade principal. 

Essa funcionalidade foi implementada apenas em uma única região, a `us-east-2`. Logo, para que seja possível testar esse recurso, basta acessar a região 2.

## Execução :racing_car:

No programa da interface visual feita em Python, é rodado os seguintes comandos, necessários para a execução do Terraform:

```
terraform init
terraform plan -var-files=secret.tfvars
terraform apply -var-files=secret.tfvars
```

O comando do `terraform init` é responsável por inicializar e configurar o _backend_ do Terraform, precisando ser executado uma única vez. Já o comando `terraform plan -var-files=secret.tfvars` é responsável por checar se há erros de resources ou configurações nos arquivos do Terraform, isso tudo utilizando o arquivo de variáveis contendo ACCESS_KEY_ID e SECRET_KEY_ID, necessários para que o Terraform seja capaz de acessar a AWS do usuário e realizar as operações.

***IMPORTANTE:*** Para que o usuário seja capaz de utilizar esse repositório, basta preencher os valores de access_key e secret_key no arquivo secret_template.tfvars e renomeá-lo para secret.tfvars

## Bibliotecas necessárias :books:

Para a criação da interface visual foi utilizado a linguagem Python e as bibliotecas Click, Json, OS, TQDM, Time e Boto3. Será necessário instalar apenas a Click, Boto3 e TQDM:

```
pip install boto3 click tqdm
```

Para fornecer explicações do que cada uma delas fazem:
- Click = manipulação de inputs e funções no terminal do python de fácil uso;
- Boto3 = acesso à AWS para que seja possível listar usuários, instâncias, security_groups etc. pelo próprio terminal do python;
- TQDM = utilizada para criar a barra de carregamento, puramente visual.

## Instruções de uso:

Executar o comando abaixo dentro da pasta projeto-compnuvem:
```
python ./main.py program
```

Após executar, caso tenha dado tudo certo, a seguinte tela deverá aparecer:

![image](https://user-images.githubusercontent.com/62613979/203544563-a8f35d31-2299-4e2d-abfe-72e455516edf.png)

Ao selecionar a região desejada, será listado todas as opções ao usuário de funcionalidades disponíveis no programa:

![image](https://user-images.githubusercontent.com/62613979/203544704-94c56db6-86ff-4def-91a6-21ffb22735ac.png)

Após isso, sinta-se livre para usar e explorar as funcionalidades oferecidas, sendo elas descritas logo no início desse READ.me, nos conceitos do Projeto :D

