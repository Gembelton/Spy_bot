import sqlite3,random
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file,timeout=10)
    except Error as e:
        print(e)

    return conn


def db_select_all_users(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM User")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def db_check_user_exist(curent_id):
    conn = create_connection(r"database\User_options.db")
    with conn:
        cur = conn.cursor()
        cur.execute(" SELECT count(id) FROM User WHERE id='{0}'".format(curent_id))

        # if the count is 1, then table exists
        if cur.fetchone()[0] == 1:
            return True

def db_check_curent_tier(curent_id,tier_name):
    conn = create_connection(r"database\User_options.db")
    with conn:
        cur = conn.cursor()
        cur.execute(" SELECT curent_tier FROM User WHERE id='{0}'".format(curent_id))
        if cur.fetchone()[0] == tier_name:
            return True


def db_change_curent_CoP(user_id,count_of_players):
    """изменение кол-ва игроков"""
    conn = create_connection(r"database\User_options.db")
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE User SET count_of_players = '{0}' WHERE id = '{1}'".format(count_of_players, user_id))
            conn.commit()
        except Error:
            pass

def db_change_spy_number(user_id,count_of_players):
    """рандом шпиона в последовательности"""
    conn = create_connection(r"database\User_options.db")
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE User SET spy_number = '{0}' WHERE id = '{1}'"
                        .format(random.randint(3,int(count_of_players)), user_id))
            conn.commit()
        except Error:
            pass

def db_change_curent_tier(user_id,tier_name):
    """изменение текущего тира юзера"""
    conn = create_connection(r"database\User_options.db")
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE User SET curent_tier = '{0}' WHERE id = '{1}'".format(tier_name,user_id))
            conn.commit()
        except Error:
            pass

def db_insert_user(user_id):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    conn = create_connection(r"database\User_options.db")
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO User(id,curent_list_number) VALUES({0},1)".format(user_id))
            conn.commit()
        except (sqlite3.IntegrityError):
            pass



if __name__ == '__main__':
    # create a database connection

    #db_change_curent_tier(1113,"rfl")
    print(db_check_curent_tier(1111,"rfdl"))