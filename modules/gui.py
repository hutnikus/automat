import tkinter
from typing import Dict
from PIL import Image, ImageTk
from modules.automat import Automat
from modules.row import Row
from tkinter.filedialog import askopenfile

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


class Item(Row):
    def __init__(self, x, y, automat, row, frame, image_path="images/empty.png"):
        if row is not None:
            super().__init__(row.quantity, row.price, row.goods)
        self.image_path = image_path
        frame.update()
        self.width = frame.winfo_width() / len(automat.items)
        self.height = frame.winfo_height() / len(automat.items[0])
        self.parent_frame = frame

        self.x, self.y = x, y
        self.automat = automat

        self.empty = row is None
        
        self.create_widget(x, y, frame)

    def create_widget(self, x, y, frame):
        if self.empty:
            color = "grey"
        else:
            color = "green"
        self.create_frame(x, y, frame,color)
        self.create_name_label()
        self.create_image()
        self.create_price_label()
        

    def create_frame(self,x,y,frame,color):
        self.frame = tkinter.Frame(frame, background=color, width=self.width, height=self.height)
        self.frame.place(x=x * self.width, y=y * self.height)
        self.frame.bind("<Button-1>", lambda event: self.on_click(event))

    def create_name_label(self):
        text = ""
        if not self.empty:
            text = self.goods
        self.frame.update()
        self.name_label = tkinter.Label(self.frame,
                                        text=text,
                                        font=("Arial", 12),
                                        background=self.frame.configure("background")[-1])
        self.name_label.place(x=self.frame.winfo_width() / 2, y=self.frame.winfo_height() / 2 - 65, anchor="center")
        self.name_label.bind("<Button-1>", lambda event: self.on_click(event))

    def create_image(self):
        self.frame.update()
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((100, 100), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label = tkinter.Label(self.frame,
                                         background=self.frame.configure("background")[-1])
        self.image_label.place(x=self.frame.winfo_width() / 2, y=self.frame.winfo_height() / 2, anchor="center")
        if not self.empty:
            self.image_label.config(image=self.image)
        self.image_label.bind("<Button-1>", lambda event: self.on_click(event))
        

    def create_price_label(self):
        price = ""
        if not self.empty:
            price = f"{self.price}€"
        self.frame.update()
        self.price_label = tkinter.Label(self.frame,
                                         text=price,
                                         font=("Arial", 12),
                                         background=self.frame.configure("background")[-1])
        self.price_label.place(x=self.frame.winfo_width() / 2, y=self.frame.winfo_height() / 2 + 65, anchor="center")
        self.price_label.bind("<Button-1>", lambda event: self.on_click(event))
        

    def destroy(self):
        self.frame.destroy()

    def update(self,row):
        self.destroy()
        self.__init__(self.x, self.y, self.automat, row, self.parent_frame)

    def on_click(self, event):
        self.frame.update()
        if self.parent_frame.selected_item is not None :
            self.parent_frame.selected_item.frame.config(highlightthickness = 0)
            self.parent_frame.selected_item.frame.update()
        self.frame.config(highlightbackground = "blue", highlightthickness = 5)
        self.parent_frame.selected_item = self
        ...  # TODO


class GUI(tkinter.Tk):
    automat_frame = None  # left part of the window, shows automat visually
    management_frame = None  # right part of the window, contains buttons and widgets
    insert_coins_frame = None  # (user mode) frame for inserting coins
    cash_return_frame = None  # (user mode) frame for returning coins
    modify_product_frame = None  # (admin mode) frame for modifying products
    cash_register_frame = None  # (admin mode) frame for modifying cash register
    automat_items_frame = None  # frame for displaying products
    automat_balance_frame = None  # frame for displaying worth of inserted coins
    automat_return_frame = None  # frame for displaying bought items

    mode_button = None  # button for changing mode
    card_button = None  # (user mode) button for paying with card
    storno_button = None  # (user mode) button for cancelling payment with cash
    coins_buttons = None  # (user mode) dict of buttons for inserting coins ("2€" - <Button>)
    product_image_button = None  # (admin mode) button for changing product image
    submit_changes_button = None  # (admin mode) button for submitting changes in product

    cash_return_canvas = None  # (user mode) canvas for showing returned coins
    automat_insert_canvas = None  # decorative canvas for place to pay with cash
    automat_card_canvas = None  # decorative canvas for place to pay with card

    name_entry = None  # (admin mode) entry for changing product name
    price_entry = None  # (admin mode) entry for changing product price

    quantity_spinner = None  # (admin mode) spinner for changing product quantity
    cash_spinners = None  # (admin mode) dict of spinners for changing product quantity ("2€" - <Spinbox>)

    actual_cash_label = None  # (admin mode) label for showing actual balance in automat
    inserted_balance_label = None  # label for showing worth of inserted coins

    def __init__(self, automat:Automat):
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
            self.destroy_admin_widgets()
            self.create_customer_widgets()
            self.mode = "Zákazník"
        else:
            self.mode = "Admin"
            self.destroy_customer_widgets()
            self.create_admin_widgets()
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
        # todo
        ...

    def create_general_management_frame(self, bg, position, text):
        if position == "top":
            y = self.height - self.padding * 3 - self.height * (2 / 5)
        else:
            y = self.height - self.padding

        frame = tkinter.Frame(self.management_frame, background=bg)
        frame.place(x=self.padding,
                    y=y,
                    width=self.width / 2 - self.padding * 2,
                    height=self.height * (2 / 5),
                    anchor="sw")
        label = tkinter.Label(frame,
                              text=text,
                              font=("Helvetica", 15, "bold"),
                              background=bg)
        label.place(x=self.padding, y=self.padding, anchor="nw")
        return frame

    def create_insert_coins_frame(self):
        self.insert_coins_frame = self.create_general_management_frame("yellow", "top", "Vhodiť mince")
        self.create_coins_buttons()

    def create_coins_buttons(self):
        self.coins_buttons = dict()
        for i in range(2):
            for j in range(4):
                self.create_coin_button(i, j)
        self.create_storno_button()

    def create_coin_button(self, i, j):
        coin = list(coins.keys())[i * 4 + j]
        self.coins_buttons[coin] = tkinter.Button(self.insert_coins_frame,
                                                  text=coin,
                                                  command=lambda: self.coin_button_clicked(coin),
                                                  width=10,
                                                  height=2,
                                                  font=("Helvetica", 12))
        self.coins_buttons[coin].place(x=self.padding + j * (self.width / 2 - self.padding * 2) / 4,
                                       y=50 + i * (self.height * (2 / 5) - self.padding * 3) / 2,
                                       anchor="nw")

    def coin_button_clicked(self, coin):
        self.automat.insertCoin(coin.replace("€", "e"))
        self.setBalance(self.automat.cashRegister.getBufferSum())

    def create_storno_button(self):
        self.update()
        self.storno_button = tkinter.Button(self.insert_coins_frame,
                                            text="STORNO",
                                            command=self.storno_button_clicked,
                                            width=20,
                                            height=1,
                                            font=("Helvetica", 12))
        self.storno_button.place(x=self.insert_coins_frame.winfo_width() / 2,
                                 y=self.insert_coins_frame.winfo_height() / 2 + self.padding,
                                 anchor="center")

    def storno_button_clicked(self):
        returnedCoins = self.automat.cashRegister.returnCoins()
        self.draw_cash_return(returnedCoins)
        self.setBalance(0)
        print(returnedCoins)

    def create_cash_return_frame(self):
        self.cash_return_frame = self.create_general_management_frame("red", "bottom", "Výdavok")
        self.create_cash_return_canvas()

    def create_cash_return_canvas(self):
        self.update()
        self.cash_return_canvas = tkinter.Canvas(self.cash_return_frame,
                                                 width=self.cash_return_frame.winfo_width(),
                                                 height=self.cash_return_frame.winfo_height(),
                                                 background="pink")
        self.cash_return_canvas.place(x=0, y=self.padding * 5, anchor="nw")

    def draw_cash_return(self, coins:dict):
        self.cash_return_canvas.update()
        self.cash_return_canvas.delete('all')
        padding = 5
        diameter = 70
        x = 0
        y = padding
        numberOfCoins = sum(coins.values())
        while True :
            width = int(self.cash_return_canvas.winfo_width() / (diameter + 2 * padding))
            height = int(self.cash_return_canvas.winfo_height() / (diameter + padding)) - 1
            print(width * height)
            if numberOfCoins > width * height :
                diameter -= 5
            else:
                break


        for coin in coins : 
            for i in range(coins[coin]):
                x += padding
                self.draw_coin(coin.replace("e", "€"), x , y, diameter)
                x += diameter
                if x+diameter >= self.cash_return_canvas.winfo_width() :
                    y += padding + diameter
                    x = 0

    def draw_coin(self, coin, x, y, diameter):
        self.cash_return_canvas.create_oval(x, y, x + diameter, y + diameter, fill= 'yellow')
        self.cash_return_canvas.create_text(x + diameter/2, y + diameter/2, text=coin, anchor='center', font=("Helvetica", 12))


    def destroy_customer_widgets(self):
        self.card_button.destroy()
        self.cash_return_frame.destroy()
        self.insert_coins_frame.destroy()

    def create_admin_widgets(self):
        self.create_modify_product_frame()
        self.create_modify_product_widgets()
        self.create_cash_register_frame()
        self.create_cash_register_widgets()

    def create_modify_product_frame(self):
        self.modify_product_frame = self.create_general_management_frame("yellow", "top", "Zvolený produkt")

    def create_modify_product_widgets(self):
        self.name_entry = self.create_entry_with_label(self.padding, 50, "Názov:", self.modify_product_frame)
        self.price_entry = self.create_entry_with_label(self.padding, 100, "Cena:", self.modify_product_frame)
        self.quantity_spinner = self.create_spinner_with_label(250, 50, "Množstvo:", self.modify_product_frame)
        self.product_image_button = self.create_image_button(350, 100, 100, 100, "images/empty.png",
                                                             self.modify_product_frame,
                                                             self.product_image_button_clicked)

        self.submit_changes_button = tkinter.Button(self.modify_product_frame,
                                                    text="Potvrdiť zmeny",
                                                    command=self.submit_changes_button_clicked,
                                                    width=20,
                                                    height=1,
                                                    font=("Helvetica", 12))
        self.submit_changes_button.place(x=150,
                                         y=self.modify_product_frame.winfo_height() / 2 + 50,
                                         anchor="center")

    def submit_changes_button_clicked(self):
        item = self.automat_items_frame.selected_item
        if item is not None:
            if not item.empty:
                item.update(item)

        ...  # todo

    def create_entry_with_label(self, x, y, label_text, frame):
        label = tkinter.Label(frame,
                              text=label_text,
                              font=("Helvetica", 12),
                              background=frame.configure("background")[-1])
        label.place(x=x, y=y, anchor="nw")
        entry = tkinter.Entry(frame,
                              width=15,
                              font=("Helvetica", 12))
        self.update()
        entry.place(x=50 + label.winfo_x() + self.padding,
                    y=y,
                    anchor="nw")
        return entry

    def create_spinner_with_label(self, x, y, label_text, frame, width=5, method=lambda x: None, methodArgs=None):
        label = tkinter.Label(frame,
                              text=label_text,
                              font=("Helvetica", 12),
                              background=frame.configure("background")[-1])
        label.place(x=x, y=y, anchor="nw")
        spinner = tkinter.Spinbox(frame,
                                  from_=0,
                                  to=100,
                                  width=width,
                                  font=("Helvetica", 12),
                                  command=lambda: method(methodArgs))
        self.update()
        spinner.place(x=label.winfo_width() + label.winfo_x() + self.padding,
                      y=y,
                      anchor="nw")
        return spinner

    @staticmethod
    def create_image_button(x, y, width, height, image_path, frame, command):
        img = Image.open(image_path)
        resized = img.resize((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(resized)
        button = tkinter.Button(frame,
                                image=image,
                                command=command,
                                width=image.width(),
                                height=image.height())
        button.image = image
        button.place(x=x, y=y, anchor="nw")
        return button

    def product_image_button_clicked(self):
        file_path = askopenfile(mode='r', filetypes=[('Image Files', '*jpeg'), ('Image Files', '*jpg'), ('Image Files', '*png')])
        print(file_path)
        if file_path is None:
            return
        # set image on button
        self.product_image_button.destroy()
        self.product_image_button = self.create_image_button(350, 100, 100, 100, file_path.name, 
                                                                self.modify_product_frame,
                                                                self.product_image_button_clicked)
                                                                
        # set image on card
        ...  # todo

    def create_cash_register_frame(self):
        self.cash_register_frame = self.create_general_management_frame("red", "bottom", "Kasa")

    def create_cash_register_widgets(self):
        self.update()
        self.actual_cash_label = tkinter.Label(self.cash_register_frame,
                                               text=f"Aktuálne: {self.automat.cashRegister.getCoinsSum():.2f}€",
                                               font=("Helvetica", 15, "bold"),
                                               background=self.cash_register_frame.configure("background")[-1])
        self.actual_cash_label.place(x=self.cash_register_frame.winfo_width() - self.padding, y=self.padding,
                                     anchor="ne")

        self.create_cash_register_spinners()

    def update_actual_cash_label(self):
        self.actual_cash_label.configure(text=f"Aktuálne: {self.automat.cashRegister.getCoinsSum():.2f}€")
        self.update()

    def create_cash_register_spinners(self):
        keys = list(coins.keys())
        self.cash_spinners = {}
        for i in range(2):
            for j in range(4):
                key = keys[i * 4 + j]
                self.cash_spinners[key] = self.create_spinner_with_label(
                    self.padding + j * 100, 70 + i * 80, key,
                    self.cash_register_frame, 3, self.change_cash_spinner_value, key)

        self.update_spinners()

    def change_cash_spinner_value(self, key):
        self.cash_spinners[key].update()
        value = self.cash_spinners[key].get()
        self.automat.cashRegister.coins[key.replace("€", "e")] = int(value)
        self.update_actual_cash_label()

    def update_spinners(self):
        values = self.automat.cashRegister.coins.copy()
        for key in self.cash_spinners:
            self.cash_spinners[key].delete(0, tkinter.END)
            self.cash_spinners[key].insert(0, values[key.replace("€", "e")])

    def destroy_admin_widgets(self):
        self.modify_product_frame.destroy()
        self.cash_register_frame.destroy()

    def create_automat_widgets(self):
        self.create_automat_frame()
        self.create_automat_items_frame()
        self.create_automat_items_widgets()
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
        self.automat_items_frame.selected_item = None

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

        self.automat_insert_canvas.create_line(17, 10, 17, 40, width=5)
        self.automat_insert_canvas.create_line(17, 60, 17, 90, width=5)
        self.automat_insert_canvas.create_arc(10, 70, 24, 90, start=0, extent=-180, style="arc", width=5)
        self.automat_insert_canvas.create_rectangle(40, 30, 60, 60, fill="red", outline="black", width=3)

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
                                        width=(self.width / 2 - 100) - 2 * padding,
                                        height=100,
                                        anchor="sw")
        self.automat_return_frame.configure(background="brown")

    def create_automat_items_widgets(self):
        self.items = [[Item(i, j, self.automat, item, self.automat_items_frame) for j, item in enumerate(row)] for
                      i, row in enumerate(self.automat.items)]
        print(self.items)
        ...  # TODO
