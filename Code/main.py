from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.config import Config
from datetime import datetime
import os
import multiprocessing as mp
import subprocess
import re
import webbrowser
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.dropdown import DropDown
from kivymd.uix.pickers import MDDatePicker
from kivymd.toast import toast
from matplotlib import pyplot as plt
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from kivy.properties import StringProperty
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class MainApp(MDApp):
    bg = r"og.jpg"
    ico = r"og1.png"
    def build(self):
        self.icon = r"og1.png"
        self.title = "Trend Trace"
        Window.maximize()
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "A700"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.accent_hue = "A700"
        self.theme_cls.theme_style = "Dark" 
        self.roi_x1 = None
        self.roi_x2 = None
        self.drawing = False
        self.roi_crossed = False
        self.last_screenshot_time = None
        self.screenshot_interval = 1.5  
        self.captured_boxes = []
        self.Column = ""
        self.menu = None
        self.lendata = None
        self.l = []
        self.i = 0

        return Builder.load_string('''
MDBoxLayout:
    orientation: "vertical"
    MDTopAppBar:
        title: "Trend Trace"
        left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
        elevation: 10
    MDNavigationLayout:
        ScreenManager:
            id: screen_manager
            Screen:
                name: "Home"
                RelativeLayout:
                    orientation: 'vertical'
                    Image:
                        source: app.bg 
                        allow_stretch: True
                        keep_ratio: False
                        size_hint: None, None
                        size: self.parent.size
                        pos: self.parent.pos
                    MDLabel:
                        text: "1. Download IP Webcam App from play store."
                        pos_hint: {"center_x": 1.08, "center_y": 0.9}
                        color: 'cyan'
                    MDLabel:
                        text: "2. Open App in and scroll down and Click on 'Start Server' and Put IPv4 Url in below box. "
                        pos_hint: {"center_x": 1.08, "center_y": 0.8}
                        color: 'cyan'
                        multiline: True
                    MDLabel:
                        text: "Note: Make sure to connect both devices on the same network. "
                        pos_hint: {"center_x": 1.08, "center_y": 0.7}
                        color: 'cyan'
                    MDLabel:
                        text: "Url: "
                        pos_hint: {"center_x": 1.08, "center_y": 0.6}
                        color: 'cyan'
                    MDTextField:
                        id: text_input
                        hint_text: "Enter Url Of Phone Cam"
                        pos_hint: {"center_x": 0.7, "center_y": 0.6}
                        size_hint: 0.1,0.1
                    MDFillRoundFlatIconButton:
                        size_hint: 0.1,0.1
                        text: "WebCam Process"
                        pos_hint: {"center_x": 0.3, "center_y": 0.4}
                        on_release: app.webcam()
                    MDFillRoundFlatIconButton:
                        size_hint: 0.1,0.1
                        text: "Phone Camera Process"
                        pos_hint: {"center_x": 0.7, "center_y": 0.4}
                        on_release: app.phonecam()
            Screen:
                name: "Trace"
                RelativeLayout:
                    orientation: 'vertical'
                    Image:
                        source: app.bg 
                        allow_stretch: True
                        keep_ratio: False
                        size_hint: None, None
                        size: self.parent.size
                        pos: self.parent.pos
                    MDLabel:
                        text: "-->  Type : "
                        pos_hint: {"center_x": 0.1, "center_y": 0.95}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input10
                        hint_text: "Enter Type of Cloth "
                        pos_hint: {"center_x": 0.2, "center_y": 0.95}
                        size_hint: 0.1,0.1
                    MDLabel:
                        text: "-->  Color : "
                        pos_hint: {"center_x": 0.1, "center_y": 0.85}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input1
                        hint_text: "Enter dominant color of Cloth "
                        pos_hint: {"center_x": 0.2, "center_y": 0.85}
                        size_hint: 0.1,0.1
                    MDLabel:
                        text: "-->  Pattern : "
                        pos_hint: {"center_x": 0.1, "center_y": 0.75}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input2
                        hint_text: "Enter Pattern of Cloth "
                        pos_hint: {"center_x": 0.2, "center_y": 0.75}
                        size_hint: 0.1,0.1
                    MDLabel:
                        text: "-->  Texture : "
                        pos_hint: {"center_x": 0.1, "center_y": 0.65}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input3
                        hint_text: "Enter Texture of Cloth "
                        pos_hint: {"center_x": 0.2, "center_y": 0.65}
                        size_hint: 0.1,0.1
                    MDLabel:
                        text: "-->  Brand : "
                        pos_hint: {"center_x": 0.1, "center_y": 0.55}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input4
                        hint_text: "Enter Brand of Cloth "
                        pos_hint: {"center_x": 0.2, "center_y": 0.55}
                        size_hint: 0.1,0.1
                    MDLabel:
                        text: "-->  Style : "
                        pos_hint: {"center_x": 0.1, "center_y": 0.45}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input5
                        hint_text: "Enter Style of Cloth "
                        pos_hint: {"center_x": 0.2, "center_y": 0.45}
                        size_hint: 0.1,0.1
                    MDLabel:
                        text: "-->  Season : "
                        pos_hint: {"center_x": 0.1, "center_y": 0.35}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input6
                        hint_text: "Enter Season of Cloth "
                        pos_hint: {"center_x": 0.2, "center_y": 0.35}
                        size_hint: 0.1,0.1
                    MDLabel:
                        text: "-->  Gender : "
                        pos_hint: {"center_x": 0.1, "center_y": 0.25}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input7
                        hint_text: "Enter Gender "
                        pos_hint: {"center_x": 0.2, "center_y": 0.25}
                        size_hint: 0.1,0.1
                    MDLabel:
                        text: "-->  Usage : "
                        pos_hint: {"center_x": 0.1, "center_y": 0.15}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input8
                        hint_text: "Enter Cloth Usage"
                        pos_hint: {"center_x": 0.2, "center_y": 0.15}
                        size_hint: 0.1,0.1
                    MDLabel:
                        text: "-->  Date : "
                        pos_hint: {"center_x": 0.1, "center_y": 0.05}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input9
                        hint_text: "Enter Date "
                        pos_hint: {"center_x": 0.2, "center_y": 0.05}
                        size_hint: 0.1,0.1
                    MDFillRoundFlatIconButton:
                        size_hint: 0.1,0.1
                        text: "Trace"
                        pos_hint: {"center_x": 0.5, "center_y": 0.9}
                        on_release: app.filter_data()
                    RelativeLayout:
                        id: table_layout
                        orientation: 'vertical'
                    MDLabel:
                        text: "Row Index to get video : "
                        pos_hint: {"center_x": 0.5, "center_y": 0.15}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input11
                        hint_text: "Enter Index of row starts fron 0 "
                        pos_hint: {"center_x": 0.6, "center_y": 0.15}
                        size_hint: 0.1,0.1
                    
                    MDTextField:
                        id: text_input13
                        hint_text: "Enter File to Analysis (upper, lower or full)"
                        pos_hint: {"center_x": 0.65, "center_y": .9}
                        size_hint: 0.1,0.1
                                   
                    MDFillRoundFlatIconButton:
                        text: "Go to video"
                        pos_hint: {"center_x": 0.75, "center_y": 0.15}
                        on_release: app.open_video()
                                               
            Screen:
                name: "Trend"
                RelativeLayout:
                    orientation: 'vertical'
                    padding: dp(20)
                    spacing: dp(20)
                                   
                    Image:
                        source: app.bg 
                        allow_stretch: True
                        keep_ratio: False
                        size_hint: None, None
                        size: self.parent.size
                        pos: self.parent.pos

                    MDFillRoundFlatIconButton:
                        id: button
                        size_hint: 0.1,0.1
                        text: "Select Column"
                        pos_hint: {"center_x": .4, "center_y": .9}
                        on_release: app.menu_open()

                    MDTextField:
                        id: date_from
                        hint_text: "Date From"
                        size_hint_y: 0.1
                        size_hint_x: 0.2
                        pos_hint: {"center_x": .15, "center_y": .7}
                        on_focus: if self.focus: app.show_date_picker('from')

                    MDTextField:
                        id: date_to
                        hint_text: "Date To"
                        size_hint_y: 0.1
                        size_hint_x: 0.2
                        pos_hint: {"center_x": .85, "center_y": .7}
                        on_focus: if self.focus: app.show_date_picker('to')
                                   
                    MDTextField:
                        id: text_input12
                        hint_text: "Enter File to Analysis (upper, lower or full)"
                        pos_hint: {"center_x": 0.5, "center_y": .8}
                        size_hint: 0.1,0.1

                    MDFillRoundFlatIconButton:
                        size_hint: 0.1,0.1
                        text: "Show Bar Graph"
                        pos_hint: {"center_x": 0.6, "center_y": 0.9}
                        on_release: app.show_bar_graph()

                    RelativeLayout:
                        id: graph_box
                        orientation: 'vertical'
                        pos_hint: {"center_x": 0.5, "center_y": 0.4}
                                   
            Screen:
                name: "AboutUs"
                RelativeLayout:
                    orientation: 'vertical'
                    RelativeLayout:
                        orientation: 'vertical'
                        Image:
                            source: app.bg 
                            allow_stretch: True
                            keep_ratio: False
                            size_hint: None, None
                            size: self.parent.size
                            pos: self.parent.pos
                        Image:
                            source: app.ico
                            pos_hint: {"center_x": 0.5, "center_y": 0.7}
                            size_hint: None, None
                            size: 400,400
                            spacing: [0, 50]
                        Label:
                            text: "Developer Name's: Strike, Night Wolf"
                            font_size: "25sp"
                            color: "cyan"
                            bold: True
                            pos_hint: {"center_x": 0.5, "center_y": 0.4}
                        Label:
                            text: "Email: contact.trend.trace@gmail.com"
                            font_size: "25sp"
                            color: "cyan"
                            bold: True
                            pos_hint: {"center_x": 0.5, "center_y": 0.2}
        MDNavigationDrawer:
            id: nav_drawer
            BoxLayout:
                orientation: "vertical"
                Image:
                    source: app.ico
                MDList:
                    OneLineIconListItem:
                        text: "Home"
                        theme_text_color: "Custom" 
                        text_color: 0, 1, 1, 1 
                        on_press:
                            nav_drawer.set_state("close")
                            screen_manager.current = "Home"
                        IconLeftWidget:
                            icon: "home"
                            theme_text_color: "Custom" 
                            text_color: 0, 1, 1, 1 
                    OneLineIconListItem:
                        text: "Trace"
                        theme_text_color: "Custom" 
                        text_color: 0, 1, 1, 1 
                        on_press:
                            nav_drawer.set_state("close")
                            screen_manager.current = "Trace"
                        IconLeftWidget:
                            icon: "google-lens"
                            theme_text_color: "Custom" 
                            text_color: 0, 1, 1, 1 
                    OneLineIconListItem:
                        text: "Trend"
                        theme_text_color: "Custom" 
                        text_color: 0, 1, 1, 1 
                        on_press:
                            nav_drawer.set_state("close")
                            screen_manager.current = "Trend"
                        IconLeftWidget:
                            icon: "graph"
                            theme_text_color: "Custom" 
                            text_color: 0, 1, 1, 1 
                    OneLineIconListItem:
                        text: "About Us"
                        theme_text_color: "Custom" 
                        text_color: 0, 1, 1, 1  
                        on_press:
                            nav_drawer.set_state("close")
                            screen_manager.current = "AboutUs"
                        IconLeftWidget:
                            icon: "information"
                            theme_text_color: "Custom" 
                            text_color: 0, 1, 1, 1 
                    OneLineIconListItem:
                        text: "Feedback"
                        theme_text_color: "Custom" 
                        text_color: 0, 1, 1, 1 
                        on_press:
                            nav_drawer.set_state("close")
                            app.feedback()
                        IconLeftWidget:
                            icon: "comment-quote"
                            theme_text_color: "Custom" 
                            text_color: 0, 1, 1, 1 
                    OneLineIconListItem:
                        text: "Rate Us"
                        theme_text_color: "Custom" 
                        text_color: 0, 1, 1, 1 
                        on_press:
                            nav_drawer.set_state("close")
                            app.rate_us_link("com.example.trendtrace")
                        IconLeftWidget:
                            icon: "star"
                            theme_text_color: "Custom" 
                            text_color: 0, 1, 1, 1 
''')

    def show_popup(self):
        title = "Not Valid URL"
        message = "Please Enter Valid URL"
        dialog = MDDialog(
            title=title,
            type="alert",
            text=message,
            size_hint=(0.8, 0.3),
            auto_dismiss=True,
            buttons=[
                MDFillRoundFlatIconButton(
                    text="Close",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def webcam(self):
        try:
            command = ["python","webcam.py"]
            subprocess.run(command)
        except Exception as e:
            self.show_error_dialog(str(e))

    def phonecam(self):
    
        url = self.root.ids.text_input.text
        ipv4_pattern = re.compile(
            r'^(http|https):\/\/'
            r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
            r'(:[0-9]{1,5})?$'
        )
        if re.match(ipv4_pattern, url):
            url = url + "/shot.jpg"
            try:
                command = ["python","phonecam.py",f"{url}"]
                subprocess.run(command)
            except Exception as e:
                self.show_error_dialog(str(e))
        else:
            self.show_popup()
         
    #Trend

    def menu_open(self):
        
        columns = ["Type", "Color", "Pattern", "Texture", "Brand", "Style", "Season", "Gender", "Usage"]
        menu_items = [
            {"text": f"{columns[i]}", "on_release": lambda x=f"{columns[i]}": self.menu_callback(x)}
            for i in range(len(columns))
        ]
        self.menu = MDDropdownMenu(caller=self.root.ids.button, items=menu_items)
        self.menu.open()


    def menu_callback(self, text_item):
        self.Column = text_item
        toast(f"Selected column {text_item}")
        if self.menu:  
            self.menu.dismiss()

    def show_date_picker(self, date_type):
        self.date_type = date_type
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        if self.date_type == 'from':
            self.root.ids.date_from.text = value.strftime('%Y-%m-%d')
        else:
            self.root.ids.date_to.text = value.strftime('%Y-%m-%d')

    def show_bar_graph(self):
        column_name = self.Column
        date_from_str = self.root.ids.date_from.text.strip()
        date_to_str = self.root.ids.date_to.text.strip()

        if not column_name:
            self.show_error_dialog("Please select a column.")
            return

        if not date_from_str or not date_to_str:
            self.show_error_dialog("Please select both 'Date From' and 'Date To'.")
            return

        try:
            # Parse selected dates
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d')
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d')

            # Validate date range
            if date_from > date_to:
                self.show_error_dialog("'Date To' must be later than 'Date From'.")
                return

            self.get_data(column_name,date_from,date_to)

        except KeyError:
            self.show_error_dialog("No Data Available for selected Column ")

    def get_data(self, column,datef,datet):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        current_directory = os.path.dirname(os.path.abspath(__file__))
        cred = os.path.join(current_directory, r'')
        creds = ServiceAccountCredentials.from_json_keyfile_name(cred, scope)
        client = gspread.authorize(creds)
        file = self.root.ids.text_input12.text.strip()
        if(file in ["upper","lower","full"]):
            sheet = client.open(file).sheet1
            data = sheet.get_all_records()
            df = pd.DataFrame(data)
            df['Date'] = pd.to_datetime(df['Date'])

            # Filter the DataFrame based on the date range
            filtered_df = df[(df['Date'] >= datef) & (df['Date'] <= datet)]

            if filtered_df.empty:
                    self.show_error_dialog(f"No data available for '{column}' column within the specified date range.")
                    return

            color_counts = filtered_df[column].value_counts()

            if color_counts.empty:
                    self.show_error_dialog(f"No data available for '{column}' column within the specified date range.")
                    return

            # Plot the bar graph
            plt.figure(figsize=(8, 6))
            plt.bar(color_counts.index, color_counts.values, align='center', alpha=0.5)
            plt.xlabel(column)
            plt.ylabel('Count')
            plt.title(f'{column} Trend')
            plt.xticks(rotation=45)
            plt.tight_layout()

            graph_filename = f'bar_graph_{self.i}.png'
            self.i += 1
            plt.savefig(graph_filename)

            # Display the image using Kivy's Image widget
            self.root.ids.graph_box.clear_widgets()
            self.root.ids.graph_box.add_widget(Image(source=graph_filename))

            os.remove(graph_filename)

        else:
            self.show_error_dialog(f"{file} file is not there in database. Type valid file name.")

    def show_error_dialog(self,Message):
        self.dialog = MDDialog(
                title="Error",
                text=Message,
                buttons=[
                    MDFillRoundFlatIconButton(
                        text="Close",
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ]
            )
        self.dialog.open()
        

# Trace
    def load_data(self,file):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        current_directory = os.path.dirname(os.path.abspath(__file__))
        cred = os.path.join(current_directory, '')
        creds = ServiceAccountCredentials.from_json_keyfile_name(cred, scope)
        client = gspread.authorize(creds)
        sheet = client.open(file).sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        return df

    def filter_data(self):
        file = self.root.ids.text_input13.text.strip()
        if(file in ["upper","lower","full"]):
            data_df = self.load_data(file)
            if data_df.empty:
                self.show_error_dialog(f"No data available in {file}")
                return
            else:
                filters = {
                    "Type": self.root.ids.text_input10.text.strip(),
                    "Color": self.root.ids.text_input1.text.strip(),
                    "Pattern": self.root.ids.text_input2.text.strip(),
                    "Texture": self.root.ids.text_input3.text.strip(),
                    "Brand": self.root.ids.text_input4.text.strip(),
                    "Style": self.root.ids.text_input5.text.strip(),
                    "Season": self.root.ids.text_input6.text.strip(),
                    "Gender": self.root.ids.text_input7.text.strip(),
                    "Usage": self.root.ids.text_input8.text.strip(),
                    "Date": self.root.ids.text_input9.text.strip()
                }

                filtered_df = data_df.copy()
                for key, value in filters.items():
                    if value:
                        filtered_df = filtered_df[filtered_df[key].str.contains(value, case=False, na=False)]

                self.update_table(filtered_df)
        else:
            self.show_error_dialog(f"{file} file is not there in database. Type valid file name.")

    def update_table(self, df):
        table_layout = self.root.ids.table_layout
        table_layout.clear_widgets()

        if df.empty:
            table_layout.add_widget(Label(text="No matching records found.",color="cyan"))
            return

        data_table = MDDataTable(
            size_hint=(0.5, 0.5),
            pos_hint= {'center_x': 0.6, 'center_y': 0.5},
            column_data=[
                ("Index", dp(30)),
                ("Date", dp(30)),
                ("Type", dp(30)),
                ("Color", dp(30)),
                ("Pattern", dp(30)),
                ("Texture", dp(30)),
                ("Brand", dp(30)),
                ("Style", dp(30)),
                ("Season", dp(30)),
                ("Gender", dp(30)),
                ("Usage", dp(30)),
                ("Timestamp", dp(30))
            ]
        )

        table_layout.add_widget(data_table)
        k = 0
        for _, row in df.iterrows():
            row_text = (k,row['Date'] , row['Type'] , row['Color'] , row['Pattern'] , row['Texture'], row['Brand'], 
                        row['Style'] , row['Season'] ,row['Gender'] , row['Usage'] , row['TimeStamp'])
            self.l = self.l + [[row['Date'],row['TimeStamp']]]
            data_table.row_data.append(row_text)
            k +=1
        self.lendata = len(data_table.row_data)
    
    def open_video(self):
        i = self.root.ids.text_input11.text.strip()
        if self.lendata == 0 or self.lendata == None:
            self.show_error_dialog("Please Trace the details first")
            return
        if not i.isdigit():
            self.show_error_dialog("Please enter a valid number.")
            return

        index = int(i)
        if index < 0 or index >= self.lendata:
            self.show_error_dialog(f"Please enter a valid index between 0 and {self.lendata - 1}.")
            return
        
        path =self.l[index][0]+".mp4"
        timestamp = self.l[index][1]
        seconds = self.timestamp_to_seconds(timestamp)
        if os.path.exists(path):
            command = f"vlc --start-time={seconds} {path}"
            subprocess.Popen(command, shell=True)
        else:
            self.show_error_dialog(f"Video file {path} doesn't Exist")

    def timestamp_to_seconds(self,timestamp):
        hours, minutes, seconds = map(int, timestamp.split(':'))
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds
    
    def open_link(self,link):
        webbrowser.open(link)
    
    def rate_us_link(self,package_name):
        link = ""
        self.open_link(link)

    def feedback(self):
        link = ""
        self.open_link(link)
    
if __name__ == '__main__':
    MainApp().run()
