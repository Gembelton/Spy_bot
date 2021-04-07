import sqlite3, random
from sqlite3 import Error
from config import DIRECTORY_PATH

conn = sqlite3.connect(DIRECTORY_PATH + 'database/User_options.db')


def db_get_field(user_id, field_name: "Название поля"):
    query_string = ""
    if field_name == "cop":
        query_string = " SELECT count_of_players FROM User WHERE id='{0}'".format(user_id)

    elif field_name == "cop_FINAL":
        query_string = " SELECT count_of_players_FINAL FROM User WHERE id='{0}'".format(user_id)

    elif field_name == "delete_message_id":
        query_string = " SELECT delete_message_id FROM User WHERE id='{0}'".format(user_id)

    elif field_name == "spy_number":
        query_string = " SELECT spy_number FROM User WHERE id='{0}'".format(user_id)

    elif field_name == "location":
        query_string = " SELECT curent_location_number FROM User WHERE id='{0}'".format(user_id)

    elif field_name == "list_number":
        query_string = "SELECT curent_list_number FROM User WHERE id='{0}'".format(user_id)

    with conn:
        cur = conn.cursor()
        cur.execute(query_string)
        return cur.fetchone()[0]


def db_set_field(user_id, data, field_name: "Название поля"):
    query_string = ""
    if field_name == "cop":
        query_string = "UPDATE User SET count_of_players = '{0}' WHERE id = '{1}'".format(data, user_id)

    elif field_name == "list_number":
        query_string = "UPDATE User SET curent_list_number = '{0}' WHERE id = '{1}'".format(data, user_id)

    elif field_name == "delete_message_id":
        query_string = "UPDATE User SET delete_message_id = '{0}' WHERE id = '{1}'".format(data, user_id)

    elif field_name == "spy_number":
        query_string = "UPDATE User SET spy_number = '{0}' WHERE id = '{1}'".format(random.randint(1, int(data)),
                                                                                    user_id)
    elif field_name == "curent_tier":
        query_string = "UPDATE User SET curent_tier = '{0}' WHERE id = '{1}'".format(data, user_id)

    elif field_name == "cop_FINAL":
        query_string = "UPDATE User SET count_of_players_FINAL = '{0}' WHERE id = '{1}'".format(data, user_id)

    elif field_name == "location":
        query_string = "UPDATE User SET curent_location_number = '{0}' WHERE id = '{1}'".format(random.choice(data),
                                                                                                user_id)
    with conn:
        cur = conn.cursor()
        try:
            cur.execute(query_string)
            conn.commit()
        except Error:
            pass

def db_check_user_exist(user_id):
    with conn:
        cur = conn.cursor()
        cur.execute(" SELECT count(id) FROM User WHERE id='{0}'".format(user_id))

        # if the count is 1, then table exists
        if cur.fetchone()[0] == 1:
            return True


def db_check_jurnal_exist(user_id, location_number):
    with conn:
        cur = conn.cursor()
        cur.execute(" SELECT count(id) FROM Jurnal_of_disable"
                    " WHERE user_id='{0}' AND list_number='{1}' AND location_number='{2}' ".
                    format((user_id), db_get_field(user_id, "list_number"), location_number))

        # if the count is 1, then table exists
        if cur.fetchone()[0] == 1:
            return True


def db_delete_from_jurnal_one(user_id, location_number):
    with conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM Jurnal_of_disable WHERE user_id='{0}' AND list_number='{1}' AND location_number='{2}' ".
                    format((user_id), db_get_field(user_id, "list_number"), location_number))
            conn.commit()
        except Error:
            pass


def db_delete_from_jurnal_all(user_id):
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Jurnal_of_disable WHERE user_id='{0}' AND list_number='{1}' ".
                        format((user_id), db_get_field(user_id, "list_number")))
            conn.commit()
        except Error:
            pass


def db_set_all_jurnal(user_id):
    with conn:
        cur = conn.cursor()
        try:
            for i in range(30):
                cur.execute("INSERT INTO Jurnal_of_disable(user_id,list_number,location_number) VALUES({0},{1},{2})"
                            .format(user_id,
                                    db_get_field(user_id, "list_number"),
                                    i))
            conn.commit()
        except Error:
            pass


def db_check_curent_tier(user_id, tier_name):
    with conn:
        cur = conn.cursor()
        cur.execute(" SELECT curent_tier FROM User WHERE id='{0}'".format(user_id))
        if cur.fetchone()[0] == tier_name:
            return True


def db_get_all_disabled_from_jurnal(user_id):
    with conn:
        cur = conn.cursor()
        cur.execute(" SELECT location_number FROM Jurnal_of_disable"
                    " WHERE user_id='{0}' AND list_number='{1}'".
                    format((user_id), db_get_field(user_id, "list_number")))
        disabled_locations_list = []
        for line in cur.fetchall():
            disabled_locations_list.append(line[0])

        return disabled_locations_list


def db_decrease_CoP(user_id):
    count_of_players = db_get_field(user_id, "cop") - 1

    with conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE User SET count_of_players = '{0}' WHERE id = '{1}'".format(count_of_players, user_id))
            conn.commit()
            return count_of_players
        except Error:
            pass


def db_insert_user(user_id):
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO User(id,curent_list_number) VALUES({0},1)".format(user_id))
            conn.commit()
        except (sqlite3.IntegrityError):
            pass


def db_insert_jurnal_one(user_id, location_number):
    with conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Jurnal_of_disable(user_id,list_number,location_number) VALUES({0},{1},{2})"
                        .format(user_id,
                                db_get_field(user_id, "list_number"),
                                location_number))
            conn.commit()
        except (sqlite3.IntegrityError):
            pass




def db_clear_user_info(user_id):
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
