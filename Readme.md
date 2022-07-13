##Install Components:

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


## Kubernets kubectl
(codineric)
> The kubernetes command line tool, kubectl, allows you to run commands againts Kubernetes cluster.
check https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/

1- Install: 

curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

2- Install kubectl:

sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

3- Check version:

kubectl version --client --output=yaml 


## Kind
> Install
* curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.14.0/kind-linux-amd64
chmod +x ./kind
* sudo mv ./kind /usr/local/bin

## Helm
> the best way to find, share , and use software built for Kubernetes.

https://helm.sh/docs/intro/install

Install:

* curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

-----------------------------------------------------------  -----------------------------------------------------------
                            USAGE
-----------------------------------------------------------  -----------------------------------------------------------

## Set up the cluster

-Create a kubernetes cluster of 1 control plane and 3 worker nodes
* kind create cluster --name airflow-poc --config values.yaml

- Check the cluster info
* kubectl cluster-info

## Use HELM

- Add repo and update
- Add the official repository of the Airflow Helm Chart

* helm repo add stable https://charts.helm.sh/stable
* helm repo add apache-airflow https://airflow.apache.org
* helm repo update

- Choose cluster:
* kubectl config get-contexts
* kubectl config set current-context k3d-airflow-poc

- Create namespace (logic sep):
* kubectl create namespace airflow

- Check the namespace
* kubectl get namespaces

- Install helmchart (same as docker build):
* helm install airflow apache-airflow/airflow --namespace airflow --debug

- Get pods (see components created)
* kubectl get pods -n airflow

- Check release
* helm ls -n airflow

- Port forward 8080:8080 (acces webserver)
* kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow
- Get the Chart values
* helm show values apache-airflow/airflow > values.yaml

- Check the current revision
* helm ls -n airflow

- Upgrade the chart
* helm upgrade --install airflow apache-airflow/airflow -n airflow -f values.yaml --debug

- Check after
* helm ls -n airflow


- Configure values.yaml -> extraEnv.
extraEnv: |
  - name: AIRFLOW__CORE__LOAD__EXAMPLES
    value: 'True'
Save and upgrade chart ( helm upgrade --install .....)
Hit command PORT forwarding (kubectl port-forward ....)

# If for some reasons the release is stuck in pending-install or timed out
# Resinstall the chart
- Delete the Helm release
* helm delete airflow --namespace airflow

- Check your PODs
* kubectl get pods -n airflow

- If airflow-migrations is in ContainerCreating state delete it
* kubectl get jobs -n airflow
* kubectl delete jobs <pods_name_of_airflow_migrations> -n airflow

- Install the chart again
helm install airflow apache-airflow/airflow --namespace airflow --debug --timeout 10m0s
