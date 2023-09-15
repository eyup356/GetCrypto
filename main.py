import json
from tkinter import messagebox

import requests
from tkinter import *
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar

window = Tk()
window.title("Crypto Price")
window.minsize(width=400, height=700)
window.config(padx=20, pady=50)
original_image = Image.open("crypto.png")
resized_image = original_image.resize((200, 200))
img = ImageTk.PhotoImage(resized_image)

panel = Label(window, image=img)
panel.config(padx=200, pady=200)
panel.pack()


key = "https://api.binance.com/api/v3/ticker/price?symbol="


currencies = [
    "BTCUSDT", "DOGEUSDT", "LTCUSDT", "ETHUSDT", "BNBUSDT",
    "XRPUSDT", "ADAUSDT", "DOTUSDT", "BCHUSDT", "LINKUSDT",
    "XLMUSDT", "TRXUSDT", "VETUSDT", "EOSUSDT", "XMRUSDT",
    "XTZUSDT", "DASHUSDT", "ZECUSDT", "UNIUSDT", "AAVEUSDT",
    "MKRUSDT", "COMPUSDT", "SOLUSDT", "ICPUSDT", "FTTUSDT",
    "AVAXUSDT", "FILUSDT", "YFIUSDT", "MATICUSDT", "CAKEUSDT"
]

def get_crypto_prices():
    name_list = []
    j = 0
    progress['value'] = 0
    progress.update()

    for i, crypto in enumerate(currencies, start=1):
        url = key + crypto
        data = requests.get(url)
        data = data.json()
        j = j + 1
        price = float(data['price'])
        formatted_price = '{:.2f}'.format(price).rstrip('0').rstrip('.')
        name_list.append(f"{data['symbol']} price is {formatted_price} $")
        my_listbox.insert(j, name_list[j - 1])
        progress['value'] = (i / len(currencies)) * 100
        progress.update()
    messagebox.showinfo(title="Download status", message="All data downloaded")

spacer2 = Label(window, text="", height=1)
spacer2.pack()

button = Button(text="Get Crypto Prices", command=get_crypto_prices)
button.config()
button.pack()

scrollbar = Scrollbar(window)
scrollbar.pack(side='right', fill='y')

my_listbox = Listbox(window, yscrollcommand=scrollbar.set)
my_listbox.pack(fill='both', expand=True)

scrollbar.config(command=my_listbox.yview)

progress = Progressbar(window, orient="horizontal", length=200, mode="determinate")
progress.pack()

window.mainloop()
