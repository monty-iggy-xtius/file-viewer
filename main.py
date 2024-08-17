# imports for the project
from CTkMessagebox import CTkMessagebox
from bs4 import BeautifulSoup as bs
from tkinter import _tkinter
import customtkinter as ctk
import random
import tkinter as tk
import pandas as pd
import PyPDF2
import json
import time
import os
import csv
import sys

WIDTH, HEIGHT, DISPLAY_WINDOW_WIDTH, DISPLAY_WINDOW_HEIGHT = "820", "260", "886", "514"
valid_extensions = [".c", ".csv", ".html", ".htm",
                    ".java", ".js", ".pdf", ".py", ".php", ".json", ".txt", ".xml", ".md"]

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# app constants
APP_TITLE = "i3 FILE VIEWER"
LABEL_FONT = ("Monospace", 24, "bold")
SCROLL_WINDOW_FONT = ("Verdana", 11)
BUTTON_FONT = ("Verdana", 13)
GENERAL_FONT = ("Verdana", 12)
BUTTON_WIDTH = 200
PDF_ERROR = "\t  error encountered in displaying this pdf file"
GENERAL_ERROR = "\t sorry....unable to decode some characters in your file "
EMPTY_ENTRY_ERROR = "EMPTY ENTRY DETECTED"
FILE_OPEN_ERROR = "FILE ERROR"
EXTENSION_NOT_SUPPORTED_ERROR = "Extension not supported"

# configure application themes
ctk.set_default_color_theme("green")
ctk.set_appearance_mode("dark")


def display_file_contents(received_file):
    """
    This function creates the window for displaying data in a valid file. It makes use of a top-level widget so that it doesn't cause errors to the parent widget when closed/destroyed.
    """
    # final message will be concatenated to a string to make the whole data
    final_message = ''

    # optional backgrounds for the data display window
    data_bg = random.choice(["#0d1f23", "gray12"])

    # using a top level widget dissipates the error
    data_display_window = ctk.CTkToplevel()
    data_display_window.geometry("{}x{}".format(
        DISPLAY_WINDOW_WIDTH, DISPLAY_WINDOW_HEIGHT))

    # the name of the current open file will be te window title
    data_display_window.title(received_file.split("\\")[-1])

    try:
        data_display_window.iconbitmap("icons/logo.ico")
    except _tkinter.TclError as err:
        # print(err)
        pass
    finally:
        data_display_window.resizable(False, False)

        data_display_frame = ctk.CTkFrame(
            data_display_window, corner_radius=0, fg_color=data_bg)
        data_display_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

        scroll_window = ctk.CTkTextbox(
            data_display_frame,
            font=GENERAL_FONT,
            # tuple for light theme and dark theme
            fg_color=("#ffffff", data_bg),
            wrap="word",
            activate_scrollbars=False,
            corner_radius=3
        )
        scroll_window.place(relx=0, rely=0, relwidth=0.99, relheight=1)

        # create a scroll bar for lengthy text and data
        data_scroll_bar = ctk.CTkScrollbar(
            data_display_frame,
            # bg_color="#403d39",  # background of the scrollbar
            # actual color of the scrollbar
            button_hover_color=("#0d1f23", "#f9844a"),
            command=scroll_window.yview
        )
        data_scroll_bar.place(
            relx=0.99, rely=0.1, relheight=0.8)

        scroll_window.configure(yscrollcommand=data_scroll_bar.set)
        scroll_window.grid_columnconfigure(0, weight=1)

    # filtering content to display by file type
    if received_file.endswith(".json"):
        try:
            if "win" in sys.platform:
                data_display_window.iconbitmap("icons/code1.ico")
            with open(received_file, "r", encoding="utf-8") as file_:
                json_data = json.load(file_)
                final_message += json_data

        except Exception as err:
            print(err)
            final_message += GENERAL_ERROR

    elif received_file.endswith(".txt") or received_file.endswith(".py") or received_file.endswith(".java") or received_file.endswith(".c") or received_file.endswith(".md") or received_file.endswith(".xml") or received_file.endswith(".js") or received_file.endswith(".php"):
        try:
            if "win" in sys.platform:
                data_display_window.iconbitmap("icons/code1.ico")
            with open(received_file, "r", encoding="utf8") as file_:
                file_to_read = file_.read()
                final_message += file_to_read
        except UnicodeDecodeError:
            final_message += GENERAL_ERROR

    elif received_file.endswith(".html") or received_file.endswith(".htm"):
        try:
            if "win" in sys.platform:
                data_display_window.iconbitmap("icons/code1.ico")
            with open(received_file, "rb") as file_:
                soup_object = bs(file_, 'html.parser')
                final_message += soup_object.prettify()
        except:
            final_message += GENERAL_ERROR

    elif received_file.endswith(".pdf"):
        try:
            if "win" in sys.platform:
                data_display_window.iconbitmap("icons/pdf1.ico")
            with open(received_file, "rb") as file_:
                # create pdf object
                pdf_file = PyPDF2.PdfReader(file_)

                # get no. of pages in the pdf file
                number_of_pages = len(pdf_file.pages)

                for current_page_number in range(number_of_pages):
                    current_page = pdf_file.pages[current_page_number]
                    current_page_data = current_page.extract_text()
                    final_message += f"\n\t Page: {current_page_number} \n{current_page_data} \n"

        except:
            final_message += GENERAL_ERROR

    elif received_file.endswith(".csv"):
        try:
            if "win" in sys.platform:
                data_display_window.iconbitmap("icons/csv_icon.ico")
            csv_reader = pd.read_csv(received_file, encoding="utf8")
            final_message = csv_reader
        except Exception:
            final_message += GENERAL_ERROR

    # get content of display content window
    scroll_window.configure(state="normal")
    scroll_window.insert("1.0", final_message)
    scroll_window.configure(state="disabled")

    # display content window loop
    data_display_window.mainloop()


