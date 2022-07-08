from platform import python_compiler
from tracemalloc import start
from datetime import datetime
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

from random import choice


def _push_task():
    array = ['echo a', 'echo b', 'echo c']
    return array

def _pull_task(ti):
    ls = ti.xcom_pull(task_ids='push_task')
    print(ls)
    element = choice(ls)
    return element

def _choose_one(**context):
    ti = context['ti']
    bash_msj = ti.xcom_pull(task_ids=[
        'pull_task',
    ])
    if bash_msj[0] == 'echo a':
        return 'print_a'
    elif bash_msj[0] == 'echo b':
        return 'print_b'
    return 'print_c'
    

with DAG(dag_id='test_dag',start_date=datetime.now(),
         schedule_interval='@once') as dag:
    
    push_task = PythonOperator(
        task_id = 'push_task',
        python_callable=_push_task
    )
    
    pull_task = PythonOperator(
        task_id = 'pull_task',
        python_callable=_pull_task
    )
    
    choose_one = BranchPythonOperator(
        task_id = 'choose_one',
        python_callable=_choose_one
    )
    
    print_a = BashOperator(
        task_id = 'print_a',
        bash_command='echo a'
    )
    print_b = BashOperator(
        task_id = 'print_b',
        bash_command='echo b'
    )    
    print_c = BashOperator(
        task_id = 'print_c',
        bash_command='echo Hola Mundo'
    )
    
    push_task >> pull_task >> choose_one >> [print_a, print_b, print_c]