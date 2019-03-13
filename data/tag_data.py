#!/usr/bin/env python3
"""Tags table

Store tags by tag id in a MySQL table.
"""
import mysql
from mysql.connector import connect

DB_NAME = "data"
PASSWORD = open("data/password.txt", "r").read()

def create_tag_tables():
    """Create MySQL table of tags"""
    table = (
        "CREATE TABLE `tags` ("
        "   `name` char(100) NOT NULL,"
        "   `owner` char(18) NOT NULL,"
        "   `content` LONGTEXT NOT NULL,"
        "PRIMARY KEY(`name`)"
        ") ENGINE=InnoDB")

    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    try:
        cursor.execute(table)
    except mysql.connector.Error as err:
        print(err.msg)

    table = (
        "CREATE TABLE `editing_tag` ("
        "   `owner` char(18) NOT NULL,"
        "   `name` char(100) NOT NULL,"
        "PRIMARY KEY(`owner`)"
        ") ENGINE=InnoDB")

    try:
        cursor.execute(table)
    except mysql.connector.Error as err:
        print(err.msg)
        
    table = (
        "CREATE TABLE `charts` ("
        "   `owner` char(18) NOT NULL,"
        "   `content` LONGTEXT NOT NULL,"
        "PRIMARY KEY(`owner`)"
        ") ENGINE=InnoDB")

    table = (
        "CREATE TABLE `ryms` ("
        "   `owner` char(18) NOT NULL,"
        "   `content` LONGTEXT NOT NULL,"
        "PRIMARY KEY(`owner`)"
        ") ENGINE=InnoDB")

    try:
        cursor.execute(table)
    except mysql.connector.Error as err:
        print(err.msg)

    cursor.close()
    cnx.close()

def get_tag_content(name):
    """Get tag content by tag name"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    name = name.replace("'", "\\'")
    get_tag_content = ("SELECT `content` FROM `tags` "
                    "WHERE `name` = '{}'".format(name))

    cursor.execute(get_tag_content)
    tag_content = None
    for item in cursor:
        tag_content = item[0]

    cursor.close()
    cnx.close()

    return tag_content
    
def get_chart_content(owner):
    """Get content by chart user"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    get_chart_content = ("SELECT `content` FROM `charts` "
                    "WHERE `owner` = '{}'".format(owner))

    cursor.execute(get_chart_content)
    chart_content = None
    for item in cursor:
        chart_content = item[0]

    cursor.close()
    cnx.close()

    return chart_content

def get_rym_content(owner):
    """Get content by chart user"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    get_rym_content = ("SELECT `content` FROM `ryms` "
                    "WHERE `owner` = '{}'".format(owner))

    cursor.execute(get_rym_content)
    rym_content = None
    for item in cursor:
        rym_content = item[0]

    cursor.close()
    cnx.close()

    return rym_content

def set_tag_content(owner, content):
    """Have owner change tag content"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    name = get_tag_editing(owner)
    
    name = name.replace("'", "\\'")
    content = content.replace("'", "\\'")
    set_tag = ("REPLACE INTO `tags` "
                "(`name`, `owner`, `content`) "
                "VALUES ('{}', '{}', '{}') ".format(name, owner, content))

    cursor.execute(set_tag)
    cnx.commit()

    cursor.close()
    cnx.close()

def set_chart_content(owner, content):
    """Have owner set chart"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    content = content.replace("'", "\\'")
    set_chart = ("REPLACE INTO `charts` "
                "(`owner`, `content`) "
                "VALUES ('{}', '{}') ".format(owner, content))

    cursor.execute(set_chart)
    cnx.commit()

    cursor.close()
    cnx.close()

def set_rym_content(owner, content):
    """Have owner set rym"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    content = content.replace("'", "\\'")
    set_rym = ("REPLACE INTO `ryms` "
                "(`owner`, `content`) "
                "VALUES ('{}', '{}') ".format(owner, content))

    cursor.execute(set_rym)
    cnx.commit()

    cursor.close()
    cnx.close()

def get_tag_owner(name):
    """Get tag owner by tag name"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    name = name.replace("'", "\\'")
    get_tag_owner = ("SELECT `owner` FROM `tags` "
                    "WHERE `name` = '{}'".format(name))

    cursor.execute(get_tag_owner)
    tag_owner = None
    for item in cursor:
        tag_owner = item[0]

    cursor.close()
    cnx.close()

    return tag_owner

def get_tag_editing(owner):
    """Get tag owner is currently editing"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    get_tag_editing = ("SELECT `name` FROM `editing_tag` "
                    "WHERE `owner` = '{}'".format(owner))

    cursor.execute(get_tag_editing)
    tag_editing = None
    for item in cursor:
        tag_editing = item[0]

    cursor.close()
    cnx.close()

    return tag_editing

def edit_tag(owner, name):
    """Have owner edit a different tag"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    name = name.replace("'", "\\'")
    edit_tag = ("REPLACE INTO `editing_tag` "
                "(`owner`, `name`) "
                "VALUES ('{}', '{}') ".format(owner, name))

    cursor.execute(edit_tag)
    cnx.commit()

    cursor.close()
    cnx.close()

def list_tags(owner):
    """List tags belonging to an owner"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    list_tags = ("SELECT `name` FROM `tags` "
                 "WHERE `owner` = '{}'".format(owner))

    cursor.execute(list_tags)
    tags = list()
    for (name,) in cursor:
        tags.append(name)

    cursor.close()
    cnx.close()

    return tags

def search_tags(name):
    """Search tags with certain names"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    name = name.replace("'", "\\'")
    search_tags = ("SELECT `name` FROM `tags` "
                    "WHERE `name` LIKE '%{}%'".format(name))

    cursor.execute(search_tags)
    tags = list()
    for (name,) in cursor:
        tags.append(name)

    cursor.close()
    cnx.close()

    return tags

def find_tag_owner(name):
    """Find owner of tag"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    name = name.replace("'", "\\'")
    find_owner = ("SELECT `owner` FROM `tags` "
                  "WHERE `name` = '{}'".format(name))

    cursor.execute(find_owner)
    owner = None
    for (o,) in cursor:
        owner = o

    cursor.close()
    cnx.close()

    return owner

def delete_tag(name):
    """Delete a tag from the table"""
    cnx = connect(user="root", database=DB_NAME, password=PASSWORD)
    cursor = cnx.cursor()

    name = name.replace("'", "\\'")
    delete_tag = ("DELETE FROM `tags` "
                  "WHERE `name` = '{}'".format(name))

    cursor.execute(delete_tag)
    cnx.commit()

    cursor.close()
    cnx.close()