import logging
import psycopg2
from conf import SETTINGS

logger = logging.getLogger(__name__)


def connect():
    db = SETTINGS["database"]
    return psycopg2.connect(
        database=db["db_name"],
        user=db["db_user"],
        password=db["db_pass"],
        host=db["db_host"],
        port=db["db_port"],
    )


def yield_results(query):
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        for row in cursor.fetchall():
            yield row
    except (Exception) as error:
        logger.exception("Error while connecting to PostgreSQL %s", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            logger.debug("PostgreSQL connection is closed")


def fetch_one(query):
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchone()

    except (Exception) as error:
        logger.exception("Error while connecting to PostgreSQL %s", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            logger.debug("PostgreSQL connection is closed")


def execute(query):
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    except (Exception) as error:
        logger.exception("Error while connecting to PostgreSQL %s", error)
        raise error
    finally:
        if conn:
            cursor.close()
            conn.close()
            logger.debug("PostgreSQL connection is closed")


if __name__ == "__main__":
    record = fetch_one("SELECT version();")
    logger.debug("You are connected to - ", record[0], "\n")
