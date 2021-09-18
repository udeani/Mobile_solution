import certifi
import os

os.environ['SSL_CERT_FILE'] = certifi.where()

import math
from haversine import haversine, Unit
from kivymd.app import MDApp
# from kivy.core.window import Window
from kivy.metrics import Metrics
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, AnimationTransition, CardTransition, \
    NoTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.toast import toast
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.scatter import Scatter
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty, OptionProperty, \
    ObjectProperty
from kivy.storage.dictstore import DictStore
from kivy.animation import Animation
from kivymd.theming import ThemableBehavior
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput, TextInputCutCopyPaste
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.list import OneLineListItem
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from Power_App.Power_App_Query.db_connector import DbConnect
from Power_App.Power_App_Query.sqlite_db_con import SqliteConnect
from kivy.graphics.vertex_instructions import Line, Ellipse, Rectangle
from akivymd.uix.progresswidget import AKCircularProgress
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color
import datetime


class ScreenManager(ScreenManager):
    pass


class Login_screen(MDScreen):
    pass


class RM_menu(MDScreen):
    pass


class DBR_menu(MDScreen):
    pass


class Dialy_atten_menu(MDScreen):
    pass


class Enforcement_menu(MDScreen):
    pass


class Enumeration_menu(MDScreen):
    pass


class Grid_reading_menu(MDScreen):
    pass


class HR_mgt_menu(MDScreen):
    pass


class Meter_reading_screen(MDScreen):

    def clear_label(self, **kargs):
        if self.ids.meter_dss_selector.text:
            if len(self.ids.meter_dss_selector.text) >= 1:
                self.ids.faker1.text = ''
        else:
            self.ids.faker1.text = 'Search DSS name to change'


class Mobile_report_menu(MDScreen):
    pass


class Supervisor_menu(MDScreen):
    pass


class Trial_billing_menu(MDScreen):
    pass


class Menu_controller(MDScreen):
    pass


class Meter_read_per_acc(MDScreen):
    def clear_label(self, **kargs):
        if self.ids.reading_textbox.text:
            if len(self.ids.reading_textbox.text) >= 1:
                self.ids.faker1.text = ''
        else:
            self.ids.faker1.text = 'Enter Reading'


class Waiting_screen(MDScreen):
    pass


class Loading_widget():
    pass


class Customer_details(MDScreen):
    pass


