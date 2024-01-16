'''
Color print utility
'''
import click

def cprint(msg, color="green", bold=False):
    '''
    This function us intended to create a standard way of printing messages'''

    click.echo(click.style(msg, fg=color, bold=bold))
