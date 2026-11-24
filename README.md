
# Cloud-Native DevOps Platform

An end-to-end DevOps project demonstrating containerization, Kubernetes orchestration, infrastructure automation, CI/CD, and cloud monitoring.

## Project Overview

This project deploys a Python Flask application using Docker and Kubernetes. It demonstrates Kubernetes deployments, services, health probes, persistent storage, autoscaling, and ingress routing.

## Technology Stack

- Python Flask
- Docker
- Kubernetes
- Terraform
- Jenkins
- AWS (planned)
- Prometheus and Grafana (planned)
- Git and GitHub

## Architecture

Developer → GitHub → Jenkins CI/CD → Docker Image → Kubernetes → Flask Application

## Current Features

- Flask application with health-check API
- Docker image and container
- Kubernetes Deployment and Service
- ConfigMap and Secret
- Liveness, readiness, and startup probes
- CPU and memory resource limits
- Development namespace
- Persistent Volume Claim
- Horizontal Pod Autoscaler
- NGINX Ingress Controller

## Project Structure

```text
Cloud-Native-DevOps-Platform/
├── app/
├── docker/
├── kubernetes/
├── terraform/
├── jenkins/
├── monitoring/
├── docs/
└── README.md
```

## Project Status

Currently running locally using Docker Desktop Kubernetes.

Upcoming stages:
- Jenkins CI/CD pipeline
- Terraform infrastructure automation
- AWS EKS and ECR deployment
- Prometheus and Grafana monitoring
- Security and documentation

## Author

Sameed Khan

GitHub: https://github.com/Sameedkhan469
