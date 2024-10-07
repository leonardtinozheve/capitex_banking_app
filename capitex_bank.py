# Libraries used to deploy the banking app
from tkinter import *
from tkinter import messagebox as msg
import csv
from random import randint
import os
import re

""" This class serves as the base for the user's bank account
    Contains the main functions of a checking bank account
    Functions: withdrawing, depositing, transferring, checking balance
"""
class Bank_Account:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance

    # User can only deposit any amount from 1 to 3000 in one function
    def deposit(self, amount):
        if 1 <= amount < 3000:
            self.balance += amount
            return True
        return False

    # User cannot overdraw from their checking account
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def check_balance(self):
        return self.balance
    
    # Returns a bool function to determine if user can transfer money 
    def can_transfer(self, amount):
        return 0 < amount <= self.balance



""" The Admin_Bank class inherits username and password from Bank_Account class
    This class is for setting up and authenticating a checking account
    Assigns a special account number for the user's checking account
    Works for signup and regular login by user
    Initializes bank account balance at 0 for new users
"""
class Admin_Bank(Bank_Account):
    def __init__(self, account_number, balance=0):
        super().__init__(account_number, balance)



""" The Account_User class manages user credentials
    i.e username, account and password
"""
class Account_User:
    def __init__(self, username, password, account):
        self.username = username
        self.password = password
        self.account = account



