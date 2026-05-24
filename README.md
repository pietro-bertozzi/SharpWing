# SharpWing

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