'''
Module for daily reports
'''

from datetime import datetime
from timesheet.table import get
from dateutil.parser import parse
from collections import defaultdict


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
        print(
            "id\t\t\t\t       ",
            "date_str ",
            "time",
            "end_time",
            "project",
            "work")
        for t in get(where_clause):

            if tt is None:
                tt = t[2]

            dt = datetime.fromtimestamp(t[2])
            tsk_time = t[2] - tt
            projectwise_work[t[4]] += tsk_time
            print(
                t[0],
                t[1],
                f"{(tsk_time)/60:.0f} min".rjust(10),
                dt.strftime("%H:%M"),
                t[4].rjust(12),
                t[3],
            )
            tt = t[2]
    else:
        for t in get(where_clause):
            print("date_str", "time", "end_time", "project", "work")
            if tt is None:
                tt = t[2]

            dt = datetime.fromtimestamp(t[2])
            tsk_time = t[2] - tt
            projectwise_work[t[4]] += tsk_time
            print(
                t[1],
                f"{(tsk_time)/60:.0f} min".rjust(10),
                dt.strftime("%H:%M"),
                t[4].rjust(12),
                t[3],
            )
            tt = t[2]
    print("Projectwise work")
    for k, v in projectwise_work.items():
        print(k.rjust(12), f"{v/60:.0f} min".rjust(10))
