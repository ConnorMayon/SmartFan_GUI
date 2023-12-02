import subprocess
from tkinter import *
from tkinter import ttk
from subprocess import run
import threading
import mouse
import time
import threading

global page
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
global sched_list
global sched_label_list

global button_min_temp_inc
global button_min_temp_dec
global button_max_temp_inc
global button_max_temp_dec
global set_range_header
global min_temp_disp
global max_temp_disp
global min_label
global max_label

global button_sched_hour_inc
global button_sched_hour_dec
global button_sched_min_tens_inc
global button_sched_min_tens_dec
global button_sched_min_ones_inc
global button_sched_min_ones_dec
global set_sched_header
global sched_hour_disp
global colon_label
global sched_min_tens_disp
global sched_min_ones_disp
global button_save_time
global button_switch_page

start_time = time.time()
page = 0
display_on = True
min_temp = 70
max_temp = 90
sched_hour = 12
sched_min_tens = 0
sched_min_ones = 0
sched_label_list = []
sched_list = []

def main():
    global min_temp_str
    global max_temp_str
    global sched_hour_str
    global sched_min_tens_str
    global sched_min_ones_str
    global button_switch_page
    global button_save_time

    window = Tk()
    window.title('SMARTFAN GUI')
    window.geometry("800x480")  # Matches res of pi display
    window.configure(background="#FFF")
    window.resizable(False, False)

    min_temp_str = StringVar(window, str(min_temp))
    max_temp_str = StringVar(window, str(max_temp))

    create_temp_range_widgets(window)
    create_sched_widgets(window)

    button_save_time = Button(window, text="Save time", fg="white", bg="#3f91cc", font='Helvetica 14', width=8,
                                 height=1, command=save_time)
    button_switch_page = Button(window, text="Switch page", fg="white", bg="#3f91cc", font='Helvetica 14', width=8,
                              height=1, command=switch_page)
    place_save_time_button()
    place_switch_page_button()

    place_temp_range_widgets()
    place_sched_widgets()

    t1 = threading.Thread(target=sleep_timer, kwargs={'window':window})
    t2 = threading.Thread(target=check_click, kwargs={'window':window})
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

def sleep_timer(window):
    global start_time
    global display_on

    while True:
        time.sleep(1)
        if time.time() - start_time >= 15 and display_on:
            hide_save_time_button()
            hide_switch_page_button()
            if page == 0:
                hide_temp_range_widgets()
                hide_sched_widgets()
            elif page == 1:
                hide_sched_label_list()

            window.configure(background="#000000")
            display_on = False


def check_click(window):
    global page
    global start_time
    global display_on
    while True:
        if mouse.is_pressed("left"):
            start_time = time.time()
            window.configure(background="#FFFFFF")
            display_on = True

            if page == 0:
                place_temp_range_widgets()
                place_sched_widgets()
                place_save_time_button()
            elif page == 1:
                place_sched_label_list()
            place_switch_page_button()


def create_temp_range_widgets(window):
    global button_min_temp_inc
    global button_min_temp_dec
    global button_max_temp_inc
    global button_max_temp_dec
    global set_range_header
    global min_temp_disp
    global max_temp_disp
    global min_label
    global max_label

    button_min_temp_inc = Button(window, text="Up", fg="white", bg="#3f91cc", font='Helvetica 14', width=4,
                                 height=1, command=inc_min_temp)
    button_min_temp_dec = Button(window, text="Down", fg="white", bg="#3f91cc", font='Helvetica 14', width=4,
                                 height=1, command=dec_min_temp)
    button_max_temp_inc = Button(window, text="Up", fg="white", bg="#3f91cc", font='Helvetica 14', width=4,
                                 height=1, command=inc_max_temp)
    button_max_temp_dec = Button(window, text="Down", fg="white", bg="#3f91cc", font='Helvetica 14', width=4,
                                 height=1, command=dec_max_temp)

    set_range_header = ttk.Label(text="Set prefered temperature range", background="#FFF", font='Helvetica 12 bold')
    min_temp_disp = ttk.Label(textvariable=min_temp_str, background="#FFF", font='Helvetica 12')
    max_temp_disp = ttk.Label(textvariable=max_temp_str, background="#FFF", font='Helvetica 12')
    min_label = ttk.Label(text="Min temp", background="#FFF")
    max_label = ttk.Label(text="Max temp", background="#FFF")

def place_temp_range_widgets():
    global button_min_temp_inc
    global button_min_temp_dec
    global button_max_temp_inc
    global button_max_temp_dec
    global set_range_header
    global min_temp_disp
    global max_temp_disp
    global min_label
    global max_label

    set_range_header.place(x=125, y=100)
    min_temp_disp.place(x=165, y=205)
    button_min_temp_inc.place(x=150, y=150)
    button_min_temp_dec.place(x=150, y=250)
    min_label.place(x=148, y=305)
    max_temp_disp.place(x=290, y=205)
    button_max_temp_inc.place(x=275, y=150)
    button_max_temp_dec.place(x=275, y=250)
    max_label.place(x=273, y=305)


