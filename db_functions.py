import sqlite3, random
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file, timeout=10)
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


def db_check_user_exist(user_id):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        cur.execute(" SELECT count(id) FROM User WHERE id='{0}'".format(user_id))

        # if the count is 1, then table exists
        if cur.fetchone()[0] == 1:
            return True


def db_check_jurnal_exist(user_id, location_number):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        cur.execute(" SELECT count(id) FROM Jurnal_of_disable"
                    " WHERE user_id='{0}' AND list_number='{1}' AND location_number='{2}' ".
                    format((user_id), db_get_current_list_number(user_id), location_number))

        # if the count is 1, then table exists
        if cur.fetchone()[0] == 1:
            return True


def db_delete_from_jurnal_one(user_id, location_number):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM Jurnal_of_disable WHERE user_id='{0}' AND list_number='{1}' AND location_number='{2}' ".
                format((user_id), db_get_current_list_number(user_id), location_number))
            conn.commit()
        except Error:
            pass


def db_delete_from_jurnal_all(user_id):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Jurnal_of_disable WHERE user_id='{0}' AND list_number='{1}' ".
                        format((user_id), db_get_current_list_number(user_id)))
            conn.commit()
        except Error:
            pass


def db_set_all_jurnal(user_id):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        try:
            for i in range(30):
                cur.execute("INSERT INTO Jurnal_of_disable(user_id,list_number,location_number) VALUES({0},{1},{2})"
                            .format(user_id,
                                    db_get_current_list_number(user_id),
                                    i ))
            conn.commit()
        except Error:
            pass


def db_get_current_list_number(user_id):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT curent_list_number FROM User WHERE id='{0}'".format(user_id))
        return cur.fetchone()[0]


def db_check_curent_tier(user_id, tier_name):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        cur.execute(" SELECT curent_tier FROM User WHERE id='{0}'".format(user_id))
        if cur.fetchone()[0] == tier_name:
            return True


def db_set_curent_CoP(user_id, count_of_players):
    """изменение кол-ва игроков"""
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE User SET count_of_players = '{0}' WHERE id = '{1}'".format(count_of_players, user_id))
            conn.commit()
        except Error:
            pass


def db_set_curent_list(user_id, number_of_list):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE User SET curent_list_number = '{0}' WHERE id = '{1}'".format(number_of_list, user_id))
            conn.commit()
        except Error:
            pass


def db_set_delete_message_id(user_id, message_id):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE User SET delete_message_id = '{0}' WHERE id = '{1}'".format(message_id, user_id))
            conn.commit()
        except Error:
            pass


def db_get_all_disabled_from_jurnal(user_id):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        cur.execute(" SELECT location_number FROM Jurnal_of_disable"
                    " WHERE user_id='{0}' AND list_number='{1}'".
                    format((user_id), db_get_current_list_number(user_id)))
        disabled_locations_list = []
        for line in cur.fetchall():
            disabled_locations_list.append(line[0])

        return disabled_locations_list


def db_get_CoP(user_id):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        cur.execute(" SELECT count_of_players FROM User WHERE id='{0}'".format(user_id))
        return cur.fetchone()[0]

def db_get_CoP_FINAL(user_id):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        cur.execute(" SELECT count_of_players_FINAL FROM User WHERE id='{0}'".format(user_id))
        return cur.fetchone()[0]


def db_get_message_id(user_id):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        cur.execute(" SELECT delete_message_id FROM User WHERE id='{0}'".format(user_id))
        return cur.fetchone()[0]


def db_get_spy_number(user_id):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        cur.execute(" SELECT spy_number FROM User WHERE id='{0}'".format(user_id))
        return cur.fetchone()[0]


def db_get_location(user_id):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        cur.execute(" SELECT curent_location_number FROM User WHERE id='{0}'".format(user_id))
        return cur.fetchone()[0]


def db_decrease_CoP(user_id):
    count_of_players = db_get_CoP(user_id) - 1
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE User SET count_of_players = '{0}' WHERE id = '{1}'".format(count_of_players, user_id))
            conn.commit()
            return count_of_players
        except Error:
            pass


def db_set_spy_number(user_id, count_of_players):
    """рандом шпиона в последовательности"""
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE User SET spy_number = '{0}' WHERE id = '{1}'"
                        .format(random.randint(1, int(count_of_players)), user_id))
            conn.commit()
        except Error:
            pass


def db_set_curent_tier(user_id, tier_name):
    """изменение текущего тира юзера"""
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE User SET curent_tier = '{0}' WHERE id = '{1}'".format(tier_name, user_id))
            conn.commit()
        except Error:
            pass


def db_set_COP_FINAL(user_id, cop_FINAL):
    """изменение текущего тира юзера"""
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE User SET count_of_players_FINAL = '{0}' WHERE id = '{1}'".format(cop_FINAL, user_id))
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
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO User(id,curent_list_number) VALUES({0},1)".format(user_id))
            conn.commit()
        except (sqlite3.IntegrityError):
            pass


def db_insert_jurnal_one(user_id, location_number):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Jurnal_of_disable(user_id,list_number,location_number) VALUES({0},{1},{2})"
                        .format(user_id,
                                db_get_current_list_number(user_id),
                                location_number))
            conn.commit()
        except (sqlite3.IntegrityError):
            pass


def db_set_location(user_id, list_of_access):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE User SET curent_location_number = '{0}' WHERE id = '{1}'"
                        .format(random.choice(list_of_access), user_id))
            conn.commit()
        except Error:
            pass


def db_clear_user_info(user_id):
    conn = sqlite3.connect('/home/Gembelton/Spy_bot/database/User_options.db')
    with conn:
        cur = conn.cursor()

        cur.execute("UPDATE User SET curent_tier = 'START' ,"
                    " count_of_players = NULL ,"
                    " curent_location_number = NULL ,"
                    " spy_number = NULL ,"
                    " delete_message_id = NULL,"
                    " count_of_players_FINAL = NULL WHERE id = '{0}'".format(user_id))
        conn.commit()



if __name__ == '__main__':
    # create a database connection
    db_clear_user_info(891898477)
