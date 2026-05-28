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

helm upgrade kube-prom-stack prometheus-community/kube-prometheus-stack -n monitoring -f grafana-loki.yaml --reuse-values

helm upgrade --install loki grafana/loki-stack --set promtail.enabled=true --namespace default
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
  --set prometheus.serviceMonitor.enabled=true \
  --set prometheus.serviceMonitor.namespace="default" \
  --set prometheus.serviceMonitor.additionalLabels.release="kube-prom-stack" \
  --set env[0].name="DATA_SOURCE_URI" \
  --set env[0].value="postgres-service.default.svc.cluster.local:5432/postgres?sslmode=disable" \
  --set env[1].name="DATA_SOURCE_USER" \
  --set env[1].value="postgres" \
  --set env[2].name="DATA_SOURCE_PASS" \
  --set env[2].value="postgres"

helm install redis-exporter prometheus-community/prometheus-redis-exporter \
  --set prometheus.serviceMonitor.enabled=true \
  --set prometheus.serviceMonitor.namespace="default" \
  --set prometheus.serviceMonitor.additionalLabels.release="kube-prom-stack" \
  --set redisAddress="redis://redis-service.default.svc.cluster.local:6379"

helm install kafka-exporter prometheus-community/prometheus-kafka-exporter \
  --set kafkaServer="{my-kafka.default.svc.cluster.local:9092}" \
  --set prometheus.serviceMonitor.enabled=true \
  --set prometheus.serviceMonitor.namespace="default" \
  --set prometheus.serviceMonitor.additionalLabels.release="kube-prom-stack" \
  --set "prometheus.serviceMonitor.relabelings[0].targetLabel=job" \
  --set "prometheus.serviceMonitor.relabelings[0].replacement=kafka-exporter"

kubectl port-forward -n monitoring deployment/kube-prom-stack-grafana 3000:3000
kubectl port-forward -n monitoring svc/kube-prom-stack-kube-prome-prometheus 9090:9090
'''

pietro@PB-IdeaPad-Slim:~/magistrale/scalable-reliable-services-m/SharpWing/chat $ kubectl delete deployments --all
kubectl delete services --all
kubectl delete pods --all
deployment.apps "kafka-deployment" deleted
deployment.apps "kafka-exporter-prometheus-kafka-exporter" deleted
deployment.apps "layer1-deployment" deleted
deployment.apps "layer2-deployment" deleted
deployment.apps "layer3-deployment" deleted
deployment.apps "postgres-deployment" deleted
deployment.apps "postgres-exporter-prometheus-postgres-exporter" deleted
deployment.apps "redis-deployment" deleted
deployment.apps "redis-exporter-prometheus-redis-exporter" deleted
service "kafka-exporter-prometheus-kafka-exporter" deleted
service "kubernetes" deleted
service "loki" deleted
service "loki-headless" deleted
service "loki-memberlist" deleted
service "my-kafka" deleted
service "postgres-exporter-prometheus-postgres-exporter" deleted
service "postgres-service" deleted
service "redis-exporter-prometheus-redis-exporter" deleted
service "redis-service" deleted
pod "kafka-deployment-7889695949-4zsth" deleted
pod "kafka-exporter-prometheus-kafka-exporter-79c4997ff-v8mpp" deleted
pod "layer1-deployment-5c856cfc47-l5mxg" deleted
pod "layer2-deployment-79cc5d6dbb-zs474" deleted
pod "layer3-deployment-64dcd689c-k6wnc" deleted
pod "loki-0" deleted
pod "loki-promtail-958pl" deleted
pod "postgres-deployment-b884bd8b6-25qkp" deleted
pod "postgres-exporter-prometheus-postgres-exporter-59dcb6b7dc-tp87s" deleted
pod "redis-deployment-6c6fcd64b8-7fx6w" deleted
pod "redis-exporter-prometheus-redis-exporter-6dbd4d65df-ckdg8" deleted