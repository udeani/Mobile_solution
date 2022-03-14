import math
from haversine import haversine, Unit
import io
import os
from plyer import camera, filechooser, gps, storagepath

from kivymd.app import MDApp
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.toast import toast
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import OneLineListItem
from kivymd.theming import ThemableBehavior
from kivymd.uix.textfield import MDTextField
from kivy.metrics import Metrics
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty, OptionProperty, \
    ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, AnimationTransition, CardTransition, \
    NoTransition
from kivy.storage.dictstore import DictStore
from kivy.animation import Animation
from kivy.graphics.vertex_instructions import Line, Ellipse, Rectangle, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color
from kivy.lang import Builder
from kivy.uix.image import Image, AsyncImage
from kivy.uix.textinput import TextInput, TextInputCutCopyPaste
from kivy.uix.button import Button
from kivy.utils import platform
from kivy.uix.filechooser import FileChooserListView
from kivy.core.camera import Camera
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label
from kivy.clock import Clock

from akivymd.uix.progresswidget import AKCircularProgress
# from Power_App.Power_App_Query.db_connector import DbConnect
# from Power_App.Power_App_Query.sqlite_db_con import SqliteConnect
from menu_o import MenuOptions
from sqlite_db_con import SqliteConnect
from sqlite_inmemory import meter_reading_inMemory
from login_anim import login_anim
#from progress_line import widget_class
from animations import AnimationClass


# import datetime


