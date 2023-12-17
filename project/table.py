'''
Table: project

'''
from datetime import datetime
from uuid import uuid4
import pg


table_query = (
    """CREATE TABLE IF NOT EXISTS project (
        id VARCHAR(255) PRIMARY KEY NOT NULL,
        name VARCHAR(255),
        short_name VARCHAR(25),
        description TEXT,
        created_at BIGINT,
        updated_at BIGINT) """,
)


def insert(name, short_name, description):
    u = uuid4()
    name = name.replace("'", "''")
    short_name = short_name.replace("'", "''")
    description = description.replace("'", "''")
    s = f"""INSERT INTO project (id, name, short_name, description, created_at) values (
        'tk_{str(u)}',
        '{name}',
        '{short_name}',
        '{description}',
        {datetime.now().timestamp()}
    )"""
    print("-->", s)
    pg.execute(s)


def delete(id):
    q = f"DELETE FROM timesheet where id = '{id}'"
    print(q)
    pg.execute(q)


def get(
    where_clause="",
    order_by_clause="order by name ASC",
    limit_clause="limit 50 offset 0",
):
    '''
    Get entry from table
    '''

    if where_clause.strip() != "" and not where_clause.lower().startswith("where"):
        raise Exception("where_clause must start with WHERE")

    query = f"select id, name, short_name, description, created_at " \
            f"from project {where_clause} {order_by_clause} {limit_clause};"
    return pg.yield_results(query)

