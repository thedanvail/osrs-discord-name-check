from detect_names import get_score
import os
import psycopg2

from datetime import datetime, timezone


def shift(s, n):
    return ''.join(chr(ord(char) - n) for char in s)


def create_table():
    ## Create table
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        cur = conn.cursor()

        # -- Table Definition ----------------------------------------------
        create_table_query = """
        DROP TABLE IF EXISTS user_data;
        CREATE TABLE IF NOT EXISTS user_data (
            username text PRIMARY KEY,
            score text,
            pulled_at timestamp without time zone,
            last_failed_at timestamp without time zone
        );
        """

        cur.execute(create_table_query)

        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to create table", error)

    finally:
        if conn:
            cur.close()
            conn.close()
            print("Table closed")


def update_user_info(user, score, time=datetime.now(timezone.utc)):
    ## Insert into table
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        cur = conn.cursor()

        insert_query = """INSERT INTO user_data (username, score, pulled_at) VALUES (%s,%s,%s)"""

        update_query = """
        INSERT INTO user_data (username, score, pulled_at, last_failed_at) values (%s, %s, %s, NULL)
        ON CONFLICT (username) DO UPDATE SET 
        (username, score, pulled_at, last_failed_at) = 
        (EXCLUDED.username, EXCLUDED.score, EXCLUDED.pulled_at, EXCLUDED.last_failed_at)
        """
        record_to_insert = (user, score, time)
        cur.execute(update_query, record_to_insert)

        conn.commit()
        count = cur.rowcount
        print(count, "Record inserted successfully into user table")


    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into user table", error)

    finally:
        if conn:
            cur.close()
            conn.close()
            print("Table closed")


def update_user_fail(user, time=datetime.now(timezone.utc)):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        cur = conn.cursor()

        update_query = """
        INSERT INTO user_data (username, score, pulled_at, last_failed_at) values (%s, null, null, %s)
        ON CONFLICT (username) DO UPDATE SET last_failed_at = %s
        """

        record_to_insert = (user, time, time)
        cur.execute(update_query, record_to_insert)

        conn.commit()
        count = cur.rowcount
        print(count, "Record updated successfully in user table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to update record into user table", error)

    finally:
        if conn:
            cur.close()
            conn.close()
            print("Table closed")


def print_table():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    cur = conn.cursor()
    cur.execute("SELECT * FROM user_data")

    records = cur.fetchall()
    print(records)


os.environ['DATABASE_URL']=shift('kjnobm`n5**l`ifculiequuqq51,^3`1]`,]\\+]`4-10+^/_33^`^2^324]_44.4+]0\\4.aa+.02...3`012/41-`^;`^-(0/(--0(,.+(-,-)^jhkpo`(,)\\h\\uji\\rn)^jh50/.-*_.j_/]do,lhgb4', -5)

DATABASE_URL = os.environ['DATABASE_URL']


update_user_fail('feather-like', datetime.now(timezone.utc))

get_score('feather-like')

update_user_info('feather-like', get_score('feather-like'))

print_table()

