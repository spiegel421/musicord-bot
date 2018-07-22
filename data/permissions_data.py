#!/usr/bin/env python3
"""Permissions table

Store the allowed channels for each command in a MySQL table.
"""
import mysql
from mysql.connector import connect

DB_NAME = "data"
PASSWORD = open("data/password.txt", "r").read()


def create_command_tables(commands):
    """Create MySQL table of lastfm usernames"""
    table = (
        "CREATE TABLE `{}` ("
        "   `channel_id` char(18) NOT NULL,"
        "PRIMARY KEY(`channel_id`)"
        ") ENGINE=InnoDB")

    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    for command in commands:
        try:
            cursor.execute(table.format(command))
        except mysql.connector.errors.ProgrammingError as err:
            print(err.msg)

    cursor.close()
    cnx.close()


def add_allowed_channel(command, channel_id):
    """Allow a command to be used with a particular channel"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    add_allowed = ("REPLACE INTO `{}` "
                   "VALUES('{}')".format(command, channel_id))

    try:
        cursor.execute(add_allowed)
    except mysql.connector.errors.ProgrammingError as err:
        return False

    cnx.commit()

    cursor.close()
    cnx.close()

    return True


def remove_allowed_channel(command, channel_id):
    """Remove a command from the table"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    remove_allowed = ("DELETE FROM `{}` "
                      "WHERE `channel_id` = '{}'".format(command, channel_id))

    try:
        cursor.execute(remove_allowed)
    except mysql.connector.errors.ProgrammingError as err:
        return False

    cnx.commit()

    cursor.close()
    cnx.close()

    return True


def get_allowed_channels(command):
    """Return a list of channel ids in which a command is allowed"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    get_allowed = ("SELECT `channel_id` FROM `{}`").format(command)

    cursor.execute(get_allowed)

    allowed_channels = list()
    for (channel_id,) in cursor:
        allowed_channels.append(channel_id)

    return allowed_channels
