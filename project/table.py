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