def error_message(name):
    """
    This function returns different error messages for different scenarios.
    """
    # check for length of error message
    if len(name) > 0:
        CTkMessagebox(
            title=FILE_OPEN_ERROR,
            message=f"Unable to open file {name}",
            icon="warning",
            option_1="Cancel",
            button_color="tomato",
            button_hover_color="#f9844a",
            fade_in_duration=0,
            sound=True
        )

    else:
        CTkMessagebox(
            title=EMPTY_ENTRY_ERROR,
            message="Filename cannot be empty",
            icon="warning",
            option_1="Close",
            button_color="#f99c39",
            button_hover_color="#f7ad64",
            fade_in_duration=0,
            sound=True
        )


def read_file(file_name):
    """
    This function checks the given file input for a valid file extension and decides what action to take.
    """
    # remove any trailing/leading spaces in the filename
    file_name = file_name.strip()
    # get extension of current file
    current_file_extension = "." + file_name.split(".")[-1]
    if len(file_name) > 0:
        if os.path.isfile(file_name):
            # check if file extension is supported
            if current_file_extension in valid_extensions:
                display_file_contents(file_name)
            else:
                CTkMessagebox(
                    title=EXTENSION_NOT_SUPPORTED_ERROR,
                    message=f"File type {current_file_extension} currently not supported",
                    icon="warning",
                    option_1="Cancel",
                    button_color="tomato",
                    button_hover_color="#f9844a",
                    fade_in_duration=0,
                    sound=True
                )
        else:
            error_message(file_name)
    else:
        error_message(file_name)


def update_time():
    """
    This function updates the time label after every 1000ms
    """
    global time_label
    current_time = time.strftime("%a %H: %M: %S")
    time_label.configure(text=current_time)
    time_label.after(1000, update_time)


def stop():
    # destroy main window and exit
    global main_window
    main_window.destroy()
    sys.exit()


def main_screen():
    """
    This is the main app window of the application.
    It takes in user input and calls the display data function.
    """
    global time_label, main_window

    main_window = ctk.CTk()
    main_window.title(APP_TITLE)
    main_window.geometry("{}x{}".format(WIDTH, HEIGHT))
    main_window.resizable(False, False)
    main_window.configure(bg="gray12")
    file_path = tk.StringVar(value='', name='file')

    try:
        main_window.iconbitmap("icons/logo.ico")
    except _tkinter.TclError as err:
        # error occurs in displaying iconbitmap on some unix systems
        # print(err)
        pass
    finally:

        # this label will display and update the time on the app
        time_label = ctk.CTkLabel(
            main_window,
            text_color="#f9844a",
            font=LABEL_FONT
        )
        time_label.place(relx=0.4, rely=0.03)

        description_label = ctk.CTkLabel(
            main_window,
            font=GENERAL_FONT,
            text_color=("#403d39", "#ffffff"),
            text="Type path to file below"
        )
        description_label.place(relx=0.049, rely=0.24)

        text_entry = ctk.CTkEntry(
            main_window,
            placeholder_text="File path here",
            placeholder_text_color=("#495057", "#f8f9fa"),
            textvariable=file_path,
            width=400
        )
        text_entry.place(relx=0.05, rely=0.37, relwidth=0.9, relheight=0.11)

        # view file button
        view_file_button = ctk.CTkButton(main_window, text="View File", font=BUTTON_FONT, width=BUTTON_WIDTH,
                                         # define colors for the button effects
                                         fg_color=("#6b9080", "#196e73"),
                                         hover_color="#449a9a",
                                         # pass data from the text entry widget
                                         command=lambda: read_file(file_path.get()))

        view_file_button.place(relx=0.23, rely=0.56)

        exit_button = ctk.CTkButton(main_window, text="Exit", font=BUTTON_FONT, width=BUTTON_WIDTH,
                                    # define colors for the button effects
                                    fg_color=("#f94144", "tomato"),
                                    hover_color=("#f9844a", "#f9844a"),
                                    command=stop)

        exit_button.place(relx=0.57, rely=0.56)

        update_time()
        # defines what happens when the x on the app is clicked
        main_window.protocol("WM_DELETE_WINDOW", stop)
        main_window.mainloop()


if __name__ == "__main__":
    main_screen()
