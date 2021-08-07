import mysql.connector


class DbConnect:
    def __init__(self, username, password):
        # super(DbConnect, self).__init__(self, username, password)
        try:
            connector = mysql.connector.connect(host="localhost", user=username, passwd=password)
            cursor = connector.cursor()
            self.cursor = cursor
            self.connect = connector
            print("Login Success")

            self.user_id = username
            self.password = password
        except:
            print("error logging in")

    def menu_rank_checker(self):
        sql = "SELECT staff_rank FROM `staff_info_db`.`staff_table` WHERE staff_id = {}".format(self.user_id)
        self.cursor.execute(sql)
        rank = self.cursor.fetchone()
        return rank

    def navigation_content(self):
        sql = "SELECT bu_name AS BU, staff_firstName, staff_lastName,su_name AS SU " \
              "FROM `bu_info_db`.`bu_table` " \
              "INNER JOIN `su_info_db`.`su_table` ON `su_table`.`bu_id` = `bu_table`.bu_id " \
              "INNER JOIN `staff_info_db`.`staff_table` ON `staff_table`.staff_su = `su_table`.su_id" \
              " WHERE staff_id = {}".format(self.user_id)

        self.cursor.execute(sql)
        nav_details = self.cursor.fetchone()

        if nav_details is None:
            sql = "SELECT bu_name AS BU, staff_firstName, staff_lastName " \
                  "FROM `bu_info_db`.`bu_table` " \
                  "INNER JOIN `staff_info_db`.`staff_table` ON `staff_table`.staff_bu = `bu_table`.bu_id" \
                  " WHERE staff_id = {}".format(self.user_id)

            self.cursor.execute(sql)
            nav_details = self.cursor.fetchone() + tuple(" ")

        return nav_details

    def meter_reading_items(self):
        sql = """SELECT customerAccNo,
            customerFirstName,
            customerLastName,
            ST_X(customerGPSpoint),
            ST_Y(customerGPSpoint)
            FROM `customers_general_info_db`.`total_customer_table`
            WHERE customerMarketer = '{}' AND customerAccType = {} """.format(self.user_id, 2)

        self.cursor.execute(sql)
        self.meter_details = self.cursor.fetchall()
        return self.meter_details

    def last_payment(self, account_no):
        sql = """SELECT amount,
            DATE(date)
            FROM `customers_info_db`.`{}`
            WHERE type = 'Payment' 
            ORDER BY `date` DESC
            LIMIT 1 """.format(account_no)

        self.cursor.execute(sql)
        self.last_payment_details = self.cursor.fetchone()
        return self.last_payment_details

    def meter_reading_dssList(self):
        sql = """
        SELECT dss_name
        FROM `dss_general_info_db`.`dss_info`
        WHERE staff_id = '{}'""".format(self.user_id)

        self.cursor.execute(sql)
        self.dss_list = []
        for dss in self.cursor.fetchall():
            for items in dss:
                self.dss_list.append(items)
        return self.dss_list

    def readable_dss_filter(self, dss_name):
        pass
        sql = """SELECT customerAccNo,
            customerFirstName,
            customerLastName,
            ST_X(customerGPSpoint),
            ST_Y(customerGPSpoint)
            FROM `customers_general_info_db`.`total_customer_table`
            WHERE customerMarketer = '{}' AND customerAccType = {} AND dss_id =  """.format(self.user_id, 2)

        self.cursor.execute(sql)
        self.meter_details = self.cursor.fetchall()
        return self.meter_details

    def maintain_connection(self):
        pass

    def logout(self):
        self.connect.close()