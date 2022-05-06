import tkinter
from PIL import Image, ImageTk

coins = {
    "2€": 2,
    "1€": 1,
    "50c": 0.5,
    "20c": 0.2,
    "10c": 0.1,
    "5c": 0.05,
    "2c": 0.02,
    "1c": 0.01
}


class GUI(tkinter.Tk):
    def __init__(self, automat):
        super().__init__()
        self.automat = automat
        self.title("Automat")
        self.width = 1000
        self.height = 600
        self.padding = 10
        self.images = dict()
        self.mode = "Zákazník"
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.create_widgets()
        self.setBalance(self.automat.cashRegister.getBufferSum())

    def create_widgets(self):
        self.create_automat_widgets()
        self.create_management_frame()
        self.create_mode_button()
        if self.mode == "Zákazník":
            self.create_customer_widgets()
        elif self.mode == "Admin":
            self.create_admin_widgets()

    def create_automat_frame(self):
        self.automat_frame = tkinter.Frame(self)
        self.automat_frame.place(x=0, y=0, width=self.width / 2, height=self.height)
        self.automat_frame.configure(background="#050505", relief="ridge")

    def create_management_frame(self):
        self.management_frame = tkinter.Frame(self)
        self.management_frame.place(x=self.width / 2, y=0, width=self.width / 2, height=self.height)
        self.management_frame.configure(background="green")

    def create_mode_button(self):
        self.mode_button = tkinter.Button(self.management_frame,
                                          text=self.mode,
                                          command=self.change_mode,
                                          width=10,
                                          height=2,
                                          font=("Helvetica", 12))
        self.mode_button.place(x=self.width / 2, y=0, anchor="ne")

    def change_mode(self):
        if self.mode == "Admin":
            self.mode = "Zákazník"
        else:
            self.mode = "Admin"
        self.mode_button.configure(text=self.mode)

    def create_customer_widgets(self):
        self.create_card_button()
        self.create_insert_coins_frame()
        self.create_cash_return_frame()

    def create_card_button(self):
        self.card_button = tkinter.Button(self.management_frame,
                                          text="Platba kartou",
                                          command=self.card_button_clicked,
                                          width=20,
                                          height=2,
                                          font=("Helvetica", 12))
        self.card_button.place(x=self.padding, y=self.padding, anchor="nw")

    def card_button_clicked(self):
        #todo
        ...

    def create_insert_coins_frame(self):
        bg = "yellow"
        self.insert_coins_frame = tkinter.Frame(self.management_frame)
        self.insert_coins_frame.place(x=self.padding,
                                      y=self.height - self.padding * 3 - self.height * (2 / 5),
                                      width=self.width / 2 - self.padding * 2,
                                      height=self.height * (2 / 5),
                                      anchor="sw")
        self.insert_coins_frame.configure(background=bg)

        label = tkinter.Label(self.insert_coins_frame,
                                text="Vhodiť mince",
                                font=("Helvetica", 15, "bold"),
                                background=bg)
        label.place(x=self.padding, y=self.padding, anchor="nw")
        self.create_coins_buttons()

    def create_coins_buttons(self):
        #todo
        ...

    def create_cash_return_frame(self):
        self.cash_return_frame = tkinter.Frame(self.management_frame)
        self.cash_return_frame.place(x=self.padding,
                                     y=self.height - self.padding,
                                     width=self.width / 2 - self.padding * 2,
                                     height=self.height * (2 / 5),
                                     anchor="sw")
        self.cash_return_frame.configure(background="red")

    def create_automat_widgets(self):
        self.create_automat_frame()
        self.create_automat_items_frame()
        self.create_automat_balance()
        self.create_automat_insert_canvas()
        self.create_automat_card_canvas()
        self.create_automat_return_frame()

    def create_automat_items_frame(self):
        self.automat_items_frame = tkinter.Frame(self.automat_frame)
        self.automat_items_frame.place(x=0,
                                       y=0,
                                       width=self.width / 2 - 100,
                                       height=self.height - 120,
                                       anchor="nw")
        self.automat_items_frame.configure(background="#aaaaaa")

    def create_automat_balance(self):
        bg = "grey"
        self.automat_balance_frame = tkinter.Frame(self.automat_frame)
        self.automat_balance_frame.place(x=self.width / 2 - self.padding,
                                         y=self.padding,
                                         width=80,
                                         height=100,
                                         anchor="ne")
        self.automat_balance_frame.configure(background=bg)

        self.inserted_balance_label = tkinter.Label(self.automat_balance_frame,
                              text="Vhodené:\n0.00€",
                              font=("Helvetica", 12, "bold"),
                              background=bg,
                              foreground="darkred")
        self.inserted_balance_label.place(x=40, y=50, anchor="center")

    def setBalance(self, balance):
        self.inserted_balance_label.configure(text=f"Vhodené:\n{balance:.2f}€")

    def create_automat_insert_canvas(self):
        self.automat_insert_canvas = tkinter.Canvas(self.automat_frame,
                                                    width=75,
                                                    height=100)
        self.automat_insert_canvas.place(x=self.width / 2 - self.padding,
                                         y=self.padding * 3 + 100,
                                         anchor="ne")

        self.automat_insert_canvas.create_line(17,10,17,40, width=5)
        self.automat_insert_canvas.create_line(17,60,17,90, width=5)
        self.automat_insert_canvas.create_arc(10,70,24,90, start=0, extent=-180, style="arc", width=5)
        self.automat_insert_canvas.create_rectangle(40,30,60,60, fill="red",outline="black",width=3)

    def create_automat_card_canvas(self):
        self.automat_card_canvas = tkinter.Canvas(self.automat_frame,
                                                  width=75,
                                                  height=100,
                                                  background="grey")
        self.automat_card_canvas.place(x=self.width / 2 - self.padding,
                                       y=self.padding * 5 + 200,
                                       anchor="ne")

        img = Image.open("images/contactless.png")
        resized = img.resize((75, 70), Image.ANTIALIAS)

        self.images["card"] = ImageTk.PhotoImage(resized)
        self.automat_card_canvas.create_image(37, 50, anchor="center", image=self.images["card"])

    def create_automat_return_frame(self):
        padding = self.padding * 5
        self.automat_return_frame = tkinter.Frame(self.automat_frame)
        self.automat_return_frame.place(x=padding,
                                        y=self.height - self.padding,
                                        width=(self.width / 2 - 100) - 2*padding,
                                        height=100,
                                        anchor="sw")
        self.automat_return_frame.configure(background="brown")