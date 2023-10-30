#!/usr/bin/env python3.11
"""
This is the entry point for command line interface.
"""

from datetime import datetime
import shutil
import sys

import click

# from constants import BASE_DIR
from conf import SETTINGS

WORD_COUNT = "word_count"

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
    from timesheet.reports.daily import daily_report

    if len(entry) == 0:
        click.echo("No entry passed. Running daily report")
        daily_report(verbose=VERBOSE)
        return

    from timesheet.parser import make_entry

    make_entry(entry)


@cli.command
def report():
    pass


@cli.command
def run():
    pass

@cli.command
def check():
    import pg

    try:
        record = pg.fetch_one("SELECT version();")
    except Exception as exc:
        print("You are not connected to database")
        print(exc)
        return
    print("You are connected to - ", record[0], "\n")


def main():
    argument_count = len(sys.argv)
    if argument_count == 1:
        print("No argument passed")
        exit(0)

    if sys.argv[1] == "--delete":
        if argument_count < 3:
            print("Insufficient options for --delete")
            exit(1)
        from timesheet.table import delete

        if sys.argv[2] != "":
            print(sys.argv[2])
            delete(sys.argv[2])
        else:
            print("Delete option needs timesheet id")
            exit(1)
        exit(0)

    if sys.argv[1] == "--daily-work" or sys.argv[1] == "-d":
        from timesheet.reports.daily import daily_report

        v = SETTINGS["timesheet"]["verbose"]
        if len(sys.argv) == 3:
            date_str = sys.argv[2]
            daily_report(date_str, v)
        else:
            daily_report(verbose=v)
        exit(0)

    if sys.argv[1] == "-r":
        shutil.copyfile(
            WORD_COUNT,
            f"{WORD_COUNT}_{datetime.now().isoformat()}")
        with open(WORD_COUNT, "w") as f:
            f.write("0")
        exit()

    if sys.argv[1] == "run":
        from server import run_server

        run_server()
        exit(0)


if __name__ == "__main__":
    cli()
