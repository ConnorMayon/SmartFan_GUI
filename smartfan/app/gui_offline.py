from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
from smartfan.data.local_weather import Climate
from smartfan.prediction.prediction import Prediction
import urllib.parse
import urllib.request
import threading
import os
import time
import asyncio
import socket
from argparse import _SubParsersAction

def define_argparser(command_parser: _SubParsersAction):
    """
    Define `run` subcommand.
    """
    p = command_parser.add_parser(
        'run_offline', help='run smartfan app')

    p.set_defaults(handler=lambda args: run())


class SchedulingPage(GridLayout):
    def __init__(self, switch_home_callback, sched_list, **kwargs):
        super().__init__(**kwargs)
        self.cols = 5
        self.rows = 10
        self.col_force_default=True
        self.col_default_width=90
        self.sched_list=sched_list
        self.message=""
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label(color=[0,0,0,1], halign='center', bold=True, text='Scheduling Page'))
        self.add_widget(Label())
        home_btn=Button(text='Home', background_color= [0.075, 0.71, 0.918, 1], on_press=switch_home_callback)
        self.add_widget(home_btn)
        if len(self.sched_list) != 0:
            for item in sched_list:
                label = Label(text=item)
                self.add_widget(label)
            #self.send_message("savedtime", self.message)

