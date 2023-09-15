import asyncio
import aiohttp
from tkinter import *
from PIL import Image, ImageTk
from tkinter.ttk import Treeview

class CryptoPriceApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Crypto Price")
        self.window.minsize(width=400, height=700)
        self.window.config(padx=20, pady=20)

        original_image = Image.open("crypto.png")
        resized_image = original_image.resize((200, 200))
        self.img = ImageTk.PhotoImage(resized_image)

        self.panel = Label(self.window, image=self.img)
        self.panel.pack(padx=20, pady=20)

        self.treeview = Treeview(self.window, columns=("Crypto", "Price"))
        self.treeview.heading("#1", text="Crypto")
        self.treeview.heading("#2", text="Price")
        self.treeview.pack(fill='both', expand=True)

        scrollbar = Scrollbar(self.window)
        scrollbar.pack(side='right', fill='y')
        self.treeview.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.treeview.yview)

        spacer2 = Label(self.window, text="", height=1)
        spacer2.pack()

    async def fetch_crypto_price(self, session, currency):
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={currency}"
        async with session.get(url) as response:
            data = await response.json()
            price = float(data['price'])
            formatted_price = '{:.2f}'.format(price).rstrip('0').rstrip('.')
            return data['symbol'], formatted_price

    async def update_crypto_prices(self):
        while True:
            self.treeview.delete(*self.treeview.get_children())

            currencies = [
                "BTCUSDT", "DOGEUSDT", "LTCUSDT", "ETHUSDT", "BNBUSDT",
                "XRPUSDT", "ADAUSDT", "DOTUSDT", "BCHUSDT", "LINKUSDT",
                "XLMUSDT", "TRXUSDT", "VETUSDT", "EOSUSDT", "XMRUSDT",
                "XTZUSDT", "DASHUSDT", "ZECUSDT", "UNIUSDT", "AAVEUSDT",
                "MKRUSDT", "COMPUSDT", "SOLUSDT", "ICPUSDT", "FTTUSDT",
                "AVAXUSDT", "FILUSDT", "YFIUSDT", "MATICUSDT", "CAKEUSDT"
            ]

            async with aiohttp.ClientSession() as session:
                tasks = [self.fetch_crypto_price(session, crypto) for crypto in currencies]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                for result in results:
                    if isinstance(result, Exception):
                        print(result)
                    else:
                        symbol, price = result
                        self.treeview.insert("", "end", values=(symbol, price))

           # await asyncio.sleep(5)

def main():
    window = Tk()
    app = CryptoPriceApp(window)
    loop = asyncio.get_event_loop()
    loop.create_task(app.update_crypto_prices())
    window.mainloop()

if __name__ == "__main__":
    main()