class Power_App(MDApp):

    def __init__(self, **kwargs):
        super(Power_App, self).__init__(**kwargs)
        self.to_read_acc_no = ""
        self.to_read_acc_name = ""
        self.current_circular_progress = 0
        self.readable_acc_numbers = None
        self.dss_list = None
        self.dss_checkbox_filter = []
        self.dss_search_text_state = "Load All"
        self.items = "user logged in details"

    def build(self):
        # Window.size = (255, 529)  # delete later
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_hue = '900'
        self.theme_cls.primary_palette = 'BlueGray'
        # self.theme_cls.theme_text_color = 'Dark'

        # self.kv_file = Builder.load_file("Power_App_KVs/meter_reading_details.kv")

        self.dialog = None

    def on_start(self):
        self.root.ids.toolbar.title = 'Mobile App'
        self.anim_circle_deg = 3

    def login_animation(self, *args):
        widget = self.root.ids.screen_manager.get_screen('login_screen').ids.animation_label1
        widget1 = self.root.ids.screen_manager.get_screen('login_screen').ids.animation_text

        widget1.text = 'Logging in..'

        """
        with widget.canvas:
            Color(0, 1, 0, 1)
            Line(circle=(widget.x + 20, widget.center_y, 7, widget.circle_start, widget.circle_stop))
            
        """
        widget.circle_stop += self.anim_circle_deg

        if widget.circle_stop >= 360:
            self.anim_circle_deg *= -1
            widget.canvas.clear()
            widget.text = 'Loading..'
            widget.circle_stop = 0
            widget.circle_start = 0

        if widget.circle_stop <= 0:
            self.anim_circle_deg *= -1
            widget.canvas.clear()
            widget.text = 'Loading..'
            widget.circle_stop = 0
            widget.circle_start = 0

    def notification_toast(self, toast_msg, time):
        toast(toast_msg, time)

    def user_login(self, user_name, password):
        # animating the login delay...
        Clock.schedule_interval(self.login_animation, 1 / 60)
        fake_button = Button(text='', size=(12, 12))

        joan = Animation(size=(16, 16), duration=3)
        joan.start(fake_button)
        # creating connection and logging in..
        try:
            #self.user = DbConnect(user_name, password)
            self.user = SqliteConnect(user_name, password)
            # fetching the rank of the user to select the usefull menu
            for item in self.user.menu_rank_checker():

                # cancelling the login animation once the data has been fetched
                # Clock.unschedule(self.login_animation)
                if item == "Route Marshal":
                    self.change_screen(screen_name='menu selector', step=1, menu_screen='Route Martial Menu')

                elif item == "Service Manager":
                    self.change_screen(screen_name='menu selector', step=1, menu_screen='Supervisor Menu')

                elif item == "Human Resources":
                    self.change_screen(screen_name='menu selector', step=1, menu_screen='Supervisor Menu')

                elif item == "Data Analyst":
                    self.change_screen(screen_name='menu selector', step=1, menu_screen='Supervisor Menu')

                # fetching the navigation label item...
                self.items = self.user.navigation_content()
                self.root.ids.nav_user_name.text = f'{self.items[1]} {self.items[2][0]}.'
                self.root.ids.nav_user_bu.text = f'{self.items[0]} BU {self.items[3]}'
                self.root.ids.nav_date.text = str(datetime.datetime.now())
                self.root.ids["menu_selector"].ids["meter_reading"].ids['BU'].text = f'{self.items[0]}'

        except:
            toast("Error in connection or Login details", 1.1)

    def change_screen(self, screen_name, direction='left', step=None, menu_screen=None):

        """Dictionaries with screen names as keys and screen title for toolbar as value"""

        self.Screen_identifier = {'menu selector': 'Menu',
                                  'Route Martial Menu': 'Menu',
                                  'Supervisor Menu': 'Menu',
                                  'Meter Reading': 'Meter Reading',
                                  "Meter reading page": "Meter Reading",
                                  "HR page": "HR Menu"}
        if step == 1:  # for the main screen change from login to main menu
            screen = self.root.ids.screen_manager

            if direction == 'None':
                screen.transition = NoTransition()
                screen.current = screen_name

            else:
                screen.transition = SlideTransition(direction=direction)
                screen.current = screen_name

            step = 3
            # if screen_name == 'menu selector':
            self.root.ids.toolbar.title = 'Mobile App'

            # else:
            # self.root.ids.toolbar.title = 'Power App'
        elif step == 2:
            screen = self.root.ids.screen_manager.get_screen(
                'menu selector').ids.controller_scr  # defining the 2nd screen manager to change

            if direction == 'None':
                screen.transition = NoTransition()
                screen.current = screen_name

            else:
                screen.transition = SlideTransition(direction=direction)
                screen.current = screen_name

            # self.root.ids.toolbar.title = self.Screen_identifier[screen_name]

        if step == 3:
            screen = self.root.ids.screen_manager.get_screen(
                'menu selector').ids.controller_scr  # defining the 2nd screen manager to change

            if direction == 'None':
                screen.transition = NoTransition()
                screen.current = menu_screen

            else:
                screen.transition = SlideTransition(direction=direction)
                screen.current = menu_screen

            # self.root.ids.toolbar.title = self.Screen_identifier[screen_name]

    def work_offline(self, checkbox, value):
        if value:
            self.root.ids.screen_manager.get_screen('login_screen').ids.work_offline_label.text = 'Online Mode'
            # plus other sqlite functions
        else:
            self.root.ids.screen_manager.get_screen('login_screen').ids.work_offline_label.text = 'Offline Mode'
            # plus other sqlite functions

    def lightening_chooser(self, checkbox, value, *args):
        if value:
            self.root.ids.screen_manager.get_screen('login_screen').ids.dark_mode_label.text = 'Light Theme'
            self.theme_cls.theme_style = 'Light'
            self.theme_cls.primary_palette = 'BlueGray'
            self.theme_cls.theme_text_color = 'Dark'

        else:
            self.root.ids.screen_manager.get_screen('login_screen').ids.dark_mode_label.text = 'Dark Theme'
            self.theme_cls.theme_style = 'Dark'
            self.theme_cls.primary_palette = 'Amber'
            self.theme_cls.theme_text_color = 'Light'

    def meter_reading_menu_items(self):
        # self.meter_reading_clear_items()

        # resetting all object instance of this function before setting them up again
        try:
            self.meter_reading_clear_items()
        except:
            print("error clearing dic stores")
        meters_to_read = ""
        # for the meter to read progress widget control
        meter_progress_widget = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
            'Meter Reading').ids.meter_read_progress
        data_counter = 0
        data_counter1 = 0

        if self.dss_search_text_state == "Load All":

            self.current_percent = 0

            if not self.readable_acc_numbers:
                self.readable_meters = self.user.meter_reading_items()
                print(len(self.readable_meters))
                self.readable_acc_numbers = DictStore('accounts_unquoted')
                ''' the idea behind this 'if' statement is: setting the self.readable_acc_numbers to None at the main function
                    (ie the build level) and checking if its value is None here, which if true, by the idea of inheritance we change it to dict store
                    and carry it over without reading it from server again. iteration is needed at the background to check if the
                    file is complete or there have been changes.
                    '''
                print(f' empty dic count is {len(self.readable_acc_numbers)}')
                for row in self.readable_meters:
                    # def individual_meter_items():
                    acc_number = row[0]
                    first_name = row[1]
                    last_name = row[2]
                    x_coordinate = row[3]
                    y_coordinate = row[4]
                    customerDSS = row[5]
                    print(f'1st string {customerDSS}')
                    last_paid = self.user.last_payment(acc_number)
                    last_amount = last_paid[0]
                    last_date = last_paid[1]

                    display_name = first_name + " " + last_name

                    # assigning the individual meter items to a general dictionary:
                    self.readable_acc_numbers.put(acc_number, names=display_name, payments=[last_amount, last_date],
                                                  coordinates=[x_coordinate, y_coordinate], dss=customerDSS,
                                                  read_status=False, reading="")
                    print(f' self.readable meter 1st count is: {len(self.readable_acc_numbers.keys())}')
                    data_counter += 1
            else:
                print("readable meters intact, no re-download needed")

            if self.readable_acc_numbers:
                meter_progress_widget.max_percent = len(self.readable_acc_numbers.keys())
                print(meter_progress_widget.max_percent)
            else:
                meter_progress_widget.max_percent = 1

            print(self.readable_acc_numbers.keys())
            for accounts in self.readable_acc_numbers.keys():
                data_counter1 += 1

                meters_to_read = Builder.load_file('Power_App_KVs/meter_reading_details.kv')

                # def individual_meter_items():
                meters_to_read.id = accounts
                meters_to_read.name = str(accounts)
                meters_to_read.x_coordinate = self.readable_acc_numbers[accounts]['coordinates'][0]
                meters_to_read.y_coordinate = self.readable_acc_numbers[accounts]['coordinates'][1]
                meters_to_read.read_status = self.readable_acc_numbers[accounts]['read_status']
                meters_to_read.ids.acc_number.text = str(accounts)
                meters_to_read.ids.names.text = str(self.readable_acc_numbers[accounts]['names'])
                meters_to_read.ids.payment_details.text = "Last Paid: [color=ff0000]{}[/color] | {}".format(
                    str(self.readable_acc_numbers[accounts]['payments'][0]),
                    str(self.readable_acc_numbers[accounts]['payments'][1]))

                # testing if any account have been read before
                if self.readable_acc_numbers[int(accounts)]['read_status'] is True:
                    self.current_percent += 1
                else:
                    print(self.readable_acc_numbers[int(accounts)]['read_status'])
                meter_progress_widget.current_percent = self.current_percent

                widget = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
                    'Meter Reading').ids.meter_read_grid

                widget.add_widget(meters_to_read)
                widget2 = self.root.ids["menu_selector"].ids["meter_reading"]
                widget2.ids[f"{accounts}"] = meters_to_read
                print(meters_to_read.id)
            print(f'data counter 1: {data_counter}. data counter 2: {data_counter1}')

        elif self.dss_search_text_state == "Filter":

            self.current_percent = 0

            if not self.readable_acc_numbers:
                print(self.dss_checkbox_filter)

                self.filter_readable_acc_numbers = DictStore('account_2nd')
                ''' the idea behind this 'if' statement is: setting the self.readable_acc_numbers to None at the main function
                    (ie the build level) and checking if its value is None here, which if true, by the idea of inheritance we change it to dict store
                    and carry it over without reading it from server again. iteration is needed at the background to check if the
                    file is complete or there have been changes.
                    '''

                for dss_ids in self.dss_checkbox_filter:

                    self.filter_readable_meters = self.user.readable_dss_filter(dss_ids)

                    for row in self.filter_readable_meters:
                        # def individual_meter_items():
                        acc_number = row[0]
                        first_name = row[1]
                        last_name = row[2]
                        x_coordinate = row[3]
                        y_coordinate = row[4]
                        customerDSS = row[5]
                        print(f'2nd string {customerDSS}')
                        last_paid = self.user.last_payment(acc_number)
                        last_amount = last_paid[0]
                        last_date = last_paid[1]
                        data_counter += 1
                        display_name = first_name + " " + last_name

                        # assigning the individual meter items to a general dictionary:
                        self.filter_readable_acc_numbers.put(acc_number, names=display_name,
                                                             payments=[last_amount, last_date],
                                                             coordinates=[x_coordinate, y_coordinate], dss=customerDSS,
                                                             read_status=False, reading="")
            else:
                self.filter_readable_acc_numbers = DictStore('account_3rd')
                ''' the idea behind this 'if' statement is: setting the self.readable_acc_numbers to None at the main function
                    (ie the build level) and checking if its value is None here, which if true, by the idea of inheritance we change it to dict store
                    and carry it over without reading it from server again. iteration is needed at the background to check if the
                    file is complete or there have been changes.
                    '''
                for account in self.readable_acc_numbers.keys():
                    if self.readable_acc_numbers[account]["dss"] in self.dss_checkbox_filter:
                        data_counter += 1
                        acc_number = account
                        x_coordinate = self.readable_acc_numbers[account]["coordinates"][0]
                        y_coordinate = self.readable_acc_numbers[account]["coordinates"][1]
                        customerDSS = self.readable_acc_numbers[account]["dss"]
                        print(f' 3rd string {self.readable_acc_numbers[account]["dss"]}')
                        last_amount = self.readable_acc_numbers[account]["payments"][0]
                        last_date = self.readable_acc_numbers[account]["payments"][1]

                        display_name = self.readable_acc_numbers[account]["names"]

                        # assigning the individual meter items to a general dictionary:
                        self.filter_readable_acc_numbers.put(acc_number, names=display_name,
                                                             payments=[last_amount, last_date],
                                                             coordinates=[x_coordinate, y_coordinate],
                                                             dss=customerDSS,
                                                             read_status=False, reading="")

            if self.filter_readable_acc_numbers:
                meter_progress_widget.max_percent = len(self.filter_readable_acc_numbers.keys())
                print(meter_progress_widget.max_percent)
            else:
                meter_progress_widget.max_percent = 1

            # since the akcircularprogress bar has refused to auto update at entry, i decided to add it manually through
            # python

            # print (f'second level {len(self.filter_readable_acc_numbers.keys())}')
            for accounts in self.filter_readable_acc_numbers.keys():
                # print(self.filter_readable_acc_numbers[accounts]['dss'])
                meters_to_read = Builder.load_file('Power_App_KVs/meter_reading_details.kv')

                # def individual_meter_items():
                meters_to_read.id = accounts
                meters_to_read.name = str(accounts)
                meters_to_read.x_coordinate = self.filter_readable_acc_numbers[accounts]['coordinates'][0]
                meters_to_read.y_coordinate = self.filter_readable_acc_numbers[accounts]['coordinates'][1]
                meters_to_read.read_status = self.filter_readable_acc_numbers[accounts]['read_status']
                meters_to_read.ids.acc_number.text = str(accounts)
                meters_to_read.ids.names.text = str(self.filter_readable_acc_numbers[accounts]['names'])
                meters_to_read.ids.payment_details.text = "Last Paid: [color=ff0000]{}[/color] | {}".format(
                    str(self.filter_readable_acc_numbers[accounts]['payments'][0]),
                    str(self.filter_readable_acc_numbers[accounts]['payments'][1]))
                # data_counter1 += 1
                # testing if any account have been read before
                if self.filter_readable_acc_numbers[int(accounts)]['read_status'] is True:
                    self.current_percent += 1
                else:
                    print(self.filter_readable_acc_numbers[int(accounts)]['read_status'])
                meter_progress_widget.current_percent = self.current_percent

                widget = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
                    'Meter Reading').ids.meter_read_grid
                # widget.height = self.widget_sizer(id="meter_to_read_height", parent_height=self.parent.height, child_number=len(self.children))
                widget.add_widget(meters_to_read)
                widget2 = self.root.ids["menu_selector"].ids["meter_reading"]
                widget2.ids[f"{accounts}"] = meters_to_read

            print(f'data counter 1: {data_counter}. data counter 2: {data_counter1}')

    def meter_reading_filter(self, dss_id):
        # resetting all object instance of this function before setting them up again
        try:
            self.meter_reading_clear_items()
        except:
            print("error clearing dic stores")
        meters_to_read = ""
        # for the meter to read progress widget control
        meter_progress_widget = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
            'Meter Reading').ids.meter_read_progress

        self.current_percent = 0

        if not self.readable_acc_numbers:

            self.filter_readable_acc_numbers = DictStore('account_2nd')
            ''' the idea behind this 'if' statement is: setting the self.readable_acc_numbers to None at the main function
                (ie the build level) and checking if its value is None here, which if true, by the idea of inheritance we change it to dict store
                and carry it over without reading it from server again. iteration is needed at the background to check if the
                file is complete or there have been changes.
                '''

            self.filter_readable_meters = self.user.readable_dss_filter(dss_id)

            for row in self.filter_readable_meters:
                # def individual_meter_items():
                acc_number = row[0]
                first_name = row[1]
                last_name = row[2]
                x_coordinate = row[3]
                y_coordinate = row[4]
                customerDSS = row[5]
                print(f'2nd string {customerDSS}')
                last_paid = self.user.last_payment(acc_number)
                last_amount = last_paid[0]
                last_date = last_paid[1]
                display_name = first_name + " " + last_name

                # assigning the individual meter items to a general dictionary:
                self.filter_readable_acc_numbers.put(acc_number, names=display_name,
                                                     payments=[last_amount, last_date],
                                                     coordinates=[x_coordinate, y_coordinate], dss=customerDSS,
                                                     read_status=False, reading="")
        else:
            self.filter_readable_acc_numbers = DictStore('account_4rd')
            ''' the idea behind this 'if' statement is: setting the self.readable_acc_numbers to None at the main function
                (ie the build level) and checking if its value is None here, which if true, by the idea of inheritance we change it to dict store
                and carry it over without reading it from server again. iteration is needed at the background to check if the
                file is complete or there have been changes.
                '''
            for account in self.readable_acc_numbers.keys():
                if self.readable_acc_numbers[account]["dss"] == dss_id:
                    acc_number = account
                    x_coordinate = self.readable_acc_numbers[account]["coordinates"][0]
                    y_coordinate = self.readable_acc_numbers[account]["coordinates"][1]
                    customerDSS = self.readable_acc_numbers[account]["dss"]
                    print(f' 3rd string {self.readable_acc_numbers[account]["dss"]}')
                    last_amount = self.readable_acc_numbers[account]["payments"][0]
                    last_date = self.readable_acc_numbers[account]["payments"][1]

                    display_name = self.readable_acc_numbers[account]["names"]

                    # assigning the individual meter items to a general dictionary:
                    self.filter_readable_acc_numbers.put(acc_number, names=display_name,
                                                         payments=[last_amount, last_date],
                                                         coordinates=[x_coordinate, y_coordinate],
                                                         dss=customerDSS,
                                                         read_status=False, reading="")

            if self.filter_readable_acc_numbers:
                meter_progress_widget.max_percent = len(self.filter_readable_acc_numbers.keys())
                print(meter_progress_widget.max_percent)
            else:
                meter_progress_widget.max_percent = 1

            # since the akcircularprogress bar has refused to auto update at entry, i decided to add it manually through
            # python

        for accounts in self.filter_readable_acc_numbers.keys():
            meters_to_read = Builder.load_file('Power_App_KVs/meter_reading_details.kv')

            # def individual_meter_items():
            meters_to_read.id = accounts
            meters_to_read.name = str(accounts)
            meters_to_read.x_coordinate = self.filter_readable_acc_numbers[accounts]['coordinates'][0]
            meters_to_read.y_coordinate = self.filter_readable_acc_numbers[accounts]['coordinates'][1]
            meters_to_read.read_status = self.filter_readable_acc_numbers[accounts]['read_status']
            meters_to_read.ids.acc_number.text = str(accounts)
            meters_to_read.ids.names.text = str(self.filter_readable_acc_numbers[accounts]['names'])
            meters_to_read.ids.payment_details.text = "Last Paid: [color=ff0000]{}[/color] | {}".format(
                str(self.filter_readable_acc_numbers[accounts]['payments'][0]),
                str(self.filter_readable_acc_numbers[accounts]['payments'][1]))

            # testing if any account have been read before
            if self.filter_readable_acc_numbers[int(accounts)]['read_status'] is True:
                self.current_percent += 1
            else:
                print(self.filter_readable_acc_numbers[int(accounts)]['read_status'])
            meter_progress_widget.current_percent = self.current_percent

            widget = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
                'Meter Reading').ids.meter_read_grid

            widget.add_widget(meters_to_read)
            widget2 = self.root.ids["menu_selector"].ids["meter_reading"]
            widget2.ids[f"{accounts}"] = meters_to_read

    def red_meter(self, red_acc_number, red_acc_name):

        self.to_read_acc_no = red_acc_number
        self.to_read_acc_name = red_acc_name

        widget = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
            'Meter reading page').ids
        widget.acc_no_to_read.text = self.to_read_acc_no
        widget.acc_name_o_read.text = self.to_read_acc_name

        self.change_screen('Meter reading page', step=2)

    def save_reading(self, reading):
        if reading == "":
            self.notification_toast("Enter reading to save", 1)
        else:
            meter_progress = self.root.ids.screen_manager.get_screen(
                'menu selector').ids.controller_scr.get_screen(
                'Meter Reading').ids.meter_read_progress

            try:
                red = float(reading)
                self.readable_acc_numbers[int(self.to_read_acc_no)]['reading'] = red
                self.readable_acc_numbers[int(self.to_read_acc_no)]['read_status'] = True
                self.notification_toast("Saved", 1)
                # print(self.root.ids["menu_selector"].ids["meter_reading"].ids['1064432229'])#.ids.keys())
                self.change_screen('Meter Reading', step=2)

                meter_progress_widget = \
                    self.root.ids["menu_selector"].ids["meter_reading"].ids[f'{self.to_read_acc_no}'].ids[
                        'main_template_background']

                meter_progress_widget.md_bg_color = [0, .9, 0, 1]
                self.current_percent += 1
                meter_progress.current_percent = self.current_percent
            except TypeError:
                red = float(reading)
                self.filter_readable_acc_numbers[int(self.to_read_acc_no)]['reading'] = red
                self.filter_readable_acc_numbers[int(self.to_read_acc_no)]['read_status'] = True
                self.notification_toast("Saved", 1)
                self.change_screen('Meter Reading', step=2)

                meter_progress_widget = \
                    self.root.ids["menu_selector"].ids["meter_reading"].ids[f'{self.to_read_acc_no}'].ids[
                        'main_template_background']
                meter_progress_widget.md_bg_color = [0, .9, 0, 1]
                self.current_percent += 1
                meter_progress.current_percent = self.current_percent
            except:
                self.notification_toast("Special character detected, check reading", 1.1)

    def meter_reading_clear_items(self):
        widget = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
            'Meter Reading').ids.meter_read_grid
        widget.clear_widgets()

        self.filter_readable_acc_numbers.clear()
        self.readable_acc_numbers.clear()

        widget2 = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
            'Meter Reading').ids.progress_bar_main_layout
        # widget2.clear_widgets()

    def meter_proximity_calc(self, x_coordinate, y_coordinate, *args):

        # making a list(Dic) to store all the index of the children widget
        meter_proximity = DictStore("meter_and_distance")
        sort_list = []
        widget = self.root.ids["menu_selector"].ids["meter_reading"].ids['meter_read_grid']

        try:
            for items in widget.children:
                Q1 = float(items.x_coordinate)
                P1 = float(items.y_coordinate)
                Q2 = float(x_coordinate)
                P2 = float(y_coordinate)
                my_loc = (Q2, P2)
                acc_loc = (Q1, P1)

                d = haversine(my_loc, acc_loc, unit=Unit.METERS)
                # Qc = Q2 - Q1
                # PhiC = P2 - P1
                # a = (math.sin(Qc / 2) ** 2) + math.cos(Q1) * math.cos(Q2) * (math.sin(PhiC / 2) ** 2)
                # c = 2 * (math.atan2(math.sqrt(a), math.sqrt(1 - a)))
                # d = 6371e3 * c

                # appending the calculated distance to the dict
                meter_proximity.put(items.id, distance=d)

                self.root.ids["menu_selector"].ids["meter_reading"].ids[f'{items.id}'].ids[
                    'distance_label'].text = f'{d} m'

            # sorting the distances into an ordered list
            for keys in meter_proximity.keys():
                sort_list.append(meter_proximity[keys]['distance'])
            sorted_list = sorted(sort_list)

            # getting the coordinates of widget children in meter reading grid
            widget = self.root.ids["menu_selector"].ids["meter_reading"].ids['meter_read_grid']
            y_widget_pos = []
            x_widget_pos = []
            for widgets in widget.children:
                y_widget_pos.append(widgets.pos[1])
                # sorting in ascending order and reversing the y coordinates
                y_widget_pos = sorted(y_widget_pos)
                y_widget_pos_rev = (y_widget_pos[::-1])

                x_widget_pos.append(widgets.pos[0])

            # finding the widget_id(from the dictionary) that has the closest distance from the sorted list
            i = 0
            for keys in widget.children:
                for key, value in meter_proximity.find(distance=sorted_list[i]):
                    print(key, value)
                    self.root.ids["menu_selector"].ids["meter_reading"].ids[f'{key}'].pos = [x_widget_pos[i],
                                                                                             y_widget_pos_rev[i]]
                    i += 1
            for items in widget.children:
                print(items.id,
                      self.root.ids["menu_selector"].ids["meter_reading"].ids[f'{items.id}'].ids['distance_label'].text,
                      items.pos)
            y_widget_pos = None
            x_widget_pos = None
            y_widget_pos_rev = None
            meter_proximity.clear()
        except:
            pass

    def set_toolbar_font_size(self, *args):
        self.root.ids.toolbar.font_size = '15sp'

    def user_details(self):
        pass

    def go_to_home(self):
        pass

    def nothing(self):
        pass

    def manual_meter_reading_1(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Address:",
                type="confirmation",
                size_hint=(1, 1),
                buttons=[MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color),
                         MDFlatButton(text="OK", text_color=self.theme_cls.primary_color), ], )
        self.dialog.open()

    def manual_meter_reading(self):
        toast("Uploading", 1.2)

    def manual_popup(self):
        MDCard

    def filter_button_label(self, **kwargs):
        self.dss_search_text_state = "Load All"
        self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
            "Meter Reading").ids.filter_button.text = self.dss_search_text_state

    def transformer_selector_1(self, dss_text=""):

        layout_counter = 0
        self.dss_checkbox_filter = []

        # the below func is trying to calculate the height for the child widgets for the dss list
        def height_resolver(children, step):
            if step == 0:
                if children is 0 or None:
                    box_layout.height = 0
                    return box_layout.height
                else:
                    box_layout.height = children * 24
                    return box_layout.height
            elif step == 1:
                if 13 < children < 20:
                    return (children / 2) * 24
                elif children < 13:
                    return children * 24
                else:
                    return (children / 3) * 24

        if not self.dss_list:
            self.dss_list = self.user.meter_reading_dssList()

        root_layout = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
            "Meter Reading").ids.dss_scrollview
        width_calc = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
            "Meter Reading").ids.meter_dss_selector
        box_layout = MDGridLayout(rows=1,
                                  size_hint=[None, None], height=0, width=width_calc.width, md_bg_color=[1, 1, 1, .9])

        scroll_view = ScrollView(do_scroll_y=True, size_hint=[None, None], size=box_layout.size)
        # scroll_view.bind(on_touch_up=self.filter_button_label)

        scatter_layout = Scatter(center=width_calc.center,
                                 x=width_calc.x, y=width_calc.y - scroll_view.height,
                                 size_hint=[None, None], size=scroll_view.size)

        # clearing any widget at the mdgridlayout before adding another
        root_layout.clear_widgets()

        def printer(label, *args):
            self.notification_toast(f'{label.dss_id} selected', 0.4)
            self.meter_reading_filter(label.dss_id)

        def dss_checkbox_monitor(label, value, *args):
            self.notification_toast(f'{label.dss_id} selected', 0.4)
            print(label.state)

            if value:
                self.dss_checkbox_filter.append(label.dss_id)
                print(f'{label.dss_id} is active and added')
                print(self.dss_checkbox_filter)

                self.dss_search_text_state = "Filter"

            else:
                self.dss_checkbox_filter.remove(label.dss_id)
                print(f'{label.dss_id} is inactive and deleted')

                if len(self.dss_checkbox_filter) == 0:
                    self.dss_search_text_state = "Load All"

                else:
                    pass
            self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
                "Meter Reading").ids.filter_button.text = self.dss_search_text_state

        dss = ""  # this is a fake string, created so as to avoid error while creating the class dss_label

        # dss_label = Label(text=f'{dss}', font_size="11dp", size_hint=(1, None), height="16dp")
        # dss_label.bind(on_press=printer)

        class dss_label(Button):
            def __init__(self, dss_id, **kwargs):
                super(dss_label, self).__init__(**kwargs)
                self.text = dss
                self.dss_id = dss_id
                self.background_normal = ''
                self.background_color = [1, 1, 1, 0]
                self.color = [0, 0, 0, 1]
                self.size_hint = (.9, None)
                self.height = "24dp"
                self.font_size = "11dp"
                self.bind(on_press=printer)

        class dss_filter_check(MDCheckbox):
            def __init__(self, dss_id, **kwargs):
                super(dss_filter_check, self).__init__(**kwargs)
                self.dss_id = dss_id
                self.bind(active=dss_checkbox_monitor)
                self.size_hint = (.1, None)
                self.height = "24dp"

        for dss in self.dss_list:

            if dss_text == "" or None:
                dss_label.text = dss
                box_layout.add_widget(dss_label(dss_id=self.dss_list[dss]))
                box_layout.add_widget(dss_filter_check(dss_id=self.dss_list[dss]))
                layout_counter += 1

            elif dss_text is "clear_widgets":
                root_layout.clear_widgets()

            else:
                if dss_text.lower() in dss.lower():
                    dss_label.text = dss
                    box_layout.add_widget(dss_label(dss_id=self.dss_list[dss]))
                    box_layout.add_widget(dss_filter_check(dss_id=self.dss_list[dss]))
                    layout_counter += 1

                else:
                    pass

        # self.notification_toast(f"{layout_counter} DSS displayed", .2)

        box_layout.height = height_resolver(layout_counter, step=0)
        box_layout.rows = layout_counter
        box_layout.width = width_calc.width

        scroll_view.height = height_resolver(layout_counter, step=1)

        # adding a line effect at the border of the scroll view
        with scroll_view.canvas.after:
            Color(0, .7, 0, .6)
            Line(points=(scroll_view.x, scroll_view.y + scroll_view.height,
                         scroll_view.x, scroll_view.y,
                         scroll_view.x + scroll_view.width, scroll_view.y,
                         scroll_view.x + scroll_view.width, scroll_view.y + scroll_view.height))

        # Updating all the layouts to affect the calculated change
        scatter_layout.x = root_layout.x
        scatter_layout.y = width_calc.y - scroll_view.height
        scatter_layout.size = scroll_view.size

        scroll_view.add_widget(box_layout)
        scatter_layout.add_widget(scroll_view)
        root_layout.add_widget(scatter_layout)

    def clear_screen(self, coordinates):
        pass

    def widget_sizer(self, id="", parent_width=0, parent_height=0, child_number=0):
        if id == "meter_to_read_height":
            try:
                "changing/determining the size of the scroll_view of meter_mgt_menu page from the number of children"
                meter_grid_height = (parent_height * 0.2) * child_number
                return meter_grid_height
            except:
                print(f"an error occurred at the widget sizer line 6 above")

        if id == "main_menu":
            """for Rm menu:
            The grid or list column for the menu has to be either 2 if x is greater than y, or
             5 if x is less than y """
            if parent_width <= parent_height:
                return 2
            else:
                return 5

        if id == "main_menu_padding":
            """ for RM menu:
            To determine the MDcard padding, compare the parent width and height,
                if x is greater, then the padding will be the remainder of the parent width divided by 2"""
            if parent_width <= parent_height:
                width = divmod(parent_width, 2)
                return width[1] / 2
            else:
                width = divmod(parent_width, 2)
                return width[1] / 2

        if id == "general_mdcard":
            """ for Power_App.kv:
            To determine the MDcard width, compare the parent width and height,
                if x is greater, then the width will be parent width divided by 2 minus the remainder for padding """
            if parent_width <= parent_height:
                width = divmod(parent_width, 2)
                return width[0] - width[1]  # Notice: when the remainder is large, the wudth becomes too little
            else:
                width = divmod(parent_width, 5)
                return width[0] - width[1]
        if id == "login_misc":
            """for Login.kv"""
            if parent_width <= parent_height:
                return 2
            else:
                return 1

    def check_all_action(self):
        pass


Power_App().run()
