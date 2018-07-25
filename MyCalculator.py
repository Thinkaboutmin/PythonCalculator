#! python3

# MyCalculator.py - A calculator capable of realising small problems
# Made by Thinkaboutmin

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
except ImportError:
    raise Exception("Unavailable tkinter module")

import logging


class Calculator:
    def __init__(self, master=None):
        logging.debug("Initializing Calculator")

        self.master = master
        self.__window_conf()

        self.mainframe = ttk.Frame(master)
        self.mainframe.grid()

        self.about = tk.Menu(self.mainframe)
        self.ab_program = tk.Menu(self.mainframe, tearoff=0)
        self.__top_menu_commands()

        self.buttons = []
        [self.buttons.append(ttk.Button(self.mainframe, text=i)) for i in range(10)]

        __sings = ["+", "-", "=", "÷", "×", "√x", "ˣ√x", "C", "CA", "←", "xˣ", "x²", ","]
        self.special_buttons = {i:
                                ttk.Button(self.mainframe, text="{}".format(i))
                                \
                                for i in __sings
                                }
        self.special_buttons[r"\r"] = self.special_buttons["="]
        self.special_buttons["/"] = self.special_buttons["÷"]
        self.special_buttons["*"] = self.special_buttons["×"]

        self.visor_value = tk.StringVar()
        self.visor_value.set("0")
        self.visor = ttk.Entry(self.mainframe, width=40, style="W.TEntry",
                               textvariable=self.visor_value)
        self.visor["state"] = "readonly"
        self.visor.grid(row=0, columnspan=5)
        self.visor["font"] = ("TimesNewRoman", "20")

        self.storage = {
            "operator": "",  # Grabs the operator
            "value1": "",  # Grabs the first value
            "value2": "",  # Grabs the second value
            "result": ""  # The final result
        }

        self.__binds_gen()
        self.__buttons_organizer()

        logging.debug("init was run entirely")

    def __window_conf(self):
        """Configures the window, such as colors and styles from ttk"""
        logging.debug("Initializing window confing")

        self.master.resizable(False, False)
        self.master.title("Calculator")
        ttk.Style().configure("W.TEntry", foreground="black")
        ttk.Style().map("TEntry", fieldbackground=[("readonly", "white")])
        ttk.Style().configure("ClickBtn.TButton", relief="sunken")
        ttk.Style().configure("UnclickBtn.TButton", relief="raised")
        ttk.Style().configure(".", background="#606060")

        logging.debug("Window config was run entirely")

    def __buttons_organizer(self):
        """Organizes the buttons"""
        logging.debug("Initializing organizer")

        control = 0
        col = 0
        raw = 1
        while True:
            val = control
            try:
                if val != 0:
                    self.buttons[val].grid(column=col, row=raw, pady=5)
                else:
                    self.buttons[val].grid(column=1, row=4, pady=5)
                    control += 1
                    continue
            except IndexError:
                break
            if control % 3 == 0:
                col = 0
                raw += 1
                control += 1
                continue
            else:
                col += 1
                control += 1
                continue
        self.special_buttons["+"].grid(column=0, row=4)
        self.special_buttons["-"].grid(column=2, row=4)
        self.special_buttons["="].grid(column=3, row=1)
        self.special_buttons["÷"].grid(column=3, row=2)
        self.special_buttons["×"].grid(column=3, row=3)
        self.special_buttons["←"].grid(column=4, row=1)
        self.special_buttons["C"].grid(column=4, row=2)
        self.special_buttons["CA"].grid(column=4, row=3)

        logging.debug("button organizer was run entirely")

    def __binds_gen(self):
        """Generates all the necessary binds for the buttons"""
        logging.debug("Initializing buttons gen")

        [
            i.bind_all("<Key-KP_{}>".format(i["text"]), self.__visor_adder)
            and
            i.bind_all("<Key-{}>".format(i["text"]), self.__visor_adder)
            for i in self.buttons
        ]
        for i in self.buttons:
            i["command"] = lambda o=i["text"]: self.__visor_adder(o)

        self.special_buttons["="].bind_all("<Key-Return>", lambda _: self.__calculus())
        self.special_buttons["="].bind_all("<Key-equal>", lambda _: self.__calculus())

        self.special_buttons["←"].bind_all("<Key-BackSpace>", lambda x: self.__visor_del(x))
        self.special_buttons["C"].bind_all("<Key-Delete>", lambda x: self.__visor_del(x))
        self.special_buttons["CA"].bind_all("<Key-End>", lambda x: self.__visor_del(x))

        self.special_buttons["+"].bind_all("<Key-KP_Add>", lambda x: self.__common_task(x))
        self.special_buttons["+"].bind_all("<Key-plus>", lambda x: self.__common_task(x))
        self.special_buttons["-"].bind_all("<Key-KP_Subtract>", lambda x: self.__common_task(x))
        self.special_buttons["-"].bind_all("<Key-minus>", lambda x: self.__common_task(x))
        self.special_buttons["÷"].bind_all("<Key-division>", lambda x: self.__common_task(x))
        self.special_buttons["÷"].bind_all("<Key-slash>"), lambda x: self.__common_task(x)
        self.special_buttons["÷"].bind_all("<Key-KP_Divide>", lambda x: self.__common_task(x))
        self.special_buttons["×"].bind_all("<Key-KP_Multiply>", lambda x: self.__common_task(x))
        self.special_buttons["×"].bind_all("<Key-asterisk>", lambda x: self.__common_task(x))

        self.special_buttons["="]["command"] = self.__calculus
        self.special_buttons["+"]["command"] = lambda: self.__common_task("+")
        self.special_buttons["-"]["command"] = lambda: self.__common_task("-")
        self.special_buttons["÷"]["command"] = lambda: self.__common_task("/")
        self.special_buttons["×"]["command"] = lambda: self.__common_task("*")
        self.special_buttons["←"]["command"] = lambda: self.__visor_del("←")
        self.special_buttons["C"]["command"] = lambda: self.__visor_del("C")
        self.special_buttons["CA"]["command"] = lambda: self.__visor_del("CA")

        logging.debug("Buttons gen was run")

    def __top_menu_commands(self):
        """Adds a top menu for info, version and constants"""
        logging.debug("Initializing top menu")

        # TODO Constants, options and such...
        self.ab_program.add_command(label="me", command=lambda: messagebox.showinfo("Me, a bad developer"))
        self.ab_program.add_command(label="program",
                                    command=lambda: messagebox.showinfo("Program", "A small calculator"))

        self.about.add_cascade(label="About", menu=self.ab_program)
        self.master.config(menu=self.about)

        logging.debug("Top menu was ran")

    def __visor_adder(self, from_):
        """Adds values into the visor according to the needs"""

        logging.debug("Initializing visor adder")

        __pick = self.__event_finder(from_)

        logging.debug("The number of __pick = {}".format(__pick))

        if self.visor_value.get() == "0" or self.storage["result"]:
            self._visor_alter(__pick, s=True)
            logging.debug("First time adding a number or 0")
        else:
            self._visor_alter(__pick)
            logging.debug("Adding another number")

        __pick = self.buttons[int(__pick)]
        self.__button_effect(__pick)

        logging.debug("End of visor adder")

    def __common_task(self, from_):
        """Realizes the common task of adding numbers to the storage"""
        logging.debug("Running common task")

        __operator = self.__event_finder(from_)
        if self.storage["operator"]:
            self.__calculus()
            self.storage["value2"] = ""
            self.storage["operator"] = __operator
            logging.debug("Already have a operator, here is the storage {}".format(self.storage))
        else:
            self.storage["operator"] = __operator
            self.storage["value1"] = self._comma_to_dot(self.visor_value.get(), True)
            self._visor_alter(s=True)

        self.__button_effect(self.special_buttons[__operator])
        logging.debug("End of the common task - {}".format(self.storage))

    def __calculus(self):
        """Realizes the actual calculus of the calculator"""
        logging.debug("Initializing calculus")
        if self.storage["operator"]:
            logging.debug("Calculus state of self.storage - {}".format(self.storage))
            self.storage["value2"] = self._comma_to_dot(self.visor_value.get(), True)
            exec("try: picker=str(" + self.storage["value1"] + self.storage["operator"] + self.storage["value2"] + ")"
                 "\n"
                 "except ZeroDivisionError: picker='0'"
                 "\n"
                 "self._visor_alter(self._comma_to_dot(picker), True)"
                 )
            self.storage["operator"] = ""
            self.storage["result"] = self._comma_to_dot(self.visor_value.get(), True)
            logging.debug("End of state of self.storage - {}".format(self.storage))
            if self.storage["result"]:
                self.storage["value1"] = self.storage["result"]
        else:
            self.storage["value1"] = self._comma_to_dot(self.visor_value.get(), True)
            self.storage["result"] = self.storage["value1"]
        self.__button_effect(self.special_buttons["="])
    
    def _visor_alter(self, v="0", s=False):
        """Alters the visor value and moves the cursor to the last number"""

        if not s:
            self.visor_value.set(self.visor_value.get() + v)
            self.visor.xview_moveto(len(self.visor_value.get()) + 1)
        else:
            self.visor_value.set(v)
            self.storage["result"] = ""

    def __visor_del(self, from_):
        """Deletes values from the visor entirely, partially or everything from variables"""

        operator = self.__event_finder(from_)

        if operator == "←":
            self.visor_value.set(self.visor_value.get()[0: -1])
            self.__button_effect(self.special_buttons["←"])
        elif operator == "C":
            self.visor_value.set("0")
            self.__button_effect(self.special_buttons["C"])
        else:
            self.visor_value.set("0")

            for i in self.storage.keys():
                self.storage[i] = ""

        if self.visor_value.get() == "":
            self.visor_value.set("0")

        self.__button_effect(self.special_buttons[operator])

    def _visor_humanizer(self, foo):
        """Transforms the value on the visor as it increases and decreases"""
        # TODO make a more readable screen for user
        # 144.444.444 or possibility for 14,54 and return values that can be rounded without any trouble like 14,0 to 14
        print(self, foo)
        if True:
            pass
        pass

    @staticmethod
    def _comma_to_dot(v, s=False):
        """Exchange the comma to dot when necessary"""
        # FIXME It's use is ugly and confusing, even if it's for a easy thing
        # line = {"Line": [], "Char": []}
        # cnt = 0
        # for i in v[1:]:
        #     cnt += 1
        #     if i == "." or ",":
        #         line["Line"].append(cnt)
        #         line["Char"].append(i)
            
        if not s:
            v = v.replace(".", ",")
        else:
            v = v.replace(",", ".")
        return v

    @staticmethod
    def __button_effect(btn):
        """Adds the clicked and focus effect on buttons"""
        btn["style"] = "ClickBtn.TButton"
        btn.after(100, lambda: [None for btn["style"] in ["UnclickBtn.TButton"]])
        btn.focus_set()

    @staticmethod
    def __event_finder(evt):
        """Finds the event of the button"""
        if isinstance(evt, tk.Event):
            evt = str(evt)
            evt = evt.split()
            evt = evt[5].split("char='" and "'")
            __operator = evt[1]
        else:
            __operator = evt

        return __operator


logging.basicConfig(level="CRITICAL", format="%(lineno)s - %(levelname)s: %(message)s ")
root = tk.Tk()
Calculator(root)
root.mainloop()
