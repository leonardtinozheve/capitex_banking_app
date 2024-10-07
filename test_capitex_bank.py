import pytest
from capitex_banking_app.capitex_bank import CapitEx_App, Bank_Account, Account_User

# Sets up a root tkinter window for testing
from tkinter import *
root = Tk()

# The fixture creates an instance of CapitEx_App
@pytest.fixture
def app():
    return CapitEx_App(root)



""" Tests for the signup process
    Tests for a valid username and password
"""
# Tests the validate_username function for all input
def test_valid_username(app):
    assert app.validate_username("tinotenda_21") == True
    assert app.validate_username("tinotendamuk") == True
    assert app.validate_username("Tafadzwa27_") == True


def test_invalid_username(app):
    assert app.validate_username("tinotend@_21") == False
    assert app.validate_username("") == False
    assert app.validate_username("Tafadzwa27_%") == False
    assert app.validate_username("nyashadzaishewacho") == False


# Tests the validate_password function for all input
def test_valid_password(app):
    assert app.validate_password("Password@") == True
    assert app.validate_password("Leonard%$!") == True
    assert app.validate_password("password#") == True

def test_invalid_password(app):
    assert app.validate_password("Welcometomypage") == False
    assert app.validate_password("leon1") == False
    assert app.validate_password("password*") == False

# Tests for valid user signup details
def test_valid_user(app, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *args: None)

    app.signup_username = Entry(root)
    app.signup_username.insert(0, "lennyzhe")

    app.signup_password = Entry(root)
    app.signup_password.insert(0, "password@12")

    app.authenticate_signup()

    assert "lennyzhe" in app.users

    user = app.users.get("lennyzhe")
    assert user is not None
    assert user.password == "password@12"



"""Tests the login page
   Checks for valid username and password
"""
def test_login(app, monkeypatch):
    # Mocks user data stored in .csv file
    app.users = {
        "lennyzhe": Account_User("lennyzhe", "password@12", Bank_Account("12345678", 500.00))
    }

    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *args, **kwargs: None)
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *args, **kwargs: None)

    monkeypatch.setattr(app.username_input, 'get', lambda: "lennyzhe")
    monkeypatch.setattr(app.password_input, 'get', lambda: "password@12")

    app.authenticate_login()

    assert app.current_user is not None
    assert app.current_user.username == "lennyzhe"
    assert app.current_user.password == "password@12"


"""Tests the functions in the homepage
    Function tests are separated"""
# Tests the deposit functionality
def test_valid_deposit_money(app, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *args: None)
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *args: None)

    app.login_page()

    app.users = {
        "lennyzhe": Account_User("lennyzhe", "password@12", Bank_Account("12345678", 500.00))
    }

    app.current_user = app.users["lennyzhe"]

    # Deposits 200 to return a balance of 700.00
    app.deposit_log = Entry(app.root)
    app.deposit_log.insert(0, "200")

    app.deposit_money()

    assert app.current_user.account.check_balance() == 700.00

    # Deposits 3,000 and returns same balance (700.00)
    app.deposit_log =Entry(app.root)
    app.deposit_log.insert(0, "3000")

    app.deposit_money()

    assert app.current_user.account.check_balance() == 700.00

    # Deposit 0 and return the same balance (700.00)
    app.deposit_log =Entry(app.root)
    app.deposit_log.insert(0, "0")

    app.deposit_money()

    assert app.current_user.account.check_balance() == 700.00

# Tests for deposit values as string
def test_invalid_deposit_money(app, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *args: None)
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *args: None)

    app.login_page()

    app.users = {
        "lennyzhe": Account_User("lennyzhe", "password@12", Bank_Account("12345678", 500.00))
    }

    app.current_user = app.users["lennyzhe"]

    # Deposits cat to return a balance of 500.00
    app.deposit_log = Entry(app.root)
    app.deposit_log.insert(0, "cat")

    app.deposit_money()

    assert app.current_user.account.check_balance() == 500.00

    # Deposit negative int to return a balance of 500.00
    app.deposit_log = Entry(app.root)
    app.deposit_log.insert(0, "-500")

    app.deposit_money()

    assert app.current_user.account.check_balance() == 500.00

