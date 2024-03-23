from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.widget import Widget
import socket
import os
import threading
import time
global start_time
global display_on

class WakeScreen(Widget):
    def on_touch_down(self, touch):
        global start_time
        global display_on
        start_time = time.time()
        display_on = True
        os.popen('bash backlight_on.sh')
            

class SchedulingPage(GridLayout):
    def __init__(self, switch_home_callback, **kwargs):
        super().__init__(**kwargs)
        self.cols = 5
        self.rows = 10
        self.col_force_default=True
        self.col_default_width=90
        self.saved_times=[]
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label(color=[0,0,0,1], halign='center', bold=True, text='Scheduling Page'))
        self.add_widget(Label())
        home_btn=Button(text='Home', background_color= [0.075, 0.71, 0.918, 1], on_press=switch_home_callback)
        self.add_widget(home_btn)

    def switch_home(self, instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(app.build())



class SmartFanApp(App):
    Window.clearcolor = (1, 1, 1, 1)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min_temp_label = None
        self.max_temp_label = None
        self.display_on = True
        self.start_time = time.time()

    def build(self):
        self.page = 0
        self.min_temp = 70
        self.max_temp = 90
        self.hour = 12
        self.ten = 0
        self.min = 0
        self.sched_list = []
        self.sched_label_list = []
        
        t1 = threading.Thread(target=self.sleep_timer)
        t1.start()
        
        # Conn
        HOST = '192.168.1.161'    # The remote host
        PORT = 50007              # The same port as used by the server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((HOST, PORT))
        
        layout = GridLayout(cols=2, rows=6, row_force_default=True, col_force_default= True, col_default_width=350, row_default_height=50)

        title_lable_layout = GridLayout(cols=2, col_force_default=True, col_default_width=305, row_force_default=True, row_default_height=40)

        range_label=Label(color=[0, 0, 0, 1], bold=True, text="Set Perferred Temperature Range")

        title_lable_layout.add_widget(range_label)

        sched_label=Label(color=[0, 0, 0, 1], bold=True, text="Set Perferred Cooling Time")

        title_lable_layout.add_widget(sched_label)

        layout.add_widget(title_lable_layout)
        layout.add_widget(Label())  # Empty space

        temp_layout = GridLayout(rows=3, cols=2, col_force_default=True, col_default_width=70, row_force_default= True, row_default_height=60, padding=[70, 0])

        min_temp_inc_button = Button(text='Up', background_color= [0.075, 0.71, 0.918, 1], on_press=self.on_min_temp_inc_press)

        self.min_temp_label = Label(color=[0, 0, 0, 1], text=str(self.min_temp))

        min_temp_dec_button = Button(text='Down', background_color= [0.075, 0.71, 0.918, 1], on_press=self.on_min_temp_dec_press)

        max_temp_inc_button = Button(text='Up', background_color= [0.075, 0.71, 0.918, 1], on_press=self.on_max_temp_inc_press)

        self.max_temp_label = Label(color=[0, 0, 0, 1], text=str(self.max_temp))

        max_temp_dec_button = Button(text='Down', background_color= [0.075, 0.71, 0.918, 1], on_press=self.on_max_temp_dec_press)

        temp_layout.add_widget(min_temp_inc_button)
        temp_layout.add_widget(max_temp_inc_button)
        temp_layout.add_widget(self.min_temp_label)
        temp_layout.add_widget(self.max_temp_label)
        temp_layout.add_widget(min_temp_dec_button)
        temp_layout.add_widget(max_temp_dec_button)

        layout.add_widget(temp_layout)

        time_layout = GridLayout(rows=3, cols=3, col_force_default=True, col_default_width=70, row_default_height=60)

        hour_inc_button = Button(text='Up', background_color= [0.075, 0.71, 0.918, 1], on_press=self.hour_inc_press)

        self.hour_label = Label(color=[0, 0, 0, 1], text=str(self.hour))

        hour_dec_button = Button(text='Down', background_color= [0.075, 0.71, 0.918, 1], on_press=self.hour_dec_press)

        ten_inc_button = Button(text='Up', background_color= [0.075, 0.71, 0.918, 1], on_press=self.ten_inc_press)

        self.ten_label = Label(color=[0, 0, 0, 1], text=str(self.ten))

        ten_dec_button = Button(text='Down', background_color= [0.075, 0.71, 0.918, 1], on_press=self.ten_dec_press)

        min_inc_button = Button(text='Up', background_color= [0.075, 0.71, 0.918, 1], on_press=self.min_inc_press)

        self.min_label = Label(color=[0, 0, 0, 1], text=str(self.min))

        min_dec_button = Button(text='Down', background_color= [0.075, 0.71, 0.918, 1], on_press=self.min_dec_press)

        #These are formatted so that the inc btns are the top row, labels are middle, and dec btns are bottom.
        time_layout.add_widget(hour_inc_button)
        time_layout.add_widget(ten_inc_button)
        time_layout.add_widget(min_inc_button)
        time_layout.add_widget(self.hour_label)
        time_layout.add_widget(self.ten_label)
        time_layout.add_widget(self.min_label)
        time_layout.add_widget(hour_dec_button)
        time_layout.add_widget(ten_dec_button)
        time_layout.add_widget(min_dec_button)

        layout.add_widget(time_layout)

        button_row_layout=GridLayout(cols=3, rows=1, row_force_default=True, row_default_height=40, padding=[25, 0])

        save_time_button = Button(text='Save Time', background_color= [0.075, 0.71, 0.918, 1], on_press=self.save_time)

        button_row_layout.add_widget(save_time_button)

        switch_page_button = Button(text='Switch Page', background_color= [0.075, 0.71, 0.918, 1], on_press=self.switch_page)
         
        button_row_layout.add_widget(switch_page_button)

        fan_power_button = Button(text='Fan ON/OFF', background_color= [0.075, 0.71, 0.918, 1], on_press=self.fan_power)

        button_row_layout.add_widget(fan_power_button)

        layout.add_widget(Label())  # Empty space
        layout.add_widget(Label())  # Empty space
        layout.add_widget(Label())  # Empty space
        layout.add_widget(Label())  # Empty space
        layout.add_widget(Label())  # Empty space
        layout.add_widget(button_row_layout)
        layout.add_widget(WakeScreen())

        return layout

    def on_min_temp_dec_press(self, instance):
        self.min_temp -= 1
        self.update_temp_labels()

    def on_min_temp_inc_press(self, instance):
        self.min_temp += 1
        self.update_temp_labels()

    def on_max_temp_dec_press(self, instance):
        self.max_temp -= 1
        self.update_temp_labels()

    def on_max_temp_inc_press(self, instance):
        self.max_temp += 1
        self.update_temp_labels()

    def update_temp_labels(self):
        if self.min_temp_label:
            self.min_temp_label.text = str(self.min_temp)
        if self.max_temp_label:
            self.max_temp_label.text = str(self.max_temp)

    def update_time_labels(self):
        if self.hour_label:
            self.hour_label.text = str(self.hour)
        if self.ten_label:
            self.ten_label.text = str(self.ten)
        if self.min_label:
            self.min_label.text = str(self.min)
    
    def hour_dec_press(self, instance):
        if self.hour > 1:
            self.hour -= 1
            self.update_time_labels()

    def hour_inc_press(self, instance):
        if self.hour < 24:
            self.hour += 1
            self.update_time_labels()

    def ten_dec_press(self, instance):
        if self.ten > 0:
            self.ten -= 1
            self.update_time_labels()

    def ten_inc_press(self, instance):
        self.ten += 1
        self.update_time_labels()

    def min_dec_press(self, instance):
        if self.min > 0:
            self.min -= 1
            self.update_time_labels()

    def min_inc_press(self, instance):
        self.min += 1
        self.update_time_labels()

    def sleep_timer(self, dt):
        if self.display_on:
            # Check if it's time to turn off the display
            pass

    def save_time(self, instance):
        # Create a label with the formatted time
        time_label = Label(text=f"{self.hour:02}:{self.ten}{self.min}", color=[0, 0, 0, 1])
        # Add the label to the scheduling page
        self.switch_page(instance)
        self.sched_label_list.append(time_label)
        self.root.children[0].add_widget(time_label)

    def switch_page(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(SchedulingPage(switch_home_callback=self.switch_home))

    def switch_home(self, instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(app.build())

    def fan_power(self, instance):
        output = bytes("power", 'utf-8')
        self.server_socket.sendall(output)

    def sleep_timer(self):
        global start_time
        global display_on
        start_time = time.time()
        display_on = True
        while True:
            if time.time() - start_time >= 10 and display_on:
                display_on = False
                os.popen('bash backlight_off.sh')

   

if __name__ == '__main__':
    SmartFanApp().run()