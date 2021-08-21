import sqlite3

class sqlite_command:

    def __init__(self):
        sql_command = "CREATE TABLE IF NOT EXISTS `power_app_memory.db`"



import mysql.connector
class DbConnect:
    def __init__(self, host, username, password, *args):
        super(DbConnect, self).__init__(self, host, username, password)
        try:
            connector = mysql.connector.connect(host=host,user=username,passwd=password)
            cursor = connector.cursor()
            self.cursor = cursor
            self.connect = connector
            print("Login Success")
        except:
            print("error logging in")

    def menu_rank_checker(self, user_id):
        sql = "SELLECT `staff_rank` FROM `staff_info_db`.`staff_table` WHERE `staff_id = {user_id}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
