'''
Module containing table functions for timesheet
'''
import logging
from datetime import datetime
from uuid import uuid4
import pg

logger = logging.getLogger(__name__)

table_query = (
    """CREATE TABLE IF NOT EXISTS timesheet (
        id VARCHAR(255) PRIMARY KEY NOT NULL,
        date_str VARCHAR(8),
        end_time BIGINT,
        work TEXT,
        project VARCHAR(255),
        created_at BIGINT) """,
)


def insert(time_obj, project, work):
    '''
    Insert entry in to table
    '''
    uid = uuid4()
    project = project.replace("'", "''")
    work = work.replace("'", "''")
    sql_query = f"""INSERT INTO timesheet (id, date_str, end_time, work, project, created_at) values (
        'ts_{str(uid)}',
        '{time_obj.date().isoformat()}',
        {time_obj.timestamp()},
        '{work}',
        '{project}',
        {datetime.now().timestamp()}
    )"""
    logger.debug("--> %v", sql_query)
    pg.execute(sql_query)


def get(
    where_clause="",
    order_by_clause="order by end_time ASC",
    limit_clause="limit 50 offset 0",
):
    '''
    Get entry from table
    '''
    query = f"select id, date_str, end_time, work, project, created_at " \
            f"from timesheet {where_clause} {order_by_clause} {limit_clause};"
    return pg.yield_results(query)


def delete(id: str):
    '''
    Delete entry
    '''
    if len([a for a in get(f"where id = '{id}'")]) == 1:
        s = f"DELETE FROM timesheet WHERE id = '{id}'"
        logger.debug("--> %v", s)
        pg.execute(s)
    else:
        print("no timesheet entry work found")