""" The CapitEx_App class defines the banking application with a GUI
    Contains user authentication measures to protect user accounts
"""
class CapitEx_App:
    def __init__(self, root):
        self.root = root
        self.root.title("CapitEx Banking Application")
        self.root.geometry("500x550")

        # Loads the main screen for the app
        self.login_page()

        # Use a dictionary to store user account information
        self.users = {}
        self.current_user = None

        # Loads the users from the .csv file
        self.load_users()

        self.root.protocol("WM_DELETE_WINDOW", self.quit_program)


    # Handles the closing of a window
    def quit_program(self):
        if msg.askyesno("Quit", "Do you want to exit the program?"):
            self.root.destroy()


    # Function loads the users from .csv file
    # Raises an error if the user data file does not exist
    def load_users(self):
        if os.path.exists("bank_users.csv"):
            with open("bank_users.csv", mode='r') as user_file:
                reader = csv.reader(user_file)
                for row in reader:
                    username, password, account_number, balance = row
                    account = Bank_Account(account_number, float(balance))
                    # Re-encode the password for security purposes
                    self.users[username] = Account_User(username, password, account)
        else:
            msg.showerror("Error", "The user data file does not exist. Maybe make a new .csv file")


    # Saves new users to the .csv file with user information
    def save_users(self):
        with open("bank_users.csv", mode='w', newline='') as user_file:
            writer = csv.writer(user_file)
            for user in self.users.values():
                # Converts the hashed password to string before saving
                writer.writerow([user.username, user.password, user.account.account_number, user.account.check_balance()])

    # Clears the window
    def clear_windows(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Displays the login page
    def login_page(self):
        # Clears the windows
        self.clear_windows()

        Label(self.root, text="Account Login").grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        # Label and input for username
        Label(self.root, text="Username:").grid(row=1, column=0, padx=10, pady=10)
        self.username_input = Entry(self.root)
        self.username_input.grid(row=1, column=1, padx=10, pady=10)

        # Label and input for password
        Label(self.root, text="Password:").grid(row=2, column=0, padx=10, pady=10)
        self.password_input = Entry(self.root, show="*")
        self.password_input.grid(row=2, column=1, padx=10, pady=10)

        # Authenticates the user's login input
        Button(self.root, text="Login", command=self.authenticate_login).grid(row=3, columnspan=2, padx=20, pady=20)

        # Directs user to the sign up page
        Button(self.root, text="Don't have an account? Sign up", command=self.signup_page).grid(row=4, columnspan=2, padx=20, pady=20)

        self.root.update_idletasks()


    # Displays the signup page
    def signup_page(self):
        # Clears current screen for signup page to open
        self.clear_windows()

        Label(self.root, text="Set up a new checking account").grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        # Input username
        Label(self.root, text="Choose your username:").grid(row=1, column=0, padx=10, pady=10)
        self.signup_username = Entry(self.root)
        self.signup_username.grid(row=1, column=1, padx=10, pady=10)

        # Input password
        Label(self.root, text="Create a password:").grid(row=2, column=0, padx=10, pady=10)
        self.signup_password = Entry(self.root, show="*")
        self.signup_password.grid(row=2, column=1, padx=10, pady=10)

        # Sign up button
        Button(self.root, text="Sign up", command=self.authenticate_signup).grid(row=3, columnspan=2, padx=20, pady=20)

        # Directs user to login page
        Button(self.root, text="Already have an account? Log in", command=self.login_page).grid(row=4, columnspan=2, padx=20, pady=20)

    # Use regular expression to check if username is valid
    def validate_username(self, username):
        return bool(re.match(r"^[a-zA-Z0-9_]{8,12}$", username))

    # Regex to check if the password is valid (letters, numbers, @, #, $, ! only accepted)
    def validate_password(self, password):
        return bool(re.match(r"^[a-zA-Z0-9_@$#!%]{8,12}$", password))
        
    # Validates the creation of a new checking account    
    def authenticate_signup(self):
        username = self.signup_username.get()
        password = self.signup_password.get()
        
        # Validates username
        if not self.validate_username(username):
            msg.showerror("Error", "Username must be 8-12 letters and can only include letters, numbers and underscores")
            return
        
        # Vaidates password
        if not self.validate_password(password):
            msg.showerror("Error", "Password must be 8-12 characters and can only contain letters, numbers, and @, %, #, $, !")
            return

        if username in self.users:
            msg.showerror("Error", "Username is already taken. Choose a different username.")
        elif not username or not password:
            msg.showerror("Error", "The username and/or password field(s) are empty")
        else:
            # Generate an account with a random 8-number ID (account number)
            # Directs the user back to the login page
            account_number = str(randint(10000000, 999999999))
            new_account = Admin_Bank(account_number)
            self.users[username] = Account_User(username, password, new_account)
            msg.showinfo("Success", f"Welcome to CapitEx, {username}. You can login.")
            self.save_users() # Saves the new user to the .csv file
            self.login_page()


    def authenticate_login(self):
        username = self.username_input.get()
        password = self.password_input.get()

        user = self.users.get(username)

        if user and user.password == password:
            self.current_user = user
            msg.showinfo("Success", "Login successful!")
            self.home_page()
        else:
            msg.showerror("Error", "Try again. Either your name or password is invalid")


    def home_page(self):
        # Clears current screen for home page to open
        self.clear_windows()

        Label(self.root, text=f"Welcome to CapitEx, {self.current_user.username}").grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        # Initializes the "Deposit Amount" button and entry for input
        Label(self.root, text="Deposit Amount:").grid(row=1, column=0, padx=10, pady=10)
        self.deposit_log = Entry(self.root)
        self.deposit_log.grid(row=1, column=1, padx=10, pady=10)

        Button(self.root, text="Deposit", command=self.deposit_money).grid(row=2, columnspan=2, padx=20, pady=20)

        # Initializes the "Withdraw Amount" button and entry for input
        Label(self.root, text="Withdraw Amount:").grid(row=3, column=0, padx=10, pady=10)
        self.withdraw_log = Entry(self.root)
        self.withdraw_log.grid(row=3, column=1, padx=10, pady=10)

        Button(self.root, text="Withdraw Money", command=self.withdraw_money).grid(row=4, columnspan=2, padx=20, pady=20)

        # Initializes the "Transfer Amount" button and entry for amount and recipient
        Label(self.root, text="Transfer Amount:").grid(row=5, column=0, padx=10, pady=10)
        self.transfer_amount_log = Entry(self.root)
        self.transfer_amount_log.grid(row=5, column=1, padx=10, pady=10)

        Label(self.root, text="Recipient Account:").grid(row=6, column=0, padx=10, pady=10)
        self.transfer_recipient_log = Entry(self.root)
        self.transfer_recipient_log.grid(row=6, column=1, padx=10, pady=10)

        Button(self.root, text="Transfer Money", command=self.transfer_money).grid(row=7, columnspan=2, padx=20, pady=20)

        # Initializes the "Check Balance" button
        Button(self.root, text="Check Balance", command=self.check_balance).grid(row=8, column=0, columnspan=2, padx=20, pady=20)

        # Initialize the "Log Out" button
        Button(self.root, text="Log Out", command=self.logout).grid(row=8, column=2, columnspan=2, padx=20, pady=20)


    # Checks if the deposit money is between 1 and 3000
    # Clears the entry box and prompts the user again, if otherwise
    def deposit_money_logic(self, amount):
        if self.current_user is None:
            raise ValueError("You must be logged in to access account")

        if self.current_user.account.deposit(amount):
            self.save_users()
            return self.current_user.account.check_balance()
        else:
            raise ValueError("Deposit amount must be between 1 and 3,000")
        

    # Deposits money into the bank
    def deposit_money(self):
        try:
            amount = float(self.deposit_log.get())
            new_balance = self.deposit_money_logic(amount)
            msg.showinfo("Success", f"Deposited ${amount:.2f}. New balance is ${new_balance:.2f}")
            self.deposit_log.delete(0, END) 
        except ValueError as e:
            msg.showerror("Error", str(e))
            self.deposit_log.delete(0, END)


    # Withdraws money from the bank
    # Should not overdraw from the bank account
    # Clears the entry box for withdrawl if input is valid
    def withdraw_money(self):
        if self.current_user is None:
            msg.showerror("Error", "Please log in first")
            return


        # Validates the withdrawal amount
        try:
            amount = float(self.withdraw_log.get())
            if self.current_user.account.withdraw(amount):
                msg.showinfo("Success", f"Withdrew ${amount:.2f}. New balance is ${self.current_user.account.check_balance():.2f}")
                self.save_users()
            else:
                msg.showerror("Error", "You have insufficient funds in your account or you entered an invalid amount")
            self.withdraw_log.delete(0, END)
        except ValueError:
            msg.showerror("Error", "Please enter a valid amount for withdrawal")
            self.withdraw_log.delete(0, END)


    # Transfers money to a valid recipient account
    # Clears the entry boxes if there is invalid input
    def transfer_money(self):
        if self.current_user is None:
            msg.showerror("Error", "Please log in first")
            return


        # Validates the transfer amount
        try:
            amount = float(self.transfer_amount_log.get())
            recipient_username = self.transfer_recipient_log.get()

            if not self.current_user.account.can_transfer(amount):
                msg.showerror("Error", "Transfer amount must be between 1 and your current balance")
                self.transfer_amount_log.delete(0, END)
                self.transfer_recipient_log.delete(0, END)
                return
            
            recipient_user = self.users.get(recipient_username)
            if recipient_user is None:
                msg.showerror("Error", "Recipient account does not exist.")
                self.transfer_amount_log.delete(0, END)
                self.transfer_recipient_log.delete(0, END)
                return

            # Proceeds with the transfer
            if self.current_user.account.withdraw(amount):
                recipient_user.account.deposit(amount)
                msg.showinfo("Success", f"Transferred ${amount:.2f} to {recipient_username}.")
                self.save_users()
            else:
                msg.showerror("Error", "You either have insufficient funds or you entered an invalid amount.")
            self.transfer_amount_log.delete(0, END)
            self.transfer_recipient_log.delete(0, END)
        except ValueError:
            msg.showerror("Error", "Please enter a valid amount.")
        self.transfer_amount_log.delete(0, END)
        self.transfer_recipient_log.delete(0, END)


    # Prints out the user's balance when prompted
    def check_balance(self):
        if self.current_user is None:
            msg.showerror("Error", "You need to log in to access your account.")
            return
        msg.showinfo("Balance", f"Your bank balance is: ${self.current_user.account.check_balance():.2f}")


    # Handles logging out
    def logout(self):
        self.current_user = None
        msg.showinfo("Logged out", "You have been logged out successfully")
        self.login_page()

   

def main():
    root = Tk()
    app = CapitEx_App(root)
    app.login_page()
    root.mainloop()


if __name__ == "__main__":
    main()