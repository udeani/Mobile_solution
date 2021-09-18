import sqlite3
from kivymd.toast import toast


class SqliteConnect:

    def __init__(self, username, password, **kwargs):

        self.connection = sqlite3.connect("Power_App_DB.db")
        self.cursor = self.connection.cursor()
        self.user_id = username
        self.password = password


    def menu_rank_checker(self):
        sql = "SELECT staff_rank FROM staff_table WHERE staff_id = '{}'".format(self.user_id)
        self.cursor.execute(sql)
        rank = self.cursor.fetchone()
        return rank

    def navigation_content(self):
        sql = "SELECT bu_name AS BU, staff_firstName, staff_lastName,su_name AS SU " \
              "FROM `bu_table` " \
              "INNER JOIN `su_table` ON `su_table`.`bu_id` = `bu_table`.bu_id " \
              "INNER JOIN `staff_table` ON `staff_table`.staff_su = `su_table`.su_id" \
              " WHERE staff_id = '{}'".format(self.user_id)

        self.cursor.execute(sql)
        nav_details = self.cursor.fetchone()

        if nav_details is None:
            sql = "SELECT bu_name AS BU, staff_firstName, staff_lastName " \
                  "FROM `bu_table` " \
                  "INNER JOIN `staff_table` ON `staff_table`.staff_bu = `bu_table`.bu_id" \
                  " WHERE staff_id = '{}'".format(self.user_id)

            self.cursor.execute(sql)
            nav_details = self.cursor.fetchone() + tuple(" ")

        return nav_details

    def last_payment(self, account_no):
        sql = """SELECT amount,
            DATE(date)
            FROM `{}`
            WHERE type = 'Payment' 
            ORDER BY `date` DESC
            LIMIT 1 """.format(account_no)

        self.cursor.execute(sql)
        self.last_payment_details = self.cursor.fetchone()
        return self.last_payment_details

    def meter_reading_dssList(self):
        sql = """
        SELECT dss_name, dss_id
        FROM `dss_info`
        WHERE staff_id = '{}'""".format(self.user_id)

        self.cursor.execute(sql)
        self.dss_list = {}
        # making a dict of the dss and their ID after fetching them
        for dss in self.cursor.fetchall():
            self.dss_list[dss[0]] = dss[1]
        return self.dss_list

    def meter_reading_items(self):
        sql = """SELECT customerAccNo,
            customerFirstName,
            customerLastName,
            x_customerGPSpoint,
            y_customerGPSpoint,
            customerDSS
            FROM `total_customer_table`
            WHERE customerMarketer = '{}' AND customerAccType = '{}' """.format(self.user_id, 2)

        self.cursor.execute(sql)
        self.meter_details = self.cursor.fetchall()
        return self.meter_details

    def readable_dss_filter(self, dss_ids):
        sql = """SELECT customerAccNo,
            customerFirstName,
            customerLastName,
            x_customerGPSpoint,
            y_customerGPSpoint,
            customerDSS
            FROM `total_customer_table`
            WHERE customerDSS = '{}' AND customerAccType = '{}' AND customerMarketer = '{}'""".format(dss_ids, 2, self.user_id)

        self.cursor.execute(sql)
        self.meter_details = self.cursor.fetchall()
        return self.meter_details

    def maintain_connection(self):
        pass

    def logout(self):
        self.connect.close()


