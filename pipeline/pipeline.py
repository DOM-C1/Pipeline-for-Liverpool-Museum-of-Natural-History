"""This file handles uploads to the database."""
import logging

from utils import get_consumer, get_db_connection, initialise_argparse
from validate_ratings import check_message


def process_message(msg: dict, conn) -> dict:
    """
    Processes a message by inserting it into either the 'ratings' or 'alerts' table 
    based on the message contents.
    Parameters:
    - msg: The message dictionary containing 'site', 'val', 'type', and 'at'.
    - conn: The database connection object.
    """
    action_dict = {
        -2: 'Emergency',
        -1: 'Assistance',
        0: 'Terrible',
        1: 'Bad',
        2: 'Neutral',
        3: 'Good',
        4: 'Amazing'
    }
    with conn.cursor() as cur:
        exh_id = "EXH_0" + str(msg['site'])
        if msg['val'] >= 0:
            val_name = action_dict[msg['val']]
            cur.execute(
                """INSERT INTO ratings (at, exhibition_id, value, value_name) 
                    VALUES (%s, %s, %s, %s)""",
                (msg['at'], exh_id, msg['val'], val_name))
        else:
            key = -1 if msg['type'] == 0 else -2
            val_name = action_dict[key]
            cur.execute(
                """INSERT INTO alerts (at, exhibition_id, value,value_name,type) 
                    VALUES (%s, %s, %s, %s,%s)""",
                (msg['at'], exh_id, msg['val'], val_name, msg['type']))

        conn.commit()


def setup_logging(flag):
    """Takes True or False as an input, if true
        it will log to terminal else a file."""
    if flag:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s', filename='chall3.log', filemode='a')


if __name__ == '__main__':
    log = initialise_argparse()
    flag = True if log == "terminal" else False
    setup_logging(flag)

    c = get_consumer()
    c.subscribe(['lmnh'])
    conn = get_db_connection()

    while True:
        msg = c.poll(1)
        msg = check_message(msg)
        if msg:
            process_message(msg, conn)
