#------ file check --------

import os

#-------- engrypted password -------

import hashlib

#---------- inport curent date and time -------------

from datetime import datetime

# -------------------- File paths -------------------- 

ACCOUNTS_FILE = 'accounts.txt'
TRANSACTIONS_FILE = 'transactions.txt'
FEEDBACK_FILE = 'feedback.txt'

# ------------------ Admin user name and password hard coded ----------------

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = hashlib.sha256('1234'.encode()).hexdigest()  # Hashed admin password

# ----------- Ensure required files exist -------------

for file in [ACCOUNTS_FILE, TRANSACTIONS_FILE, FEEDBACK_FILE]:
    if not os.path.exists(file):
        open(file, 'w').close()

# ----------------- engripted password funtion ------------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def read_accounts():
    accounts = {}
    try:
        with open(ACCOUNTS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:                                                       # 7 fields (acc_num, name, acc_type, balance, password, nic, phone)
                    acc_num, name, acc_type, balance, password, nic, phone = parts
                    try:
                        accounts[acc_num] = {
                            'name': name,
                            'type': acc_type,
                            'balance': float(balance),
                            'password': password,
                            'nic': nic,
                            'phone': phone
                        }
                    except ValueError:
                        print(f"Skipping invalid balance value: {line.strip()}")
                else:
                    print(f"Skipping malformed account line: {line.strip()}")
    except FileNotFoundError:
        print("____ ❌❌❌ ____")
        print(" Accounts file not found.")
    return accounts

def write_accounts(accounts):
    try:
        with open(ACCOUNTS_FILE, 'w') as f:
            for acc_num, info in accounts.items():
                f.write(f"{acc_num}|{info['name']}|{info['type']}|{info['balance']:.2f}|{info['password']}|{info['nic']}|{info['phone']}\n")
    except IOError:
        print("____❌❌❌____")
        print("Error writing to the accounts file.")

def append_transaction(acc_num, trans_type, amount):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(TRANSACTIONS_FILE, 'a') as f:
            f.write(f"{acc_num}|{trans_type}|{amount:.2f}|{date}\n")
    except IOError:
        print("____❌❌❌____")
        print("Error appending to transactions file.")

def append_feedback(acc_num, feedback):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(FEEDBACK_FILE, 'a') as f:
            f.write(f"{acc_num}|{feedback}|{date}\n")
    except IOError:
        print("____❌❌❌____")
        print("Error appending to feedback file.")

def view_transaction_history(acc_num):
    print("\n------ Your Transaction History ------\n")
    print("_______________________________________________________\n")
    found = False
    try:
        with open(TRANSACTIONS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == acc_num:
                    print(f"{parts[1]} of ${parts[2]} on {parts[3]}")
                    found = True
    except IOError:
        print("____❌❌❌____")
        print(" Error reading transactions file.")
    
    if not found:
        print("No transactions found.")
    print("_______________________________________________________\n")

# ---------------- Account Number Generator ----------------

def generate_account_number():
    accounts = read_accounts()
    existing_numbers = set(int(acc) for acc in accounts.keys() if acc.isdigit())
    next_number = 10000001
    while next_number in existing_numbers:
        next_number += 1
    return str(next_number)

# --------------- Account creation ------------------

def create_account():
    accounts = read_accounts()
    acc_num = generate_account_number()
    print(f"Generated Account Number: {acc_num}")

    name = input("Enter Account Holder Name: ").strip()

    acc_type = input("Enter Account Type (Savings/Current): ").strip().capitalize()
    while acc_type not in ["Savings", "Current"]:
        print("____❌❌❌____")
        print("Invalid account type. Must be 'Savings' or 'Current'.")
        acc_type = input("Enter Account Type (Savings/Current): ").strip().capitalize()

    balance = None
    while balance is None:
        try:
            balance = float(input("Enter Initial Balance: $ "))
            if balance < 0:
                print("____❌❌❌___")
                print("Balance cannot be negative.")
                balance = None
        except ValueError:
            print("___❌❌❌___")
            print("Invalid balance amount.")
    
    password = input("Set Account Password: ")
    hashed_password = hash_password(password)

    # --------------- NIC and Telephone Number -------------

    nic = input("Enter your NIC number 🪪: ").strip()
    phone = input("Enter your Telephone Number ☎️: ").strip()

    accounts[acc_num] = {
        'name': name,
        'type': acc_type,
        'balance': balance,
        'password': hashed_password,
        'nic': nic,         
        'phone': phone     
    }
    write_accounts(accounts)
    print("____✅✅✅____")
    print(f" Account created successfully. Your Account Number is 👉: {acc_num}👈")

def view_account(acc_num):
    accounts = read_accounts()
    if acc_num in accounts:
        info = accounts[acc_num]
        print("\n----- Account Details -----\n")
        print("_____________________________________________________\n")
        print(f"Account Number : {acc_num}")
        print(f"Holder Name    : {info['name']}")
        print(f"Account Type   : {info['type']}")
        print(f"Balance        : ${info['balance']:.2f}")
        print(f"NIC            : {info['nic']}")
        print(f"Phone Number   : {info['phone']}")
        print("_____________________________________________________")
    else:
        print("____❌❌❌____ ")
        print("Account not found.")

def modify_account(acc_num):
    accounts = read_accounts()
    if acc_num in accounts:
        name = input("Enter new Holder Name: ")
        acc_type = input("Enter new Account Type (Savings/Current): ").strip().capitalize()
        while acc_type not in ["Savings", "Current"]:
            print("____❌❌❌____")
            print(" Invalid account type.")
            acc_type = input("Enter new Account Type (Savings/Current)🤷‍♂️: ").strip().capitalize()

        # Allow modification of NIC and phone number
        nic = input("Enter new NIC number: ").strip()
        phone = input("Enter new Telephone Number: ").strip()

        accounts[acc_num]['name'] = name
        accounts[acc_num]['type'] = acc_type
        accounts[acc_num]['nic'] = nic
        accounts[acc_num]['phone'] = phone

        write_accounts(accounts)
        print("____ ✅✅✅ ____")
        print("Account updated successfully.")
    else:
        print("____❌❌❌____")
        print(" Account not found.")

def delete_account(acc_num):
    accounts = read_accounts()
    if acc_num in accounts:
        del accounts[acc_num]
        write_accounts(accounts)
        print("____✅✅✅ ____  ")
        print(" Account deleted successfully.")
    else:
        print("____❌❌❌____")
        print(" Account not found.")

# ---------------- deposit amount  ----------------

def deposit(acc_num):
    accounts = read_accounts()
    if acc_num in accounts:
        try:
            amount = float(input("Enter amount to deposit: $"))
            if amount <= 0:
                print("⚠️ Please enter a valid amount.")
                return
            accounts[acc_num]['balance'] += amount
            write_accounts(accounts)
            append_transaction(acc_num, 'Deposit', amount)
            print(f"✅ ${amount:.2f} deposited successfully.\n")
            print(f"💰 Updated Balance: ${accounts[acc_num]['balance']:.2f}")
        except ValueError:
            print("❌ Invalid amount.")
    else:
        print("❌ Account not found.")


def withdraw(acc_num):
    accounts = read_accounts()
    if acc_num in accounts:
        try:
            amount = float(input("Enter amount to withdraw: $"))
            if amount <= 0:
                print("⚠️ Please enter a valid amount.")
                return
            if accounts[acc_num]['balance'] >= amount:
                accounts[acc_num]['balance'] -= amount
                write_accounts(accounts)
                append_transaction(acc_num, 'Withdrawal', amount)
                print(f"✅ ${amount:.2f} withdrawn successfully.\n")
                print(f"💰 Remaining Balance: ${accounts[acc_num]['balance']:.2f}")
            else:
                print("❌ Insufficient balance.\n")
                print(f"💰 Your Balance: ${accounts[acc_num]['balance']:.2f}")
        except ValueError:
            print("❌ Invalid amount.")
    else:
        print("❌ Account not found.")

# ----------------- Feedback System -----------------

def submit_feedback(acc_num):
    feedback = input("Enter your feedback: ").strip()
    if feedback:
        append_feedback(acc_num, feedback)
        print("🥳🥳🥳")
        print("Thank you for your feedback !")
    else:
        print("❌ Feedback cannot be empty.")

# ----------------- Admin Panel ---------------------

def admin_panel():
    while True:
        print("\n-------- Admin Panel --------\n")
        print("1. View All Accounts")
        print("2. View All Transactions")
        print("3. View All Feedback")
        print("4. Create New Account")
        print("5. Delete Account")
        print("6. Logout")
        choice = input("Enter your choice: ")
        if choice == '1':
            accounts = read_accounts()
            print("\nAccount Number | Name | Type | Balance\n")
            for acc_num, info in accounts.items():
                print(f"{acc_num} | {info['name']} | {info['type']} | ${info['balance']:.2f}")
        elif choice == '2':
            try:
                with open(TRANSACTIONS_FILE, 'r') as f:
                    print("\nTransactions:")
                    for line in f:
                        print(line.strip())
            except IOError:
                print("❌ Error reading transactions file.")
        elif choice == '3':
            try:
                with open(FEEDBACK_FILE, 'r') as f:
                    print("\nFeedbacks:")
                    for line in f:
                        print(line.strip())
            except IOError:
                print("❌ Error reading feedback file.")
        elif choice == '4':
            create_account()
        elif choice == '5':
            acc_num = input("Enter Account Number to delete: ")
            delete_account(acc_num)
        elif choice == '6':
            print("✅ Logged out from admin panel.")
            break
        else:
            print("❌ Invalid choice.")

# --------------- Customer Panel -------------------

def customer_panel(acc_num):
    while True:
        print(f"\n--- Welcome, {acc_num} ---\n")
        print("1. View Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Submit Feedback")
        print("5. View Transaction History")
        print("6. Logout")
        choice = input("Enter your choice: ")
        if choice == '1':
            view_account(acc_num)
        elif choice == '2':
            deposit(acc_num)
        elif choice == '3':
            withdraw(acc_num)
        elif choice == '4':
            submit_feedback(acc_num)
        elif choice == '5':
            view_transaction_history(acc_num)
        elif choice == '6':
            print("✅ Logged out.")
            break
        else:
            print("❌ Invalid choice.")

# ------------------ Login Systems ------------------

def admin_login():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    if hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD:
        print("✅ Admin login successful.")
        admin_panel()
    else:
        print("❌ Invalid admin credentials.")

def customer_login():
    accounts = read_accounts()
    acc_num = input("Enter Account Number: ")
    password = input("Enter Password: ")
    if acc_num in accounts and accounts[acc_num]['password'] == hash_password(password):
        print(f"✅ Login successful. Welcome, {accounts[acc_num]['name']}!")
        customer_panel(acc_num)
    else:
        print("❌ Invalid account number or password.")

# --------------------- Main Menu ---------------------

def main():
    while True:
        print("\n===== 💲 Mini Banking System 💲 =====\n")
        print("1. Admin Login")
        print("2. Customer Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            admin_login()
        elif choice == '2':
            customer_login()
        elif choice == '3':
            print("🙏 Thank you for using Mini Banking System!")
            break
        else:
            print("❌ Invalid choice. Please select again.")

if __name__ == "__main__":
    main()

#======= tooo =======
