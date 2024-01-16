#!/usr/bin/env python3.11
"""
This is the entry point for command line interface.
"""

import click
from conf import SETTINGS
from utils.cprint import cprint


VERBOSE = None


@click.group
@click.option("--verbose", is_flag=True, help="Switch verbosity")
def cli(verbose):
    """
    Global options for commandline
    """

    if verbose:
        SETTINGS["timesheet"]["verbose"] = not SETTINGS["timesheet"]["verbose"]
        cprint(
            f'Default verbosity is {not SETTINGS["timesheet"]["verbose"]}.'
            f' Verbosity switched to {SETTINGS["timesheet"]["verbose"]}'
        )
    else:
        cprint(f'Default verbosity is {SETTINGS["timesheet"]["verbose"]}')

@cli.command
@click.argument("entry", nargs=-1)
def work(entry):
    '''
    Add entry to timesheet
    '''
    from timesheet.parser import make_entry

    if len(entry) == 0:
        cprint("No entry passed. Exiting", 'red')
        return
    
    make_entry(entry)

@cli.command
@click.argument("uid", nargs=1)
def delete(uid):
    '''
    Delete entry from timesheet using uid. 
    # TODO: If uid is not passed, it will delete last entry
    '''

    from timesheet.table import delete

    try:
        delete(uid)
    except Exception as exc:
        cprint(exc, 'red')

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

    first = True
    for e in get():
        if first:
            cprint(f"id\t\t\t\tname\tshort_name\tdescription")
            first = False
        cprint(f"{e[0]}\t\t\t\t{e[1]}\t{e[2]}\t{e[3]}")


@cli.command
@click.argument("date_str", nargs=-1)
def report(date_str):
    '''
    Generate report
    '''
    from timesheet.reports.daily import daily_report

    if len(date_str) == 0:
        cprint("No entry passed. Running daily report")
        daily_report(verbose=SETTINGS["timesheet"]["verbose"])
        return

    daily_report(date_str[0], verbose=SETTINGS["timesheet"]["verbose"])


@cli.command
def run():
    '''
    run a fastapi server
    '''
    cprint("not implemented fastapi server", "red")


@cli.command
@click.option("--tables", is_flag=True, help="Table name")
def check(tables):
    '''
    Check if database is connected
    '''
    import utils.pg as pg

    try:
        record = pg.fetch_one("SELECT version();")
    except Exception as exc:
        cprint("You are not connected to database", "red")
        cprint(exc, "red")
        return
    cprint(f"You are connected to - {record[0]}\n")

    if tables:
        cprint("Checking tables")

        query = "SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"
        tables = [a[1] for a in pg.yield_results(query)]
        cprint("Tables found: {tables}")

        if 'project' not in tables:
            return cprint("project table not found", "red")
        if 'timesheet' not in tables:
            return cprint("timesheet table not found", "red")

        cprint("All tables found")


if __name__ == "__main__":
    cli()
