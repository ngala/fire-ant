#!/usr/bin/env python3.11
"""
This is the entry point for command line interface.
"""

import click

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
@click.option("--name", prompt="Project name", help="Project name")
@click.option("--short_name", prompt="Project short name", help="Project short name")
@click.option("--description", prompt="Project description", help="Project description")
def create_project(name, short_name, description):
    '''
    Add project to timesheet
    '''

    from project.table import insert

    insert(name, short_name, description)


@cli.command
def lprj():
    '''
    List projects
    '''
    from project.table import get

    for e in get():
        click.echo(f"{e}")

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


@cli.command
@click.option("--tables", is_flag=True, help="Table name")
def check(tables):
    '''
    Check if database is connected
    '''
    import pg

    try:
        record = pg.fetch_one("SELECT version();")
    except Exception as exc:
        click.echo("You are not connected to database")
        click.echo(exc)
        return
    click.echo("You are connected to - ", record[0], "\n")

    if tables:
        click.echo("Checking tables")

        query = "SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"
        tables = [a[1] for a in pg.yield_results(query)]
        click.echo("Tables found:", tables)

        if 'project' not in tables:
            return click.echo("project table not found")
        if 'timesheet' not in tables:
            return click.echo("timesheet table not found")

        click.echo("All tables found")

if __name__ == "__main__":
    cli()
