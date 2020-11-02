import json
import os

import boto3

# Override this with different environment variables
ENV = os.environ.get('EnvStageName', 'dev')
STACK_NAME = os.environ.get('VpcStackName', 'my-vpc-stack')
CONTAINER_NAME = os.environ.get('ContainerName', 'django_ecs_app')

cf = boto3.client('cloudformation')
ecs = boto3.client('ecs')
ecs_waiter = ecs.get_waiter('tasks_stopped')


cf_outputs = cf.describe_stacks(StackName=STACK_NAME)['Stacks'][0]['Outputs']
subnets = [x['OutputValue'] for x in cf_outputs if 'PrivateSubnet' in x['OutputKey']]
security_groups = [x['OutputValue'] for x in cf_outputs if 'AppSecurityGroup' in x['OutputKey']]


task_inputs = {
    'taskDefinition': 'django-ecs-app-serviceDjangoAppTaskDefinition',
    'cluster': f'my-cluster-resources-GeneralECSCluster-{ENV}',
    'count': 1,
    'launchType': 'FARGATE',
    'networkConfiguration': {
        'awsvpcConfiguration': {
            'subnets': subnets,
            'securityGroups': security_groups,
            'assignPublicIp': 'DISABLED'
        }
    },
    'overrides': {
        'containerOverrides': [
            {
                'name': 'django_ecs_app',
                'command': ['python', '/app/manage.py', 'migrate'],
            }
        ]
    }
}

print('Starting task with configs')
print(json.dumps(task_inputs, indent=2))

run_state = ecs.run_task(**task_inputs)
print('Task started')
print(run_state)    

task_id = run_state['tasks'][0]['taskArn']
ecs_waiter.wait(
    cluster=task_inputs['cluster'],
    tasks=[task_id],
    WaiterConfig={
        'Delay': 60,
        'MaxAttempts': 100
    }
)
print('Completed updating S3 with new static files!')
