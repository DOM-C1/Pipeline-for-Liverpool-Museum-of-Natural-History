"""This file provides useful functions to support the challenges; these functions
   handle various forms of connecting to servers. """
import argparse

from confluent_kafka import Consumer
from dotenv import load_dotenv
from os import environ as ENV
from psycopg2 import connect
from psycopg2.extras import RealDictCursor


def get_db_connection():
    """Gets a DB connection to AWS RDS"""
    load_dotenv()
    return connect(cursor_factory=RealDictCursor,

                   host=ENV["DB_HOST"],
                   user=ENV["DB_USERNAME"],
                   password=ENV["DB_PASSWORD"],
                   dbname=ENV["DB_NAME"])


def get_consumer():
    """Provides access to the Kafka client"""
    load_dotenv()
    return Consumer({'bootstrap.servers': ENV['BOOTSTRAP_SERVERS'],
                     'security.protocol': ENV['SECURITY_PROTOCOL'],
                     'sasl.mechanisms': ENV['SASL_MECHANISM'],
                     'sasl.username': ENV['USERNAME'],
                     'sasl.password': ENV['PASSWORD'],
                     'group.id': ENV['G_ID'],
                     'auto.offset.reset': 'latest'})


def initialise_argparse():
    parser = argparse.ArgumentParser(description='Process some inputs.')
    parser.add_argument('--log', '--l', type=str,
                        help="write 'terminal' or 'file', default is file")
    args = parser.parse_args()
    log = args.log
    return log