class Power_App(MDApp):
    sp_size = NumericProperty(10)
    user = None
    to_read_acc_no = None
    to_read_acc_name = None

    # root = ObjectProperty()

    def __init__(self, **kwargs):
        super(Power_App, self).__init__(**kwargs)
        self.items = "user logged in details"

        if platform is not "android":
            Window.size = [324, 679]  # (255, 529)  # delete later

        elif platform == "android":
            import certifi
            import android
            os.environ['SSL_CERT_FILE'] = certifi.where()

            from android.permissions import request_permissions, Permission

            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE],
                                Permission.CAMERA)
            # for gps permission and callback
            request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION])
            # android.map_key(android.KEYCODE_BACK, 1001)

            Window.softinput_mode = 'below_target'

        Window.bind(on_keyboard=self.onBackBtn)

    def build(self):

        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_hue = '900'
        self.theme_cls.primary_palette = 'BlueGray'
        # self.theme_cls.theme_text_color = 'Dark'
        self.dialog = None

    def onBackBtn(self, window, key, keyboard, keycode, keycode1, *args):
        """ To be called whenever user presses Back/Esc Key """
        # If user presses Back/Esc Key
        if key in [27, 1001]:
            # Do whatever you need to do, like check if there are any
            # screens that you can go back to.
            # return True if you don't want to close app
            # return False if you do
            print("back btn pressed")
            toast("Back Button coming soon", .8)
            return True

    def on_start(self):
        # self.root.ids.toolbar.title = 'Mobile App'
        self.anim_circle_deg = 3

    def login_animation(self, *args):
        widget = self.root.ids.screen_manager.get_screen('login_screen').ids.animation_label1
        widget1 = self.root.ids.screen_manager.get_screen('login_screen').ids.animation_text

        widget1.text = 'Logging in..'

        with widget.canvas:
            Color(0, 1, 0, 1)
            Line(circle=(widget.x + 20, widget.center_y, 7, widget.circle_start, widget.circle_stop))

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

    def notification_toast(toast_msg, time):
        toast(toast_msg, time)

    def toast(self, text, time):
        toast(text, time)

    def user_login(self, user_name, password):
        # animating the login delay...
        """        #Clock.schedule_interval(self.login_animation, 1 / 60)

                fake_button = Button(text='', size=(12, 12))

                joan = Animation(size=(16, 16), duration=3, t='out_quad')
                joan.repeat = True
                joan.start(fake_button)
        """
        # creating connection and logging in..
        try:
            # self.user = DbConnect(user_name, password)
            Power_App.user = SqliteConnect(user_name, password)
            # fetching the rank of the user to select the useful menu
            for item in Power_App.user.menu_rank_checker():
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
                self.items = Power_App.user.navigation_content()
                self.root.ids.nav_user_name.text = f'{self.items[1]} {self.items[2][0]}.'
                self.root.ids.nav_user_bu.text = f'{self.items[0]} BU {self.items[3]}'
                # self.root.ids.nav_date.text = str(datetime.datetime.now()) self.root.ids["menu_selector"].ids[
                # "meter_reading"].ids['BU'].text = f'{self.items[0]}' used to display the staff bu at the meter
                # reading page:: depreciated

        except:
            toast("Error in connection or Login details", 1.1)

            connector = self.root.ids.screen_manager.get_screen('login_screen')
            for items in connector.ids.login_float_layout.children:
                if items.opacity is not 0:
                    # connector.ids.login_float_layout.remove_widget(items)
                    items.active = False
                else:
                    items.opacity = 100
                    items.active = True

    def change_screen(self, screen_name, direction='left', step=None, menu_screen=None, *args):

        """Dictionaries with screen names as keys and screen title for toolbar as value"""

        self.Screen_identifier = {'menu selector': 'Menu',
                                  'Route Martial Menu': 'Menu',
                                  'Supervisor Menu': 'Menu',
                                  'Meter Reading': 'Meter Reading',
                                  "Meter reading page": "Meter Reading",
                                  "HR page": "HR Menu"}
        if step == 1:
            # for the main screen change from login to main menu
            screen = self.root.ids.screen_manager

            if direction == 'None':
                screen.transition = NoTransition()
                screen.current = screen_name

            else:
                screen.transition = SlideTransition(direction=direction)
                screen.current = screen_name

            step = 3
            # setting it to step 3 above makes this function to enter the second phase which is to load the desired menu
            self.root.ids.toolbar.title = 'Mobile App'

        elif step == 2:
            # this section is used within the app menu after login to select other screen activities
            screen = self.root.ids.screen_manager.get_screen(
                'menu selector').ids.controller_scr

            if direction == 'None':
                screen.transition = NoTransition()
                screen.current = screen_name

            else:
                screen.transition = SlideTransition(direction=direction)
                screen.current = screen_name

        if step == 3:
            # explicitly to select the menu to load after identifying the rank of the user
            screen = self.root.ids.screen_manager.get_screen(
                'menu selector').ids.controller_scr

            if direction == 'None':
                screen.transition = NoTransition()
                screen.current = menu_screen

            else:
                screen.transition = SlideTransition(direction=direction)
                screen.current = menu_screen

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

    def font_sizer(self, level):

        # for low level fonts eg. label, text input
        if level == 1:
            font_size = f"{self.sp_size}sp"
            return font_size

        # for titles eg. menu, title bar
        elif level == 2:
            title_size = f"{self.sp_size + 6}sp"
            return title_size

        # for icon_fonts only
        elif level == 3:
            title_size = f"{self.sp_size + 12}sp"
            return title_size

    def widget_sizer(self, id="", parent_width=0, parent_height=0, child_number=0):
        if id == "meter_to_read_height":
            try:
                "changing/determining the size of the scroll_view of meter_mgt_menu page from the number of children"
                meter_grid_height = (parent_height * 0.18) * child_number
                return meter_grid_height
            except:
                pass  # print(f"an error occurred at the widget sizer line 6 above")

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
            if parent_height > parent_width:
                width = divmod(parent_width, 2)
                return width[0]  # Notice: when the remainder is large, the width becomes too little
            elif parent_height < parent_width:
                width = divmod(parent_width, 5)
                return width[0] - 4
            else:
                width = divmod(parent_width, 5)
                return width[0] - 4

        if id == "login_misc":
            """for Login.kv"""
            if parent_width <= parent_height:
                return 2
            else:
                return 1

    def orientation_checker(self, parent_x, parent_y):
        """ To check the orientation of the device, the active screen is checked and the size
         is set to "get_screen" variable as a list. this is then compared at the final statement
            orientation"""

        if parent_y > parent_x:
            return True
        elif parent_y < parent_x:
            return False
        else:
            return False

    def check_all_action(self):
        pass

    def toolbar_title(self, title="Mobile App"):
        # setting the toolbar title for every page entered
        self.root.ids.toolbar.title = title

    def account_widget_filter(self):
        pass

    def red_meter(self, red_acc_number, red_acc_name):

        Power_App.to_read_acc_no = red_acc_number
        Power_App.to_read_acc_name = red_acc_name

        widget = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
            'Meter reading page').ids
        widget.acc_no_to_read.text = Power_App.to_read_acc_no
        widget.acc_name_o_read.text = Power_App.to_read_acc_name

    def menu_options(self):
        #  Power_App.notification_toast("This screen option is coming soon ^_^", 1)

        #  MDApp.get_running_app().root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen("Meter Reading").ids.top_widget.add_widget(MenuOptions(screen_name="Meter Reading"))
        def screen_name_checker():
            return self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.current

        screen_menus = MenuOptions(screen_name=screen_name_checker(), callback=self.menu_functions)

    def menu_functions(self, Object_with_id, *kwargs):
        function_id = Object_with_id.function_id
        print(function_id)

        if function_id == "b_clear_screen_id":
            MDApp.get_running_app().root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
                "Meter Reading").clear_reading_screen()
            Power_App.notification_toast("Function added. Screen Cleared", 2)

        elif function_id == "b_refresh_gps_id":
            MDApp.get_running_app().root.ids.screen_manager.get_screen("menu selector").ids.controller_scr.get_screen(
                "Meter Reading").meter_proximity_calc(34, 56)
            Power_App.notification_toast("Function added. GPS Refreshed", 2)
        else:
            Power_App.notification_toast("This function is not yet added. Try later Updates", 2)


