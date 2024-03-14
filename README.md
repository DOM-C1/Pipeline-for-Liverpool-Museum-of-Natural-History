# LMNH ETL Pipeline Project

# Getting set-up:
In order to run this script you will need to be in the root directory of the project and run:
 ```pip3 install -r requirements.txt
    brew tap hashicorp/tap
    brew install hashicorp/tap/terraform```


Then you will need to set-up the database, this will be done through terraform, you will need to create file called 'terraform.tfvars' with the following information:
```
AWS_ACCESS_KEY_ID 
AWS_SECRET_ACCESS_KEY 
DB_PASSWORD 
DB_USERNAME 
REGION
DB_ID 
SG_NAME
VPC_ID 
VPC_NAME 
ID 



```
then run `terraform apply` in the set-up_db folder

You will also need to set up your .env file. This is the structure you will need:
```
AWS_KEY
AWS_SECRET_KEY
DB_PASSWORD
DB_USERNAME
DB_HOST
DB_NAME
BOOTSTRAP_SERVERS
SECURITY_PROTOCOL
SASL_MECHANISM
USERNAME
PASSWORD
TOPIC
G_ID
```


With all this setup you can simply run `python3 pipeline.py` from the pipeline file






# Overview

This project focuses on developing a comprehensive ETL (Extract, Transform, Load) pipeline to handle data from the London Museum of Natural History (LMNH). The objective is to efficiently manage the flow of data from live kiosk interactions within the museum, ensuring the data is clean, valid, and stored securely in a cloud-based database for further analysis.


## Competencies Demonstrated


- **Connecting to the live data stream on a Kafka cluster**: Consuming from the live data stream.
- **Cleaning the data**: Implementing filters and validation rules to ensure only relevant and accurate data is inserted into the database.

- **Hosting the ETL script on an EC2 instance**: Ensuring our pipeline is running on a stable, scalable platform.

##

### Potential Issues

Invalid data may arise from:

- **Human error**: Accidental interactions with kiosks by staff or visitors outside operational hours.
- **Mechanical failure**: Issues like stuck buttons or accidental impacts on kiosks.
- **Wireless interference**: Non-kiosk messages received over the network.
- **Incorrect exhibitions**: Data from similar kiosks not part of this project should be disregarded.

### Handling Invalid Data

To maintain data integrity, we apply the following rules:

- **Operational hours**: Only consider kiosk interactions between 8:45am and 18:15pm, aligning with LMNH's public hours.
- **Valid interactions**: Ratings should be within 0-4
- **Exhibit inclusion**: Ignore interactions from exhibits not listed in our project's AWS S3 bucket.
- **Data keys**: Discard any message with invalid keys.

## Kiosk Interface Design

The kiosks feature five rating buttons and two 'assistance' buttons, designed for intuitive public interaction which take on a value, either 1 for emergence or 0 for assistance.
