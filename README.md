# tree-schema-ecs-example

This repo contains the code, templates and other development resources that along with the Tree Schema articles for creating a [complete ECS deployment](https://treeschema.com/blog/)

Note - to run these commands you will need to have the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) installed.

# Article 1 - VPC deployment 
In [the first article](https://treeschema.com/blog/comprehensive-ecs-deployments-vpcs-deployment) the following VPC is deployed, which generally contains the following resources:

![VPC Resources](./imgs/vpc_deployment_v1.jpg?raw=true "VPC Resources")

The VPC can be deployed by running this command from the root directory (change `my-vpc` to the name of the stack you would like):

```bash 
sam deploy \
--template templates/vpc-template.yaml \
--stack-name my-vpc \
--capabilities CAPABILITY_AUTO_EXPAND
```


# Article 2 - ECS Cluster, CloudFront Distribution & S3 Buckets
In [the second article](https://treeschema.com/blog/comprehensive-ecs-deployments-ecs-cluster-deployment/) the following CloudFormation, ECS 
resources are deployed in line with the following deployment:

![ECS Deployment Resources](./imgs/ecs-deployment.jpg?raw=true "ECS Deployment Resources")

The ECS resources, including the ECS cluster, required roles, CloudFront distribution, and S3 buckets can be deployed by running this command from the root directory (change `my-cluster-resources` to the name of the stack you would like and `your-user-id` to your user's user ID):

```bash 
sam deploy \
--template templates/ecs-cluster-template.yaml \
--stack-name my-cluster-resources \
--capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM \
--parameter-overrides "ParameterKey=YourUserId,ParameterValue=your-user-id"
```

# Article 3 - Creating the Django & Celery Application
In [the third article](https://treeschema.com/blog/comprehensive-ecs-deployments-building-the-django-app/) the Django & Celery app are created.

The application can be found under the `app` directory and generally has the following general flow:

![ECS Deployment Resources](./imgs/django-app-flow.jpg?raw=true "ECS Deployment Resources")

This repo can be cloned and the app can be run locally. Redis must be running locally on port 6379. Execute the following command in the `app` directory to start Django:

```bash 
python manage.py runserver 0.0.0.0:8001 
```
And in a second terminal, but the same directory, run the following to start Celery:
```bash 
celery -A ecs_example worker -l info 
```

