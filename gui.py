from tkinter import filedialog, messagebox
import customtkinter
from typing import Union, Callable
import main
import os

class MyScrollableApplicationFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
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
    
class MyScrollableInfrastructureFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.values = values
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value="")
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # for i, value in enumerate(self.values):
        #     radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.variable)
        #     radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
        #     self.radiobuttons.append(radiobutton)
        
        self.open_button = customtkinter.CTkButton(self, text="Open File", command=self.open_file)
        self.open_button.grid(row=0, column=0, padx=50, pady=(10, 0), sticky="w")
        self.save_button = customtkinter.CTkButton(self, text="Save File", command=self.save_file)
        self.save_button.grid(row=0, column=1, padx=50, pady=(10, 0), sticky="w")

        self.textbox = customtkinter.CTkTextbox(self, wrap="word")
        self.textbox.grid(row=1, column=0, columnspan=2, padx=25, pady=(25, 0), sticky="nsew")

        self.current_file = None

    def get(self):
        return self.textbox.get("1.0", "end-1c")

    def set(self, value):
        self.variable.set(value)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.textbox.delete("1.0", "end")
                self.textbox.insert("1.0", content)
                self.current_file = file_path
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file:\n{e}")

    def save_file(self):
        if self.current_file:
            file_path = self.current_file
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if not file_path:
                return

        try:
            content = self.textbox.get("1.0", "end-1c")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Success", f"File saved to:\n{file_path}")
            self.current_file = file_path
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")

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

        self.configure(fg_color=("gray78", "gray28"))

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

class FirstPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.radiobutton_frame = MyScrollableInfrastructureFrame(self, "Infrastructure Upload", values=["EU", "US"])
        self.radiobutton_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")
        self.radiobutton_frame.configure(fg_color="transparent")
        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=1)
        # self.checkbox_frame = MyScrollableApplicationFrame(self, "Scenarios", values=["Change Nodes", "Change Application"])
        # self.checkbox_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew")
        # self.checkbox_frame.configure(fg_color="transparent")
        
        self.button = customtkinter.CTkButton(self, text="Go to Application Upload", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def button_callback(self):
        print(self.radiobutton_frame.get())
        self.controller.show_page("SecondPage")

class SecondPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.radiobutton_frame = MyScrollableInfrastructureFrame(self, "Application Upload", values=["EU", "US"])
        self.radiobutton_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")
        self.radiobutton_frame.configure(fg_color="transparent")
        # self.checkbox_frame = MyScrollableApplicationFrame(self, "Scenarios", values=["Change Nodes", "Change Application"])
        # self.checkbox_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew")
        # self.checkbox_frame.configure(fg_color="transparent")
        
        self.buttonback = customtkinter.CTkButton(self, text="Back to Infrastructure Upload", command=self.button_back)
        self.buttonback.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.buttonforward = customtkinter.CTkButton(self, text="Go to Deployment Upload", command=self.button_forward)
        self.buttonforward.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

    def button_back(self):
        self.controller.show_page("FirstPage")

    def button_forward(self):
        self.controller.show_page("ThirdPage")

class ThirdPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.radiobutton_frame = MyScrollableInfrastructureFrame(self, "Deployment Upload", values=["EU", "US"])
        self.radiobutton_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")
        self.radiobutton_frame.configure(fg_color="transparent")
        # self.checkbox_frame = MyScrollableApplicationFrame(self, "Scenarios", values=["Change Nodes", "Change Application"])
        # self.checkbox_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew")
        # self.checkbox_frame.configure(fg_color="transparent")
        
        self.buttonback = customtkinter.CTkButton(self, text="Back to Application Upload", command=self.button_back)
        self.buttonback.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.buttonforward = customtkinter.CTkButton(self, text="Go to Deployment Upload", command=self.button_forward)
        self.buttonforward.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

    def button_back(self):
        self.controller.show_page("SecondPage")

    def button_forward(self):
        self.controller.show_page("FourthPage")

class FourthPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = customtkinter.CTkLabel(self, text="This is the second page!", font=customtkinter.CTkFont(size=20))
        label.pack(pady=20)

        back_button = customtkinter.CTkButton(self, text="Back to Editor", command=lambda: controller.show_page("ThirdPage"))
        back_button.pack()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Energy Analyzer")
        self.geometry("1080x600")
        self.container = customtkinter.CTkFrame(self, width=1080, height=600)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.pages = {}

        for PageClass in (FirstPage, SecondPage, ThirdPage, FourthPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[page_name] = frame

        self.show_page("FirstPage")
    
    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()

app = App()
app.mainloop()