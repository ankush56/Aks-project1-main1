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
#### Environment variables ###

``` 
      containers:
      - name: hellopythonappcontainer
        image: walia56/pyhello:latest
        env:
          - name: customenv
            value: "Hello from customenv"
          - name: lob
            value: "XYZLOB"
          - name: DATA_PATH
            value: '/app/appdata'
```
#### Volumes###
<p>
<b>Mount volumes, secrets , configmaps as volumes. You can also get secrets, config map values without mounting as volume </b>
</p>

#### Secrets setup
<p>
secret.yml manifest define it
First encode secret as base64
To do that run-> echo "somesecret" | base64
Add this base64 encoded to secret.yml in password value
</p>

```
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  username: YWRtaW4=      #base 64 encoded, echo "somesecret" | base64 
  password: MWYyZDFlMmU2N2Rm

```

```
deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp-container
        image: myapp:latest
        env:
        - name: username
          valueFrom:
            secretKeyRef:
              name: mysecret  #name of object in secret manifest file
              key: username   # Key to refer in secrets
        - name: password
          valueFrom:
            secretKeyRef:
              name: mysecret
              key: password

```


```
#in your Deployment.yaml file, you can modify the container spec to add the secrets as environment variables:
# The ENVIRONMENT variable CLIENT_SECRET is set to the value of the key key in the mysecret secret. No, need to mount if you are using this way         
          - name: CLIENT_SECRET
            valueFrom:
              secretKeyRef:
                name: mysecret
                key: clientsecret
                
```

```
<b>You can also get secrets, config map values without mounting as volume </b>

#### Full deployment.yml with volume secret mounted
This will create a volume named mysecret that is backed by the mysecret secret, 
and mount it at /etc/mysecret in the container.
        volumeMounts:
        - name: mysecret  
          mountPath: /etc/mysecret

In your Deployment.yaml file, 
you can modify the container spec to add the secrets as environment variables:
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
<p>
Persistent Volumes (PVs) are pod and node independent volumes.
The idea is that instead of storing the data in the pod or a node, 
we have entirely separate entities in our K8s cluster that are detached from our nodes.

Each pod then will have a Persistent Volume Claim (PVC), and it will use this to access the standalone entities we created
</p>

<p>
SET up PV-
The hostPath type allows us to set a path on the host machine
and then the data from that path will be exposed to different pods.
path under hostpath- which refers to the folder on our host machine where we want to save the data.
</p>

<p>
Setting up the PVC

Simply defining the PV is not enough. 
We also need to define the PV Claim which the pods will use later. 
For this create a host-pvc.yaml file 
</p>


<p>
PV and PVC
Final configuration
Now that we have our PV and PVC set up, 
all that needs to be done is make changes in the deployment.yaml file so that we use this PV
</p>


```
microk8s
kubectl port-forward <pod_name> <local_port>:<pod_port> 
```

### Readiness and Liveness probe checks

<p>
A liveness probe is used to determine whether the container is still running 
and able to handle requests. If the liveness probe fails,
Kubernetes will restart the container. 
This is useful in cases where a container may become stuck or unresponsive, 
and needs to be restarted in order to continue functioning properly.
</p>

<p>
A readiness probe, on the other hand, is used to determine 
whether a container is ready to handle requests. 
When a pod is created or starts up, 
it may not be immediately ready to handle requests. 
For example, it may be initializing a database connection or loading configuration files. 
The readiness probe allows Kubernetes to know when the container is ready to handle requests and start sending traffic to it.
If the readiness probe fails, Kubernetes will not send traffic to the container, but it won't restart the container.
</p>


```
<b>Readiness check </b>
In this example, the readinessProbe is configured to make an HTTP GET request to the path /healthz on port 80 of the container. The probe will wait 5 seconds before the first check and will repeat every 5 seconds until the container is considered ready.

You can check the readiness and liveness of the pod using kubectl describe pod <pod-name> 
and look for the Readiness and Liveness sections.

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

```
<b>Liveness probe </b>

The livenessProbe is configured to make an HTTP GET request to the path / on port 80 of the container. The probe will wait 15 seconds before the first check 
and will repeat every 15 seconds until the container is considered live.

        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 15
          periodSeconds: 15


You can check the readiness and liveness of the pod using 
kubectl describe pod <pod-name> and look for the Readiness and Liveness sections.
```

#### Config map
```
> Use a ConfigMap to keep your application code separate from your configuration.

> This lets you change easily configuration depending on the environment (development, production, testing) and to dynamically change configuration at runtime.

> A ConfigMap stores configuration settings for your code. Store connection strings, public credentials, hostnames, and URLs in your ConfigMap. You can use ConfigMaps to store configuration data that your pods need to access at runtime.

> First, you have multiple ConfigMaps, one for each environment.
  Second, a ConfigMap is created and added to the Kubernetes cluster.
  Third, containers in the Pod reference the ConfigMap and use its values.

Create configmap.yml
Apply

You can then reference the ConfigMap in your pod or deployment configuration using the configMap field. Here's an example of how to reference a ConfigMap in a pod specification:

apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: my-container
    image: my-image
    env:
    - name: key1
      valueFrom:
        configMapKeyRef:
          name: my-configmap
          key: key1


 
2nd way
You can also use configMapRef in the volumeMounts to mount the configMap as a volume in a container.
Mount the ConfigMap through a Volume in deployment.yml
Each property name in this ConfigMap becomes a new file in the mounted directory (`/etc/config`) after you mount it.

apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: my-container
    image: my-image
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: my-configmap

```
### DB connection
```
Create 3 files
mongo-db deployment-  To create pod with mongodb image
mongo-db service- Ports communication
mongodb pv and pvc - For persistent storage

In deployment.yml mongo
Mount mongo pvc volume- section under volumes and container to define path

Python App deployment file- 
Set environment variables to configure the connection to the MongoDB service in your app deployment.yml file
``` 