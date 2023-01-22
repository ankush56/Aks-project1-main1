#### PODS ####
###
```
pod.yml
pod2.yml
deplpoyment.yml
replicaset.yml
```

```
kubectl get pods
Filter by label
kubectl get pods -l name=pod_label
```

```
#Print in particulat namespace
kubectl get pods -n <NAME-SPACE>

Print Pods in all NameSpace
kubectl get pods -A
```
```
> Print the pod output in YAML/JSON format

$ kubectl get pods <POD-NAME> -o yaml  
$ kubectl get pods <POD-NAME> -o json
```
########################################
#### POD2 #####

```
Set envrionment variable
```
  - name: nginxcontainer
    image: nginx
    env:
      - name: greeting
        value: "hello from environment variable" 
```
```
Now sh to pod
kubectl exec -it sh podname
# environment Variables

```
output-
greeting=hello from environment variable
```

#### YAML Walkthrough
```
apiversion -This refers to the version of Kubernetes
Some common ones are v1, apps/v1, and extensions/v1beta1.
```

```
kind- This is the type of Kubernetes object. In this case (the example above), we’re creating a pod.
```
```
Metadata-The metadata houses information that describes the object briefly. name the object is the only mandatory field and the remaining are optional. Name of object..like pod or deployment
```

```
spec: The spec section is where we define containers that will run inside the pod.
The image of the application you want to run in your pods.
The name of the container that you’ll run in your pod.
ContainerPort is the port of your application in your container and the environment variable inside the containers.
```


```
Get all in 1 line
 kubectl get pods,deployment,rs  
 no space 
```


#### Nodeport, Ingress, Loadbalancer - To get external traffic to the cluster
<p> #### <b>ClusterIP</b> is default kubernetes service. Automatically created. There is no external access.</p>

<p><b>NodePort</b>, as the name implies, opens a specific port on all the Nodes (the VMs), and any traffic that is sent to this port is forwarded to the service.</p>
![NodePort](nodeportservice1.yml)


