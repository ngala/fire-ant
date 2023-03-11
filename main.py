#!/usr/bin/env python3.11
"""
This is the entry point for command line interface.
"""
from os import path
from datetime import datetime
import shutil
import sys

# from constants import BASE_DIR
from conf import SETTINGS

WORD_COUNT = "word_count"


def main():
    ll = len(sys.argv)
    if ll == 1:
        print("No argument passed")
        exit(0)

    if sys.argv[1] == "--work" or sys.argv[1] == "-w":

        from timesheet.reports.daily import daily_report

        if len(sys.argv[2:]) != 0:
            from timesheet.parser import make_entry

            e = " ".join(sys.argv[2:])
            make_entry(e)

        v = SETTINGS["timesheet"]["verbose"]

        daily_report(verbose=v)
        exit(0)

    if sys.argv[1] == "--check":
        import pg

        try:
            record = pg.fetch_one("SELECT version();")
        except Exception as exc:
            print("You are not connected to database")
            print(exc)
            exit(1)
        print("You are connected to - ", record[0], "\n")
        exit(0)

    if sys.argv[1] == "--delete":
        if ll < 3:
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
        shutil.copyfile(WORD_COUNT, f"{WORD_COUNT}_{datetime.now().isoformat()}")
        with open(WORD_COUNT, "w") as f:
            f.write("0")
        exit()

    if sys.argv[1] == "run":
        from server import run_server

        run_server()
        exit(0)


if __name__ == "__main__":
    main()
