from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.metrics import Metrics
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, AnimationTransition, CardTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.toast import toast
from kivy.uix.scatter import Scatter
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty, OptionProperty, \
    ObjectProperty
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
from kivy.graphics.vertex_instructions import Line, Ellipse, Rectangle
from akivymd.uix.progresswidget import AKCircularProgress
from kivymd.uix.boxlayout import MDBoxLayout
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
    pass


class Waiting_screen(MDScreen):
    pass


class Power_App(MDApp):

    def build(self):
        Window.size = (255, 529)  # delete later
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

    def user_login(self, user_name, password):
        # animating the login delay...
        Clock.schedule_interval(self.login_animation, 1 / 60)
        fake_button = Button(text='', size=(12, 12))

        joan = Animation(size=(16, 16), duration=3)
        joan.start(fake_button)
        # creating connection and logging in..
        self.user = DbConnect(user_name, password)

        # fetching the rank of the user to select the usefull menu
        for item in self.user.menu_rank_checker():

            # cancelling the login animation once the data has been fetched
            # Clock.unschedule(self.login_animation)
            if item == "Route Marshal":
                self.change_screen(screen_name='menu selector', step=1, menu_screen='Route Martial Menu')

            if item == "Service Manager":
                self.change_screen(screen_name='menu selector', step=1, menu_screen='Supervisor Menu')

            if item == "Human Resources":
                self.change_screen(screen_name='menu selector', step=1, menu_screen='Supervisor Menu')

            if item == "Data Analyst":
                self.change_screen(screen_name='menu selector', step=1, menu_screen='Supervisor Menu')

            # fetching the navigation label item...
            items = self.user.navigation_content()
            self.root.ids.nav_user_name.text = f'{items[1]} {items[2][0]}.'
            self.root.ids.nav_user_bu.text = f'{items[0]} BU {items[3]}'
            self.root.ids.nav_date.text = str(datetime.datetime.now())

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

        self.readable_meters = self.user.meter_reading_items()

        if self.readable_meters:
            self.max_per = len(self.readable_meters)
        else:
            self.max_per = 1

        # since the akcircularprogress bar has refused to auto update at entry, i decided to add it manually through
        # python
        circularProgress = AKCircularProgress(pos_hint={"center_x": .5, "center_y": .5}, size_hint=(None, None),
                                              size=('40dp', '40dp'),
                                              percent_size='7dp', line_width='2dp', percent_type="relative",
                                              start_deg=180,
                                              end_deg=540, max_percent=self.max_per)
        widget2 = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
            'Meter Reading').ids.progress_bar_main_layout

        widget2.add_widget(circularProgress)

        for items in self.readable_meters:
            kv_file = Builder.load_file('Power_App_KVs/meter_reading_details.kv')

            #def individual_meter_items():
            acc_number = items[0]
            first_name = items[1]
            last_name = items[2]
            x_coordinate = items[3]
            y_coordinate = items[4]

            last_paid = self.user.last_payment(acc_number)
            last_amount = last_paid[0]
            last_date = last_paid[1]

            display_name = first_name + " " + last_name
            kv_file.ids.acc_number.text = str(acc_number)
            kv_file.ids.names.text = str(display_name)
            kv_file.ids.payment_details.text = "Last Paid: [color=ff0000]{}[/color] | {}".format(str(last_amount), str(last_date))

            widget = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
                'Meter Reading').ids.meter_read_grid
            widget.add_widget(kv_file)

    def meter_reading_clear_items(self):
        widget = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
            'Meter Reading').ids.meter_read_grid
        widget.clear_widgets()
        widget2 = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
            'Meter Reading').ids.progress_bar_main_layout
        widget2.clear_widgets()

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

    def transformer_selector_1(self, dss_text=""):

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
                    return (children/2) * 24
                elif children < 13:
                    return children * 24
                else:
                    return (children/3) * 24

        """dss_list = ['thuerhr', 'sdrlkfdjjter', 'gfjkdkjg', 'thhk', 'ytjhmncn', 'for', 'RM', 'menu',
                    'To', 'determine', 'the', 'MDcard', 'padding', 'compare', 'the', 'parent', 'width', 'and', 'height',
                    'if', 'x', 'is', 'greater', 'then', 'the', 'padding', 'will', 'be', 'the', 'remainder,' 'of', 'the',
                    'parent', 'width', 'divided', 'lhu', '2','if']"""
        dss_list = self.user.meter_reading_dssList()

        root_layout = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
            "Meter Reading").ids.dss_scrollview
        width_calc = self.root.ids.screen_manager.get_screen('menu selector').ids.controller_scr.get_screen(
            "Meter Reading").ids.meter_dss_selector
        box_layout = MDBoxLayout(orientation="vertical",
                                 size_hint=[None, None], height=0, width=width_calc.width)

        scroll_view = ScrollView(do_scroll_y=True, size_hint=[None, None], size=box_layout.size)

        scatter_layout = Scatter(center=width_calc.center,
                                 x=width_calc.x, y=width_calc.y - scroll_view.height,
                                 size_hint=[None, None], size=scroll_view.size)

        # clearing any widget at the mdgridlayout before adding another
        root_layout.clear_widgets()
        layout_counter = 0

        def printer(label, *args):
            print(f'I was pressed: {label.text}')

        dss = ""  # this is a fake string, created so as to avoid error while creating the class dss_label

        # dss_label = Label(text=f'{dss}', font_size="11dp", size_hint=(1, None), height="16dp")
        # dss_label.bind(on_press=printer)

        class dss_label(Button):
            def __init__(self, **kwargs):
                super(dss_label, self).__init__(**kwargs)
                self.text = dss
                self.background_normal = ''
                self.background_color = [1, 1, 1, .9]
                self.color = [0, 0, 0, 1]
                self.size_hint = (1, None)
                self.height = "24dp"
                self.font_size = "11dp"
                self.bind(on_press=printer)

        for dss in dss_list:

            if dss_text == "" or None:
                dss_label.text = dss
                box_layout.add_widget(dss_label())
                layout_counter += 1

            elif dss_text is "clear_widgets":
                root_layout.clear_widgets()

            else:
                if dss_text in dss:
                    dss_label.text = dss
                    box_layout.add_widget(dss_label())
                    layout_counter += 1

                else:
                    pass

        print(layout_counter)

        box_layout.height = height_resolver(layout_counter, step=0)
        box_layout.width = width_calc.width

        scroll_view.height = height_resolver(layout_counter, step=1)

        # adding a line effect at the border of the scroll view
        with scroll_view.canvas.after:
            Color(0, .7, 0, .6)
            Line(points=(scroll_view.x, scroll_view.y+scroll_view.height,
                         scroll_view.x, scroll_view.y,
                         scroll_view.x+scroll_view.width, scroll_view.y,
                         scroll_view.x+scroll_view.width, scroll_view.y+scroll_view.height))

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
                meter_grid_height = (parent_height * 0.2) * len(self.readable_meters)  # child_number
                return meter_grid_height
            except:
                "changing/determining the size of the scroll_view of meter_mgt_menu page from the number of children"
                meter_grid_height = (parent_height * 0.2) * child_number
                return meter_grid_height

        if id == "main_menu":
            """for Rm menu:
            The grid or list colume for the menu has to be either 2 if x is greater than y, or
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


Power_App().run()
