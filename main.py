from tkinter import *
from tkinter import ttk

def main():
    window = Tk()
    window.title('SMARTFAN UI')
    window.geometry("800x480")  # Matches res of pi display
    window.resizable(False, False)
    frm = ttk.Frame(window, padding=10)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    button = Button(window, text="Set min temp pref", fg="white", bg="#3f91cc", font=('15'), height=5, command=window.destroy).grid(column=2, row=1)
    window.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
