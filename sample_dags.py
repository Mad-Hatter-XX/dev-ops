from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
import logging
import docker

args={
    'owner' : 'Chris Green',
    'start_date': days_ago(1)
}

dag = DAG(dag_id= 'sample_dags', default_args=args, schedule_interval=None)

def run_this_func(**context):
    print('hi')

def do_test_docker(**context):
    #client = docker.APIClient(base_url='unix://var/run/docker.sock')
    #client.version()
    print('hi')
    client = docker.from_env()
    #client.containers.run("ubuntu", "echo hello world")
    #client.container.list()
    # print(client.containers.list())
    for image in client.images.list():
    #    print(image)
        logging.info(str(image))

def gloabal_docker(**context):
    print('hi')
    client = docker.from_env()
    client.containers.run("cgreen010/hbtest:version1")

with dag:
    run_this_task = PythonOperator(
        task_id='run_this',
        python_callable=run_this_func,
        provide_context=True
    )
    run_this_task2 = PythonOperator(
        task_id='run_this2',
        python_callable=run_this_func,
        provide_context=True
    )
    t1_5 = PythonOperator(
        task_id='test_docker',
        python_callable=do_test_docker,
        provide_context=True
    )
    t1_6 = PythonOperator(
        task_id='test_docker3',
        python_callable=do_test_docker,
        provide_context=True
    )
    t1_7 = PythonOperator(
        task_id='global_docker',
        python_callable=gloabal_docker,
        provide_context=True
    )

    t1_5 
    run_this_task >> [run_this_task2, t1_5] >> t1_6 >> t1_7 #running a task after another