# imports
import time
import tkinter
import PyPDF2
import os
import pandas
import csv
import random
from tkinter import scrolledtext, messagebox, _tkinter
from bs4 import BeautifulSoup as bs


width, height, small_window_width, small_window_height = "820", "260", "886", "514"
valid_extensions = [".c", ".csv", ".html", ".htm", ".java", ".js", ".pdf", ".py", ".txt", ".xml", ".md"]


# error messages
pdf_error_message = "\t  error encountered in displaying this pdf file"
other_files_error_message = "\t sorry....unable to decode some characters in your file "
empty_error_heading = "EMPTY ENTRY DETECTED"
opening_file_error = "FILE ERROR"


def shown(received_file):
    # new pop-up window to display selected content
    # global new_window
    final_message = ''
    color = random.choice(['lime', 'white', 'blue'])

    new_window = tkinter.Tk()
    new_window.geometry("{}x{}".format(small_window_width, small_window_height))
    new_window.title(received_file.split("\\")[-1])

    try:
        new_window.iconbitmap("icons/logo.ico")
    except _tkinter.TclError as err:
        print(err)
    finally:
        new_window.resizable(False, False)

        frame_1 = tkinter.Frame(new_window)

        scroll_window = tkinter.scrolledtext.ScrolledText(frame_1, width=2, height=30, wrap=tkinter.WORD)

        scroll_window.config(state="disabled", width=108,fg=color, bg="black", font=("Monospace", 11))
        scroll_window.grid(row=0, column=0)

    # filtering content to display by file type
    if received_file.endswith(".pdf"):
        try:
            new_window.iconbitmap("icons/pdf1.ico")
            with open(received_file, "rb") as file_:
                file_to_read = PyPDF2.PdfFileReader(file_)
                for pag in range(file_to_read.numPages):
                    this_page = file_to_read.getPage(pag)
                    final_message += ("\t" + "PAGE: " + str(pag + 1) +" \n" + this_page.extractText() + "\n")
        except UnicodeDecodeError:
            final_message += pdf_error_message.upper()

    elif received_file.endswith(".txt") or received_file.endswith(".py") or received_file.endswith(".java") or received_file.endswith(".c") or received_file.endswith(".md") or received_file.endswith(".xml") or received_file.endswith(".js"):
        try:
            new_window.iconbitmap("icons/code1.ico")
            with open(received_file, "r") as file_:
                file_to_read = file_.read()
                final_message += file_to_read
        except UnicodeDecodeError:
            final_message += other_files_error_message.upper()

    elif received_file.endswith(".html") or received_file.endswith(".htm"):
        try:
            new_window.iconbitmap("icons/code1.ico")
            with open(received_file, "rb") as file_:
                soup_object = bs(file_, 'html.parser')
                final_message += soup_object.prettify()
        except:
            final_message += other_files_error_message.upper()

    elif received_file.endswith(".csv"):
        try:
            new_window.iconbitmap("icons/csv_icon.ico")
            csv_reader = pandas.read_csv(received_file)
            final_message = csv_reader
        except Exception:
            final_message += other_files_error_message.upper()

    #get content of display content window
    scroll_content = scroll_window.get("1.0", "end")

    #check if there is any existing content on display window
    if len(scroll_content) > 0:
        scroll_window.config(state="normal")
        scroll_window.delete("1.0", "end")

        scroll_window.insert("1.0", final_message)
        scroll_window.config(state="disabled")

    frame_1.grid(row=0, column=0)

    #display content window loop
    new_window.mainloop()


def error_message(name):
    #check for length of error message
    if len(name) > 0:
        messagebox.showerror(opening_file_error, " Cannot open file specified as:: \n {} ".format(name))
    else:
        messagebox.showwarning(empty_error_heading, "your filename cannot be empty".capitalize())


def read_file():
    #text will be updated
    global text

    #get content of input box and check if empty
    file_name = text.get()
    if len(file_name) > 0:
        if os.path.isfile(file_name):
            for extension in valid_extensions:
                if file_name.endswith(extension):
                    shown(file_name)
        else:
            error_message(file_name)
    else:
        error_message(file_name)


def update_time():
    #update time label every second
    global time_label
    current_time = time.strftime("%a :: %H: %M: %S")
    time_label.config(text=current_time)
    time_label.after(1000, update_time)


def stop():
    #destroy main window and exit
    global main_window
    main_window.destroy()
    exit(0)


def main_screen():
    """
    main application window
    """
    global text, time_label, main_window

    main_window = tkinter.Tk()
    main_window.geometry("{}x{}".format(width, height))
    main_window.title("File viewer")
    main_window.configure(bg="gray12")
    main_window.resizable(False, False)

    try:
        main_window.iconbitmap("icons/logo.ico")
    except _tkinter.TclError as err:
        print(err)
    finally:
        main_label = tkinter.Label(text="I3Y FILE VIEWER", font=("C:/wen_mon_messed/@kiritsugu/k@ra/flights/static/flights/fontawesome-5.5/webfonts/fa-solid-900.ttf", 18, "bold"), fg="spring green2", bg="gray12")
        description_label = tkinter.Label(text="Full Path to file: ", font=("monospace", 13, "bold"), fg="spring green2", bg="gray12")
        time_label = tkinter.Label(main_window, font=("papyrus", 28, "bold"), fg="spring green2", bg="gray12")
        text = tkinter.Entry(width=73, master=main_window, font=('arial', 13))
        text.configure(fg="navyblue")
        first_button = tkinter.Button(main_window, text="SHOW CONTENT", bg="grey22",fg="spring green2", font="bold", width=21, border="1pt", command=read_file)
        exit_button = tkinter.Button(main_window, text="LEAVE APP", bg="indianred",fg="silver", font="bold", width=19, border="1pt", command=main_window.destroy)

        main_label.grid(row=0, column=1, pady=11)
        description_label.grid(row=2, column=0, padx=3, pady=10)
        time_label.grid(row=1, column=1)
        text.grid(row=2, column=1, pady=10)
        first_button.grid(row=3, column=1)
        exit_button.grid(row=4, column=1, pady=13)

        update_time()
        main_window.protocol("WM_DELETE_WINDOW", stop)
        main_window.mainloop()


if __name__ == "__main__":
    main_screen()