def hide_temp_range_widgets():
    global button_min_temp_inc
    global button_min_temp_dec
    global button_max_temp_inc
    global button_max_temp_dec
    global set_range_header
    global min_temp_disp
    global max_temp_disp
    global min_label
    global max_label

    set_range_header.place(x=-100, y=-100)
    min_temp_disp.place(x=-100, y=-100)
    button_min_temp_inc.place(x=-100, y=-100)
    button_min_temp_dec.place(x=-100, y=-100)
    min_label.place(x=-100, y=-100)
    max_temp_disp.place(x=-100, y=-100)
    button_max_temp_inc.place(x=-100, y=-100)
    button_max_temp_dec.place(x=-100, y=-100)
    max_label.place(x=-100, y=-100)


def create_sched_widgets(window):
    global button_sched_hour_inc
    global button_sched_hour_dec
    global button_sched_min_tens_inc
    global button_sched_min_tens_dec
    global button_sched_min_ones_inc
    global button_sched_min_ones_dec
    global set_sched_header
    global sched_hour_disp
    global colon_label
    global sched_min_tens_disp
    global sched_min_ones_disp
    global button_save_time

    global sched_hour_str
    global sched_min_tens_str
    global sched_min_ones_str

    sched_hour_str = StringVar(window, str(sched_hour))
    sched_min_tens_str = StringVar(window, str(sched_min_tens))
    sched_min_ones_str = StringVar(window, str(sched_min_ones))

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
    button_save_time = Button(window, text="Save", fg="white", bg="#3f91cc", font='Helvetica 14', width=2,
                                       height=1, command=save_time)

    set_sched_header = ttk.Label(text="Set prefered cooling time", background="#FFF", font='Helvetica 12 bold')
    sched_hour_disp = ttk.Label(textvariable=sched_hour_str, background="#FFF", font='Helvetica 12')
    colon_label = ttk.Label(text=":", background="#FFF", font='Helvetica 12')
    sched_min_tens_disp = ttk.Label(textvariable=sched_min_tens_str, background="#FFF", font='Helvetica 12')
    sched_min_ones_disp = ttk.Label(textvariable=sched_min_ones_str, background="#FFF", font='Helvetica 12')


def place_sched_widgets():
    global button_sched_hour_inc
    global button_sched_hour_dec
    global button_sched_min_tens_inc
    global button_sched_min_tens_dec
    global button_sched_min_ones_inc
    global button_sched_min_ones_dec
    global set_sched_header
    global sched_hour_disp
    global colon_label
    global sched_min_tens_disp
    global sched_min_ones_disp

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


def hide_sched_widgets():
    global button_sched_hour_inc
    global button_sched_hour_dec
    global button_sched_min_tens_inc
    global button_sched_min_tens_dec
    global button_sched_min_ones_inc
    global button_sched_min_ones_dec
    global set_sched_header
    global sched_hour_disp
    global colon_label
    global sched_min_tens_disp
    global sched_min_ones_disp

    set_sched_header.place(x=-100, y=-100)
    sched_hour_disp.place(x=-100, y=-100)
    button_sched_hour_inc.place(x=-100, y=-100)
    button_sched_hour_dec.place(x=-100, y=-100)
    colon_label.place(x=-100, y=-100)
    sched_min_tens_disp.place(x=-100, y=-100)
    button_sched_min_tens_inc.place(x=-100, y=-100)
    button_sched_min_tens_dec.place(x=-100, y=-100)
    sched_min_ones_disp.place(x=-100, y=-100)
    button_sched_min_ones_inc.place(x=-100, y=-100)
    button_sched_min_ones_dec.place(x=-100, y=-100)


def save_time():
    global sched_hour_str
    global sched_min_tens_str
    global sched_min_ones_str
    global sched_list
    global sched_label_list

    time_str = sched_hour_str.get() + ':' + sched_min_tens_str.get() + sched_min_ones_str.get()

    sched_list.append(time_str)
    sched_label_list.append(ttk.Label(text=time_str, background="#FFF", font='Helvetica 15 bold'))


def place_sched_label_list():
    global sched_label_list

    hide_temp_range_widgets()
    hide_sched_widgets()

    for i, label in enumerate(sched_label_list):
        label.place(x=100, y=100+(50*i))


def hide_sched_label_list():
    global sched_label_list

    for label in sched_label_list:
        label.place(x=-100, y=-100)


def place_save_time_button():
    global button_save_time

    button_save_time.place(x=495, y=330)


def hide_save_time_button():
    global button_save_time

    button_save_time.place(x=-100, y=-100)


def place_switch_page_button():
    global button_switch_page

    button_switch_page.place(x=500, y=400)


def hide_switch_page_button():
    global button_switch_page

    button_switch_page.place(x=-100, y=-100)


def switch_page():
    global page
    if page == 0:
        hide_temp_range_widgets()
        hide_sched_widgets()
        hide_save_time_button()
        place_sched_label_list()
        page = 1
    elif page == 1:
        hide_sched_label_list()
        place_temp_range_widgets()
        place_sched_widgets()
        place_save_time_button()
        page = 0

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
