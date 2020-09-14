#https://stackoverflow.com/questions/61186983/airflow-dockeroperator-connect-sock-connectself-unix-socket-filenotfounderror
FROM puckel/docker-airflow:latest
USER root
ARG DOCKER_GROUP_ID
# Install Docker
RUN pip install 'Docker==4.2.0'
# Add permissions for running docker.sock
RUN groupadd -g $DOCKER_GROUP_ID docker && gpasswd -a airflow docker
USER airflow