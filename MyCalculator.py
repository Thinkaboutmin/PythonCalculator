#! python3

# TkInterSixth.py - A calculator capable of realising small problems
# Made by Thinkaboutmin

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
except ImportError:
    raise Exception("Unavailable tkinter module")

import logging
import copy
# Configure the logging for debugging. Default is CRITICAL
logging.basicConfig(level="DEBUG", format="%(lineno)s - %(levelname)s: %(message)s ")
logging.debug("Start of the calculator")


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
        [self.buttons.append(ttk.Button(self.mainframe, text=str(i))) for i in range(10)]

        __sings = ["+", "-", "=", "÷", "×", "√x", "ˣ√x", "C", "CA", "←", "xˣ", "x²", ",", "∓"]
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
        logging.debug("Initializing window configuration")

        self.master.resizable(False, False)
        self.master.title("Calculator")
        ttk.Style().configure("W.TEntry", foreground="black")
        ttk.Style().map("TEntry", fieldbackground=[("readonly", "white")])
        ttk.Style().configure("ClickBtn.TButton", relief="sunken")
        ttk.Style().configure("UnclickBtn.TButton", relief="raised")
        ttk.Style().configure(".", background="#606060")

        logging.debug("Window configuration was run entirely")

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
        self.special_buttons["∓"].grid(column=1, row=5)
        self.special_buttons[","].grid(column=2, row=5)

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

        self.special_buttons["←"].bind_all("<Key-BackSpace>", lambda _: self.__visor_del("←"))
        self.special_buttons["C"].bind_all("<Key-Delete>", lambda _: self.__visor_del("C"))
        self.special_buttons["CA"].bind_all("<Key-End>", lambda _: self.__visor_del("CA"))

        self.special_buttons["+"].bind_all("<Key-KP_Add>", lambda x: self.__common_task(x))
        self.special_buttons["+"].bind_all("<Key-plus>", lambda x: self.__common_task(x))
        self.special_buttons["-"].bind_all("<Key-KP_Subtract>", lambda x: self.__common_task(x))
        self.special_buttons["-"].bind_all("<Key-minus>", lambda x: self.__common_task(x))
        self.special_buttons["÷"].bind_all("<Key-division>", lambda x: self.__common_task(x))
        self.special_buttons["÷"].bind_all("<Key-slash>"), lambda x: self.__common_task(x)
        self.special_buttons["÷"].bind_all("<Key-KP_Divide>", lambda x: self.__common_task(x))
        self.special_buttons["×"].bind_all("<Key-KP_Multiply>", lambda x: self.__common_task(x))
        self.special_buttons["×"].bind_all("<Key-asterisk>", lambda x: self.__common_task(x))
        self.special_buttons["∓"].bind_all("<Key-Control_L>", lambda _: self._pos_to_neg())
        self.special_buttons[","].bind_all("<Key-comma>", lambda _: self.__visor_comma_adder())

        self.special_buttons["="]["command"] = self.__calculus
        self.special_buttons["+"]["command"] = lambda: self.__common_task("+")
        self.special_buttons["-"]["command"] = lambda: self.__common_task("-")
        self.special_buttons["÷"]["command"] = lambda: self.__common_task("/")
        self.special_buttons["×"]["command"] = lambda: self.__common_task("*")
        self.special_buttons["←"]["command"] = lambda: self.__visor_del("←")
        self.special_buttons["C"]["command"] = lambda: self.__visor_del("C")
        self.special_buttons["CA"]["command"] = lambda: self.__visor_del("CA")
        self.special_buttons["∓"]["command"] = self._pos_to_neg
        self.special_buttons[","]["command"] = self.__visor_comma_adder

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
            self.storage["value1"] = self._visor_humanizer(text=self.visor_value.get(), humanizer=False)
            self._visor_alter(s=True)

        self.__button_effect(self.special_buttons[__operator])
        logging.debug("End of the common task - {}".format(self.storage))

    def __calculus(self):
        """Realizes the actual calculus of the calculator"""
        logging.debug("Initializing calculus")
        if self.storage["operator"]:
            logging.debug("Calculus state of self.storage - {}".format(self.storage))
            self.storage["value2"] = self._visor_humanizer(text=self.visor_value.get(), humanizer=False)
            exec("try: picker=str(" + self.storage["value1"] + self.storage["operator"] + self.storage["value2"] + ")"
                 "\n"
                 "except ZeroDivisionError: picker='0'"
                 "\n"
                 "self._visor_alter(self._visor_humanizer(text=picker, humanizer=True), True)"
                 )
            self.storage["operator"] = ""
            self.storage["result"] = self._visor_humanizer(text=self.visor_value.get(), humanizer=False)
            logging.debug("End of state of self.storage - {}".format(self.storage))
            if self.storage["result"]:
                self.storage["value1"] = self.storage["result"]
        else:
            self.storage["value1"] = self._visor_humanizer(text=self.visor_value.get(), humanizer=False)
            self.storage["result"] = self.storage["value1"]
        self.__button_effect(self.special_buttons["="])

    def _visor_alter(self, v="0", s=False):
        """Alters the visor value and moves the cursor to the last number"""

        if not s:
            tmp_text = self._visor_humanizer(self.visor_value.get() + v, humanizer=False)
            tmp_text = self._visor_humanizer(text=tmp_text, humanizer=True)
            self.visor_value.set(tmp_text)
            self.visor.xview_moveto(len(self.visor_value.get()) + 1)
        else:
            self.visor_value.set(v)
            self.storage["result"] = ""

    def __visor_del(self, from_):
        """Deletes values from the visor entirely, partially or everything from variables"""

        operator = self.__event_finder(from_)

        if operator == "←":
            tmp_text = self._visor_humanizer(self.visor_value.get()[0: -1], humanizer=False)
            tmp_text = self._visor_humanizer(text=tmp_text, humanizer=True)
            self.visor_value.set(tmp_text)
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
        try:
            self.__button_effect(self.special_buttons[operator])
        except KeyError:
            self.__button_effect(b"" + self.special_buttons[operator])

    def __visor_comma_adder(self):
        self.visor_value.set(self.__comma_adder(self.visor_value.get()))

    @staticmethod
    def __comma_adder(text):
        """Verifies if there's a need for a comma else it adds one"""
        logging.debug("Starting _comma_adder")
        comma_iden = False

        for i in text:
            if i == ",":
                comma_iden = True
            else:
                continue

        if not comma_iden:
            logging.debug("Possible to add comma")
            text += ","

        else:
            logging.debug("Impossible to add another comma")

        logging.debug("Ending _comma_adder")
        return text

    @staticmethod
    def _visor_humanizer(text, humanizer):
        """Transforms the value on the visor as it increases and decreases"""
        # TODO Rename variables for a better understanding of what's happening
        # TODO Investigate further possibilities for this algorithm

        if humanizer:
            logging.debug("Transforming text value into human readable")
            dissabler = []
            times = 0
            tmp_dissabler = []

            text = text.replace(".", ",")

            for i in reversed(text):
                times += 1
                tmp_dissabler.append(i)
                logging.debug("The tmp value: {}".format(tmp_dissabler))
                if i == ",":
                    dissabler.append(copy.copy(tmp_dissabler))
                    tmp_dissabler = []
                    times = 0

                    for k in dissabler:
                        for m in k:
                            tmp_dissabler.append(m)
                    logging.debug("The tmp value: {}".format(tmp_dissabler))
                    dissabler = [copy.copy(tmp_dissabler)]
                    tmp_dissabler = []

                elif times == 3:
                    dissabler.append(copy.copy(tmp_dissabler))
                    tmp_dissabler = []
                    times = 0

                else:
                    continue
            dissabler.append(copy.copy(tmp_dissabler))

            text = ""
            usual = 3
            min_usual = 1

            logging.debug("Dissabler value before: {}".format(dissabler))

            only_nums = False
            for k, i in enumerate(dissabler):
                for o in i:
                    try:
                        int(o)
                    except ValueError:
                        only_nums = True
                if len(i) == usual and len(dissabler[k + 1]) >= min_usual and not only_nums:
                    i.append(".")

                only_nums = False
            for i in reversed(dissabler):
                for m in reversed(i):
                    text += m
            logging.debug("Dissabler value after: {}".format(dissabler))
        else:
            logging.debug("Transforming text value into a computer readable")

            text = text.replace(".", "")
            text = text.replace(",", ".")

        logging.debug("Text value: {}".format(text))
        logging.debug("Transforming ended")
        return text

    def _pos_to_neg(self):
        """Transform the actual value to a negative number"""

        if self.visor_value.get() != "0":
            if not self.visor_value.get()[0] == "-":
                self.visor_value.set("-" + self.visor_value.get())
            else:
                self.visor_value.set(self.visor_value.get()[1:])

        self.__button_effect(self.special_buttons["∓"])

    @staticmethod
    def __button_effect(btn):
        """Adds the clicked and focus effect on buttons"""
        btn["style"] = "ClickBtn.TButton"
        btn.after(100, lambda: [None for btn["style"] in ["UnclickBtn.TButton"]])
        btn.focus_set()

    @staticmethod
    def __event_finder(evt):
        """Finds the event of the button"""
        logging.debug("Initialiazing __event_finder")

        if isinstance(evt, tk.Event):
            evt = str(evt)
            evt = evt.split()
            evt = evt[5].split("char='" and "'")
            __operator = evt[1]
        else:
            __operator = evt

        logging.debug("Result of the __event_finder: {}".format(__operator))
        logging.debug("End of the __event_finder")

        return __operator


root = tk.Tk()
Calculator(root)
root.mainloop()
logging.debug("End of the calculator")
