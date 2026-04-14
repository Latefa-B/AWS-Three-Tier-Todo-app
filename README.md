# Step by step Guide to Deploying a To-Do List Web Application on AWS using the Three Tier-Architecture

The project is about deploying a To-Do List Web Application on AWS using the three tier Architecture. This Architecture consists of three layers : the Presentation layer (frontend), the Logic layer (backend) and the Data layer (database) for a highly available and fault-tolerant web application. 

For this purpose, I will be presenting the steps to the process of deploying a web application on AWS using services like : IAM, VPC, EC2, ELB & ASG, S3, EFS and RDS. Built using the three tier architecture for a fault tolerance and high available application. 

## Architecture of the Web Application : Three tier Application
<img width="779" height="492" alt="Screenshot 2024-09-15 at 2 43 54 AM" src="https://github.com/user-attachments/assets/6b04a8c9-ca3e-4aa7-b9a3-805e4da825d8" />

## Step-by-step instructions 

### Step 1 : Set up the infrastructure
The infrastructure set up for this project is a virtual private network over the Cloud for secure and isolated resources. The VPC and its components will be deployed in the North Virginia Region across two availability zones AZa and AZb. 
- Create a Virtual Private Cloud (VPC)
- Navigate to the VPC dashboard in the AWS Management Console\
- Click on “Create VPC”
- Configure the VPC settings (CIDR block, name…) and leave other settings as default.
- Click “Create VPC”
- specify the region 
<img width="1187" height="614" alt="1" src="https://github.com/user-attachments/assets/f48676b4-8ff3-4b0f-ac47-a946159707a1" />

- Create and Configure Subnets
- Create two Public subnets that will host the frontend app, located in two different AZs. These subnets allow resources within them to have direct internet access.
- go to the subnets section in the VPC dashboard 
- click on “create subnet”
- select your vpc
- create two subnets one in each AZ (AZa and AZb), name it, specify  a CIDR block.
<img width="1180" height="629" alt="2" src="https://github.com/user-attachments/assets/231e4156-9387-44e1-aa0b-178aba5dcfae" />
<img width="1191" height="610" alt="3" src="https://github.com/user-attachments/assets/456d0e2a-bebc-40a4-abd5-821674cdd787" />

Create two Private subnets to host the backend app, located in two different AZs:
- go to the subnets section in the VPC dashboard 
- click on “create subnet”
- select your vpc
- create two subnets one in each AZ (AZa and AZb), name it, specify  a CIDR block.
<img width="1187" height="634" alt="4" src="https://github.com/user-attachments/assets/07854124-90b0-4d35-b4e4-a29cb9602569" />
<img width="1171" height="638" alt="5" src="https://github.com/user-attachments/assets/920a324e-aaa9-4d0c-ad79-5c759b9af3a1" />

- Create one Private subnet to host the database app, located in AZa:
- go to the subnets section in the VPC dashboard 
- click on “create subnet”
- select your vpc
- create two subnets one in each AZ (AZa and AZb), name it, specify  a CIDR block.
<img width="1225" height="621" alt="6" src="https://github.com/user-attachments/assets/dfa555fc-8b3b-49df-b1ca-d34f4e35b652" />
<img width="1187" height="643" alt="7" src="https://github.com/user-attachments/assets/32419b00-0c61-4f38-86ec-deb0b25b875d" />

- Set up the Internet Gateway 
- Set up an internet gateway and attach it to your VPC, to allow communication over the internet between the resources.
- Go to the internet gateways section
- click on “create internet gateway”
- name it and click “Create”.
<img width="1186" height="411" alt="8" src="https://github.com/user-attachments/assets/e2b76b8a-ab7f-4ab4-b61b-3d1c504f07d4" />

- Attach the internet gateway to your vpc
<img width="1171" height="562" alt="9" src="https://github.com/user-attachments/assets/5fdfe6d3-4b6f-4f26-a5a5-f1cf0ad06308" />

