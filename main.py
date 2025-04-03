from tkinter import *
from tkinter import ttk, messagebox
import requests

def get_currency_list():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/RUB"
        response = requests.get(url).json()
        return list(response["rates"].keys())  
    except:
        return ["USD", "EUR", "RUB"]

def convert_currency():
    try:
        amount_text = entry_amount.get().strip()
        if not amount_text:
            messagebox.showerror("Ошибка", "Введите сумму для конвертации.")
            return
        amount = float(amount_text)
        if amount <= 0:
            messagebox.showerror("Ошибка", "Сумма должна быть больше нуля.")
            return
        base = base_currency.get()
        target = target_currency.get()
        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        response = requests.get(url).json()
        if target in response["rates"]:
            rate = response["rates"][target]
            converted_amount = amount * rate
            result_label.config(text=f"{amount} {base} = {converted_amount:.2f} {target}")
        else:
            messagebox.showerror("Ошибка", "Выбранная валюта недоступна.")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число.")
    except:
        messagebox.showerror("Ошибка", "Не удалось получить курсы валют.")

root = Tk()
root.title("Конвертер валют")
root.geometry("300x250+600+200")
root.iconbitmap(default="./currency.ico")

currencies = get_currency_list()

Label(root, text="Сумма:").pack()
entry_amount = Entry(root)
entry_amount.pack()

Label(root, text="Исходная валюта:").pack()
base_currency = ttk.Combobox(root, values=currencies)
base_currency.pack()
base_currency.set("USD")

Label(root, text="Целевая валюта:").pack()
target_currency = ttk.Combobox(root, values=currencies)
target_currency.pack()
target_currency.set("RUB")

convert_button = ttk.Button(root, text="Конвертировать", command=convert_currency)
convert_button.pack(pady=10)

result_label = Label(root, text="")
result_label.pack()

root.mainloop()
