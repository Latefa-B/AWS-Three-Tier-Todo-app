# AWS-Three-Tier-Todo-app
Deploying a To-Do List Web Application on AWS using the Three Tier-Architecture

Introduction
The project is about deploying a To-Do List Web Application on AWS using the three tier Architecture. This Architecture consists of three layers : the Presentation layer (frontend), the Logic layer (backend) and the Data layer (database) for a highly available and fault-tolerant web application. 

For this purpose, I will be presenting the steps to the process of deploying a web application on AWS using Amazon services : IAM, VPC, EC2, ELB & ASG, S3, EFS and RDS. Built using the three tier architecture for a fault tolerance and high available application. 

Architecture of the Web Application : Three tier Application


Steps to the process of building and deploying the To-do-list Web Application using the three tier Architecture on AWS : 

Step 1 : Set up the infrastructure
The infrastructure set up for this project is a virtual private network over the Cloud for secure and isolated resources. The VPC and its components will be deployed in the North Virginia Region across two availability zones AZa and AZb. 


Create a Virtual Private Cloud (VPC)
Navigate to the VPC dashboard in the AWS Management Console
Click on “Create VPC”
Configure the VPC settings (CIDR block, name…) and leave other settings as default. 
Click “Create VPC”
specify the region 



Create and Configure Subnets
Create two Public subnets that will host the frontend app, located in two different AZs. These subnets allow resources within them to have direct internet access.
go to the subnets section in the VPC dashboard 
click on “create subnet”
select your vpc
create two subnets one in each AZ (AZa and AZb), name it, specify  a CIDR block.






Create two Private subnets to host the backend app, located in two different AZs:
go to the subnets section in the VPC dashboard 
click on “create subnet”
select your vpc
create two subnets one in each AZ (AZa and AZb), name it, specify  a CIDR block.










Create one Private subnet to host the database app, located in AZa:
go to the subnets section in the VPC dashboard 
click on “create subnet”
select your vpc
create two subnets one in each AZ (AZa and AZb), name it, specify  a CIDR block.



Set up the Internet Gateway 
Set up an internet gateway and attach it to your VPC, to allow communication over the internet between the resources.

Go to the internet gateways section
click on “create internet gateway”
name it and click “Create”.
Attach the internet gateway to your vpc

   


Configure Route Tables 
Create route tables for the public and private subnets. Then associate the public subnets with a route table that has a route to the internet via an Internet Gateway (IGW). And associate the private subnets with a route table that routes traffic through a Network Address Translation (NAT) Gateway or NAT instance in the public subnets.

Go to the route tables section
click on “create route table”
name it and associate it with the project VPC
Add a route to the Public-Route-Table : destination: 0.0.0.0/0 . target: name of the internet gateway
associate the Public-Route-table with the public-subnet




Create NAT Gateways for Private Subnets
Create two NAT Gateways one for the backend layer and the database layer :
go to the NAT gateways section
click on “create NAT Gateway”
select the public-subnet and allocate an elastic IP address
click create Nat gateway 




Update Route Tables for private subnets:
Update route tables for both private subnets (backend and database layers): 
go to the route tables section 
click on create route table
name it  and associate it with the project vpc
add a route to the private-route-table, destination 0.0.0.0/0 and target: todo-app Nat gateway 
associate the private-route-table with the private-subnet

For the Backend instance: 



For the Database instance: 




Step 2 : Secure the Application

For this project I will configure five SG to control inbound and outbound traffic to instances and secure the application:
The first security group of External ELB  to allow HTTP access from anywhere
The second security group of frontend instance : to allow HTTP access from anywhere and from the security group of the ELB, as well as SSH access from my IP.
The third security group of backend instances: to allow traffic on TCP protocol with flask framework and SSH access from the frontend instance security group.
The fourth security group of database instance: to allow Mysql/Aurora access from the backend security group and SSH traffic from the frontend security group as well as all traffic access. 
The fifth security group of EFS Elastic file shared system to allow NFS traffic on Port 2049 from the backend instance security group

External ELB  security group to allow HTTP access from anywhere
Go to the security groups section in the vpc dashboard
create a security group, name it and add inbound rules to allow HTTP traffic on port 80 from anywhere



The Frontend instance security group to allow SSH access on Port 22 from my IP, HTTP access on Port 80 from anywhere and HTTP access from the security group of the external ELB.
Go to the security groups section in the vpc dashboard
create a security group, name it and add three inbound rules to allow SSH access on Port 22 from my IP, HTTP access on Port 80 from anywhere and HTTP access from the security group of the external ELB.



