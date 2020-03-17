import os
import yaml
import click
from PyInquirer import Token, Separator, prompt, style_from_dict

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
                    'name': 'AWS (Amazon Web Services)'
                },
            ]
        }
    ]

    answers = {}


    def ask(self):
        self.answers = prompt(self.questions, style=self.style)

    def load(self, path):
        with open(path, 'r') as f:
            self.answers = yaml.load(f, Loader=yaml.FullLoader)

    def store(self, path):
        with open(path, 'w') as f:
            yaml.dump(self.answers, f, default_flow_style=False)
