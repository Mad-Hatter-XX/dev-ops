# dev-ops
Dev-ops and software development


When running the docker file you will need to turn the file such as this.

https://stackoverflow.com/questions/61186983/airflow-dockeroperator-connect-sock-connectself-unix-socket-filenotfounderror
docker build --rm --build-arg DOCKER_GROUP_ID=`getent group docker | cut -d: -f3` -t puckel-airflow-with-docker-inside .