3. The Backend instance security group to allow traffic on TCP protocol with flask framework on Port 5000 and allow SSH access from the frontend instance security group.
Go to the security groups section in the vpc dashboard
create a security group, name it and add two inbound rules to allow SSH access on Port 22 from the frontend instance security group and TCP access with flask framework on Port 5000 for webserving purposes. 



4. The database security group to allow Mysql/Aurora access from the backend security group and SSH traffic from the frontend security group as well as all traffic access.
Go to the security groups section in the vpc dashboard
create a security group, name it and add three inbound rules to allow SSH access on Port 22 from the frontend instance security group, allow Mysql/Aurora access from the backend security group and allow all traffic access.



5. EFS security group to allow NFS traffic on Port 2049 from the backend instance security group
Go to the security groups section in the vpc dashboard
create a security group, name it and add inbound rule to allow NFS traffic on Port 2049 from the backend instance security group



Step 3 : Configure IAM roles and permissions
For this project, I will be creating a role, in order to allow EC2 instances to access other AWS resources securely. The role grants : S3ReadOnly, AmazonRDSFullAccess, and AmazonSSMManagedInstanceCore Permissions, in order to grant the instances permission to read the file in the S3 buckets related to the project, to have full access the RDS database and grant access to Session Manager  instead of using SSH.


Go to the IAM dashboard.
Create roles under access management.  
Specify the type of entity : AWS service, mention a service or use case, and add three permissions : S3ReadOnly permission, AmazonRDSFullAccess permission, and AmazonSSMManagedInstanceCore Permission. 
Name the role and create it.





Step 4 : Set up S3 Simple Storage 

After setting up the project infrastructure and configuring the traffic security, I will be setting up the S3 simple storage to store static content.

Create and configure an S3 bucket
Go to the S3 dashboard and create a new bucket.
Configure bucket settings and permissions.
Upload static file (header image of the todo-list web application).










Step 5 : Set up the Backend Application

Launch the  Backend EC2 instances
Navigate to the EC2 dashboard
click on “launch instance”
Configure the instance settings: Choose an amazon machine image AMI, Select an instance type t2.micro, in network  select the project vpc, select the private subnet
Attach the backend instance security group previously created to the instance 
Attach the IAM role to the instance profile
launch instance









Step 6 : Build the Database Application
Create a Subnet Group
Create a subnet group for the RDS database in order to allow a higher availability and a better security.

Go on Amazon RDS Dashboard
under Subnet Groups, click on create DB subnet group
Name the subnet group, specify the VPC and Subnets of the project
click on Create


Design an RDS Database 
Go to the “RDS” dashboard and click “Create database”.
Choose the database engine (MySQL).
Configure database settings (instance class, storage).
Configure the RDS instance in a private subnet for security.






Configure the RDS Security Group
Configure the RDS security group created earlier to allow inbound traffic from the backend EC2 instances.






Build The Database Application 
After setting up the backend instance and creating the RDS database instance, I will build the database application.

Connect to the instance using Session Manager
On the backend instance terminal, host mysql
Connect to the database from the backend instance using its endpoint and credentials
Once inside mysql, configure the database ( create and add tasks) and exit it.






Step 7 : Build the Backend Application 
Launch and configure EC2 instances
Backend EC2 instance was previously launched, it allowed us to connect to the RDS from it and build the project database. 

Deploy the Backend application
Install Python dependencies : python3, python3-pip, python3-venv for the virtual environment.
Transfer the application code to the backend EC2 instance.
Create a virtual environment and configure Flask as a framework and Gunicorn as a Python Web Server Gateway Interface HTTP server. 

























Step 8 : Build the Frontend Application

Launch and configure  the Frontend EC2 Instances
Navigate to the EC2 dashboard
click on “launch instance”
Configure the instance settings: Choose an amazon machine image AMI, Select an instance type t2.micro, in network  select the project vpc: select the public subnet
Attach the frontend instance security group previously created to the instance 
Attach the IAM role to the instance profile
launch instance



Deploy the Frontend EC2 Instances
HTML/CSS/JavaScript are hosted on EC2
Update apt-get package manager
Install Python and dependencies







Create a work directory for the frontend layer



Install on the terminal AWS CLI and upload the static file from S3 bucket (header image of the web app)
Transfer the frontend code (index html file) to the frontend EC2 instance.




Install and create a virtual environment
Configure inside the virtual environment flask framework and dependencies






Install Gunicorn, Python Web Server Gateway Interface HTTP server and configure the service file







test connectivity with gunicorn
















Configure web server Nginx

















Deploy and test Todo-list Web application in the browser using the Public IP address of the frontend EC2 instance























Step 9 : Configure Load Balancing & Auto Scaling for high availability 

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



Step 10 : Set up the EFS shared storage

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


Summary
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

