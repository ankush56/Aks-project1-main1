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
App code
Dockerfile builds image from src code
push image to dockerhub
deployment.yml spins container with 2 replicas from docker image built in step and pulls docker image
```

#### Secrets setup
secret.yml manifest define it
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