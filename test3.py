import json
import asyncio
import aiohttp
from tkinter import *
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar, Treeview
import threading
import urllib.parse

async def fetch_crypto_price(session, currencies, treeview, tasks):
    currencies_str = json.dumps(currencies).replace(" ", "")

    url = f"https://api.binance.com/api/v3/ticker/price?symbols={currencies_str}"

    async with session.get(url) as response:
        datas = await response.json()

        for data in datas:
            price = float(data['price'])
            formatted_price = '{:.2f}'.format(price).rstrip('0').rstrip('.')
            treeview.insert("", "end", values=(data['symbol'], formatted_price))
            tasks.append(data)
        return datas


async def update_crypto_prices(treeview):
    currencies = [
        "BTCUSDT", "DOGEUSDT", "LTCUSDT", "ETHUSDT", "BNBUSDT",
        "XRPUSDT", "ADAUSDT", "DOTUSDT", "BCHUSDT", "LINKUSDT",
        "XLMUSDT", "TRXUSDT", "VETUSDT", "EOSUSDT", "XMRUSDT",
        "XTZUSDT", "DASHUSDT", "ZECUSDT", "UNIUSDT", "AAVEUSDT",
        "MKRUSDT", "COMPUSDT", "SOLUSDT", "ICPUSDT", "FTTUSDT",
        "AVAXUSDT", "FILUSDT", "YFIUSDT", "MATICUSDT", "CAKEUSDT"
    ]

    async with aiohttp.ClientSession() as session:
        tasks = []
        treeview.delete(*treeview.get_children())
        datas = await fetch_crypto_price(session, currencies, treeview, tasks)
        #print(f"gelen datalar: {datas}")
        #await asyncio.gather(*tasks)

def update_prices_periodically(treeview):
    async def update():
        while True:
            await update_crypto_prices(treeview)
            await asyncio.sleep(5)  # Her 5 saniyede bir güncelle

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(update())

def main():
    window = Tk()
    window.title("Crypto Price")
    window.minsize(width=400, height=700)
    window.config(padx=20, pady=20)
    original_image = Image.open("crypto.png")
    resized_image = original_image.resize((200, 200))
    img = ImageTk.PhotoImage(resized_image)

    panel = Label(window, image=img)
    panel.pack(padx=20, pady=20)

    treeview = Treeview(window, columns=("Crypto", "Price"))
    treeview.heading("#1", text="Crypto")
    treeview.heading("#2", text="Price")
    treeview.pack(fill='both', expand=True)

    scrollbar = Scrollbar(window)
    scrollbar.pack(side='right', fill='y')
    treeview.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=treeview.yview)

    spacer2 = Label(window, text="", height=1)
    spacer2.pack()

    # asyncio işlemini ayrı bir thread'de çalıştır
    asyncio_thread = threading.Thread(target=update_prices_periodically, args=(treeview,))
    asyncio_thread.daemon = True
    asyncio_thread.start()

    window.mainloop()

if __name__ == "__main__":
    main()
