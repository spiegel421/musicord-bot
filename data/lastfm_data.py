#!/usr/bin/env python3
"""Lastfm username table

Store lastfm usernames by Discord id in a MySQL table.
"""
import mysql
from mysql.connector import connect

DB_NAME = "data"
PASSWORD = open("data/password.txt", "r").read()


def create_user_table():
    """Create MySQL table of lastfm usernames"""
    table = (
        "CREATE TABLE `lastfm_users` ("
        "   `id` char(18) NOT NULL,"
        "   `user` LONGTEXT NOT NULL,"
        "PRIMARY KEY(`id`)"
        ") ENGINE=InnoDB")

    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    try:
        cursor.execute(table)
    except mysql.connector.Error as err:
        print(err.msg)

    cursor.close()
    cnx.close()


def add_user(id, user):
    """Add a lastfm username to the table"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    add_user = ("REPLACE INTO `lastfm_users` "
                "(`id`, `user`) "
                "VALUES ('{}', '{}')".format(id, user))

    cursor.execute(add_user)
    cnx.commit()

    cursor.close()
    cnx.close()


def get_user(id):
    """Get a lastfm username by Discord id"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    get_username = ("SELECT `user` FROM `lastfm_users` "
                    "WHERE `id` = '{}'".format(id))

    cursor.execute(get_username)
    user = None
    for item in cursor:
        user = item[0]

    cursor.close()
    cnx.close()

    return user
