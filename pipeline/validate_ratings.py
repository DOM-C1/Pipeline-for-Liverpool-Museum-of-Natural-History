"""This file handles validating the message before sending it out"""
from datetime import datetime, time
import json
import logging


def is_valid_at(msg: dict) -> bool:
    """Checks the validity of a date by two criteria -
        Is it in valid format and are the times between 8:45, 18:15 """
    try:
        date_str = msg['at']
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        start_time = time(8, 45)
        end_time = time(18, 15)
        if start_time <= dt.time() <= end_time:
            return True
        return False
    except ValueError:
        return False


def is_valid_site(msg: dict) -> bool:
    """Checks to see if the site is correct"""
    if msg['site'].isdigit():
        if not 0 <= int(msg['site']) <= 4:
            return False
    if not msg['site'].isdigit() and msg['site'] != 'Vault':
        return False
    return True


def is_valid_type(msg: dict) -> bool:
    """Checks to see if the type is correct"""
    if msg.get('type'):
        if not isinstance(msg.get('type', 0), int):
            return False

        if msg['val'] not in [-1, 0]:
            return False

    if not msg.get('type') and msg['val'] < 0:
        return False

    return True


def is_valid_value(msg: dict) -> bool:
    """Checks to see if value is correct"""
    if not -1 <= int(msg['val']) <= 4:
        return False
    if not isinstance(msg['val'], int):
        return False
    return True


def check_message(msg: dict) -> bool:
    """Passes the message through a series of tests, only returning
       the message if it passes all of them."""
    if msg:
        msg = json.loads(msg.value().decode('utf-8'))

        if not all(key in msg for key in ['val', 'at', 'site']):
            logging.critical(f"Missing keys! {msg}")

        elif not is_valid_value(msg):
            logging.critical(f'Incorrect value! {msg}')

        elif not is_valid_at(msg):
            logging.critical(f'Incorrect date! {msg}')

        elif not is_valid_site(msg):
            logging.critical(f'Incorrect site! {msg}')

        elif not is_valid_type(msg):
            logging.critical(f'Incorrect type! {msg}')

        else:
            return msg
