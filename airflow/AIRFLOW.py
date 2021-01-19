
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflwo.operators.docker_operator import DockerOperator



if len(data) = 60:
    pass
else:
    print("data collection not ready")
    break

model1 >> model2
model1 >> model_break



def dummy_test():
    return 'model1'

A_task = DummyOperator(task_id='model_true', dag=dag)
B_task = DummyOperator(task_id='model_false', dag=dag)

branch_task = BranchPyhonOperator(task_id ='branching',
python_callable=dummy_test, dag=dag)

branch_task >> A_task
branch_task >> B_task

#function should do something like an exists or count from sql 
#we are just looking to get the specified number of return items. if its equal to the request
#we make the data pull. if not we stop the process
#aternatively we can see if a date exsit in the data yet


default_arge = {
    'owner'             : 'airflow',
    'description'       : 'Use of the DockerOperator',
    'depends_on_past'   : False
    'start_date'        : datetime(2018, 1, 3),
    'email_on_failure'  : False,
    'email_on_retry'    : False,
    'retries'           : 1,
    'retry_delay'       : timedelta(minutes=5)
}

with DAG('docker_dag', default_args=default_args, schedule_interval="5 * * * *", catchup=False) as dag:
    t1 = BashOperator(
        task_id='print_current_date',
        bash_command='date'
    )

    t2 = DockerOperator(
        task_id='docker_command',
        image='cgreen010/globalforcast:latest',
        api_version='auto',
        auto_remove=True,
        command="/bin/sleep 30",
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge'
    )

    t3 = DockerOperator(
        task_id='docker_command',
        image='cgreen010/globalforcast:latest',
        api_version='auto',
        auto_remove=True,
        command="/bin/sleep 30",
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge'
    )

t1 >> t2 #>> t3
