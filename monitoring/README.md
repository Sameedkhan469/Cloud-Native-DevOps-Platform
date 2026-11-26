# Monitoring setup

The Flask app exposes Prometheus metrics at `/metrics`. The included `flask-servicemonitor.yaml` tells Prometheus Operator to scrape the Kubernetes Service named `devops-flask-service` in the `default` namespace.

## Install kube-prometheus-stack

Install Helm and connect kubectl to your EKS cluster first. The AWS cluster was destroyed after the original lab, so this section applies only after the cluster has been recreated.

```powershell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
```

Apply the ServiceMonitor:

```powershell
kubectl apply -f monitoring/flask-servicemonitor.yaml
```

The ServiceMonitor has the `release: prometheus` label to match the Helm release name above. It scrapes the app Service's named `http` port at `/metrics`.

## Verify

```powershell
kubectl get pods -n monitoring
kubectl get servicemonitor -n monitoring
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
```

Open `http://localhost:9090/targets` and confirm the `devops-flask` target is UP. Query `flask_http_requests_total` in Prometheus.

For Grafana, run:

```powershell
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

Open `http://localhost:3000`. Retrieve the admin password from the chart-created Secret rather than storing credentials in this repository:

```powershell
kubectl get secret -n monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | %{ [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($_)) }
```

The kube-prometheus-stack chart also installs Prometheus, Grafana, Alertmanager, Node Exporter, and kube-state-metrics. These are Kubernetes workloads, not AWS managed services.

This configuration is provided as a reproducible setup guide; it has not been reinstalled and verified against the current repository revision after the AWS infrastructure was destroyed.
