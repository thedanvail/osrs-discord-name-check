from detect_names import get_score
import os
import psycopg2

from datetime import datetime, timezone


def shift(s, n):
    return ''.join(chr(ord(char) - n) for char in s)

# TODO: create table if table is missing


def delete_table():
    # Don't do this unless resetting

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        cur = conn.cursor()

        # -- Table Definition ----------------------------------------------
        create_table_query = "DROP TABLE IF EXISTS user_data;"

        cur.execute(create_table_query)
        conn.commit()

        print("Table deleted")

    except (Exception, psycopg2.Error) as error:
        print("Failed to delete table", error)

    finally:
        if conn:
            cur.close()
            conn.close()


# TODO: future work: log scores!

def create_table():
    # Create table

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    # -- Table Definition ----------------------------------------------
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        discord_id bigint PRIMARY KEY,
        rsn text,
        pulled_at timestamp with time zone,
        last_failed_at timestamp with time zone
    );
    """

    try:
        cur.execute(create_table_query)
        conn.commit()

        print("Table created")

        col_name_query = """
        SELECT column_name
          FROM information_schema.columns
         WHERE table_name = 'user_data'
        """

        cur.execute(col_name_query)
        result = cur.fetchall()
        unpack_result = [x for (x,) in result]
        print(unpack_result)

    except (Exception, psycopg2.Error) as error:
        print("Failed to create table", error)

    finally:
        if conn:
            cur.close()
            conn.close()


def update_user_info(discord_id, rsn=None, time=datetime.now(timezone.utc)):
    # Insert into table

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    if rsn:
        update_query = """
        INSERT INTO user_data (discord_id, rsn, pulled_at, last_failed_at) values (%s, %s, %s, NULL)
        ON CONFLICT (discord_id) DO UPDATE SET 
        (discord_id, rsn, pulled_at, last_failed_at) = 
        (EXCLUDED.discord_id, EXCLUDED.rsn, EXCLUDED.pulled_at, EXCLUDED.last_failed_at)
        """

        record_to_insert = (discord_id, rsn, time)
    else:
        # ignore rsn
        update_query = """
        INSERT INTO user_data (discord_id, pulled_at, last_failed_at) values (%s, %s, NULL)
        ON CONFLICT (discord_id) DO UPDATE SET 
        (discord_id, rsn, pulled_at, last_failed_at) = 
        (EXCLUDED.discord_id, EXCLUDED.pulled_at, EXCLUDED.last_failed_at)
        """

        record_to_insert = (discord_id, time)

    # score = get_score(user)

    try:
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


def update_user_fail(discord_id, rsn=None, time=datetime.now(timezone.utc)):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    update_query = """
    INSERT INTO user_data (discord_id, rsn, last_failed_at) values (%s, %s, %s)
    ON CONFLICT (discord_id) DO UPDATE SET last_failed_at = EXCLUDED.last_failed_at
    """

    try:
        record_to_insert = (discord_id, rsn, time)
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

    count = cur.rowcount
    print(count, "row(s)")

    records = cur.fetchall()
    print(*records, sep='\n')
    return records


def last_failed_at(discord_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    result = None
    try:
        cur.execute("SELECT last_failed_at FROM user_data WHERE discord_id = %s;", (discord_id,))
        [(result, )] = cur.fetchall()

    except IndexError as error:
        print("User not in table", error)

    except (Exception, psycopg2.Error) as error:
        print(f"Failed to check last failed at for {discord_id}", error)

    finally:

        if result is None:
            print('No data found for last failed')

        else:
            print('Found last failed')

        if conn:
            cur.close()
            conn.close()
            print("Table closed")

        return result


def last_pulled_at(discord_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    result = None
    try:
        cur.execute("SELECT pulled_at FROM user_data WHERE discord_id = %s;", (discord_id,))
        [(result, )] = cur.fetchall()

    except IndexError as error:
        print("User not in table", error)

    except (Exception, psycopg2.Error) as error:
        print(f"Failed to check last pulled at for {discord_id}", error)

    finally:

        if result is None:
            print('No data found for last pulled at')

        else:
            print('Found last pulled at')

        if conn:
            cur.close()
            conn.close()
            print("Table closed")

        return result


## for local runs
# os.environ['DATABASE_URL'] = shift('kjnobm`n5**l`ifculiequuqq51,^3`1]`,]\\+]`4-10+^/_33^`^2^324]_44.4+]0\\4.aa+.02...3`012/41-`^;`^-(0/(--0(,.+(-,-)^jhkpo`(,)\\h\\uji\\rn)^jh50/.-*_.j_/]do,lhgb4', -5)

DATABASE_URL = os.environ['DATABASE_URL']

# TEST
# update_user_fail('me','feather-like', datetime.now(timezone.utc))
#
# get_score('feather-like')
#
# update_user_info('feather-like')
#
# print_table()

# last_failed_at('missing')
#
# last_failed_at('feather-like')
#
# last_pulled_at('feather-like')
# last_pulled_at('missing')