- Configure Route Tables : 
Create route tables for the public and private subnets. Then associate the public subnets with a route table that has a route to the internet via an Internet Gateway (IGW). And associate the private subnets with a route table that routes traffic through a Network Address Translation (NAT) Gateway or NAT instance in the public subnets.

- Go to the route tables section
- click on “create route table”
- name it and associate it with the project VPC
- Add a route to the Public-Route-Table : destination: 0.0.0.0/0 . target: name of the internet gateway
- associate the Public-Route-table with the public-subnet
<img width="1195" height="536" alt="10" src="https://github.com/user-attachments/assets/0347adf2-df62-439a-991d-09c84af43614" />

- Create NAT Gateways for Private Subnets
- Create two NAT Gateways one for the backend layer and the database layer :
- go to the NAT gateways section
- click on “create NAT Gateway”
- select the public-subnet and allocate an elastic IP address
- click create Nat gateway 
<img width="1161" height="592" alt="11" src="https://github.com/user-attachments/assets/9e696bf8-f064-40d0-a6a9-2a5c601b8d10" />

- Update Route Tables for private subnets:
- Update route tables for both private subnets (backend and database layers): 
- go to the route tables section 
- click on create route table
- name it  and associate it with the project vpc
- add a route to the private-route-table, destination 0.0.0.0/0 and target: todo-app Nat gateway 
- associate the private-route-table with the private-subnet

For the Backend instance: 
<img width="1169" height="554" alt="12" src="https://github.com/user-attachments/assets/1b0df447-012a-4d93-9e35-1b66ffdaeb58" />
<img width="1232" height="452" alt="13" src="https://github.com/user-attachments/assets/63dad603-54df-4585-bc79-071c8f3d8c78" />


For the Database instance: 
<img width="1179" height="651" alt="14" src="https://github.com/user-attachments/assets/6e8e2fc2-fc71-4ef9-ab94-ff9bb35079c9" />
<img width="1165" height="537" alt="15" src="https://github.com/user-attachments/assets/f8fba04d-4327-43a1-aecb-3e6971da01f6" />
<img width="1168" height="533" alt="16" src="https://github.com/user-attachments/assets/cfddd637-df2d-4675-85e2-aacc05773f65" />
<img width="1103" height="640" alt="17" src="https://github.com/user-attachments/assets/8cca2370-1ded-48c5-aa00-a71954dc9044" />

### Step 2 : Secure the Application

For this project I will configure five SG to control inbound and outbound traffic to instances and secure the application:
- **External ELB security group**: to allow HTTP access from anywhere.
- **Frontend instance security group**: to allow HTTP access from anywhere and from the security group of the ELB, as well as SSH access from my IP.
- **Backend instances security group**: to allow traffic on TCP protocol with flask framework and SSH access from the frontend instance security group.
- **Database instance security group**: to allow Mysql/Aurora access from the backend security group and SSH traffic from the frontend security group as well as all traffic access. 
- **EFS Elastic file shared system security group**: to allow NFS traffic on Port 2049 from the backend instance security group.

- **External ELB security group to allow HTTP access from anywhere**
- Go to the security groups section in the vpc dashboard
- create a security group, name it and add inbound rules to allow HTTP traffic on port 80 from anywhere
<img width="1149" height="643" alt="1" src="https://github.com/user-attachments/assets/53ab5af6-421f-4cfe-ad90-7ef0a33c0adc" />

- **Frontend instance security group to allow SSH access on Port 22 from my IP, HTTP access on Port 80 from anywhere and HTTP access from the security group of the external ELB**
- Go to the security groups section in the vpc dashboard
- create a security group, name it and add three inbound rules to allow SSH access on Port 22 from my IP, HTTP access on Port 80 from anywhere and HTTP access from the security group of the external ELB.
<img width="1175" height="670" alt="2" src="https://github.com/user-attachments/assets/64f7f408-9b26-4240-8f45-8cb04b09904a" />

