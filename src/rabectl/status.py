import os
import yaml
import click
import boto3
from PyInquirer import prompt, style_from_dict
from botocore.exceptions import ProfileNotFound
from PyInquirer import Token, Separator, Validator, ValidationError

class AWSProfileValidator(Validator):
    def validate(self, profile_doc):
        try:
            boto3.Session(profile_name=profile_doc.text)
        except ProfileNotFound:
            raise ValidationError(
                message=('Profile not found! Enter a valid profile name, or create it: '
                         '"aws configure --profile <PROFILE_NAME>"'),
                cursor_position=len(profile_doc.text)
            )

class Resources:

    style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

    questions = [
        {
            'type': 'list',
            'message': 'Select your cloud provider',
            'name': 'cloud',
            'choices': [
                {
                    'name': 'AWS'
                }
            ]
        },
        {
            'when': lambda answers: answers['cloud'] == 'AWS',
            'type': 'input',
            'message': 'Insert a valid AWS CLI profile name',
            'name': 'profile',
            'validate': AWSProfileValidator
        }
    ]

    answers = {}

    def ask(self):
        self.answers = prompt(self.questions, style=self.style)
        return self.answers

    def load(self, path):
        with open(path, 'r') as f:
            self.answers = yaml.load(f, Loader=yaml.FullLoader)

    def store(self, path):
        with open(path, 'w') as f:
            yaml.dump(self.answers, f, default_flow_style=False)
