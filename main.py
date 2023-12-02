import subprocess
from tkinter import *
from tkinter import ttk
from subprocess import run
import threading
import mouse
import time
import threading

global start_time
global display_on
global min_temp
global max_temp
global min_temp_str
global max_temp_str
global sched_hour
global sched_min_tens
global sched_min_ones
global sched_hour_str
global sched_min_tens_str
global sched_min_ones_str

start_time = time.time()
display_on = True
min_temp = 70
max_temp = 90
sched_hour = 12
sched_min_tens = 0
sched_min_ones = 0

def main():
    global min_temp_str
    global max_temp_str
    global sched_hour_str
    global sched_min_tens_str
    global sched_min_ones_str

    window = Tk()
    window.title('SMARTFAN GUI')
    window.geometry("800x480")  # Matches res of pi display
    window.resizable(False, False)

    min_temp_str = StringVar(window, str(min_temp))
    max_temp_str = StringVar(window, str(max_temp))
    sched_hour_str = StringVar(window, str(sched_hour))
    sched_min_tens_str = StringVar(window, str(sched_min_tens))
    sched_min_ones_str = StringVar(window, str(sched_min_ones))

    button_min_temp_inc = Button(window, text="Up", fg="white", bg="#3f91cc", font='Helvetica 14', width=4,
                                 height=1, command=inc_min_temp)
    button_min_temp_dec = Button(window, text="Down", fg="white", bg="#3f91cc", font='Helvetica 14', width=4,
                                 height=1, command=dec_min_temp)
    button_max_temp_inc = Button(window, text="Up", fg="white", bg="#3f91cc", font='Helvetica 14', width=4,
                                 height=1, command=inc_max_temp)
    button_max_temp_dec = Button(window, text="Down", fg="white", bg="#3f91cc", font='Helvetica 14', width=4,
                                 height=1, command=dec_max_temp)

    button_sched_hour_inc = Button(window, text="Up", fg="white", bg="#3f91cc", font='Helvetica 14', width=4,
                                 height=1, command=inc_sched_hour)
    button_sched_hour_dec = Button(window, text="Down", fg="white", bg="#3f91cc", font='Helvetica 14', width=4,
                                   height=1, command=dec_sched_hour)
    button_sched_min_tens_inc = Button(window, text="U", fg="white", bg="#3f91cc", font='Helvetica 14', width=2,
                                   height=1, command=inc_sched_min_tens)
    button_sched_min_tens_dec = Button(window, text="D", fg="white", bg="#3f91cc", font='Helvetica 14', width=2,
                                   height=1, command=dec_sched_min_tens)
    button_sched_min_ones_inc = Button(window, text="U", fg="white", bg="#3f91cc", font='Helvetica 14', width=2,
                                   height=1, command=inc_sched_min_ones)
    button_sched_min_ones_dec = Button(window, text="D", fg="white", bg="#3f91cc", font='Helvetica 14', width=2,
                                   height=1, command=dec_sched_min_ones)

    set_range_header = ttk.Label(text="Set prefered temperature range", font='Helvetica 12 bold')
    min_temp_disp = ttk.Label(textvariable=min_temp_str, font='15')
    max_temp_disp = ttk.Label(textvariable=max_temp_str, font='15')
    min_label = ttk.Label(text="Min temp")
    max_label = ttk.Label(text="Max temp")

    set_sched_header = ttk.Label(text="Set prefered cooling time", font='Helvetica 12 bold')
    sched_hour_disp = ttk.Label(textvariable=sched_hour_str, font='15')
    colon_label = ttk.Label(text=":", font='Helvetica 15 bold')
    sched_min_tens_disp = ttk.Label(textvariable=sched_min_tens_str, font='15')
    sched_min_ones_disp = ttk.Label(textvariable=sched_min_ones_str, font='15')

    set_range_header.place(x=125, y=100)
    min_temp_disp.place(x=165, y=205)
    button_min_temp_inc.place(x=150, y=150)
    button_min_temp_dec.place(x=150, y=250)
    min_label.place(x=148, y=305)
    max_temp_disp.place(x=290, y=205)
    button_max_temp_inc.place(x=275, y=150)
    button_max_temp_dec.place(x=275, y=250)
    max_label.place(x=273, y=305)

    set_sched_header.place(x=448, y=100)
    sched_hour_disp.place(x=485, y=205)
    button_sched_hour_inc.place(x=465, y=150)
    button_sched_hour_dec.place(x=465, y=250)
    colon_label.place(x=525, y=205)
    sched_min_tens_disp.place(x=550, y=205)
    button_sched_min_tens_inc.place(x=540, y=150)
    button_sched_min_tens_dec.place(x=540, y=250)
    sched_min_ones_disp.place(x=590, y=205)
    button_sched_min_ones_inc.place(x=585, y=150)
    button_sched_min_ones_dec.place(x=585, y=250)

    t1 = threading.Thread(target=sleep_timer)
    t2 = threading.Thread(target=check_click)
    t1.start()
    t2.start()
    window.mainloop()


