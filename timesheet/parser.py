'''
Parser for work entry
'''
from typing import Tuple
import re
from datetime import datetime
from dateutil.parser import parse as datetime_parse
from timesheet.table import insert, get, delete


def entry_parse(entry: str) -> (Tuple[str, str]):
    """Parse entry string into project and entry"""
    if ";;" in entry:
        # tasksless entry
        return "", entry

    # task entry
    try:
        i = entry.index(":")
    except ValueError:
        return "", entry

    return entry[:i], entry[i + 1:].strip()


def insert_entry(time_str: str, entry_str: str, merge: bool = False):
    """
    Insert entry in timesheet table
    time_str: time string
    entry_str: entry string
    merge: merge with last entry if True

    Currently merge is done by deleting the last entry and inserting a new one.
    This is not ideal. But it works for now. The ideal way would be to update the last entry.
    """
    try:
        entry_time = datetime_parse(time_str)
    except Exception:
        entry_time = datetime.now()
    proj, entry = entry_parse(entry_str)
    print(entry_time, proj, entry, sep="--")

    if merge:
        date_str = entry_time.strftime("%Y-%m-%d")
        entry_ = list(
            get(
                where_clause=f"where date_str = '{date_str}'",
                order_by_clause='order by end_time desc',
                limit_clause='limit 1'
            ))

        if len(entry_) == 1:
            entry_ = entry_[0]
            if entry_[4] == proj and entry_[3] == entry:
                # delete last entry
                entry_id = entry_[0]
                print("Merging with last entry")
                delete(entry_id)

    insert(entry_time, proj, entry)


def make_entry(entry: str):
    """Make entry in timesheet table"""

    # ee = entry.strip().split()
    # if len(ee) == 0:
    #     raise Exception("Invalid")

    # ee = [e.strip() for e in ee]

    if not re.match("^[0-9:]+$", entry[0]):
        insert_entry(datetime.now().isoformat(), " ".join(entry), True)
    else:
        if len(entry) == 1:
            raise Exception("Invalid")
        insert_entry(entry[0], " ".join(entry[1:]), True)
