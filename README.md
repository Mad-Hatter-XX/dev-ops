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

# prerequisite
First you need to install docker onto your system. The install instructions for all systems can be found here https://docs.docker.com/compose/install/ on the docker website.

Once docker is installed you will need to be sure docker-compose is installed. Docker compose can be found here https://docs.docker.com/compose/install/ on the docker website.

# starting the enviorment
As mentioned above the system is already designed and configured in order to start the system you need to find the docker-compose file in the current repo. 

once in the folder where the docker-compose file is located you will need to open the secrets.env file and make changes to passwords and file locations. This file will configure the docker-compose file so you do not need to make any changes to the docker-compose file directly. 

When you've configure the secrets.env file you are ready to start the system. in the folder where your docker-compose file is located type `sudo docker-compose up` if you are using a linux system. This will start the process of downloading the docker files and loading the system.







When running the docker file you will need to turn the file such as this.

https://stackoverflow.com/questions/61186983/airflow-dockeroperator-connect-sock-connectself-unix-socket-filenotfounderror
docker build --rm --build-arg DOCKER_GROUP_ID=`getent group docker | cut -d: -f3` -t puckel-airflow-with-docker-inside .
