from tkinter import *
from tkinter import ttk, messagebox
import requests

class CurrencyConverter:
    API_URL = "https://api.exchangerate-api.com/v4/latest/"
    DEFAULT_CURRENCIES = ["USD", "EUR", "RUB"]

    def __init__(self, root):
        self.root = root
        self.currencies = self.get_currency_list()
        self.setup_ui()

    def get_currency_list(self):
        try:
            response = requests.get(f"{self.API_URL}RUB")
            return list(response.json()["rates"].keys())
        except:
            return self.DEFAULT_CURRENCIES

    def convert_currency(self):
        try:
            amount = self.validate_amount()
            base = self.base_currency.get()
            target = self.target_currency.get()

            rate = self.get_exchange_rate(base, target)
            converted_amount = amount * rate
            
            self.result_label.config(
                text=f"{amount:.2f} {base} = {converted_amount:.2f} {target}"
            )
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число.")
        except:
            messagebox.showerror("Ошибка", "Не удалось получить курсы валют.")

    def validate_amount(self):
        amount_text = self.entry_amount.get().strip()
        if not amount_text:
            raise ValueError("Введите сумму для конвертации.")
        
        amount = float(amount_text)
        if amount <= 0:
            raise ValueError("Сумма должна быть больше нуля.")
        
        return amount

    def get_exchange_rate(self, base_currency, target_currency):
        response = requests.get(f"{self.API_URL}{base_currency}")
        rates = response.json()["rates"]

        if target_currency not in rates:
            messagebox.showerror("Ошибка", "Выбранная валюта недоступна.")
        
        return rates[target_currency]

    def setup_ui(self):
        self.root.title("Конвертер валют")
        self.root.geometry("350x250+600+200")
        self.root.iconbitmap(default="./currency.ico")

        Label(self.root, text="Сумма:").pack()
        self.entry_amount = Entry(self.root)
        self.entry_amount.pack()

        Label(self.root, text="Исходная валюта:").pack()
        self.base_currency = ttk.Combobox(self.root, values=self.currencies)
        self.base_currency.pack()
        self.base_currency.set("USD")
        
        ttk.Button(
            self.root, 
            text="Поменять местами", 
            command=self.swap_currencies
        ).pack(pady=5)

        Label(self.root, text="Целевая валюта:").pack()
        self.target_currency = ttk.Combobox(self.root, values=self.currencies)
        self.target_currency.pack()
        self.target_currency.set("RUB")

        ttk.Button(
            self.root, text="Конвертировать", command=self.convert_currency
        ).pack(pady=10)

        self.result_label = Label(self.root, text="")
        self.result_label.pack()
        
    def swap_currencies(self):
        current_base = self.base_currency.get()
        current_target = self.target_currency.get()
        self.base_currency.set(current_target)
        self.target_currency.set(current_base)

def main():
    root = Tk()
    app = CurrencyConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()