- **Backend instances security group to allow traffic on TCP protocol with flask framework on Port 5000 and allow SSH access from the frontend instance security group**
- Go to the security groups section in the vpc dashboard
- create a security group, name it and add two inbound rules to allow SSH access on Port 22 from the frontend instance security group and TCP access with flask framework on Port 5000 for webserving purposes. 

- **Database instance security group to allow Mysql/Aurora access from the backend security group and SSH traffic from the frontend security group as well as all traffic access**
- Go to the security groups section in the vpc dashboard
- create a security group, name it and add three inbound rules to allow SSH access on Port 22 from the frontend instance security group, allow Mysql/Aurora access from the backend security group and allow all traffic access.
<img width="1150" height="695" alt="Screenshot 2024-09-17 at 12 09 48 PM" src="https://github.com/user-attachments/assets/2d3b81e4-1763-4b6e-a2ca-913739e41bd2" />

- **EFS security group to allow NFS traffic on Port 2049 from the backend instance security group**
- Go to the security groups section in the vpc dashboard
- create a security group, name it and add inbound rule to allow NFS traffic on Port 2049 from the backend instance security group
<img width="1146" height="663" alt="Screenshot 2024-09-17 at 12 12 20 PM" src="https://github.com/user-attachments/assets/d1b892b3-5e52-42e9-a908-645b2db1a56c" />

### Step 3 : Configure IAM roles and permissions
For this project, I will be creating a role, in order to allow EC2 instances to access other AWS resources securely. The role grants : **S3ReadOnly, AmazonRDSFullAccess,** and **AmazonSSMManagedInstanceCore Permissions**, in order to grant the instances permission to read the file in the S3 buckets related to the project, to have full access the RDS database and grant access to Session Manager  instead of using SSH.

- Go to the IAM dashboard.
- Create roles under access management.  
- Specify the type of entity : AWS service, mention a service or use case, and add three permissions : S3ReadOnly permission, AmazonRDSFullAccess permission, and AmazonSSMManagedInstanceCore Permission. 
- Name the role and create it.
<img width="1126" height="385" alt="Screenshot 2024-09-17 at 12 20 19 PM" src="https://github.com/user-attachments/assets/54136bc1-201b-4590-a503-114d053a21e5" />

<img width="1113" height="410" alt="Screenshot 2024-09-17 at 12 20 28 PM" src="https://github.com/user-attachments/assets/56466849-62e6-4e66-92bf-1808454a1521" />

### Step 4 : Set up S3 Simple Storage 
After setting up the project infrastructure and configuring the traffic security, I will be setting up the S3 simple storage to store static content.

- Create and configure an S3 bucket
- Go to the S3 dashboard and create a new bucket.
- Configure bucket settings and permissions.
- Upload static file (header image of the todo-list web application).

<img width="1109" height="518" alt="Screenshot 2024-09-17 at 12 47 45 PM" src="https://github.com/user-attachments/assets/199b5437-89b4-4a9e-82c6-81e1a5c22e18" />

<img width="1128" height="528" alt="Screenshot 2024-09-17 at 12 47 56 PM" src="https://github.com/user-attachments/assets/b7191ed1-1698-4e00-9349-7dd9467d3fbe" /> 

<img width="1108" height="530" alt="4" src="https://github.com/user-attachments/assets/32c2c6a8-ccb0-4958-b5e2-92366d52350b" />

<img width="1083" height="657" alt="5" src="https://github.com/user-attachments/assets/66240221-97d0-4e6d-8fc8-905fa057ea09" />
<img width="1401" height="650" alt="6" src="https://github.com/user-attachments/assets/6a9ef6cc-136a-4832-a84f-1f0040a2b832" />

