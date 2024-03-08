import tkinter as tk
import requests

class Banks:
    bank_name = 'Taiwan Bank'

    def __init__(self, uname, pwd, money):
        self.username = uname
        self.password = pwd
        self.balance = money

    def save_money(self, money):
        self.balance += money
        return f'存款 {money} 成功'

    def withdraw_money(self, money):
        if self.balance < money:
            return '窮逼'
        else:
            self.balance -= money
            return f'提款 {money} 成功'

    def transfer_money(self, other, money):
        if self.balance < money:
            return '窮逼'
        else:
            self.withdraw_money(money)
            other.save_money(money)
            return f'轉帳 {money} 給 {other.username} 成功'

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        message = self.save_money(amount)
        label_balance.config(text=f'餘額: {self.get_balance()}')
        return message

    def withdraw(self, amount):
        message = self.withdraw_money(amount)
        label_balance.config(text=f'餘額: {self.get_balance()}')
        return message

    def show_balance(self):
        return f"{self.username}的餘額為: {self.balance}"

def get_exchange_rate():
    # 使用 ExchangeRate-API 獲取匯率資訊
    url = 'https://v6.exchangerate-api.com/v6/462ba380aa67c01285e7dec4/latest/USD'
    response = requests.get(url)
    data = response.json()
    return data['conversion_rates']['TWD']

def convert_currency(amount):
    # 換算美元到台幣
    exchange_rate = get_exchange_rate()
    twd_amount = amount * exchange_rate
    return f'{amount} 美元換算成台幣為 {twd_amount:.2f}'

def login_click():
    username = entry_username.get()
    password = entry_password.get()
    if username == 'wangj6231' and password == '24376874':
        global wang_bank
        wang_bank = Banks('王俊麒', password, 3000)
        label_name.config(text=f'姓名: {wang_bank.username}')
        label_balance.config(text=f'餘額: {wang_bank.get_balance()}')
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, '登入成功\n')
    else:
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, '登入失敗\n')

def deposit_click():
    amount = int(entry_amount.get())
    message = wang_bank.deposit(amount)
    output_text.insert(tk.END, message + '\n')

def withdraw_click():
    amount = int(entry_amount.get())
    message = wang_bank.withdraw(amount)
    output_text.insert(tk.END, message + '\n')

def balance_click():
    message = wang_bank.show_balance()
    output_text.insert(tk.END, message + '\n')

def transfer_click():
    amount = int(entry_amount.get())
    transfer_to = entry_transfer_to.get()
    if transfer_to == '王俊麒':
        output_text.insert(tk.END, '不能轉帳給自己\n')
    else:
        other_bank = Banks(transfer_to, 'dummy', 0)  # 假設其他帳戶名稱為 transfer_to
        message = wang_bank.transfer_money(other_bank, amount)
        output_text.insert(tk.END, message + '\n')
        label_balance.config(text=f'餘額: {wang_bank.get_balance()}')

def convert_click():
    amount = float(entry_usd_amount.get())
    result = convert_currency(amount)
    output_text.insert(tk.END, result + '\n')

root = tk.Tk()
root.title('Bank Application')

label_username = tk.Label(root, text='帳號:')
label_username.pack()

entry_username = tk.Entry(root)
entry_username.pack()

label_password = tk.Label(root, text='密碼:')
label_password.pack()

entry_password = tk.Entry(root, show='*')
entry_password.pack()

button_login = tk.Button(root, text='登入', command=login_click)
button_login.pack()

label_name = tk.Label(root, text='姓名:')
label_name.pack()

label_balance = tk.Label(root, text='餘額:')
label_balance.pack()

label_amount = tk.Label(root, text='金額:')
label_amount.pack()

entry_amount = tk.Entry(root)
entry_amount.pack()

button_deposit = tk.Button(root, text='存款', command=deposit_click)
button_deposit.pack()

button_withdraw = tk.Button(root, text='提款', command=withdraw_click)
button_withdraw.pack()

button_balance = tk.Button(root, text='查詢餘額', command=balance_click)
button_balance.pack()

label_transfer_to = tk.Label(root, text='轉帳給:')
label_transfer_to.pack()

entry_transfer_to = tk.Entry(root)
entry_transfer_to.pack()

button_transfer = tk.Button(root, text='轉帳', command=transfer_click)
button_transfer.pack()

output_text = tk.Text(root, height=10, width=50)
output_text.pack()

label_usd_amount = tk.Label(root, text='金額(美元):')
label_usd_amount.pack()

entry_usd_amount = tk.Entry(root)
entry_usd_amount.pack()

button_convert = tk.Button(root, text='換算', command=convert_click)
button_convert.pack()

output_text = tk.Text(root, height=10, width=50)
output_text.pack()

root.mainloop()
