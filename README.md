# Dev-Ops
### Dev-ops and software development

This Repo is based on the developmental process of a fully integrated machine learning system. 

The system is designed to ingest data, run algorithems and display them on a dashboard for interpritation. 

In many cases these systems can be quite difficult to develop, but by utilizing software such as the ones listed below you can streamline your development process. All of your application should be ran inside of a docker; this type of system design gives you the ability to build the system without the need of a heavy development cycle. All of the application needed can be found at the docker hub (https://hub.docker.com/) prepackeged, in combination with docker-compose these application can be fired up in tandem when needed. 

- Docker
- Nifi
- Airflow
- Postgres
- Elasticsearch
- Kibana


## How to start the system

### Prerequisite
First you need to install docker onto your system. The install instructions for all systems can be found here https://docs.docker.com/compose/install/ on the docker website.

Once docker is installed you will need to be sure docker-compose is installed. Docker compose can be found here https://docs.docker.com/compose/install/ on the docker website.

## Special intructions for airflow docker container

The airflow container is quite weird and can only be configured in house. 

#### Docker:

```FROM puckel/docker-airflow:latest
USER root
ARG DOCKER_GROUP_ID
# Install Docker
RUN pip install 'Docker==4.2.0'
# Add permissions for running docker.sock
RUN groupadd -g $DOCKER_GROUP_ID docker && gpasswd -a airflow docker
USER airflow
```

Once this docker container is built you will need to launch it like so: *the period at the end of the statement needs to be included*

``` 
docker build --rm --build-arg DOCKER_GROUP_ID=`getent group docker | cut -d: -f3` -t docker-airflow .
```
Now that you've built the special docker container for the airflow system you are set to launch the docker-compose system. 

When running the docker file you will need to turn the file such as this.

# Starting the enviorment
As mentioned above the system is already designed and configured in order to start the system you need to find the docker-compose file in the current repo. 

once in the folder where the docker-compose file is located you will need to open the secrets.env file and make changes to passwords and file locations. This file will configure the docker-compose file so you do not need to make any changes to the docker-compose file directly. 

When you've configure the secrets.env file you are ready to start the system. in the folder where your docker-compose file is located type `sudo docker-compose up` if you are using a linux system. This will start the process of downloading the docker files and loading the system.

# Accessing the user interfaces
Accessing your systems is done by following the `localhost:####` locations listed in the docker compose file. Some of the locations are floating and need to be found by looking at the command line. type `sudo docker -ps` this will bring up the containers that are running and list.

- Kibana can be accessed by typeing localhost:5601 in your browser this one is hard coded.
- Nifi can be accessed by typeing localhost:#### this will be avliable on the list we created on the command line
- Postgres interface can be accessed with the aminer at localhost:8888
- Postgres direct can be accessed localhost:5240
- elasticsearch can be found at localhost:9200
- airflow can be found at localhost:####


### Streaming data
#### Integrating your model with the system
The system is designed to be configured throught the configuration.json file once a new machine learning mondel is introduced. This system will autofill any missing data backlog.

configuring:
to configure the system you dont need to know the SQL language but you have the ability to override statements if you do know the SQL script language. 
open the configuration folder and then the configuration.json file.

You will need to name your model then fill in the missing information for each variable. 
`null` values will be skipped past in the SQL commands if you want to just fill in the full script youself. 

#### Scheduling 

Airflow will need to be configured though the daq file.
you can organize the file to call your models. In my case I have my files running inside of docker containers that are call to run then close once the process is complete. 

#### Dashboard

The dashboard should get its datafeed from nifi and elasticsearch. This feed should always running if you are streaming data. You will need to construct the kibana and elasticsearch indexes. You will need to look over the kibana recipes folder to understand how to feed in your variables properly.

Visuals can be designed easily once you have the indexes set up. You just need to select the visuals tab and start creating them.

## Configuring AWS

AWS needs its own configuration we are using an EC2 instance 
AWS:
- Ubuntu Server 18.04 LTS (HVM), SSD Volume Type 
- c5.2xlarge 
- 8 vCPUs, 
- 3.4 GHz
- 16 GiB memory

once configured you can pull the repository and run your docker-compose file.

#### networking

The networking is important you dont want too many of your ports to be open as they will expose you to potenial threats. 

Open ports should be limited to Kibana and Adminer. 


### Accessing postgres public interface running on adminer

server - postgres (or whatever you named your docker)
user - user name (root)
password - password (example)
database - mydb (or whatever you name it)


### Configureing the config.json file
    "gloabal_forcast": {
        "start_date": "05/21/1968", \\ the start data of the tables data. 
        "last_pull_date_time": "05/21/2020 13:00:00.0000", \\ auto fille needs to be 0/00/0000 as place holder
        "last_pull_date_plus_one": "05/21/2020 13:00:00.0000", \\autofills keeps track off date. need to start with 0/00/0000 as place hodler
        "predictions": "8hrs", \\ how far out the model will predict.
        "data_needed": 500, \\amount of data needed to pull for model to run
        "sql_table": "omni_1hr", \\source or main table to pull data from
        "input_variables": ["*"],  \\in put variable from main source. this needs to be a list. if you type "*" with the quotes included you will get all the variables.
        "output_variables": ["ae_nt","au_nt","al","symh","kp"],  \\List of variables
        "OPTIONAL_join": "null",     \\second table to join
        "OPTIONAL_join_where": "null", \\which variable to join on
        "current_date": "10/29/2020 10:14:00.0000",  \\ this variable will fill itself
        "postgres_script": "select 'epochs', 'AE', 'AL', 'AU', 'SYM_H' from omni_1hr_prediction", \\import data to model. whatever you would send to csv
        "postgres_": "SELECT COUNT(1) FROM omni_1hr WHERE epoch ='date.current()",  \\ getting most recent data from postgres from main table you are pulling from
        "postgres_date_exist": "SELECT COUNT(1) FROM Suppliers WHERE epochs = data[gloabal_forcast][last_pull_date_plus_one]", \\checking the last date pulled
        "custom_sql_out_db": "null", \\override satement to pull data out of database---not in use
        "custom_sql_into_db": "null", \\overrid statement to put data into the database
        "send_to_sql_table": "null", \\send newly mented data from model to sql table
        "check_date_in_sql_for_main_table": "SELECT MAX(epochs) FROM omni_1hr" \\checking data from main source to see if model can run again. 

Sources:
AWS: X:\heartbeat-AWS\dev-ops-dev-branch\dev-ops-dev\dev-ops-dev\dev_ops

https://stackoverflow.com/questions/61186983/airflow-dockeroperator-connect-sock-connectself-unix-socket-filenotfounderror
