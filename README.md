# Cloud-Native DevOps Platform on AWS EKS

A Python Flask application containerized with Docker, stored in Amazon ECR and deployed to Amazon EKS with Kubernetes, on AWS infrastructure provisioned with Terraform.

![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask_3.1.2-000000?style=flat-square&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-844FBA?style=flat-square&logo=terraform&logoColor=white)
![Amazon EKS](https://img.shields.io/badge/Amazon_EKS-FF9900?style=flat-square)
![Amazon ECR](https://img.shields.io/badge/Amazon_ECR-FF9900?style=flat-square)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)

> **Project status**
> - Testing with `kubectl port-forward` was **successful**.
> - Public access on NodePort `30080` is the intended design but was **not verified**.
> - The AWS infrastructure was **destroyed with Terraform** after testing. Nothing is currently running.
> - Image build, push and deployment were performed **manually**.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Objectives](#project-objectives)
3. [Architecture Diagram](#architecture-diagram)
4. [Architecture Explanation](#architecture-explanation)
5. [End-to-End Workflow](#end-to-end-workflow)
6. [Application Request Flow](#application-request-flow)
7. [Infrastructure Provisioning with Terraform](#infrastructure-provisioning-with-terraform)
8. [Technology Stack](#technology-stack)
9. [AWS Services](#aws-services)
10. [Docker Image Build and ECR Push](#docker-image-build-and-ecr-push)
11. [Amazon EKS and Kubernetes Deployment](#amazon-eks-and-kubernetes-deployment)
12. [Kubernetes Resources](#kubernetes-resources)
13. [Application Testing and Health Check](#application-testing-and-health-check)
14. [Project Directory Structure](#project-directory-structure)
15. [Prerequisites and Installation](#prerequisites-and-installation)
16. [Step-by-Step Deployment](#step-by-step-deployment)
17. [Useful Commands](#useful-commands)
18. [Troubleshooting](#troubleshooting)
19. [Security Best Practices](#security-best-practices)
20. [Terraform Destroy and Cost Cleanup](#terraform-destroy-and-cost-cleanup)
21. [What I Learned](#what-i-learned)
22. [Future Improvements](#future-improvements)
23. [Project Summary](#project-summary)
24. [Author](#author)

## Project Overview

This project demonstrates the path of a small web application from source code to a Kubernetes cluster on AWS. The Flask application exposes three JSON endpoints. It is packaged as a Docker image, stored in a private Amazon ECR repository and run as a Pod on an Amazon EKS managed node group.

| Setting | Value |
|---|---|
| AWS Region | `ap-south-1` (Mumbai) |
| EKS cluster | `devops-eks-cluster` |
| ECR repository | `devops-flask-app` |
| Kubernetes Deployment | `devops-flask-deployment` |
| Kubernetes Service | `devops-flask-service` |
| Application port | `5000` |
| NodePort | `30080` |
| Worker instance type | `t3.small` |

> **Repository scope:** The Terraform configuration used for the AWS lab is not currently committed; `terraform/` is a placeholder. The committed Deployment also uses a local image setting, which must be changed for EKS (see [deployment step 4](#4-prepare-the-manifest-and-secret)).

## Project Objectives

- Provision AWS infrastructure as code with Terraform.
- Containerize a Flask application with Docker.
- Store the image in Amazon ECR.
- Run the application on Amazon EKS.
- Supply configuration through a ConfigMap and a Secret.
- Expose the application inside Kubernetes with a NodePort Service.
- Test and troubleshoot the deployment.
- Destroy cloud resources after testing to control cost.

## Architecture Diagram

![Cloud-Native DevOps Platform Architecture](./assets/architecture-aws-flow.svg)

*Architecture diagram of the project workflow; it is not live monitoring.*

## Architecture Explanation

| Diagram area | What it shows |
|---|---|
| Infrastructure provisioning | Terraform creates the VPC, subnets, Internet Gateway, route table and associations, IAM roles and policies, EKS cluster, managed node group and ECR repository. |
| AWS networking | The worker node runs inside the VPC. The Internet Gateway and route table provide the network route needed for public connectivity. |
| Build and image delivery | The code is kept in Git and GitHub. The Docker image is built and pushed manually. |
| Image storage | Amazon ECR holds the image, and the worker node pulls it when the Pod is scheduled. |
| EKS cluster | AWS manages the control plane. A managed worker node runs the application. |
| Deployment and Pod | `devops-flask-deployment` keeps one Flask Pod running. |
| ConfigMap and Secret | Both are injected into the container as environment variables. |
| Public request path (amber) | Intended route through the node's public IP and NodePort `30080`. **Not verified.** |
| Test path (green) | Access through `kubectl port-forward`. **Verified.** |

## End-to-End Workflow


1. Terraform provisions the AWS infrastructure.
2. The application source is committed and pushed to GitHub.
3. The Docker image is built from `docker/Dockerfile`.
4. The image is tagged and pushed to ECR.
5. `kubectl` applies the ConfigMap, Deployment and Service, after the Secret is created.
6. The worker node pulls the image and starts the Pod.
7. The application is tested with port-forwarding.
8. The infrastructure is destroyed.

All of these steps are run by hand.

## Application Request Flow

### Intended public access (not verified)


This path needs a worker node with a public IP, a route through the Internet Gateway and a security group rule allowing TCP `30080`. The response returns along the same path.

### Verified test (port-forward)


The diagram shows the logical path. Technically, `kubectl port-forward` selects one Pod behind the Service and tunnels to it through the Kubernetes API server. It therefore does not test NodePort routing or security group rules.

## Infrastructure Provisioning with Terraform

Terraform was used to provision:

- VPC and subnets
- Internet Gateway
- Route table and route table associations
- IAM roles and policy attachments
- Amazon EKS cluster
- EKS managed node group
- Amazon ECR repository

The `.tf` files are **not yet in this repository**. The commands below apply once you add your own configuration to `terraform/`.

```bash
cd terraform
terraform init        # download providers
terraform fmt         # format files
terraform validate    # check configuration
terraform plan -out=tfplan   # preview and save the changes
terraform apply tfplan       # create the reviewed resources
cd ..
```

Applying a saved plan does not ask for confirmation, so review the plan output first.

## Technology Stack

| Category | Technology |
|---|---|
| Application | Python 3.12, Flask 3.1.2 |
| Containerization | Docker (`python:3.12-slim`) |
| Orchestration | Kubernetes on Amazon EKS |
| Image registry | Amazon ECR |
| Infrastructure as Code | Terraform |
| Cloud | AWS |
| Source control | Git, GitHub |

## AWS Services

| Service | Role in this project |
|---|---|
| Amazon VPC | Isolated network for the cluster |
| Subnets | Network segments within the VPC |
| Internet Gateway | Connects the VPC to the internet |
| Route table | Directs subnet traffic |
| AWS IAM | Permissions for the cluster and worker nodes |
| Amazon EKS | Managed Kubernetes control plane |
| EKS managed node group | EC2 worker capacity (`t3.small`) |
| Amazon ECR | Private Docker image registry |

## Docker Image Build and ECR Push

Run these from the repository root in a Bash shell. The ECR repository must already exist.

```bash
export AWS_REGION=ap-south-1
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export ECR_REGISTRY=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
export IMAGE_URI=$ECR_REGISTRY/devops-flask-app:v1

# Build for the x86_64 architecture used by t3.small
docker build --platform linux/amd64 -f docker/Dockerfile -t devops-flask-app:v1 .

# Log Docker in to ECR with a temporary token
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

# Tag and push
docker tag devops-flask-app:v1 $IMAGE_URI
docker push $IMAGE_URI
```

## Amazon EKS and Kubernetes Deployment

Connect `kubectl` to the cluster and confirm the node is `Ready`:

```bash
aws eks update-kubeconfig --region ap-south-1 --name devops-eks-cluster
kubectl config current-context
kubectl get nodes -o wide
```

The manifests are in `kubernetes/`. The full order of commands is in [Step-by-Step Deployment](#step-by-step-deployment).

## Kubernetes Resources

| Resource | Name | Purpose |
|---|---|---|
| Deployment | `devops-flask-deployment` | Runs one replica of the application |
| Pod | Created by the Deployment | Runs `flask-container` on port `5000` |
| Service | `devops-flask-service` | NodePort `30080` to target port `5000`, selecting `app: devops-flask` |
| ConfigMap | `devops-flask-config` | `APP_NAME`, `APP_VERSION`, `APP_ENV` |
| Secret | `devops-flask-secret` | Sensitive values; manifest is not committed |

The Deployment also defines:

- **Resources:** requests of `100m` CPU and `64Mi` memory; limits of `500m` CPU and `128Mi` memory.
- **Probes:** startup, liveness and readiness checks on `/health`.

The current application code does not read the ConfigMap or Secret variables; its responses are hardcoded.

## Application Testing and Health Check

```bash
kubectl port-forward svc/devops-flask-service 5000:5000
```

Keep that terminal open and run these in a second one:

```bash
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/info
```

| Endpoint | Returns |
|---|---|
| `/` | Project name, message and status |
| `/health` | `UP` status and a UTC timestamp |
| `/info` | Application name, version and environment |

Response from `/`:

```json
{
  "message": "Application is running successfully!",
  "project": "Cloud-Native DevOps Platform",
  "status": "healthy"
}
```

Validation performed during the lab:

- Terraform provisioned the infrastructure.
- The worker node became `Ready`.
- The image was pushed to ECR.
- The application Pod reached `Running`.
- The application responded through port-forwarding.
- `terraform destroy` removed the infrastructure.

## Project Directory Structure

```text
Cloud-Native-DevOps-Platform/
├── app/
│   ├── app.py
│   └── requirements.txt
├── assets/
│   ├── architecture-aws-flow.svg
│   └── architecture.svg
├── docker/
│   └── Dockerfile
├── docs/                          # placeholder
├── jenkins/                       # placeholder
├── kubernetes/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── development-deployment.yaml
│   ├── ingress.yaml
│   ├── pvc.yaml
│   └── service.yaml
├── monitoring/                    # placeholder
├── terraform/                     # placeholder
├── .gitignore
└── README.md
```

Only `configmap.yaml`, `deployment.yaml` and `service.yaml` are used in the deployment documented here. See [Future Improvements](#future-improvements) for the others.

## Prerequisites and Installation

| Tool | Check |
|---|---|
| Git | `git --version` |
| Docker | `docker --version` |
| AWS CLI v2 | `aws --version` |
| Terraform | `terraform version` |
| kubectl | `kubectl version --client` |

Install each from its official documentation. You also need an AWS account with permission to manage EKS, EC2, VPC, IAM and ECR. **These resources incur charges.**

## Step-by-Step Deployment

### 1. Clone and configure

```bash
git clone https://github.com/Sameedkhan469/Cloud-Native-DevOps-Platform.git
cd Cloud-Native-DevOps-Platform
aws configure                  # set credentials; region ap-south-1
aws sts get-caller-identity    # confirm the account
```

Optionally, test the container locally first:

```bash
docker build -f docker/Dockerfile -t devops-flask-app:v1 .
docker run --rm -p 5000:5000 devops-flask-app:v1
```

Open `http://localhost:5000`, then stop the container with `Ctrl+C`.

### 2. Provision infrastructure

Add your Terraform configuration, then follow [Infrastructure Provisioning](#infrastructure-provisioning-with-terraform).

### 3. Build, push and connect

Follow [Docker Image Build and ECR Push](#docker-image-build-and-ecr-push), then run `aws eks update-kubeconfig` as shown [above](#amazon-eks-and-kubernetes-deployment).

### 4. Prepare the manifest and Secret

Print your image URI:

```bash
echo $IMAGE_URI
```

In `kubernetes/deployment.yaml`, replace these two values:

```yaml
image: <your IMAGE_URI>          # was devops-flask-app:v1
imagePullPolicy: IfNotPresent    # was Never
```

Create the Secret with a placeholder or your own value. Never commit real values.

```bash
kubectl create secret generic devops-flask-secret --from-literal=EXAMPLE_KEY=replace-me
```

### 5. Deploy

```bash
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl rollout status deployment/devops-flask-deployment
kubectl get pods,services -o wide
```

### 6. Test and clean up

Follow [Application Testing](#application-testing-and-health-check), then [Terraform Destroy](#terraform-destroy-and-cost-cleanup).

### Optional: public NodePort access

This was not verified. To try it, check the node's external IP with `kubectl get nodes -o wide`, allow TCP `30080` from **your own IP only** in the node security group, and open `http://<node-public-ip>:30080`.

## Useful Commands

```bash
# Docker
docker images
docker ps
docker logs <container-id>

# Terraform (run inside terraform/)
terraform state list
terraform output

# AWS CLI
aws eks describe-cluster --name devops-eks-cluster --region ap-south-1
aws ecr describe-images --repository-name devops-flask-app --region ap-south-1

# kubectl
kubectl get deployments,pods,services
kubectl describe pod <pod-name>
kubectl logs deployment/devops-flask-deployment
kubectl get endpoints devops-flask-service
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl rollout restart deployment/devops-flask-deployment
```

## Troubleshooting

| Problem | Possible cause | What to check |
|---|---|---|
| `ErrImageNeverPull` | `imagePullPolicy` is still `Never` | Deployment step 4 |
| `ImagePullBackOff` | Image cannot be pulled | Image URI, tag, node IAM permissions |
| `exec format error` | Image built for the wrong CPU architecture | Rebuild with `--platform linux/amd64` |
| `CreateContainerConfigError` | ConfigMap or Secret missing | `kubectl get configmap,secret` |
| Pod stays `Pending` | Scheduling problem | Node readiness and Pod events |
| Service has no endpoints | Selector mismatch or Pod not ready | Labels and readiness probe |
| NodePort times out | Networking | Public IP, route, security group |
| `kubectl` shows a local cluster | Wrong context | `kubectl config current-context` |

## Security Best Practices

Recommendations when reproducing or extending this project:

- Never commit AWS keys, passwords, tokens or real Secret manifests.
- Add `.terraform/`, `*.tfstate*`, `*.tfvars` and `tfplan` to `.gitignore`. The current file does not cover them.
- Apply least-privilege IAM policies.
- Restrict security group rules to required ports and trusted source addresses.
- Remember that Kubernetes Secrets are only base64-encoded in manifests; use RBAC and encryption at rest.
- Use unique image tags and rotate any exposed credentials.

## Terraform Destroy and Cost Cleanup

**This project's AWS infrastructure has already been destroyed.** If you reproduce it:

```bash
cd terraform
terraform plan -destroy    # review what will be removed
terraform destroy          # confirm with yes
terraform state list       # should return nothing
```

- An ECR repository that still contains images may block deletion unless `force_delete` is set in its Terraform resource.
- Check the AWS Console in `ap-south-1` for anything created outside Terraform.

## What I Learned

- Provisioning AWS networking, IAM and EKS with Terraform.
- Building container images and publishing them to ECR.
- Working with Deployments, Pods, Services, ConfigMaps and Secrets.
- The difference between port-forward testing and public exposure.
- Diagnosing problems with logs, events and `kubectl describe`.
- Cleaning up cloud resources to manage cost.

## Future Improvements

None of the following is part of the completed, verified deployment.

- Commit the Terraform configuration and configure remote state with locking.
- Verify public NodePort access.
- Make the application read its ConfigMap and Secret values.
- Add automated tests and CI/CD (GitHub Actions or Jenkins).
- Add GitOps delivery with Argo CD.
- Complete and validate the experimental NGINX Ingress, development Deployment and PersistentVolumeClaim manifests (the Service referenced by the Ingress is still missing).
- Add a load balancer with HTTPS.
- Add Prometheus and Grafana monitoring.
- Add autoscaling and container image scanning.

## Project Summary

A Flask application was containerized with Docker, stored in Amazon ECR and deployed to Amazon EKS on Terraform-provisioned infrastructure. It was successfully tested with `kubectl port-forward`. Public NodePort access was not verified, and the AWS resources have since been destroyed.

## Author

**Sameed Khan**

- GitHub: [Sameedkhan469](https://github.com/Sameedkhan469)
- Repository: [Cloud-Native-DevOps-Platform](https://github.com/Sameedkhan469/Cloud-Native-DevOps-Platform)
