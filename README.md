# tree-schema-ecs-example

This repo contains the code, templates and other development resources that along with the Tree Schema articles for creating a [complete ECS deployment](https://treeschema.com/blog/)

Note - to run these commands you will need to have the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) installed.

# Article 1 - VPC deployment 
In [the first article](https://treeschema.com/blog/comprehensive-ecs-deployments-vpcs-deployment) the following VPC is deployed, which generally contains the following resources:

![VPC Resources](./imgs/vpc_deployment.jpg?raw=true "VPC Resources")

The VPC can be deployed by running this command from the root directory (change `my-vpc` to the name of the stack you would like):

```bash 
sam deploy \
--template vpc-template.yaml \
--stack-name my-vpc \
--capabilities CAPABILITY_AUTO_EXPAND
```