# salary-app

## Deployment
### Local
```
docker build -t <image_name> .
docker run -p 8080:8080 <image_name>
```
### GCP
```
gcloud builds submit --tag gcr.io/<PROJECT_ID>/<SOME_PROJECT_NAME> --timeout=2h
```