class Login_screen(MDScreen):

    def __init__(self, **kwargs):
        super(Login_screen, self).__init__(**kwargs)

    def login_anim(self, size, pos):

        self.spinner = MDSpinner(size_hint=(None, None), size=("46dp", "46dp"), pos_hint={'center_x': .5, 'center_y': .5}, pos=pos, active=True)

        self.ids.login_button.opacity = 0
        self.ids.login_button.active = False

        self.ids.login_float_layout.add_widget(self.spinner)
        button = Button(x=9, y=6, pos=pos)
        fake_anim = Animation(x=0, y=0, pos=[10,30], d=1)
        fake_anim.start(button)

        fake_anim.bind(on_complete=lambda x,y:MDApp.get_running_app().user_login(user_name=self.ids.user_name_input.text, password=self.ids.password_input.text))

    def _on_enter(self):
        try:
            self.ids.login_float_layout.remove_widget(self.spinner)
            self.ids.login_button.opacity = 100
            self.ids.login_button.active = True
        except: pass


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
    nothing = "nothing"
    filter_readable_acc_numbers = meter_reading_inMemory()

    filter_by_acc_dssList = None

    """:arg
    SOLVED: present issues: meter_reading_grid clear widgets, in_memory database clear function, 1st error above plus white space
    """

    def __init__(reading_init, **kwargs):
        super(Meter_reading_screen, reading_init).__init__(**kwargs)
        reading_init.to_read_acc_no = ""
        reading_init.to_read_acc_name = ""
        reading_init.current_circular_progress = 0
        reading_init.readable_acc_numbers = None
        reading_init.dss_list = []
        reading_init.dss_checkbox_filter = []
        reading_init.dss_search_text_state = "Load All"
        reading_init.temp_total_meter_read = 0
        reading_init.read_meter = 0
        reading_init.total_read_upload = 0
        reading_init.total_read_meter = 0
        # reading_init.filter_readable_acc_numbers = DictStore('temporal_acc_details')

    def dss_selector_clear_label(reading_init, **kwargs):
        if reading_init.ids.meter_dss_selector.text:
            if len(reading_init.ids.meter_dss_selector.text) >= 1:
                reading_init.ids.faker1.text = ''
        else:
            reading_init.ids.faker1.text = 'Search DSS to filter'

    def meter_reading_status(reading_init, **kwargs):
        reading_init.ids.read_cycle.text = f"Sept Cycle | {reading_init.temp_total_meter_read} to read | {reading_init.read_meter} " \
                                           f"read | Total upload: {reading_init.total_read_upload} | " \
                                           f"Total read: {reading_init.total_read_meter} "
        # reading_init.parent.current = "Meter reading page"#.parent.parent.current)

    def meter_reading_filter(reading_init):
        """ Meter_mgt_menu:
            This function has been updated to use the reading_init.dss_checkbox_filter object"""

        # resetting all object instance of this function before setting them up again
        try:
            reading_init.meter_reading_clear_items()
        except:
            pass  # print("error clearing dic stores")

        if not reading_init.dss_checkbox_filter:  # checking if the list is empty
            reading_init.dss_list = Power_App.user.meter_reading_dssList()  # returns a dict
            # sorting out the values from the dict
            for dss in reading_init.dss_list.values():
                reading_init.dss_checkbox_filter.append(dss)

        # reading_init.filter_readable_acc_numbers = DictStore('temporal_acc_details')
        ''' the idea behind this 'if' statement is: setting the reading_init.readable_acc_numbers to None at the main function
            (ie the build level) and checking if its value is None here, which if true, by the idea of inheritance we change it to dict store
            and carry it over without reading it from server again. iteration is needed at the background to check if the
            file is complete or there have been changes.
            '''  # DEPRECIATED

        """ The idea behind this new variable below is to be able to avoid kivy error of deleted widget 
            but are still within the dic tree. In that case, after new dss filter is done, they will be added back to the
            screen because they are not truly deleted"""
        Meter_reading_screen.filter_by_acc_dssList = reading_init.dss_checkbox_filter
        # _______________________________________________________________________________________
        for dss_ids in reading_init.dss_checkbox_filter:
            reading_init.filter_readable_meters = Power_App.user.readable_dss_filter(dss_ids)

            for row in reading_init.filter_readable_meters:
                #  for individual accounts after fetching data
                acc_number = row[0]
                first_name = row[1]
                last_name = row[2]
                x_coordinate = row[3]
                y_coordinate = row[4]
                customerDSS = row[5]
                last_paid = Power_App.user.last_payment(acc_number)  # fetching the account history
                last_amount = last_paid[0]
                last_date = last_paid[1]
                display_name = f'{first_name} {last_name}'

                reading_init.meters_to_read = Builder.load_file('Power_App_KVs/meter_reading_details.kv')

                # passing the values to meter to read page immedietely to reduce load time
                reading_init.meters_to_read.id = acc_number
                reading_init.meters_to_read.name = str(acc_number)
                reading_init.meters_to_read.x_coordinate = x_coordinate
                reading_init.meters_to_read.y_coordinate = y_coordinate
                reading_init.meters_to_read.dss_name = customerDSS
                # reading_init.meters_to_read.read_status = read_status
                reading_init.meters_to_read.ids.acc_number.text = str(acc_number)
                reading_init.meters_to_read.ids.names.text = display_name
                reading_init.meters_to_read.ids.payment_details.text = "Last Paid: [color=ff0000]{}[/color] | {}".format(
                    str(last_amount), str(last_date))

                #  adding the screen to the reading grid
                widget = reading_init.ids.meter_read_grid
                widget.add_widget(reading_init.meters_to_read)

                # passing the widget id to the screen object tree for reference saving
                reading_init.ids["meter_read_grid"].ids[f"{acc_number}"] = reading_init.meters_to_read

                # assigning the individual meter items to a general in-memory db:
                Meter_reading_screen.filter_readable_acc_numbers.save_account(acc_number=acc_number, names=display_name,
                                                                              payment=last_amount,
                                                                              payment_date=last_date,
                                                                              x_coordinate=x_coordinate,
                                                                              y_coordinate=y_coordinate,
                                                                              dss=customerDSS,
                                                                              read_status=False, reading="")

            # adding an empty label to cussion the effect of scrollview spring up
        label = MDLabel(size_hint_y=0.5, md_bg_color=[0, 0, 0, 0], pos_hint=[0, 0])
        widget.add_widget(label)
        reading_init.ids["meter_read_grid"].ids["0000"] = label

        if reading_init.filter_readable_acc_numbers:
            reading_init.temp_total_meter_read = len(Meter_reading_screen.filter_readable_acc_numbers.fetch_data())
            reading_init.meter_reading_status()

        # calling the clear function to clean the dss scrollview before readable meter items drop
        # reading_init.transformer_selector_clear_items()

        # _______________________________________________________________________________________
        """
        # testing if any account have been read before
        # if reading_init.filter_readable_acc_numbers[int(accounts)]['read_status'] is True: for sql server version
        if reading_init.filter_readable_acc_numbers[accounts]['read_status'] is True:
            reading_init.read_meter += 1
            reading_init.meter_reading_status()
        """

    def meter_read_filter_by_acc(reading_init, search_text=""):
        """ This func works by iterating through the meter_to_read grid id's and save them on temporal
            object, then filter out the items not in the search box and remove them from the widget.
            For items deleted before will be added while deleting the search box text back by the else statmente.

            SOLVED: NEEDS OPTIMIZATION--Latest issue: the initially deleted items are still within the ids dictionary
            SOLVED: THE WHITE SPACE EXTRA ISSUE FOR BUTTON-- keys_list was created to solve this error and the
            empty label was given an id"""
        widget = reading_init.ids["meter_read_grid"]
        keys_list = []
        try:
            for wid in widget.ids.keys():

                keys_list.append(wid)
                try:
                    wid_name = widget.ids[f'{wid}'].ids["names"].text
                    wid_identifier = str(f"{wid}{wid_name.lower()}")
                    if search_text.lower() not in wid_identifier:
                        widget.remove_widget(widget.ids[f'{wid}'])

                    else:
                        try:
                            if widget.ids[f'{wid}'].dss_name in Meter_reading_screen.filter_by_acc_dssList:
                                widget.add_widget(widget.ids[f'{wid}'])
                        except:
                            pass
                except:
                    pass

            if keys_list[:-1] is not 0000:
                widget.remove_widget(widget.ids['0000'])
                widget.add_widget(widget.ids['0000'])
        except:
            pass

    def meter_reading_clear_items(reading_init):
        widget = reading_init.ids.meter_read_grid
        widget.clear_widgets()

        for items in widget.ids:
            widget.clear_widgets()

        """ Redundant: all are now a global variable at Power_app level
        reading_init.filter_readable_acc_numbers.clear()
        reading_init.readable_acc_numbers.clear()
        """

        # widget2 = reading_init.ids.progress_bar_main_layout
        # widget2.clear_widgets()

    def meter_proximity_calc(reading_init, x_coordinate, y_coordinate, *args):

        # making a list(Dic) to store all the index of the children widget
        meter_proximity = DictStore("meter_and_distance")
        sort_list = []
        widget = reading_init.ids['meter_read_grid']

        try:
            for items in widget.children:
                if items.ids == {}:
                    meter_proximity.put('0000', distance=100000000)
                    pass
                else:
                    Q1 = float(items.x_coordinate)
                    P1 = float(items.y_coordinate)
                    Q2 = float(x_coordinate)
                    P2 = float(y_coordinate)
                    my_loc = (Q2, P2)
                    acc_loc = (Q1, P1)
                    try:
                        gps.start()
                        my_loc = [lat, lon]
                    except: print("Error in getting device location")

                    d = haversine(my_loc, acc_loc, unit=Unit.METERS)

                    # appending the calculated distance to the dict
                    meter_proximity.put(items.ids['acc_number'].text, distance=d)
                    items.ids['distance_label'].text = f'{d} m'
                    print(items.ids['acc_number'].text)
            # sorting the distances into an ordered list
            for keys in meter_proximity.keys():
                sort_list.append(meter_proximity[keys]['distance'])
            sorted_list = sorted(sort_list)

            # getting the coordinates of widget children in meter reading grid
            widget = reading_init.ids['meter_read_grid']
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
                    reading_init.ids['meter_read_grid'].ids[f'{key}'].pos = [x_widget_pos[i], y_widget_pos_rev[i]]
                    i += 1

            y_widget_pos = None
            x_widget_pos = None
            y_widget_pos_rev = None
            meter_proximity.clear()
        except:
            print("error osm update")

    def manual_meter_reading(reading_init):
        toast("Uploading", 1.2)

    def filter_button_label(reading_init, **kwargs):
        reading_init.dss_search_text_state = "Load All"
        reading_init.ids.filter_button.text = reading_init.dss_search_text_state

    def transformer_selector(reading_init, dss_text="", dss=""):
        """Meter_mgt_menu:
            function that controls the dropdown of dss list at meter mgt menu"""

        layout_counter = 0
        reading_init.dss_checkbox_filter = []

        # the below func is trying to calculate the height for the child widgets for the dss list
        def height_resolver(children, step):
            if step == 0:
                if children is 0 or None:
                    box_layout.height = 0
                    return box_layout.height
                else:
                    box_layout.height = children * 24
                    return f'{box_layout.height}sp'
            elif step == 1:
                if 13 < children < 20:
                    return f'{(children / 2) * 24}sp'
                elif children < 13:
                    return f'{children * 24}sp'
                else:
                    return f'{(children / 3) * 24}sp'

        if not reading_init.dss_list:
            reading_init.dss_list = Power_App.user.meter_reading_dssList()  # this returns a dic with dss name as key and dss id as value

        root_layout = reading_init.ids.dss_scrollview
        width_calc = reading_init.ids.meter_dss_selector
        box_layout = MDGridLayout(rows=1,
                                  size_hint=[None, None], height=0, width=width_calc.width, md_bg_color=[1, 1, 1, .9])

        scroll_view = ScrollView(do_scroll_y=True, size_hint=[None, None], size=box_layout.size)
        # scroll_view.bind(on_touch_up=reading_init.filter_button_label)

        scatter_layout = Scatter(center=width_calc.center,
                                 x=width_calc.x, y=width_calc.y - scroll_view.height,
                                 size_hint=[None, None], size=scroll_view.size)

        # clearing any widget at the mdgridlayout before adding another
        root_layout.clear_widgets()

        def dss_button_press(label, *args):
            Power_App.notification_toast(f'{label.dss_id} selected', 0.4)
            reading_init.dss_checkbox_filter = [
                label.dss_id]  # this is to reset the filter to hold only this button item
            reading_init.meter_reading_filter()  # this is to call the meter to read item filtering only this dss item

        def dss_checkbox_monitor(label, value, *args):
            if value:
                reading_init.dss_checkbox_filter.append(
                    label.dss_id)  # appending the selected checkbox item to the filter list
                reading_init.dss_search_text_state = "Filter"

            else:
                reading_init.dss_checkbox_filter.remove(label.dss_id)  # removing the selected checkbox from filter list
                if len(reading_init.dss_checkbox_filter) == 0:
                    reading_init.dss_search_text_state = "Load All"
                else:
                    pass
            reading_init.ids.filter_button.text = reading_init.dss_search_text_state

        # dss_label = Label(text=f'{dss}', font_size="11dp", size_hint=(1, None), height="16dp")
        # dss_label.bind(on_press=printer)

        class dss_label(Button):
            def __init__(reading_init, dss_id, **kwargs):
                super(dss_label, reading_init).__init__(**kwargs)
                reading_init.text = dss
                reading_init.dss_id = dss_id
                reading_init.background_normal = ''
                reading_init.background_color = [1, 1, 1, 0]
                reading_init.color = [0, 0, 0, 1]
                reading_init.size_hint = (.8, None)
                reading_init.height = "24sp"
                reading_init.font_size = "12sp"
                reading_init.bind(on_press=dss_button_press)

        class dss_filter_check(MDCheckbox):
            def __init__(reading_init, dss_id, **kwargs):
                super(dss_filter_check, reading_init).__init__(**kwargs)
                reading_init.dss_id = dss_id
                reading_init.bind(active=dss_checkbox_monitor)
                reading_init.size_hint = (.2, None)
                reading_init.height = "18sp"
                reading_init.width = "18sp"

        for dss in reading_init.dss_list:
            if dss_text == "" or None:
                dss_label.text = dss
                box_layout.add_widget(
                    dss_label(dss_id=reading_init.dss_list[dss]))  # filtering the dss list dic using the key
                box_layout.add_widget(dss_filter_check(dss_id=reading_init.dss_list[dss]))
                layout_counter += 1

            elif dss_text is "clear_widgets":
                root_layout.clear_widgets()

            else:
                if dss_text.lower() in dss.lower():
                    dss_label.text = dss
                    box_layout.add_widget(dss_label(dss_id=reading_init.dss_list[dss]))
                    box_layout.add_widget(dss_filter_check(dss_id=reading_init.dss_list[dss]))
                    reading_init.dss_checkbox_filter.append(reading_init.dss_list[
                                                                dss])  # populating the filter dss id with only the dss avaliable in the list
                    layout_counter += 1

                else:
                    pass

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

    def transformer_selector_clear_items(reading_screen):
        """Meter_mgt_menu:
            this function is used at the meter management menu (on_touch_down) to clear dss scrollview items and reset
            other variable that shows glitch"""
        widget_to_clear = reading_screen.ids.dss_scrollview
        widget_to_clear.clear_widgets()

        reading_screen.dss_list = None

        reading_screen.ids.filter_button.text = "Load All"

    def clear_reading_screen(reading_init):
        reading_init.meter_reading_clear_items()
        Meter_reading_screen.filter_readable_acc_numbers.delete_table()

    def check4_previous_reading(reading_init, acc_number, status):
        def action_():
            reading_init.ids[f'{acc_number}'].ids['main_template_background'].md_bg_color = [0, .9, 0, 1]
            reading_init.read_meter += 1
            reading_init.meter_reading_status()

        try:
            if Power_App.user.check_prev_reading(acc_number):
                action_()
            elif Meter_reading_screen.filter_readable_acc_numbers.check_prev_reading(acc_number):
                action_()
            else:
                pass
        except:
            pass

    def check_last_read(reading_init):
        try:
            reading, status = Meter_reading_screen.filter_readable_acc_numbers.check_last_read(Power_App.to_read_acc_no)
            if status is 1:
                meter_read_widget = reading_init.ids["meter_read_grid"].ids[f'{Power_App.to_read_acc_no}'].ids[
                    'main_template_background']
                meter_read_widget.md_bg_color = [0, .9, 0, 1]

                meter_read_widget = reading_init.ids["meter_read_grid"].ids[f'{Power_App.to_read_acc_no}'].ids[
                    'reading_editor']
                meter_read_widget.text = reading
                meter_read_widget.disabled = False

                meter_read_widget = reading_init.ids["meter_read_grid"].ids[f'{Power_App.to_read_acc_no}'].ids[
                    'fake_label']
                meter_read_widget.text = ""

                reading_init.read_meter += 1
                reading_init.meter_reading_status()

        except:
            pass


