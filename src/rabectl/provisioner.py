import os
import boto3
import string
import random
from git import Repo
from github import Github
from python_terraform import Terraform, IsFlagged


class Provisioner:

    status = {}
    base_repo_url = 'https://github.com/rabe-gitops/base.git'
    base_local_path = 'base'
    tf = Terraform()

    def __init__(self, status):
        self.status = status

    def deploy(self):
        Repo.clone_from(self.base_repo_url, self.base_local_path)
        github = Github(base_url="https://api.github.com", login_or_token=self.status['github.token'])

        
        self.tf.init(os.path.join(
            self.base_local_path,
            self.status['cloud'].lower(),
            'base-pipeline'
        ), capture_output=True)

        os.environ['TF_VAR_GITHUB_TOKEN'] = self.status.pop('github.token')
        os.environ['TF_VAR_WEBHOOK_SECRET'] = ''.join(random.choices(
            string.ascii_uppercase + string.digits,
            k=12
        ))

        self.tf.apply(os.path.join(
                self.base_local_path,
                self.status['cloud'].lower(),
                'base-pipeline'
            ),
            input=False, no_color=IsFlagged, compact_warnings=IsFlagged,
            capture_output=False, auto_approve=IsFlagged, skip_plan=True,
            var={
                'PROJECT': self.status['project'],
                'AWS_PROFILE': self.status['aws.profile'],
                'AWS_REGION': self.status['aws.region'],
                'GITHUB_OWNER': self.status['github.owner'],
                'GITHUB_REPOSITORY': self.status['github.repo'],
                'GITHUB_BRANCH': 'master'
            }
        )

        ssm_client = boto3.Session(profile_name=self.status['aws.profile']).client('ssm')
        ssm_client.put_parameter(
            Name = '-'.join([self.status['project'].lower(), 'github', 'token']),
            Value = os.environ['TF_VAR_GITHUB_TOKEN'],
            Type = 'SecureString',
            Tags = [
                { 'Key': 'Project', 'Value': self.status['project'] },
                { 
                    'Key': 'Name',
                    'Value': '-'.join([
                        self.status['project'].lower(), 'github', 'token'
                    ])
                }
            ]
        )

        ssm_client.put_parameter(
            Name = '-'.join([self.status['project'].lower(), 'webhook', 'secret']),
            Value = os.environ['TF_VAR_WEBHOOK_SECRET'],
            Type = 'SecureString',
            Tags = [
                { 'Key': 'Project', 'Value': self.status['project'] },
                { 
                    'Key': 'Name',
                    'Value': '-'.join([
                        self.status['project'].lower(),
                        'webhook',
                        'secret'
                    ])
                }
            ]
        )

        del os.environ['TF_VAR_GITHUB_TOKEN']
        del os.environ['TF_VAR_WEBHOOK_SECRET']


    def delete(self):
        ssm_client = boto3.Session(profile_name=self.status['aws.profile']).client('ssm')
        os.environ['TF_VAR_GITHUB_TOKEN'] = ssm_client.get_parameter(
            Name = '-'.join([self.status['project'].lower(), 'github', 'token']),
            WithDecryption = True
        )['Parameter']['Value']

        ssm_client.delete_parameter(
            Name = '-'.join([self.status['project'].lower(), 'github', 'token'])
        )
        ssm_client.delete_parameter(
            Name = '-'.join([self.status['project'].lower(), 'webhook', 'secret'])
        )

        self.tf.destroy(os.path.join(
                self.base_local_path,
                self.status['cloud'].lower(),
                'base-pipeline'
            ),
            input=False, no_color=IsFlagged, compact_warnings=IsFlagged,
            capture_output=False, auto_approve=IsFlagged,
            var={
                'PROJECT': self.status['project'],
                'AWS_PROFILE': self.status['aws.profile'],
                'AWS_REGION': self.status['aws.region'],
                'GITHUB_OWNER': self.status['github.owner'],
                'GITHUB_REPOSITORY': self.status['github.repo'],
                'GITHUB_BRANCH': 'master'
            }
        )

        del os.environ['TF_VAR_GITHUB_TOKEN']
