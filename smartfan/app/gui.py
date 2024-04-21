from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
from kivy.uix.floatlayout import FloatLayout
from smartfan.data.local_weather import Climate
from smartfan.prediction.prediction import Prediction
from argparse import _SubParsersAction
from threading import Thread
import urllib.parse
import urllib.request
import time
import asyncio
import socket
import os


def define_argparser(command_parser: _SubParsersAction):
    """
    Define `run` subcommand.
    """
    on = command_parser.add_parser(
        'run', help='run smartfan app')

    on.set_defaults(handler=lambda args: run())
    
    off = command_parser.add_parser(
        'run_offline', help='run the smartfan app offline')

    off.set_defaults(handler=lambda args: run_offline())


class SmartFanApp(App):
    Window.clearcolor = (1, 1, 1, 1)
    def __init__(self, online, **kwargs):
        super().__init__(**kwargs)
        self.min_temp_label = None
        self.max_temp_label = None
        self.online = online

    def build(self):
        self.page = 0
        self.display_on = True
        self.min_temp = 64
        self.max_temp = 84
        self.hour = 5
        self.ten = 0
        self.min = 0
        self.web_is_pressed=False
        self.cd_timer=1
        self.sched_list = []
        self.sched_label_list = []
        self.in_climate = Climate("Indoors", "44:fe:00:00:0e:d5")
        self.out_climate = Climate("Outdoors", "44:8d:00:00:00:23")
        self.prediction = Prediction(self.min_temp, self.max_temp, self.in_climate, self.out_climate, self.online)
        self.acc_temp = 0
        self.in_temp = 0
        self.out_temp = 0
        self.fan_state = False
        self.user_pressed = False

        # Connect to fan
        HOST = '192.168.1.161'    # The remote host
        #HOST = '10.3.62.245'
        PORT = 50007
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((HOST, PORT))

        # GUI layout
        layout = FloatLayout()

        title_label = Label(text="Preferred Temperature Range", size_hint=(None, None), pos=(0, 425), color=[0, 0, 0, 1], size=(305, 40))
        layout.add_widget(title_label)

        range_label = Label(text="Preferred Cooling Time", size_hint=(None, None), pos=(250, 425), color=[0, 0, 0, 1], size=(305, 40))
        layout.add_widget(range_label)

        sched_label = Label(text="Scheduling", size_hint=(None, None), pos=(500, 425), color=[0, 0, 0, 1], size=(305, 40))
        layout.add_widget(sched_label)

        min_temp_inc_button = Button(text='Up', background_color=[0.075, 0.71, 0.918, 1], pos=(65, 355), size_hint=(None, None), size=(70, 60), on_press=self.on_min_temp_inc_press)
        layout.add_widget(min_temp_inc_button)

        max_temp_inc_button = Button(text='Up', background_color=[0.075, 0.71, 0.918, 1], pos=(170, 355), size_hint=(None, None), size=(70, 60), on_press=self.on_max_temp_inc_press)
        layout.add_widget(max_temp_inc_button)

        self.min_temp_label = Label(color=[0, 0, 0, 1], text=str(self.min_temp), pos=(65, 300), size_hint=(None, None), size=(70, 60))
        layout.add_widget(self.min_temp_label)
        
        self.hyphen_label = Label(color=[0, 0, 0, 1], text='-', pos=(115, 300), size_hint=(None, None), size=(70, 60))
        layout.add_widget(self.hyphen_label)

        self.max_temp_label = Label(color=[0, 0, 0, 1], text=str(self.max_temp), pos=(170, 300), size_hint=(None, None), size=(70, 60))
        layout.add_widget(self.max_temp_label)

        min_temp_dec_button = Button(text='Down', background_color=[0.075, 0.71, 0.918, 1], pos=(65, 245), size_hint=(None, None), size=(70, 60), on_press=self.on_min_temp_dec_press)
        layout.add_widget(min_temp_dec_button)

        max_temp_dec_button = Button(text='Down', background_color=[0.075, 0.71, 0.918, 1], pos=(170, 245), size_hint=(None, None), size=(70, 60), on_press=self.on_max_temp_dec_press)
        layout.add_widget(max_temp_dec_button)

        hour_inc_button = Button(text='Up', background_color=[0.075, 0.71, 0.918, 1], pos=(290, 355), size_hint=(None, None), size=(70, 60), on_press=self.on_hour_inc_press)
        layout.add_widget(hour_inc_button)

        ten_inc_button = Button(text='Up', background_color=[0.075, 0.71, 0.918, 1], pos=(365, 355), size_hint=(None, None), size=(70, 60), on_press=self.on_ten_inc_press)
        layout.add_widget(ten_inc_button)

        min_inc_button = Button(text='Up', background_color=[0.075, 0.71, 0.918, 1], pos=(440, 355), size_hint=(None, None), size=(70, 60), on_press=self.on_min_inc_press)
        layout.add_widget(min_inc_button)

        self.hour_label = Label(color=[0, 0, 0, 1], text=str(self.hour), pos=(290, 300), size_hint=(None, None), size=(70, 60))
        layout.add_widget(self.hour_label)
        
        self.colon_label = Label(color=[0, 0, 0, 1], text=':', pos=(327, 300), size_hint=(None, None), size=(70, 60))
        layout.add_widget(self.colon_label)

        self.ten_label = Label(color=[0, 0, 0, 1], text=str(self.ten), pos=(365, 300), size_hint=(None, None), size=(70, 60))
        layout.add_widget(self.ten_label)

        self.min_label = Label(color=[0, 0, 0, 1], text=str(self.min), pos=(440, 300), size_hint=(None, None), size=(70, 60))
        layout.add_widget(self.min_label)

        hour_dec_button = Button(text='Down', background_color=[0.075, 0.71, 0.918, 1], pos=(290, 245), size_hint=(None, None), size=(70, 60), on_press=self.on_hour_dec_press)
        layout.add_widget(hour_dec_button)

        ten_dec_button = Button(text='Down', background_color=[0.075, 0.71, 0.918, 1], pos=(365, 245), size_hint=(None, None), size=(70, 60), on_press=self.on_ten_dec_press)
        layout.add_widget(ten_dec_button)

        min_dec_button = Button(text='Down', background_color=[0.075, 0.71, 0.918, 1], pos=(440, 245), size_hint=(None, None), size=(70, 60), on_press=self.on_min_dec_press)
        layout.add_widget(min_dec_button)
        
        save_time_button = Button(text='Save Time', size_hint=(None, None), pos=(65, 160), background_color=[0.075, 0.71, 0.918, 1], size=(200, 60))
        save_time_button.bind(on_press=self.save_time)
        layout.add_widget(save_time_button)

        fan_power_button = Button(text='Fan ON/OFF', size_hint=(None, None), pos=(65, 85), background_color=[0.075, 0.71, 0.918, 1], size=(200, 60))
        fan_power_button.bind(on_press=self.fan_power)
        layout.add_widget(fan_power_button)

        acc_title = Label(color=[0, 0, 0, 1], text="Forecast", pos=(285, 175), size_hint=(None, None), size=(70, 60))
        layout.add_widget(acc_title)

        in_title = Label(color=[0, 0, 0, 1], text="Inside", pos=(385, 175), size_hint=(None, None), size=(70, 60))
        layout.add_widget(in_title)

        out_title = Label(color=[0, 0, 0, 1], text="Outside", pos=(485, 175), size_hint=(None, None), size=(70, 60))
        layout.add_widget(out_title)

        self.acc_label = Label(color=[0, 0, 0, 1], text="Connecting", pos=(285, 125), size_hint=(None, None), size=(70, 60))
        if not self.online:
            self.acc_label.text = "Offline"
        layout.add_widget(self.acc_label)

        self.in_label = Label(color=[0, 0, 0, 1], text="Connecting", pos=(385, 125), size_hint=(None, None), size=(70, 60))
        layout.add_widget(self.in_label)

        self.out_label = Label(color=[0, 0, 0, 1], text="Connecting", pos=(485, 125), size_hint=(None, None), size=(70, 60))
        layout.add_widget(self.out_label)

        self.alg_label = Label(color=[0, 0, 0, 1], text="Algorithm Timeout", pos=(620, 235), size_hint=(None, None), size=(70, 60))
        layout.add_widget(self.alg_label)

        self.cd_timer_label = Label(color=[0, 0, 0, 1], text=str(self.cd_timer), pos=(620, 120), size_hint=(None, None), size=(70, 60))
        layout.add_widget(self.cd_timer_label)

        alg_inc_button = Button(text='Up', background_color=[0.075, 0.71, 0.918, 1], pos=(620, 175), size_hint=(None, None), size=(70, 60), on_press=self.on_cd_timer_inc_press)
        layout.add_widget(alg_inc_button)

        alg_dec_button = Button(text='Down', background_color=[0.075, 0.71, 0.918, 1], pos=(620, 65), size_hint=(None, None), size=(70, 60), on_press=self.on_cd_timer_dec_press)
        layout.add_widget(alg_dec_button)
        
        # Perform background tasks
        Thread(target=self.update_inside_temp).start()
        Thread(target=self.update_outside_temp).start()
        if self.online:
            Thread(target=self.update_acc_weather).start()
        Thread(target=self.get_prediction).start()
        Thread(target=self.make_request).start()

        return layout

    def fan_power(self, instance):
        output = bytes("power", 'utf-8')
        self.server_socket.sendall(output)
        self.fan_state = not self.fan_state
        if instance != None:
            self.user_pressed = True
    
    def get_prediction(self):
        while True:
            pred_result = self.prediction.predict()
            if self.cd_timer != 0:
                if pred_result and not self.fan_state:
                    self.fan_power()
                if not pred_result and self.fan_state:
                    self.fan_power()

                if self.user_pressed:
                    time.sleep(self.cd_timer * 60)
                    self.user_pressed = False
                else:
                    time.sleep(1)

    def make_request(self):
        # Make a GET request
        #url = 'http://10.3.62.245:8000/data'
        url = 'http://192.168.1.18:8000/data'

        while True:
            self.request = UrlRequest(url, on_success=self.on_request_success, on_failure=self.on_request_failure)
            time.sleep(1)
        
    def on_cd_timer_dec_press(self, instance):
        self.cd_timer -= 1
        if self.cd_timer == 0:
            self.cd_timer_label.text = "Manual"
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
        self.update_labels()
        self.send_message()

    def on_min_temp_inc_press(self, instance):
        if self.min_temp < self.max_temp:
            self.min_temp += 1
            self.prediction.update_range_min(self.min_temp)
            self.update_labels()
            self.send_message()

    def on_max_temp_dec_press(self, instance):
        if self.min_temp < self.max_temp:
            self.max_temp -= 1
            self.prediction.update_range_max(self.max_temp)
            self.update_labels()
            self.send_message()

    def on_max_temp_inc_press(self, instance):
        self.max_temp += 1
        self.prediction.update_range_max(self.max_temp)
        self.update_labels()
        self.send_message()
        
    def on_hour_dec_press(self, instance):
        self.hour -= 1
        if self.hour == -1:
            self.hour = 23
        self.update_labels()
        self.send_message()

    def on_hour_inc_press(self, instance):
        self.hour += 1
        if self.hour == 24:
            self.hour = 0
        self.update_labels()
        self.send_message()

    def on_ten_dec_press(self, instance):
        self.ten -= 1
        if self.ten == -1:
            self.ten = 5
        self.update_labels()
        self.send_message()

    def on_ten_inc_press(self, instance):
        self.ten += 1
        if self.ten == 6:
            self.ten = 0
        self.update_labels()
        self.send_message()

    def on_min_dec_press(self, instance):
        self.min -= 1
        if self.min == -1:
            self.min = 9
        self.update_labels()
        self.send_message()

    def on_min_inc_press(self, instance):
        self.min += 1
        if self.min == 10:
            self.min = 0
        self.update_labels()
        self.send_message()
        
    def on_request_failure(self, request, error):
        print("Request failed:", error)
        
    def on_request_success(self, request, result):
        print("Received data:", result)
        self.web_is_pressed = result.get('latestSend')
        if self.web_is_pressed:
            self.web_update_vals(result)

    def save_time(self, instance):
        time_value = f"{self.hour:02}:{self.ten}{self.min}"
        if len(self.sched_label_list) >= 5:
            # Replace the oldest label
            oldest_label = self.sched_label_list.pop(0)
            self.sched_list.pop(0)
            oldest_label.text = time_value
            self.sched_label_list.append(oldest_label)
        else:
            # Add a new label
            new_label = Label(text=time_value, color=[0, 0, 0, 1], size_hint=(None, None), size=(305, 40), pos=(500, 390 - len(self.sched_list) * 30))
            self.root.add_widget(new_label)
            self.sched_label_list.append(new_label)
        self.sched_list.append(time_value)
   
    def send_message(self):
        # Base URL of the server
        #url = 'http://10.3.62.245:8000/log'
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
            
    def update_acc_weather(self):
        while True:
            acctemp_array = self.prediction.get_accuweather_temps()
            self.acc_temp = self.acctemp_array[0]
            if self.acc_temp != None:
                self.acc_label.text = str(round(self.acc_temp, 2))
            time.sleep(3600)

    def update_labels(self):
        if self.min_temp_label:
            self.min_temp_label.text = str(self.min_temp)
        if self.max_temp_label:
            self.max_temp_label.text = str(self.max_temp)
        if self.hour_label:
            self.hour_label.text = str(self.hour)
        if self.ten_label:
            self.ten_label.text = str(self.ten)
        if self.min_label:
            self.min_label.text = str(self.min)
                        
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
            
    def web_update_vals(self, results):
        self.min_temp = results.get('minTempValue')
        self.max_temp = results.get('maxTempValue')
        self.hour = results.get('hoursValue')
        self.ten = results.get('tenMinutesValue')
        self.min = results.get('minutesValue')
        self.update_labels()
            

def run():
    os.popen('xset dpms 30 30 30')  # Set screen blanking to 15 seconds
    
    # Set window to full screen
    # PUT THESE BACK BEFORE MERGE
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'window_state', 'maximized')
    Config.write()
    #Config.set('graphics', 'fullscreen', '0')
    #Config.set('graphics', 'window_state', 'normal')
    #Config.write()

    
    SmartFanApp(True).run()

def run_offline():
    os.popen('xset dpms 30 30 30')  # Set screen blanking to 15 seconds

    # Set window to full screen
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'window_state', 'maximized')
    Config.write()

    SmartFanApp(False).run()