# Tests the deposit_money functionality
def test_withdraw_money(app, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *args: None)
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *args: None)

    app.login_page()

    app.users = {
        "lennyzhe": Account_User("lennyzhe", "password@12", Bank_Account("12345678", 500.00))
    }

    app.current_user = app.users["lennyzhe"]

    # Withdraw 100 to return a balance of 400.00
    app.withdraw_log = Entry(app.root)
    app.withdraw_log.insert(0, "100")

    app.withdraw_money()

    assert app.current_user.account.check_balance() == 400.00

    # Withdraw negative int to return a balance of 400.00
    app.withdraw_log = Entry(app.root)
    app.withdraw_log.insert(0, "-500")

    app.withdraw_money()

    assert app.current_user.account.check_balance() == 400.00

    # Overdraws but program returns a balance of 400.00
    app.withdraw_log = Entry(app.root)
    app.withdraw_log.insert(0, "800")

    app.withdraw_money()

    assert app.current_user.account.check_balance() == 400.00

    # Withdraws 0 but program returns a balance of 400.00
    app.withdraw_log = Entry(app.root)
    app.withdraw_log.insert(0, "0")

    app.withdraw_money()

    assert app.current_user.account.check_balance() == 400.00

    # Withdraws "cat" but program returns a balance of 400.00
    app.withdraw_log = Entry(app.root)
    app.withdraw_log.insert(0, "cat")

    app.withdraw_money()

    assert app.current_user.account.check_balance() == 400.00

# Tests the transfer_money functionality
def test_transfer_money(app, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *args: None)
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *args: None)

    app.login_page()

    app.users = {
        "lennyzhe": Account_User("lennyzhe", "password@12", Bank_Account("12345678", 500.00))
    }

    app.current_user = app.users["lennyzhe"]

    # Transfer a valid amount to a valid user
    app.users["tinotendam"] = Account_User("tinotendam", "sexxyredd", Bank_Account("87654321", 300.00))

    app.transfer_amount_log = Entry(app.root)
    app.transfer_amount_log.insert(0, "200")

    app.transfer_recipient_log = Entry(app.root)
    app.transfer_recipient_log.insert(0, "tinotendam")

    try:
        app.transfer_money()
    except Exception as e:
        print(f"Error during money transfer: {e}")

    assert app.current_user.account.check_balance() == 300.00
    assert app.users["tinotendam"].account.check_balance() == 500.00

    # Transfer an invalid amount to a valid user
    app.users["tinotendam"] = Account_User("tinotendam", "sexxyredd", Bank_Account("87654321", 500.00))

    app.transfer_amount_log = Entry(app.root)
    app.transfer_amount_log.insert(0, "700")

    app.transfer_recipient_log = Entry(app.root)
    app.transfer_recipient_log.insert(0, "tinotendam")

    try:
        app.transfer_money()
    except Exception as e:
        print(f"Error during money transfer: {e}")

    assert app.current_user.account.check_balance() == 300.00
    assert app.users["tinotendam"].account.check_balance() == 500.00

    # Transfer a valid amount to an invalid user
    app.transfer_amount_log = Entry(app.root)
    app.transfer_amount_log.insert(0, "200")

    app.transfer_recipient_log = Entry(app.root)
    app.transfer_recipient_log.insert(0, app.transfer_amount_log)

    try:
        app.transfer_money()
    except Exception as e:
        print(f"Error during money transfer: {e}")

    assert app.current_user.account.check_balance() == 300.00

# Tests the check_balance functionality
def test_check_balance(app, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *args: None)

    app.login_page()

    app.users = {
        "lennyzhe": Account_User("lennyzhe", "password@12", Bank_Account("12345678", 500.00))
    }

    app.current_user = app.users["lennyzhe"]

    app.balance_label = Label(app.root)

    app.check_balance()

    assert app.current_user.account.check_balance() == 500.00

# Tests the logout functionality
def test_logout(app, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *args: None)

    app.current_user = Account_User("lennyzhe", "password@12", Bank_Account("12345678", 500.00))

    app.logout()

    assert app.current_user is None

    # Refreshes the GUI before opening the login account
    app.root.update_idletasks()

    assert app.username_input.winfo_ismapped()
    assert app.password_input.winfo_ismapped()