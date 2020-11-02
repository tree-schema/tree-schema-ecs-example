# tree-schema-ecs-example

This repo contains the code, templates and other development resources that along with the [Tree Schema](https://treeschema.com) articles for creating a [complete ECS deployment](https://treeschema.com/blog/)

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
python manage.py runserver 0.0.0.0:8000
```
And in a second terminal, but the same directory, run the following to start Celery:
```bash 
celery -A ecs_example worker -l info 
```


# Article 4 - Deploying the App to ECS
In [the fourth article](https://treeschema.com/blog/comprehensive-ecs-deployments-database-and-ecs-deploy/) the app is deployed to ECS.

Assuming that you have been following along with the other walkthroughs, you will only need to update a few parameters in the `mapping` section of the template. The template 
can be found here:
```bash 
./templates/django-app.yaml
```

The containers can be built with the following command from this directory:

```bash 
sh build.sh
```

And can be deployed with 
```bash 
sam deploy -t templates/django-app.yaml \
--stack-name django-ecs-app \
--capabilities CAPABILITY_IAM  
```


# Article 5 - Getting Ready for Prod
In [the fifth and final article](https://treeschema.com/blog/comprehensive-ecs-production-ready-application/) the finishing touches are put in place to use the app in production. Emails are sent with SES, autoscaling is put in place and Route53 sends traffic from our domain to the app.

With the new updates, the containers will need to be rebuilt with the following command from this directory:

```bash 
sh build.sh
```

And the services will need to be updated / redeployed with the same command.
```bash 
sam deploy -t templates/django-app.yaml \
--stack-name django-ecs-app \
--capabilities CAPABILITY_IAM  
```
