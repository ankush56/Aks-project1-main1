#####
```
- hellopythonapp - Python app src code
- Dockerfile - To build app images from the src code
- Requirements.txt - Python packages required by app
```

```
#### Kubernetes files
deployment.yml
nodeportservice.yml
```


```
Src App code
Dockerfile builds image from src code
push image to dockerhub
deployment.yml spins container with 2 replicas from docker image built in step and pulls docker image
```

```
 docker build -t pyhello .
 docker tag pyhello walia56/pyhello
 docker push walia56/pyhello:latest
```

#### Secrets setup
secret.yml manifest define it
encode somesecret as base64
To do that run- echo "somesecret" | base64
```
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  password: "somesecret"  #Use secret management 
```

```
deployment.yml
This will create a volume named mysecret that is backed by the mysecret secret, and mount it at /etc/mysecret in the container.
        volumeMounts:
        - name: mysecret  
          mountPath: /etc/mysecret
```

```
        env:
          - name: customenv
            value: "Hello from customenv"
          - name: lob
            value: "XYZLOB"
# Use secrets from secret.yml 
#in your Deployment.yaml file, you can modify the container spec to add the secrets as environment variables:
# The ENVIRONMENT variable CLIENT_SECRET is set to the value of the key key in the mysecret secret.          
          - name: CLIENT_SECRET
            valueFrom:
              secretKeyRef:
                name: mysecret
                key: clientsecret
```

```
Full deployment.yml
####### In your Deployment.yaml file, you can modify the container spec to add the secrets as environment variables:
secret will be setup as environment variable in the container.


  template:
    metadata:
      labels:
        app: myapp
    spec:
      volumes:
      - name: mysecret
        secret:
          secretName: mysecret
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 5000
        volumeMounts:
        - name: mysecret
          mountPath: /etc/mysecret
        env:
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: mysecret
              key: key
```        

#### Volumes
So apps dont lose data if containers or pods are restarted
https://www.educative.io/answers/how-to-use-volumes-in-kubernetes 
```
Persistent Volumes (PVs) are pod and node independent volumes. The idea is that instead of storing the data in the pod or a node, we have entirely separate entities in our K8s cluster that are detached from our nodes.

Each pod then will have a Persistent Volume Claim (PVC), and it will use this to access the standalone entities we created
```

```
SET up PV-
The hostPath type allows us to set a path on the host machine and then the data from that path will be exposed to different pods.
path under hostpath- which refers to the folder on our host machine where we want to save the data.
```

```
Setting up the PVC

Simply defining the PV is not enough. We also need to define the PV Claim which the pods will use later. For this create a host-pvc.yaml file 
```

```
PV and PVC
Final configuration
Now that we have our PV and PVC set up, all that needs to be done is make changes in the deployment.yaml file so that we use this PV

```

```
microk8s
kubectl port-forward <pod_name> <local_port>:<pod_port> 
```

### Readiness and Liveness probe checks

```
<b>Readiness check </b>
In this example, the readinessProbe is configured to make an HTTP GET request to the path /healthz on port 80 of the container. The probe will wait 5 seconds before the first check and will repeat every 5 seconds until the container is considered ready.

      containers:
      - name: my-container
        image: my-image
        readinessProbe:
          httpGet:
            path: /healthz
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
```