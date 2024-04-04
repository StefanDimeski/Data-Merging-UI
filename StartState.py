from State import State
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import pandas as pd
from tkinter import messagebox
from utils import process_files
from tkinter import ttk

# For further documentation, visit State.py

class StartState(State):
    def __init__(self, data):
        super().__init__(data)

    # Creates all the widgets and sets the layout
    def enter(self, root):
        super().enter(root)
    
        self.class_msg = tk.Message(root, text="CLASS File: ", width=600-10, bg=self.data.background_clr, font=("Arial", 10))
        self.class_msg.pack(anchor="nw", pady=(5, 0), padx=(5, 0))

        self.class_btn_msg_frame = tk.Frame(root, bg=self.data.background_clr)
        self.class_btn_msg_frame.pack(anchor="nw", padx=25)

        self.class_open_btn = tk.Button(self.class_btn_msg_frame, text="Open", command=lambda: self.open_file("CLASS"))
        self.class_open_btn.pack(side=tk.LEFT)

        self.class_filename_message = tk.Message(self.class_btn_msg_frame, text=self.data.class_filename, width=600-10, bg=self.data.background_clr, font=("Arial", 10))
        self.class_filename_message.pack()

        ####

        self.cds_msg = tk.Message(root, text="CDS Files: ", width=600-10, bg=self.data.background_clr, font=("Arial", 10))
        self.cds_msg.pack(anchor="nw", padx=(5, 0), pady=(10, 0))

        self.cds_services_frame = tk.Frame(root, bg=self.data.background_clr)
        self.cds_services_frame.pack(anchor="nw", padx=15)

        ##

        self.cds_service1_frame = tk.Frame(self.cds_services_frame, bg=self.data.background_clr)
        self.cds_service1_frame.pack(anchor="nw")

        self.cds_service1_msg = tk.Message(self.cds_service1_frame, text="Demographic data:", width=600-10, bg=self.data.background_clr)
        self.cds_service1_msg.pack(anchor="nw")

        self.cds_service1_btn_msg_frame = tk.Frame(self.cds_service1_frame, bg=self.data.background_clr)
        self.cds_service1_btn_msg_frame.pack(anchor="nw", padx=20)

        self.cds_service1_open_btn = tk.Button(self.cds_service1_btn_msg_frame, text="Open", command=lambda: self.open_file("CDS Demographic Data"))
        self.cds_service1_open_btn.pack(side=tk.LEFT)

        self.cds_service1_filename_message = tk.Message(self.cds_service1_btn_msg_frame, text=self.data.cds_demographic_filename, width=600-10, bg=self.data.background_clr, font=("Arial", 10))
        self.cds_service1_filename_message.pack()

        ##

        self.cds_service2_frame = tk.Frame(self.cds_services_frame, bg=self.data.background_clr)
        self.cds_service2_frame.pack(anchor="nw")
        
        self.cds_service2_msg = tk.Message(self.cds_service2_frame, text="Service 2:", width=600-10, bg=self.data.background_clr)
        self.cds_service2_msg.pack(anchor="nw")

        self.cds_service2_btn_msg_frame = tk.Frame(self.cds_service2_frame, bg=self.data.background_clr)
        self.cds_service2_btn_msg_frame.pack(anchor="nw", padx=20)

        self.cds_service2_open_btn = tk.Button(self.cds_service2_btn_msg_frame, text="Open", command=lambda: self.open_file("CDS Service 2"))
        self.cds_service2_open_btn.pack(side=tk.LEFT)

        self.cds_service2_filename_message = tk.Message(self.cds_service2_btn_msg_frame, text=self.data.cds_service2_filename, width=600-10, bg=self.data.background_clr, font=("Arial", 10))
        self.cds_service2_filename_message.pack()

        ##

        self.cds_service3_frame = tk.Frame(self.cds_services_frame, bg=self.data.background_clr)
        self.cds_service3_frame.pack(anchor="nw")
        
        self.cds_service3_msg = tk.Message(self.cds_service3_frame, text="Service 3:", width=600-10, bg=self.data.background_clr)
        self.cds_service3_msg.pack(anchor="nw")

        self.cds_service3_btn_msg_frame = tk.Frame(self.cds_service3_frame, bg=self.data.background_clr)
        self.cds_service3_btn_msg_frame.pack(anchor="nw", padx=20)

        self.cds_service3_open_btn = tk.Button(self.cds_service3_btn_msg_frame, text="Open", command=lambda: self.open_file("CDS Service 3"))
        self.cds_service3_open_btn.pack(side=tk.LEFT)

        self.cds_service3_filename_message = tk.Message(self.cds_service3_btn_msg_frame, text=self.data.cds_service3_filename, width=600-10, bg=self.data.background_clr, font=("Arial", 10))
        self.cds_service3_filename_message.pack()

        ##

        self.cds_service4_frame = tk.Frame(self.cds_services_frame, bg=self.data.background_clr)
        self.cds_service4_frame.pack(anchor="nw")
        
        self.cds_service4_msg = tk.Message(self.cds_service4_frame, text="Service 4:", width=600-10, bg=self.data.background_clr)
        self.cds_service4_msg.pack(anchor="nw")

        self.cds_service4_btn_msg_frame = tk.Frame(self.cds_service4_frame, bg=self.data.background_clr)
        self.cds_service4_btn_msg_frame.pack(anchor="nw", padx=20)
        
        self.cds_service4_open_btn = tk.Button(self.cds_service4_btn_msg_frame, text="Open", command=lambda: self.open_file("CDS Service 4"))
        self.cds_service4_open_btn.pack(side=tk.LEFT)

        self.cds_service4_filename_message = tk.Message(self.cds_service4_btn_msg_frame, text=self.data.cds_service4_filename, width=600-10, bg=self.data.background_clr, font=("Arial", 10))
        self.cds_service4_filename_message.pack()

        # create a frame for the encoding selection section
        encoding_frame = tk.Frame(root, bg=self.data.background_clr)
        encoding_frame.pack(padx=3, pady=(20, 5), anchor="nw", side=tk.LEFT)

        # frame used to position the combobox and message at the top of the encoding_frame
        encoding_frame_inner = tk.Frame(encoding_frame, bg=self.data.background_clr)
        encoding_frame_inner.pack(side=tk.TOP, pady=3)

        encoding_msg = tk.Message(encoding_frame_inner, width=100, text="Encoding: ", bg=self.data.background_clr)
        encoding_msg.pack(side=tk.LEFT)

        # create the combobox which allows the user to select the encoding
        self.encoding_list = ttk.Combobox(encoding_frame_inner, state="readonly", values=["cp1252", "utf-8"])
        # set "cp1252" as the encoding selected by default
        self.encoding_list.current(0)
        self.encoding_list.pack(side=tk.LEFT)

        self.process_btn = tk.Button(root, text="Process", command=self.process_btn_pressed, state="disabled")
        self.process_btn.pack(anchor="ne", padx=(0, 13), pady=(20, 5))

    def exit(self):
        super().exit()

    def open_file(self, source):
        filename_to_open = fd.askopenfilename(title=f"Choose the file with data from {source} source",
                                    filetypes=(("Excel file (.xlsx) or CSV (.csv)", ".xlsx .csv"),
                                               ("Excel file (.xlsx)", ".xlsx"),
                                               ("Comma Separated Values file (.csv)", ".csv")))
        
        if filename_to_open == "":
            return
        
        if source == "CLASS":
            self.data.class_filename = filename_to_open
            self.class_filename_message.configure(text=filename_to_open)
        elif source == "CDS Demographic Data":
            self.data.cds_demographic_filename = filename_to_open
            self.cds_service1_filename_message.configure(text=filename_to_open)
        elif source == "CDS Service 2":
            self.data.cds_service2_filename = filename_to_open
            self.cds_service2_filename_message.configure(text=filename_to_open)
        elif source == "CDS Service 3":
            self.data.cds_service3_filename = filename_to_open
            self.cds_service3_filename_message.configure(text=filename_to_open)
        elif source == "CDS Service 4":
            self.data.cds_service4_filename = filename_to_open
            self.cds_service4_filename_message.configure(text=filename_to_open)

        if self.data.class_filename != "None" and self.data.cds_demographic_filename != "None":
            self.process_btn.configure(state="normal")
        


    # Called when the "Process using defaults" button is pressed. It reads the defaults from the defaults.json
    # file and pops out a file dialog so that you choose where to save. Then it processes the file and saves
    # it as chosen.
    def process_btn_pressed(self):
        # saving file dialog
        filename_to_save = fd.asksaveasfilename(title="Save as", defaultextension=".xlsx",
                                                filetypes=(("Excel file", ".xlsx"),), confirmoverwrite=True, initialfile="aggregated_file")
        
        # if cancel was pressed, do nothing
        if filename_to_save == "":
            return
        
        # process the file using all of the gathered parameters
        final_df = process_files(self.data.class_filename,
                                 self.data.cds_demographic_filename,
                                 self.data.cds_service2_filename,
                                 self.data.cds_service3_filename,
                                 self.data.cds_service4_filename,
                                 self.encoding_list.get())

        # there was a column selected that does not exist in this file. Most likely the defaults
        # contain a column that is not present in this file. Do nothing in this case and just display
        # the error message
        #if final_df is None:
        #    messagebox.showerror("Error! Column does not exist in file!",
        #             "One or more columns selected for processing do not exist in this file. Please go to the Customise screen where they will be highlighted in red.")
        #    return

        # save the file
        final_df.to_excel(filename_to_save, index=False)
        showinfo(title="Success!", message="File has been successfully created!")

    # # Called when the "Customise" button gets pressed. Performs a state transition to the Customise state
    # def customise_btn_pressed(self):
    #     self.transition(CustomiseState(self.data))

    # # Called when the "Edit the defaults" button gets pressed. Performs a state transition to the Defaults
    # # state
    # def edit_defaults_btn_pressed(self):
    #     self.transition(DefaultsState(self.data))