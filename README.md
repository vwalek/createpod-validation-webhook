## Application for running the simple validation webhook to view the pod yaml definition before creation

### Installing

- clone the repository 

- deploy the application with the kustomize
~~~
# oc apply -f kustomize/
~~~

- check the namespace (feel free to modify if you want to use different namespace)
~~~
# oc project createpod-validation-webhook

# oc get pods
~~~

- make sure you have at least 2 replicas running, with 1 replica the webhook might fail and no pod can be added to cluster

- check the CA from the secret
~~~
# oc get secret createpod-tls-secret -o yaml | grep tls.crt | awk '{print $2}' | base64 -d
~~~

- take only the second certificate
~~~
# echo "<cert>" | base64 --wrap=0
~~~

- use the base64 ca-bundle to edit the webhooks, edit the "webhooks.clientConfig.caBundle"
~~~
vi webhook/webhook.yaml
~~~

- create the webhook in your cluster
~~~
# oc apply -f webhook/webhook.yaml
~~~

- you can use the dummy-app to deploy simple app
~~~
# oc create -f dummy-app/serviceaccount.yaml

# oc create -f dummy-app/deployment.yaml
~~~

- test if you can see that the pod was created
~~~
# oc logs <create-validation-webhook-pod-name> | grep dummy
~~~
