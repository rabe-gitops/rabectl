import os
import sys
import click
import pkg_resources
import rabectl.status
import rabectl.provisioner
from pyfiglet import Figlet
from PyInquirer import prompt
from shutil import which, rmtree


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        click.secho(Figlet(font='smkeyboard').renderText('rabectl'), fg='green', bold=True)
        click.secho('### The Rabe GitOps project CLI ###', bold=True)
        click.secho('https://github.com/rabe-gitops/', fg='bright_black')
        click.secho('https://www.rabegitops.it/', fg='bright_black')
        click.secho('v' + pkg_resources.require("rabectl")[0].version + '\n', fg='bright_black')
        click.secho(ctx.get_help())

@main.command()
@click.argument('name')
def start(name):

    if which('git') is None:
        sys.exit('Git not found! Please install it from "https://git-scm.com/downloads/"')
    elif which('terraform') is None:
        sys.exit('Terraform not found! Please install it from "https://www.terraform.io/downloads.html"')

    click.secho("""
Please note: in the following steps you're going to enter a GitHub token.
Make sure you have it before proceeding and that it has the following permissions:
  - repo
  - admin:repo_hook
  - user:email
  - delete_repo

Regarding the cloud resources, an administrator account is also recommended
(e.g. an AWS CLI profile linked to a user with the AdministratorAccess policy attached)
as several resources, belonging to many services, are going to be created.
""", bold=True)

    gitops_folder = os.path.join(os.getcwd(), name)
    if os.path.exists(gitops_folder):
        sys.exit('The "{folder_name}" folder already exists!'.format(folder_name=name))

    resources = rabectl.status.Resources()
    answers = resources.ask()
    if len(answers) == 0:
        sys.exit(1)

    os.makedirs(gitops_folder, exist_ok=False)
    os.chdir(gitops_folder)

    provisioner = rabectl.provisioner.Provisioner(answers)
    provisioner.deploy()

    resources.store(os.path.join(gitops_folder, 'rabe.yaml'))

@main.command()
@click.argument('name')
def delete(name):

    if which('git') is None:
        sys.exit('Git not found! Please install it from "https://git-scm.com/downloads/"')
    elif which('terraform') is None:
        sys.exit('Terraform not found! Please install it from "https://www.terraform.io/downloads.html"')

    gitops_folder = os.path.join(os.getcwd(), name)
    gitops_file = os.path.join(gitops_folder, 'rabe.yaml')
    if not os.path.exists(gitops_file):
        sys.exit('No rabe.yaml file found in the {folder_name} path!'.format(folder_name=name))

    prompt({
        'type': 'confirm',
        'message': 'Are you sure you want to destroy your pipeline and its local folder?',
        'name': 'exit',
        'default': False
    })

    resources = rabectl.status.Resources()
    status = resources.load(gitops_file)
    if len(status) == 0:
        sys.exit(1)

    os.chdir(gitops_folder)
    provisioner = rabectl.provisioner.Provisioner(status)
    provisioner.delete()
    os.chdir('..')

    rmtree(os.path.basename(gitops_folder), ignore_errors=True)