class Mobile_report_menu(MDScreen):
    pass


class Supervisor_menu(MDScreen):
    pass


class Trial_billing_menu(MDScreen):
    pass


class Menu_Screen_controller(MDScreen):
    pass


class reading_scatter(Scatter):
    def __init__(self, **kwargs):
        super(reading_scatter, self).__init__(**kwargs)
        self.do_rotation=False,
        #self.do_scale=False,
        self.bbox=((self.parent.x, self.parent.y), (self.parent.width, self.parent.height))


class Meter_read_per_acc(MDScreen):
    file_path = None
    scatter = Scatter(do_rotation=False, do_translation=False)

    def scaler(self):
        self.scale = 0

    scatter.bind(on_double_tap=scaler)

    def clear_label(self, **kwargs):
        if self.ids.reading_textbox.text:
            if len(self.ids.reading_textbox.text) >= 1:
                self.ids.faker1.text = ''
        else:
            self.ids.faker1.text = 'Enter Reading'

    def img_to_binary(self, file_path):
        try:
            """ Opening and converting the image file into binary format """
            with open(file_path, 'rb') as file:
                read_image = file.read()
                return read_image
        except:
            print(f'error at the img converter')

    def binary_to_img(self, binary_file):
        #try:
        """ Converting and writing to disk the saved binary file to image back """

        with open('temp_read_image.png', 'wb') as file:
            stored_image = file.write(binary_file)
            file.close()
            # stored_image = io.BytesIO(stored_image[0])
        stored_image = 'temp_read_image.png'
        return stored_image
        #except:
        #print(f'error at the binary to img converter')

    def choose_widgets(self):
        fetch_reading = Meter_reading_screen.filter_readable_acc_numbers.check_last_read(Power_App.to_read_acc_no)

        if fetch_reading[1] is 1:

            stored_image_inbinary = Meter_reading_screen.filter_readable_acc_numbers.fetch_readImage(Power_App.to_read_acc_no)
            print(f'image binary length = {len(stored_image_inbinary[0])}')
            temp_image = self.binary_to_img(stored_image_inbinary[0])

            # self.ids.option_A.clear_widgets() already been removed at the _on_leave func.
            self.image_file = AsyncImage(source=temp_image, size=self.parent.size, nocache=True)
            self.scatter.add_widget(self.image_file)
            self.ids.option_A.add_widget(self.scatter)

            try:
                self.ids.camera_label.add_widget(self.ids["option_B"])
            except:
                pass
        else:
            self.ids.camera_label.remove_widget(self.ids["option_B"])
            try:
                self.ids.option_A.clear_widgets()
                self.ids.option_A.add_widget(self.ids["camera_caller"])
                self.ids.option_A.add_widget(self.ids["file_chooser_caller"])
            except:
                pass

    def snap_meter(self, file_name):

        Meter_read_per_acc.reading_image = file_name

        try:
            self.ids.option_A.clear_widgets()
            self.ids.option_A.add_widget(Image(texture=CoreImage(self.file_name).texture))
            # self.ids.option_A.add_widget(Image(source=Meter_read_per_acc.reading_image, size=self.parent.size))
        except:
            pass
        try:
            self.ids.camera_label.add_widget(self.ids["option_B"])
        except:
            pass

    def take_picture(self):
        try:
            camera.take_picture(filename=f'{Power_App.to_read_acc_no}.jpg', on_complete=self.snap_meter)
        except:
            self.ids.option_A.clear_widgets()
            cam = Camera(play=True, resolution=(640, 480))

    def file_chooser(self):
        Meter_read_per_acc.reading_image = filechooser.open_file(filters=["*.png", "*.jpeg", "*.jpg"],
                                                                 on_selection=self.choosed_file)

    def choosed_file(self, file_name):
        try:
            # self.ids.option_A.clear_widgets() already been deleted at the _on_leave func.
            self.image_file = AsyncImage(source=file_name[0], size=self.parent.size, nocache=True)
            self.scatter.add_widget(self.image_file)
            self.ids.option_A.add_widget(self.scatter)
            self.file_path = file_name[0]
        except:
            pass
        try:
            self.ids.camera_label.add_widget(self.ids["option_B"])
        except:
            pass

    def save_reading(self, reading):
        try:
            print(self.file_path)
            binary_pic = self.img_to_binary(self.file_path)
            if binary_pic == None:
                binary_pic == self.binary_to_img('temp_read_image.png')

            if reading == "":
                Power_App.notification_toast("Enter Reading", 1)

            else:
                try:
                    red = float(reading)
                    import sqlite3

                    # image = sqlite3.Binary(self.read_image) Depriciated

                    Meter_reading_screen.filter_readable_acc_numbers.save_reading(Power_App.to_read_acc_no, red,
                                                                                  binary_pic)
                    Power_App.notification_toast("Saved", 1)

                    self.parent.current = 'Meter Reading'  # changing the screen to meter reading default page
                    self.file_path = None
                except:
                    Power_App.notification_toast("Special character detected, check reading", 1.1)
        except:
            Power_App.notification_toast("Please take or select image", 1)

    def delete(self):
        pass
        print(f'image binary is {self.read_image}')
        print(self.file_name[0])
        self.ids.option_A.add_widget(Image(source=self.file_name[0], size=self.parent.size))

    def _on_leave(self):
        working_dir = (os.getcwd())
        self.image_file.remove_from_cache()
        try:
            os.remove(f'{working_dir}'+'/temp_read_image.png')
        except:
            print('error deleting file')
        self.scatter.clear_widgets()
        self.ids.option_A.clear_widgets()


class SystemSettings:
    pass


class Loading_widget():
    pass


class Customer_details(MDScreen):
    pass


class BillDelivery(MDScreen):
    pass


class CustomerInformation(MDScreen):
    def __init__(self, **kwargs):
        super(CustomerInformation, self).__init__(**kwargs)

    def do_nothing(self):
        pass


Power_App().run()
