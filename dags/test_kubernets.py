from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.utils.dates import days_ago

from datetime import datetime, timedelta
import os

CPU_REQUEST = "650m"
CPU_LIMIT = "1000m"
MEMORY_REQUEST = "1Gi"
MEMORY_LIMIT = "1Gi"

ENV = os.getenv("ENV")

SCHEDULE_INTERVAL = "0 3 * * MON"

DOCKER_IMAGE_NAME = "k3d_test"
DOCKER_IMAGE_TAG = 'latest'

#Limits and Resources.
executor_config = {
    "KubernetesExecutor": {
        "resources" : {
            "request" : {"memory": MEMORY_REQUEST, "cpu": CPU_REQUEST},
            "limits" : {"memory": MEMORY_LIMIT, "cpu": CPU_LIMIT}
        }
    }
}

compute_resources = {
    'request_cpu': CPU_REQUEST,
    'request_memory' : MEMORY_REQUEST,
    'limit_cpu' : CPU_LIMIT,
    'limit_memory' : MEMORY_LIMIT 
}

#Kubernets config.
default_arg = dict(
    owner = 'Airflow',
    depends_on_past = False,
    executor_config = executor_config
)

#Python Operator. This will create a POD, and run.
def test(date):
    print('date is:')
    print(date)
    print(ENV)
    
#Same but using kubernets pod operator.
with DAG(
    dag_id='k8s_test',
    start_date=days_ago(2),
    default_args=default_arg,
    schedule_interval=SCHEDULE_INTERVAL
) as test_dag:
    
    data_date = '{ {ds} }'
    
    #We pass an image to kubernets pod operator.
    #We can execute differents pods in diff containers.
    k8s_op = KubernetesPodOperator(
        namespace = 'airflow',
        image = f'{DOCKER_IMAGE_NAME}:{DOCKER_IMAGE_TAG}',
        name = 'k8s_op',
        resources = compute_resources,
        is_delete_operator_pod = True,
        cmds = ['python', 'etl.py'],
        arguments = [ "--date ", "{{ ds }}"],
        get_logs=True 
    )
    
    python_op = PythonOperator(
        task_id = 'Python_op',
        python_callable=test,
        op_kwargs={'date':data_date}
    )

    k8s_op 
    python_op