### Step 5 : Set up the Backend Application
- Launch the  Backend EC2 instances
- Navigate to the EC2 dashboard
- click on “launch instance”
- Configure the instance settings: Choose an amazon machine image AMI, Select an instance type t2.micro, in network  select the project vpc, select the private subnet
- Attach the backend instance security group previously created to the instance 
- Attach the IAM role to the instance profile
- launch instance
<img width="1231" height="681" alt="Screenshot 2024-09-17 at 1 49 33 PM" src="https://github.com/user-attachments/assets/2cd1c858-c392-4bd7-a46b-c2147f6efef5" />

<img width="1173" height="677" alt="Screenshot 2024-09-17 at 1 49 51 PM" src="https://github.com/user-attachments/assets/295e75c3-16fa-4429-85cd-5dcd7699f856" />
<img width="1145" height="272" alt="Screenshot 2024-09-17 at 1 50 08 PM" src="https://github.com/user-attachments/assets/84a5707d-f336-4772-9153-6b41bd0b4827" />

### Step 6 : Build the Database Application
- **Create a Subnet Group:**
- Create a subnet group for the RDS database in order to allow a higher availability and a better security.
- Go on Amazon RDS Dashboard : under Subnet Groups, click on create DB subnet group
- Name the subnet group, specify the VPC and Subnets of the project
- click on Create


- **Design an RDS Database** 
- Go to the “RDS” dashboard and click “Create database”.
- Choose the database engine (MySQL).
- Configure database settings (instance class, storage).
- Configure the RDS instance in a private subnet for security.
<img width="1110" height="437" alt="Screenshot 2024-09-17 at 1 09 21 PM" src="https://github.com/user-attachments/assets/7becae8b-f44d-4514-a977-bb40350bd849" />

- **Configure the RDS Security Group**
- Configure the RDS security group created earlier to allow inbound traffic from the backend EC2 instances.
<img width="1104" height="680" alt="Screenshot 2024-09-17 at 1 10 12 PM" src="https://github.com/user-attachments/assets/b8b1864b-5881-4c04-a173-f27d636945f3" />


- **Build The Database Application**
After setting up the backend instance and creating the RDS database instance, I will build the database application.

- **Connect to the instance using Session Manager**
- On the backend instance terminal, host mysql
- Connect to the database from the backend instance using its endpoint and credentials
- Once inside mysql, configure the database ( create and add tasks) and exit it.

<img width="1031" height="713" alt="1" src="https://github.com/user-attachments/assets/b3099dca-5094-4687-a4f5-2b9bda7cfec7" />

<img width="1153" height="518" alt="2" src="https://github.com/user-attachments/assets/f20bc942-3ce4-42c2-9ecf-cd319bf8cf1e" />

<img width="749" height="360" alt="Screenshot 2024-09-09 at 1 37 55 PM" src="https://github.com/user-attachments/assets/2d4e74be-76b7-4c42-9be0-f1b416023637" />

<img width="631" height="515" alt="Screenshot 2024-09-09 at 1 41 20 PM" src="https://github.com/user-attachments/assets/964404f1-3ad7-4738-9595-3438198d5af7" />

<img width="622" height="514" alt="Screenshot 2024-09-09 at 1 43 41 PM" src="https://github.com/user-attachments/assets/fe830b96-4782-415b-9afc-9d7fcea3ea76" />


### Step 7 : Build the Backend Application 
- **Launch and configure EC2 instances**
Backend EC2 instance was previously launched, it allowed us to connect to the RDS from it and build the project database. 
- Deploy the Backend application
- Install Python dependencies : python3, python3-pip, python3-venv for the virtual environment.
- Transfer the application code to the backend EC2 instance.
- Create a virtual environment and configure Flask as a framework and Gunicorn as a Python Web Server Gateway Interface HTTP server. 
<img width="934" height="639" alt="Screenshot 2024-09-09 at 1 51 29 PM" src="https://github.com/user-attachments/assets/9a914aa0-0939-4a69-b893-af9e5eb2b2f0" />