class SmartFanApp(App):
    Window.clearcolor = (1, 1, 1, 1)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min_temp_label = None
        self.max_temp_label = None

    def build(self):
        self.page = 0
        self.display_on = True
        self.min_temp = 65
        self.max_temp = 85
        self.hour = 5
        self.ten = 0
        self.min = 0
        self.cd_timer = 0
        self.sched_list = []
        self.sched_label_list = []
        #self.forecast = Forecast()
        self.in_climate = Climate("Indoors", "44:fe:00:00:0e:d5")
        self.out_climate = Climate("Outdoors", "44:8d:00:00:00:23")
        self.acctemp_array = [32, 30, 29, 28, 30, 31, 32, 29, 33, 25, 31, 33]
        self.prediction = Prediction(self.min_temp, self.max_temp, self.in_climate, self.out_climate, self.acctemp_array)
        #self.acctemp_array = self.forecast.getTemperatureFahrenheit()
        self.acc_temp = self.acctemp_array[0]
        self.acc_temp = 30
        self.in_temp  = 0
        self.out_temp = 0
        self.fan_state = False
        self.user_pressed = False

        # # Conn
        HOST = '192.168.1.161'    # The remote host
        PORT = 50007              # The same port as used by the server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((HOST, PORT))

        layout = GridLayout(cols=2, rows=6, row_force_default=True, col_force_default= True, col_default_width=350, row_default_height=50)

        title_lable_layout = GridLayout(cols=2, col_force_default=True, col_default_width=305, row_force_default=True, row_default_height=40)

        range_label=Label(color=[0, 0, 0, 1], bold=True, text="Set Perferred Temperature Range")

        title_lable_layout.add_widget(range_label)

        sched_label=Label(color=[0, 0, 0, 1], bold=True, text="Set Perferred Cooling Time / Cooldown Timer")

        title_lable_layout.add_widget(sched_label)
        
        layout.add_widget(title_lable_layout)
        layout.add_widget(Label()) # Empty space

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

        time_layout = GridLayout(rows=3, cols=4, col_force_default=True, col_default_width=70, row_default_height=60)

        hour_inc_button = Button(text='Up', background_color= [0.075, 0.71, 0.918, 1], on_press=self.on_hour_inc_press)

        self.hour_label = Label(color=[0, 0, 0, 1], text=str(self.hour))

        hour_dec_button = Button(text='Down', background_color= [0.075, 0.71, 0.918, 1], on_press=self.on_hour_dec_press)

        ten_inc_button = Button(text='Up', background_color= [0.075, 0.71, 0.918, 1], on_press=self.on_ten_inc_press)

        self.ten_label = Label(color=[0, 0, 0, 1], text=str(self.ten))

        ten_dec_button = Button(text='Down', background_color= [0.075, 0.71, 0.918, 1], on_press=self.on_ten_dec_press)

        min_inc_button = Button(text='Up', background_color= [0.075, 0.71, 0.918, 1], on_press=self.on_min_inc_press)

        self.min_label = Label(color=[0, 0, 0, 1], text=str(self.min))

        min_dec_button = Button(text='Down', background_color= [0.075, 0.71, 0.918, 1], on_press=self.on_min_dec_press)
        
        cd_timer_inc_button = Button(text='Up', background_color= [0.075, 0.71, 0.918, 1], on_press=self.on_cd_timer_inc_press)

        self.cd_timer_label = Label(color=[0, 0, 0, 1], text=str(self.cd_timer))

        cd_timer_dec_button = Button(text='Down', background_color= [0.075, 0.71, 0.918, 1], on_press=self.on_cd_timer_dec_press)

        #These are formatted so that the inc btns are the top row, labels are middle, and dec btns are bottom.
        time_layout.add_widget(hour_inc_button)
        time_layout.add_widget(ten_inc_button)
        time_layout.add_widget(min_inc_button)
        time_layout.add_widget(cd_timer_inc_button)
        time_layout.add_widget(self.hour_label)
        time_layout.add_widget(self.ten_label)
        time_layout.add_widget(self.min_label)
        time_layout.add_widget(self.cd_timer_label)
        time_layout.add_widget(hour_dec_button)
        time_layout.add_widget(ten_dec_button)
        time_layout.add_widget(min_dec_button)
        time_layout.add_widget(cd_timer_dec_button)

        layout.add_widget(time_layout)

        button_row_layout=GridLayout(cols=3, rows=2, row_force_default=True, row_default_height=40, padding=[25, 0])

        save_time_button = Button(text='Save Time', background_color= [0.075, 0.71, 0.918, 1], on_press=self.save_time)

        button_row_layout.add_widget(save_time_button)

        switch_page_button = Button(text='Switch Page', background_color= [0.075, 0.71, 0.918, 1], on_press=self.switch_page)
         
        button_row_layout.add_widget(switch_page_button)

        fan_power_button = Button(text='Fan ON/OFF', background_color= [0.075, 0.71, 0.918, 1], on_press=self.fan_power)

        button_row_layout.add_widget(fan_power_button)

        update_button = Button(text='Update', background_color= [0.075, 0.71, 0.918, 1], on_press=self.make_request)

        button_row_layout.add_widget(update_button)

        layout.add_widget(Label())  # Empty space
        layout.add_widget(Label())  # Empty space
        layout.add_widget(Label())  # Empty space
        layout.add_widget(Label())  # Empty space
        layout.add_widget(Label())  # Empty space
        layout.add_widget(Label())  # Empty space
        layout.add_widget(button_row_layout)

        temperature_layout = GridLayout(rows=2, cols=3, col_force_default=True, col_default_width=70, row_default_height=60)

        acc_title = Label(color=[0, 0, 0, 1], text= "Forecast")
        self.acc_label = Label(color=[0, 0, 0, 1], text=str(self.acc_temp))

        in_title = Label(color=[0, 0, 0, 1], text= "Inside")
        self.in_label = Label(color=[0, 0, 0, 1], text="Connecting")

        out_title = Label(color=[0, 0, 0, 1], text= "Outside")
        self.out_label = Label(color=[0, 0, 0, 1], text="Connecting")
        temperature_layout.add_widget(acc_title)
        temperature_layout.add_widget(in_title)
        temperature_layout.add_widget(out_title)
        
        temperature_layout.add_widget(self.acc_label)
        temperature_layout.add_widget(self.in_label)
        temperature_layout.add_widget(self.out_label)
        
        layout.add_widget(temperature_layout)
        
        it_thread = threading.Thread(target=self.update_inside_temp).start()
        ot_thread = threading.Thread(target=self.update_outside_temp).start()
        pred_thread = threading.Thread(target=self.get_prediction).start()
        #update_thread = threading.Thread(target=self.make_request).start()

        return layout
 
    def fan_power(self, instance = None):
        output = bytes("power", 'utf-8')
        self.server_socket.sendall(output)
        self.fan_state = not self.fan_state
        if instance != None:
            self.user_pressed = True
 
    def get_prediction(self):
        while True:
            pred_result = self.prediction.predict()
            if pred_result and not self.fan_state and self.cd_timer != 0:
                self.fan_power()
            if not pred_result and self.fan_state and self.cd_timer != 0:
                self.fan_power()
                
            time.sleep(1)
            
            if self.user_pressed and self.cd_timer != 0:
                time.sleep(self.cd_timer * 60)
                self.user_pressed = False

    def make_request(self, instance):
        # Make a GET request
        # url = 'http://10.3.62.239:8000/data'
        url = 'http://192.168.1.18:8000/data'
        #while True:
        self.request = UrlRequest(url, on_success=self.on_success, on_failure=self.on_failure)
            #sleep(5)

    def on_failure(self, request, error):
        print("Request failed:", error)
        
    def on_cd_timer_dec_press(self, instance):
        self.cd_timer -= 1
        if self.cd_timer == 0:
            self.cd_timer_label.text = "Off"
        elif self.cd_timer == -1:
            self.cd_timer = 0
        else:
            self.cd_timer_label.text = str(self.cd_timer)
        
    def on_cd_timer_inc_press(self, instance):
        self.cd_timer += 1
        self.cd_timer_label.text = str(self.cd_timer)

    def on_min_temp_dec_press(self, instance):
        self.min_temp -= 1
        self.prediction.update_range_min(self.min_temp)
        self.update_temp_labels()
        self.send_message()

    def on_min_temp_inc_press(self, instance):
        if self.min_temp < self.max_temp:
            self.min_temp += 1
            self.prediction.update_range_min(self.min_temp)
            self.update_temp_labels()
            self.send_message()

    def on_max_temp_dec_press(self, instance):
        if self.min_temp < self.max_temp:
            self.max_temp -= 1
            self.prediction.update_range_max(self.max_temp)
            self.update_temp_labels()
            self.send_message()

    def on_max_temp_inc_press(self, instance):
        self.max_temp += 1
        self.prediction.update_range_max(self.max_temp)
        self.update_temp_labels()
        self.send_message()

    def on_success(self, request, result):
        print("Received data:", result)
        self.web_update_temp(result)
        self.web_update_time(result)
    
    def on_hour_dec_press(self, instance):
        self.hour -= 1
        if self.hour == -1:
            self.hour = 23
        self.update_time_labels()
        self.send_message()

    def on_hour_inc_press(self, instance):
        self.hour += 1
        if self.hour == 24:
            self.hour = 0
        self.update_time_labels()
        self.send_message()

    def on_ten_dec_press(self, instance):
        self.ten -= 1
        if self.ten == -1:
            self.ten = 5
        self.update_time_labels()
        self.send_message()

    def on_ten_inc_press(self, instance):
        self.ten += 1
        if self.ten == 6:
            self.ten = 0
        self.update_time_labels()
        self.send_message()

    def on_min_dec_press(self, instance):
        self.min -= 1
        if self.min == -1:
            self.min = 9
        self.update_time_labels()
        self.send_message()

    def on_min_inc_press(self, instance):
        self.min += 1
        if self.min == 10:
            self.min = 0
        self.update_time_labels()
        self.send_message()

    #needs update after changes
    def save_time(self, instance):
        # Create a label with the formatted time
        time_value=f"{self.hour:02}:{self.ten}{self.min}"
        self.sched_list.append(time_value)
        #self.send_message('saveTime', time_value)
        # Add the label to the scheduling page
        self.switch_page(instance)
        self.root.children[0].add_widget(Label(text=time_value, color=[0, 0, 0, 1]))

    #needs update after changes
    def switch_page(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(SchedulingPage(sched_list=self.sched_list, switch_home_callback=self.switch_home))

    #needs update after changes
    def switch_home(self, instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(app.build())
   
    def send_message(self):
        # Base URL of the server
        # url = 'http://10.3.62.239:8000/log'
        url = 'http://192.168.1.18:8000/log'

        # Construct the query string
        query_params = urllib.parse.urlencode({
        'min_temp': self.min_temp,
        'max_temp': self.max_temp,
        'hour': self.hour,
        'ten': self.ten,
        'minute': self.min
        }).encode('utf-8')

        req = urllib.request.Request(url, data=query_params)

        # Send the request
        with urllib.request.urlopen(req) as response:
            response = response.read().decode('utf-8')
            
    def get_prediction(self):
        fan_state = False
        while True:
            if self.prediction.predict() and not fan_state:
                fan_state = True
                self.fan_power()
            if not self.prediction.predict() and fan_state:
                fan_state = False
                self.fan_power()
            time.sleep(540)
            
    def update_inside_temp(self):
        while True:
            asyncio.run(self.in_climate.sensorClient())
            self.in_temp  = self.in_climate.getTempF()
            if self.in_label:
                self.in_label.text = str(self.in_temp)
            time.sleep(1)
            
    def update_outside_temp(self):
        while True:
            asyncio.run(self.out_climate.sensorClient())
            self.out_temp = self.out_climate.getTempF()
            if self.out_label:
                self.out_label.text = str(self.out_temp)
            time.sleep(1)
            
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
            
    def web_update_temp(self, results):
        self.min_temp = results.get('minTempValue')
        self.max_temp = results.get('maxTempValue')
        self.update_temp_labels()

    def web_update_time(self, results):
        self.hour = results.get('hoursValue')
        self.ten = results.get('tenMinutesValue')
        self.min = results.get('minutesValue')
        self.update_time_labels()
            


def run():
    #os.popen('xset dpms 15 15 15')  # Set screen blanking to 15 seconds
    
    # Set window to full screen
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'window_state', 'maximized')
    Config.write()
    
    SmartFanApp().run()
