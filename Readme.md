Install Components:

1- install docker
2- install docker-compose

3- Get docker-compose.yml:

    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.2/docker-compose.yaml'
    
4- create dir: 

    mkdir ./dags ./plugins ./logs
    
5- give perms: 

    echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
    
6- setup all: 

    docker-compose up airflow-init
    
7- start: 

    docker-compose up


Cleaning enviroment:
The best way to do it is to:

1- Run command in the directory you downloaded the docker-compose.yaml file: 

    docker-compose down --volumes --remove-orphans 
    
2- remove the whole directory where you downloaded the docker-compose.yaml file:

     rm -rf '<DIRECTORY>'
     
3- re-download the docker-compose.yaml file
4- re-start following the instructions from the very beginning in this guide


Spy on docker containers:
- See containers: docker ps

Run CLI commands:
- docker-compose run airflow-worker airflow info