<img width="627" height="105" alt="Screenshot 2024-09-09 at 2 09 56 PM" src="https://github.com/user-attachments/assets/6b7fb389-df96-431a-86a5-d6b081e8c0be" />

<img width="603" height="94" alt="Screenshot 2024-09-09 at 2 15 27 PM" src="https://github.com/user-attachments/assets/f9921b5d-9941-44f8-a282-06baefd545ed" />

<img width="652" height="105" alt="Screenshot 2024-09-09 at 2 29 13 PM" src="https://github.com/user-attachments/assets/c8c88499-d8ac-4315-b1cf-39f200c7e137" />

<img width="796" height="692" alt="Screenshot 2024-09-09 at 2 00 11 PM" src="https://github.com/user-attachments/assets/fe7f8264-685d-4323-a3c3-c7477cdba723" />

<img width="429" height="58" alt="Screenshot 2024-09-09 at 2 35 27 PM" src="https://github.com/user-attachments/assets/c926b898-3eeb-44df-83f6-8d4af52bdb9b" />

<img width="1171" height="501" alt="Screenshot 2024-09-09 at 2 44 35 PM" src="https://github.com/user-attachments/assets/d554a206-533e-48a9-9183-f589fbda8c75" />

<img width="1121" height="629" alt="Screenshot 2024-09-09 at 2 47 37 PM" src="https://github.com/user-attachments/assets/0995d4ed-8df4-4069-8ab3-c472d0a872b2" />

<img width="1121" height="629" alt="Screenshot 2024-09-09 at 2 47 37 PM" src="https://github.com/user-attachments/assets/07d1577f-9e8f-4c14-990f-4fa5d2b355fb" />

<img width="1374" height="278" alt="Screenshot 2024-09-09 at 2 47 59 PM" src="https://github.com/user-attachments/assets/ef7c4495-cbb3-4a2e-84f0-a916af9b99c9" />

<img width="1169" height="207" alt="Screenshot 2024-09-09 at 2 51 38 PM" src="https://github.com/user-attachments/assets/21276dfa-8fd7-4618-8dad-d38dec098b18" />

<img width="1097" height="146" alt="Screenshot 2024-09-09 at 2 52 19 PM" src="https://github.com/user-attachments/assets/4be2d896-fd56-4170-9234-66bea2f6d510" />


### Step 8 : Build the Frontend Application
- **Launch and configure  the Frontend EC2 Instances**
- Navigate to the EC2 dashboard
- click on “launch instance”
- Configure the instance settings: Choose an amazon machine image AMI, Select an instance type t2.micro, in network  select the project vpc: select the public subnet
- Attach the frontend instance security group previously created to the instance 
- Attach the IAM role to the instance profile
- launch instance
<img width="1225" height="695" alt="Screenshot 2024-09-17 at 10 57 40 PM" src="https://github.com/user-attachments/assets/0f4a0612-be71-4961-b00b-240933c654f0" />

<img width="1134" height="660" alt="Screenshot 2024-09-17 at 10 56 31 PM" src="https://github.com/user-attachments/assets/b0b37107-2d9b-4094-bbeb-e7ad678ebeab" />

- **Deploy the Frontend EC2 Instances**
- HTML/CSS/JavaScript are hosted on EC2
- Update apt-get package manager
- Install Python and dependencies
<img width="996" height="631" alt="Screenshot 2024-09-10 at 12 23 17 PM" src="https://github.com/user-attachments/assets/f06b3a61-ed79-4a8c-8a26-58b29f41ff45" />

<img width="1219" height="489" alt="Screenshot 2024-09-10 at 12 24 00 PM" src="https://github.com/user-attachments/assets/260cad3a-5161-478e-9663-f6f41ee49a9f" />

<img width="1200" height="397" alt="Screenshot 2024-09-10 at 12 31 53 PM" src="https://github.com/user-attachments/assets/aa8fe1ba-3b2a-43e4-8858-d40c764a9528" />

