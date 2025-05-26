from tkinter import *
import customtkinter
from typing import Union, Callable
import main
import os

class MyScrollableCheckboxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []
        self.spinboxes = []

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value, command=self.checked)
            checkbox.grid(row=((i+1)*2)-1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)
            spinbox = FloatSpinbox(self, width=150, step_size=1)
            self.spinboxes.append(spinbox)
            
    def checked(self):
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.get() == 1:
                self.spinboxes[i].set((i+1)*7)
                self.spinboxes[i].grid(row=(i+1)*2, column=0, padx=10, pady=(10, 0), sticky="w")
            else:
                self.spinboxes[i].grid_forget()

    def get(self):
        checked_checkboxes = []
        checked_spinboxes = []
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.get():
                checked_checkboxes.append(checkbox.cget("text"))
                if self.spinboxes[i].get():
                    checked_spinboxes.append(self.spinboxes[i].get())
        return checked_checkboxes, checked_spinboxes
    
class MyScrollableRadiobuttonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value="")

        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)

class FloatSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "0")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Energy Analyzer")
        self.geometry("720x480")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.radiobutton_frame = MyScrollableRadiobuttonFrame(self, "Options", values=["EU", "US"])
        self.radiobutton_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")
        self.radiobutton_frame.configure(fg_color="transparent")
        self.checkbox_frame = MyScrollableCheckboxFrame(self, "Scenarios", values=["Change Nodes", "Change Application"])
        self.checkbox_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew")
        self.checkbox_frame.configure(fg_color="transparent")
        
        self.button = customtkinter.CTkButton(self, text="Run Analyzer", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def button_callback(self):
        print("radio frame:", self.radiobutton_frame.get())
        print("checkbox frame:", self.checkbox_frame.get())
        #print("valuees:", self.)

app = App()
app.mainloop()