def inc_min_temp():
    global min_temp
    global max_temp
    global min_temp_str
    if min_temp < max_temp:
        min_temp += 1
    min_temp_str.set(str(min_temp))


def dec_min_temp():
    global min_temp
    global max_temp
    global min_temp_str
    if min_temp > 40:
        min_temp -= 1
    min_temp_str.set(str(min_temp))


def inc_max_temp():
    global min_temp
    global max_temp
    global max_temp_str
    if max_temp < 100:
        max_temp += 1
    max_temp_str.set(str(max_temp))


def dec_max_temp():
    global min_temp
    global max_temp
    global max_temp_str
    if max_temp > min_temp:
        max_temp -= 1
    max_temp_str.set(str(max_temp))


def inc_sched_hour():
    global sched_hour
    global sched_hour_str
    if sched_hour < 23:
        sched_hour += 1
    else:
        sched_hour = 0
    sched_hour_str.set(str(sched_hour))


def dec_sched_hour():
    global sched_hour
    global sched_hour_str
    if sched_hour > 0:
        sched_hour -= 1
    else:
        sched_hour = 23
    sched_hour_str.set(str(sched_hour))


def inc_sched_min_tens():
    global sched_min_tens
    global sched_min_tens_str
    if sched_min_tens < 5:
        sched_min_tens += 1
    else:
        sched_min_tens = 0
    sched_min_tens_str.set(str(sched_min_tens))


def dec_sched_min_tens():
    global sched_min_tens
    global sched_min_tens_str
    if sched_min_tens > 0:
        sched_min_tens -= 1
    else:
        sched_min_tens = 5
    sched_min_tens_str.set(str(sched_min_tens))


def inc_sched_min_ones():
    global sched_min_ones
    global sched_min_ones_str
    if sched_min_ones < 9:
        sched_min_ones += 1
    else:
        sched_min_ones = 0
    sched_min_ones_str.set(str(sched_min_ones))


def dec_sched_min_ones():
    global sched_min_ones
    global sched_min_ones_str
    if sched_min_ones > 0:
        sched_min_ones -= 1
    else:
        sched_min_ones = 9
    sched_min_ones_str.set(str(sched_min_ones))

def sleep_timer():
    global start_time
    global display_on

    while True:
        time.sleep(1)
        if time.time() - start_time >= 15 and display_on:
            #run('vcgencmd display_power 0', shell=True)
            subprocess.run("./backlight_off.sh", shell=True)
            display_on = False


def check_click():
    global start_time
    global display_on
    while True:
        if mouse.is_pressed("left"):
            start_time = time.time()
            #run('vcgencmd display_power 1', shell=True)
            run("./backlight_off.sh", shell=True)
            display_on = True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
