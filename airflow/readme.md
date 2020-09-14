Docker file for special airflow file. 

https://stackoverflow.com/questions/61186983/airflow-dockeroperator-connect-sock-connectself-unix-socket-filenotfounderror


build docker with
docker build --rm --build-arg DOCKER_GROUP_ID=`getent group docker | cut -d: -f3` -t puckel-airflow-with-docker-inside .
