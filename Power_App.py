from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.metrics import Metrics
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, AnimationTransition, CardTransition
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivymd.uix.label import MDLabel


#Builder.load_file('Power_App_KVs/meter_reading_details.kv')

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
    pass


class Mobile_report_menu(MDScreen):
    pass


class Supervisor_menu(MDScreen):
    pass


class Trial_billing_menu(MDScreen):
    pass


class Screen_controller(MDScreen):
    pass


class Meter_read_per_acc(MDScreen):
    pass


class Power_App(MDApp):
    def build(self):

        Window.size = (255, 529)  # delete later
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_hue = '900'
        self.theme_cls.primary_palette = 'BlueGray'
        self.theme_cls.theme_text_color = 'Dark'
        #self.nav_bar = Builder.load_file('Power_App_KVs//Navigation_drawer.kv')

    """    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.set_toolbar_font_name)
        Clock.schedule_once(self.set_toolbar_font_size)

    def set_toolbar_font_name(self, *args):
        self.root.ids.toolbar.font_name = "JetBrainsMono-ExtraBold-Italic.ttf"

    def set_toolbar_font_size(self, *args):
        self.root.ids.toolbar.font_size = '4sp'
        
        """

    def on_start(self):
        self.root.ids.toolbar.title = 'Mobile App'

    def user_login(self):
        pass

    def change_screen(self, screen_name, direction='left'):

        '''Dictionaries with screen names as keys and screen title for toolbar as value

        self.Screen_identifier = {'scr_con': 'Menu',
                                  'Route Martial Menu': 'Menu',
                                  'Supervisor Menu': 'Menu',
                                  'login_screen': ''}
        self.root.ids.toolbar_md_label.text = self.Screen_identifier[screen_name]''' # changing toolbar title once screen chnages

        screen = self.root.ids.screen_manager

        if direction == 'None':
            screen.transition = NoTransition()
            screen.current = screen_name

        else:
            screen.transition = SlideTransition(direction=direction)
            screen.current = screen_name

        #if screen_name == 'scr_con':
        self.root.ids.toolbar.title = 'Mobile App'

        #else:
            #self.root.ids.toolbar.title = 'Power App'

    def change_screen_1(self, screen_name, direction='left'):

        """Dictionaries with screen names as keys and screen title for toolbar as value"""

        self.Screen_identifier = {'scr_con': 'Menu',
                             'Route Martial Menu': 'Menu',
                             'Supervisor Menu': 'Menu',
                                  'Meter Reading': 'Meter Reading',
                                  "Meter reading page": "Meter Reading"}

        screen = self.root.ids.screen_manager.get_screen('scr_con').ids.controller_scr  # defining the 2nd screen manager to change

        if direction == 'None':
            screen.transition = NoTransition()
            screen.current = screen_name

        else:
            screen.transition = SlideTransition(direction=direction)
            screen.current = screen_name

        self.root.ids.toolbar.title = self.Screen_identifier[screen_name]

    def work_offline(self, checkbox, value):
        if value:
            self.root.ids.screen_manager.get_screen('login_screen').ids.work_offline_label.text = 'Offline Mode'
            # plus other sqlite functions
        else:
            self.root.ids.screen_manager.get_screen('login_screen').ids.work_offline_label.text = 'Online Mode'
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

    def MDcard_width_calc(self, parent_width_x, parent_width_y):
        """To determine the MDcard width, compare the parent width and height,
            if x is greater, then the width will be parent width divided by 2 minus the remainder for padding """
        if parent_width_x <= parent_width_y:
            width = divmod(parent_width_x, 2)
            return width[0] - width[1]  # Notice: when the remainder is large, the wudth becomes too little
        else:
            width = divmod(parent_width_x, 5)
            return width[0] - width[1]

    def MDGrid_or_List_cols_calc(self, parent_width_x, parent_width_y):
        """The grid or list colume for the menu has to be either 2 if x is greater than y, or 5 if x is less than y"""
        if parent_width_x <= parent_width_y:
            return 2
        else:
            return 5

    def menu_card_padding(self, parent_width_x, parent_width_y):
        """To determine the MDcard padding, compare the parent width and height,
            if x is greater, then the padding will be the remainder of the parent width divided by 2"""
        if parent_width_x <= parent_width_y:
            width = divmod(parent_width_x, 2)
            return width[1]/2
        else:
            width = divmod(parent_width_x, 2)
            return width[1]/2

    def set_toolbar_font_size(self, *args):
        self.root.ids.toolbar.font_size = '15sp'

    def user_details(self):
        pass

    def meter_screen_sizer(self, parent_height_y, child_number):
        meter_grid_height = (parent_height_y * 0.3) * child_number
        return meter_grid_height

    def go_to_home(self):
        pass

Power_App().run()
