"""
Module for daily reports
"""

from collections import defaultdict
from datetime import datetime
from dateutil.parser import parse

from utils.cprint import cprint
from timesheet.table import get


def daily_report(date_str=None, verbose=True):
    """Prints a daily report of the timesheet. A date can be specified but it is optional."""
    where_clause = ""
    if date_str is None:
        date_str = str(datetime.today())[:10]
        where_clause = f"where date_str = '{date_str}'"
    else:
        date_str = parse(date_str).strftime("%Y-%m-%d")
        where_clause = f"where date_str = '{date_str}'"
    tt = None
    projectwise_work = defaultdict(int)
    if verbose:
        first = True
        for t in get(where_clause):
            if first:
                cprint("------------------------", "yellow")
                cprint(
                    "id\t\t\t\t        date_str  time end_time project work", "yellow"
                )
                first = False

            if tt is None:
                tt = t[2]

            dt = datetime.fromtimestamp(t[2])
            tsk_time = t[2] - tt
            projectwise_work[t[4]] += tsk_time
            temp = f"{(tsk_time)/60:.0f} min".rjust(10)
            cprint(
                f"{t[0]} {t[1]} {temp} {dt.strftime('%H:%M')} {t[4].rjust(12)} {t[3]}",
                "white",
            )
            tt = t[2]
        if first:
            cprint("No entries found", "red")
    else:
        first = True
        for t in get(where_clause):
            if first:
                cprint("------------------------", "yellow")
                cprint("date_str time end_time project work", "yellow")
                first = False

            if tt is None:
                tt = t[2]

            dt = datetime.fromtimestamp(t[2])
            tsk_time = t[2] - tt
            projectwise_work[t[4]] += tsk_time
            temp = f"{(tsk_time)/60:.0f} min".rjust(10)
            cprint(
                f"{t[1]} {temp} {dt.strftime('%H:%M')} {t[4].rjust(12)} {t[3]}",
                "white",
            )
            tt = t[2]

        if first:
            cprint("No entries found", "red")

    if len(projectwise_work.keys()):
        cprint("------------------------", "yellow")
        cprint("Projectwise work", "yellow")

    for k, v in projectwise_work.items():
        temp = f"{v/60:.0f} min".rjust(10)
        cprint(f"{k.rjust(12)} {temp}", "white")
