#!/usr/bin/env python3.11
"""
This is the entry point for command line interface.
"""

import click

# from constants import BASE_DIR
from conf import SETTINGS

VERBOSE = None


@click.group
@click.option("--verbose", is_flag=True, help="Switch verbosity")
def cli(verbose):
    """
    Global options for commandline
    """

    if verbose:
        SETTINGS["timesheet"]["verbose"] = not SETTINGS["timesheet"]["verbose"]
        click.echo(
            f'Default verbosity is {not SETTINGS["timesheet"]["verbose"]}.'
            f' Verbosity switched to {SETTINGS["timesheet"]["verbose"]}'
        )
    else:
        click.echo(f'Default verbosity is {SETTINGS["timesheet"]["verbose"]}')


@cli.command
@click.argument("entry", nargs=-1)
def work(entry):
    '''
    Add entry to timesheet
    '''
    from timesheet.parser import make_entry

    if len(entry) == 0:
        click.echo("No entry passed. Exiting")
        return
    make_entry(entry)


@cli.command
@click.argument("date_str", nargs=-1)
def report(date_str):
    '''
    Generate report
    '''
    from timesheet.reports.daily import daily_report

    if len(date_str) == 0:
        click.echo("No entry passed. Running daily report")
        daily_report(verbose=VERBOSE)
        return

    daily_report(date_str[0], verbose=VERBOSE)


@cli.command
def run():
    '''
    run a fastapi server
    '''
    click.echo("not implemented fastapi server")
    # cli.echo("Starting fastapi server")


@cli.command
def check():
    '''
    Check if database is connected
    '''
    import pg

    try:
        record = pg.fetch_one("SELECT version();")
    except Exception as exc:
        print("You are not connected to database")
        print(exc)
        return
    print("You are connected to - ", record[0], "\n")


if __name__ == "__main__":
    cli()
