import os
import sys
import click
import pkg_resources
import rabectl.status
from pyfiglet import Figlet

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

    # Create GitOps folder
    gitops_folder = os.path.join(os.getcwd(), name)
    try:
        os.makedirs(gitops_folder, exist_ok=False)
    except FileExistsError:
        sys.exit('The "{folder_name}" folder already exists!'.format(
            folder_name=gitops_folder
        ))

    # Retrieve resources with the inquirer 
    resources = rabectl.status.Resources()
    resources.ask()
    resources.store(os.path.join(gitops_folder,'rabe.yaml'))
