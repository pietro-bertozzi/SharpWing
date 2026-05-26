# SharpWing

We’re currently developing a bank-grade fraud detection system with my university peers, Foroozanfar Arash and Wewiór Mikołaj, forming a highly international team. Scheduled for completion on June 7th, our engineering research focuses on balancing fast, reliable, and cost-effective checks. To achieve this, we are orchestrating a scalable data pipeline via Kubernetes, Kafka, Redis, PostgreSQL, Prometheus, Grafana, and Loki, implementing an LLM-as-a-judge architecture for real-time verification.

'''
kubectl delete deployments --all  
kubectl delete services --all
kubectl delete pods --all

cd layer-1 && docker build -t layer1-app:v1 . && cd ..
cd layer-2 && docker build -t layer2-app:v1 . && cd ..
cd layer-3 && docker build -t layer3-app:v1 . && cd ..

kubectl apply -f kafka.yaml
kubectl apply -f postgres.yaml
kubectl apply -f redis.yaml

kubectl apply -f layer-1/layer-1.yaml
kubectl apply -f layer-2/layer-2.yaml
kubectl apply -f layer-3/layer-3.yaml

kubectl get pods
kubectl get pods -w

kubectl logs -l app=layer-1 -f
kubectl logs -l app=layer-2 -f
kubectl logs -l app=layer-3 -f

kubectl exec -it deployment/postgres-deployment -- psql -U pietro_user -d pipeline_db
\dt
SELECT * FROM transazioni;
SELECT COUNT(*) FROM transazioni;
\q

watch -n 1 "kubectl exec -it deployment/redis-deployment -- redis-cli dbsize"
'''

'''
kubectl create namespace monitoring

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install kube-prom-stack prometheus-community/kube-prometheus-stack \
  -n monitoring \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false

kubectl get secret --namespace monitoring kube-prom-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

helm install postgres-exporter prometheus-community/prometheus-postgres-exporter \
  --set config.datasource.host="postgres-service.default.svc.cluster.local" \
  --set config.datasource.user="pietro_user" \
  --set config.datasource.password="super_password_123" \
  --set config.datasource.database="pipeline_db" \
  --set config.datasource.sslmode="disable" \
  --set serviceMonitor.enabled=true \
  --set serviceMonitor.additionalLabels.release="kube-prom-stack" \
  --set prometheus.monitor.enabled=true \
  --set prometheus.monitor.additionalLabels.release="kube-prom-stack"

kubectl port-forward -n monitoring deployment/kube-prom-stack-grafana 3000:3000
kubectl port-forward -n monitoring svc/kube-prom-stack-kube-prome-prometheus 9090:9090
'''