- Create a work directory for the frontend layer
<img width="349" height="107" alt="Screenshot 2024-09-10 at 12 40 43 PM" src="https://github.com/user-attachments/assets/e17e29a1-9653-4f5c-bb00-e92137c78b51" />

<img width="731" height="104" alt="Screenshot 2024-09-10 at 12 44 30 PM" src="https://github.com/user-attachments/assets/69b48f4e-7420-4488-b422-d15b7c275b5f" />

- **Install on the terminal AWS CLI and upload the static file from S3 bucket (header image of the web app)**
- Transfer the frontend code (index html file) to the frontend EC2 instance.
<img width="918" height="131" alt="Screenshot 2024-09-10 at 12 46 06 PM" src="https://github.com/user-attachments/assets/0f69c6b1-8d72-43d3-8520-21e28556b14a" />
<img width="464" height="169" alt="Screenshot 2024-09-10 at 12 46 59 PM" src="https://github.com/user-attachments/assets/cb6a29b2-435c-40fc-a6a0-fa2c2d5e5aed" />


- **Install and create a virtual environment**
- Configure inside the virtual environment flask framework and dependencies
<img width="600" height="235" alt="Screenshot 2024-09-10 at 12 51 02 PM" src="https://github.com/user-attachments/assets/c6c009e0-0a7d-4b6b-88c0-e7b250617f33" />
<img width="1151" height="480" alt="Screenshot 2024-09-10 at 12 52 43 PM" src="https://github.com/user-attachments/assets/c844f75b-bafc-4bc6-a21f-e76dd70e2916" />
<img width="1224" height="254" alt="Screenshot 2024-09-10 at 12 52 58 PM" src="https://github.com/user-attachments/assets/716e2c52-05c3-4229-88c0-a748eefb6309" />
<img width="1209" height="227" alt="Screenshot 2024-09-10 at 12 55 05 PM" src="https://github.com/user-attachments/assets/d0604502-ab3a-484b-9859-03dfe6b9231e" />

- **Install Gunicorn, Python Web Server Gateway Interface HTTP server and configure the service file**
<img width="741" height="206" alt="Screenshot 2024-09-10 at 12 55 21 PM" src="https://github.com/user-attachments/assets/4e6d4492-d36f-4c9a-a479-39736ce12102" />
<img width="874" height="406" alt="Screenshot 2024-09-10 at 1 05 14 PM" src="https://github.com/user-attachments/assets/9ad49aca-3cca-4a28-8e9a-a626f04122b0" />
<img width="1203" height="163" alt="Screenshot 2024-09-10 at 1 13 45 PM" src="https://github.com/user-attachments/assets/8f2a4488-53fa-4c39-a8d8-f70e4f253778" />

- **test connectivity with gunicorn**
<img width="725" height="711" alt="Screenshot 2024-09-10 at 1 15 05 PM" src="https://github.com/user-attachments/assets/00e93973-565d-4101-a964-96f97756e0ae" />
<img width="596" height="715" alt="Screenshot 2024-09-10 at 1 15 15 PM" src="https://github.com/user-attachments/assets/ef4b9507-6ca9-4137-a985-2228e36b8d17" />

