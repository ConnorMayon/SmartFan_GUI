from tkinter import *
from tkinter import ttk

global min_temp
global max_temp
global min_temp_str
global max_temp_str

min_temp = 70
max_temp = 90

def main():
    global min_temp_str
    global max_temp_str

    window = Tk()
    window.title('SMARTFAN UI')
    window.geometry("800x480")  # Matches res of pi display
    window.resizable(False, False)

    min_temp_str = StringVar(window, str(min_temp))
    max_temp_str = StringVar(window, str(max_temp))

    button_min_temp_inc = Button(window, text="Up", fg="white", bg="#3f91cc", font='10', width=4,
                                 height=1, command=inc_min_temp)
    button_min_temp_dec = Button(window, text="Down", fg="white", bg="#3f91cc", font='10', width=4,
                                 height=1, command=dec_min_temp)

    button_max_temp_inc = Button(window, text="Up", fg="white", bg="#3f91cc", font='10', width=4,
                                 height=1, command=inc_max_temp)
    button_max_temp_dec = Button(window, text="Down", fg="white", bg="#3f91cc", font='10', width=4,
                                 height=1, command=dec_max_temp)

    min_temp_disp = ttk.Label(textvariable=min_temp_str, font='15')
    max_temp_disp = ttk.Label(textvariable=max_temp_str, font='15')
    temp_range_label = ttk.Label(text="Set prefered temperature range", font='Helvetica 12 bold')
    min_label = ttk.Label(text="Min temp")
    max_label = ttk.Label(text="Max temp")

    button_min_temp_inc.place(x=100, y=100)
    button_min_temp_dec.place(x=100, y=200)
    button_max_temp_inc.place(x=225, y=100)
    button_max_temp_dec.place(x=225, y=200)
    min_temp_disp.place(x=115, y=155)
    max_temp_disp.place(x=240, y=155)
    temp_range_label.place(x=75, y=50)
    min_label.place(x=98, y=255)
    max_label.place(x=223, y=255)

    #main_screen(window)

    window.mainloop()

def main_screen(window):
    button_temp_pref = Button(window, text="Set min temp pref", fg="white", bg="#3f91cc", font=('15'), width=15, height=5)
    button_set_sched = Button(window, text="Set schedule", fg="white", bg="#3f91cc", font=('15'), width=15, height=5)

    button_temp_pref.place(x=10, y=5)
    button_set_sched.place(relx=0.6, rely=0.5, anchor=CENTER)

def temp_set_screen(window, button_list):
    for button in button_list:
        button.destroy
    frm = ttk.Frame(window, padding=10)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)

def inc_min_temp():
    global min_temp
    global min_temp_str
    min_temp += 1
    min_temp_str.set(str(min_temp))

def dec_min_temp():
    global min_temp
    global min_temp_str
    min_temp -= 1
    min_temp_str.set(str(min_temp))

def inc_max_temp():
    global max_temp
    global max_temp_str
    max_temp += 1
    max_temp_str.set(str(max_temp))

def dec_max_temp():
    global max_temp
    global max_temp_str
    max_temp -= 1
    max_temp_str.set(str(max_temp))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