- **Configure web server Nginx**
<img width="1038" height="663" alt="Screenshot 2024-09-10 at 1 49 08 PM" src="https://github.com/user-attachments/assets/c34cdbec-592d-46a5-b4ac-cf07a03877bf" />
<img width="709" height="623" alt="Screenshot 2024-09-10 at 2 08 46 PM" src="https://github.com/user-attachments/assets/f04bc0e1-81cf-4916-aef4-00a3b631fd34" />
<img width="791" height="662" alt="Screenshot 2024-09-10 at 2 15 59 PM" src="https://github.com/user-attachments/assets/327326dc-d06b-4dd5-b6aa-5c8e450c4d8b" />
<img width="1064" height="663" alt="Screenshot 2024-09-10 at 2 16 10 PM" src="https://github.com/user-attachments/assets/c2b03bca-54fb-4996-8867-fb673202c870" />
<img width="808" height="443" alt="Screenshot 2024-09-10 at 2 17 49 PM" src="https://github.com/user-attachments/assets/10308b16-157f-47f6-ae95-78e9387fe16f" />
<img width="630" height="84" alt="Screenshot 2024-09-10 at 2 18 14 PM" src="https://github.com/user-attachments/assets/bc26c39b-46aa-48bb-b5df-8ab6993b53f1" />
<img width="795" height="495" alt="Screenshot 2024-09-10 at 2 18 56 PM" src="https://github.com/user-attachments/assets/c630eb11-310c-496e-9320-2fadc15e9c62" />

- **Deploy and test Todo-list Web application in the browser using the Public IP address of the frontend EC2 instance**
<img width="1403" height="733" alt="Screenshot 2024-09-11 at 3 40 58 PM" src="https://github.com/user-attachments/assets/2e682d66-8619-4ee9-ac8b-4bc32d1c0ed8" />
<img width="958" height="827" alt="Screenshot 2024-09-11 at 3 41 23 PM" src="https://github.com/user-attachments/assets/aa78f29f-e70c-45f9-a7ba-7eeee4f6690e" />

### Step 9 : Configure Load Balancing & Auto Scaling for high availability 

Create and configure ELB and ASG to distribute traffic and scale the application for fault tolerance and high availability.

Set Up ELB (Elastic Load Balancer)
Create Target group





Create an ELB:
   - Go to the EC2 dashboard and select ‘Load Balancers’.
   - Click ‘Create Load Balancer’ and choose Application Load Balancer
  - Configure the ELB to be placed in public subnets and to route traffic to the frontend EC2 instances.
   - Set up listeners (HTTP on port 80).
   - Configure health checks to monitor the health of the frontend instances.



Set Up Auto Scaling Group (ASG)
Create a Launch Configuration:
Go to the EC2 dashboard and select ‘Launch Configurations’. 
Create a new launch configuration for the frontend EC2 instances. 
Specify the AMI, instance type, and security groups.







Go to the EC2 dashboard and select ‘Auto Scaling Groups’.
Create an Auto Scaling Group and associate it with the launch configuration.
Set the desired number of instances, minimum and maximum size, and scaling policies.
Configure the ASG to be placed in the public subnet and to use the ELB.










Test the web application using the ELB



### Step 10 : Set up the EFS shared storage

For this project, I will be setting up EFS for shared storage across the backend EC2 instances.

Create an EFS File System
Go to the EFS dashboard and create a new file system.
Configure the EFS settings, including the project VPC and mount targets in the subnets.







Update EFS file system network configuration


Attach the security group created previously for EFS to the EC2 instances to allow NFS traffic on port 2049. Update the backend EC2 security groups



Mount EFS on EC2 Instances
Install the NFS client on the EC2 instances
Update the apt-get package manager



Create a mount point 


Mount the EFS file system to the directory created
Verify the mount 


### Summary
This breakdown provides a step-by-step guide for Deploying a web application using the three-tier architecture on AWS. In summary, I have: 
Set up the infrastructure over the cloud (VPC) in order to isolate the resources for a secure deployment
Configure the security groups for the application in order to control inbound and outbound traffic
Configure IAM role and Permissions to secure access to the AWS resources
Set up S3 simple storage for the frontend layer
Build the database layer
Build the backend layer hosted in the private subnets that contains the application code and sensitive data.
Build the frontend layer hosted in the public subnets that contains static files
Deploying and testing the todo-list web application using the frontend Public IP address
Configure ELB and ASG for fault tolerance and high availability
Deploying and testing the todo-list web application using the ELB
Set up the EFS shared storage for the backend layer in order to store the application code.

