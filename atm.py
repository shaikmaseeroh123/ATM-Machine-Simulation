import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class ATM:
    def __init__(self):
        self.balance = 1000  # Initial account balance
        self.pin = 1234  # Default PIN
        self.transaction_history = []  # List to store transaction history

    def check_balance(self):
        """Function to check account balance"""
        self.transaction_history.append("Checked balance")
        return f"Your current balance is: ${self.balance}"

    def deposit_cash(self, amount):
        """Function to deposit cash into the account"""
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited ${amount}")
            return f"${amount} has been deposited into your account."
        else:
            return "Invalid amount. Please enter a positive value."

    def withdraw_cash(self, amount):
        """Function to withdraw cash from the account"""
        if amount <= 0:
            return "Invalid amount. Please enter a positive value."
        elif amount > self.balance:
            return "Insufficient funds."
        else:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew ${amount}")
            return f"${amount} has been withdrawn from your account."

    def change_pin(self, old_pin, new_pin):
        """Function to change PIN"""
        if old_pin == self.pin:
            if len(str(new_pin)) == 4:  # Ensure the new PIN is 4 digits long
                self.pin = new_pin
                self.transaction_history.append("Changed PIN")
                return "Your PIN has been successfully changed."
            else:
                return "New PIN must be 4 digits."
        else:
            return "Incorrect PIN. Unable to change PIN."

    def view_transaction_history(self):
        """Function to view transaction history"""
        if len(self.transaction_history) == 0:
            return "No transactions to display."
        else:
            return "\n".join(self.transaction_history)

class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Machine Simulation")
        self.root.geometry("400x500")
        self.root.config(bg="#f0f0f0")  # Lighter background color for better contrast
        self.atm = ATM()

        self.pin_entry_var = tk.StringVar()
        self.amount_entry_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        """Creates all the widgets for the ATM GUI."""
        # Frame for the PIN section
        self.pin_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.pin_frame.pack(pady=20)

        self.pin_label = tk.Label(self.pin_frame, text="Enter PIN:", font=("Arial", 14), bg="#f0f0f0", fg="#333")
        self.pin_label.grid(row=0, column=0, padx=10)

        self.pin_entry = tk.Entry(self.pin_frame, textvariable=self.pin_entry_var, show="*", font=("Arial", 14), width=20)
        self.pin_entry.grid(row=0, column=1)

        # Frame for the buttons
        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.button_frame.pack(pady=10)

        # Define button style
        style = ttk.Style()
        style.configure("TButton",
                font=("Arial", 12),
                padding=10,
                relief="solid",
                background="#9C77B7",  # Lavender/Purple background
                foreground="#4B0082",  # Dark Purple text
                hoverbackground="#D8A7D3",  # Soft Pink on hover
                hoverforeground="white")  # White text on hover

        # Buttons with visible text
        self.check_balance_button = ttk.Button(self.button_frame, text="Check Balance", command=self.check_balance, width=20, style="TButton")
        self.check_balance_button.grid(row=0, column=0, pady=5)

        self.deposit_button = ttk.Button(self.button_frame, text="Deposit Cash", command=self.deposit, width=20, style="TButton")
        self.deposit_button.grid(row=1, column=0, pady=5)

        self.withdraw_button = ttk.Button(self.button_frame, text="Withdraw Cash", command=self.withdraw, width=20, style="TButton")
        self.withdraw_button.grid(row=2, column=0, pady=5)

        self.change_pin_button = ttk.Button(self.button_frame, text="Change PIN", command=self.change_pin, width=20, style="TButton")
        self.change_pin_button.grid(row=3, column=0, pady=5)

        self.view_history_button = ttk.Button(self.button_frame, text="View History", command=self.view_history, width=20, style="TButton")
        self.view_history_button.grid(row=4, column=0, pady=5)

    def check_balance(self):
        """Checks the balance if the pin is correct."""
        pin = self.pin_entry_var.get()
        if pin == str(self.atm.pin):
            result = self.atm.check_balance()
            self.show_popup("Balance", result)
        else:
            self.show_popup("Error", "Incorrect PIN.", error=True)

    def deposit(self):
        """Deposits cash into the account."""
        pin = self.pin_entry_var.get()
        if pin == str(self.atm.pin):
            amount = self.ask_amount("Deposit Cash")
            if amount is not None:
                result = self.atm.deposit_cash(amount)
                self.show_popup("Deposit", result)
        else:
            self.show_popup("Error", "Incorrect PIN.", error=True)

    def withdraw(self):
        """Withdraws cash from the account."""
        pin = self.pin_entry_var.get()
        if pin == str(self.atm.pin):
            amount = self.ask_amount("Withdraw Cash")
            if amount is not None:
                result = self.atm.withdraw_cash(amount)
                self.show_popup("Withdraw", result)
        else:
            self.show_popup("Error", "Incorrect PIN.", error=True)

    def change_pin(self):
        """Changes the PIN."""
        pin = self.pin_entry_var.get()
        if pin == str(self.atm.pin):
            old_pin = self.ask_for_pin("Enter Old PIN:")
            if old_pin:
                new_pin = self.ask_for_pin("Enter New PIN:")
                if new_pin:
                    result = self.atm.change_pin(old_pin, new_pin)
                    self.show_popup("Change PIN", result)
        else:
            self.show_popup("Error", "Incorrect PIN.", error=True)

    def view_history(self):
        """Views the transaction history."""
        pin = self.pin_entry_var.get()
        if pin == str(self.atm.pin):
            result = self.atm.view_transaction_history()
            self.show_popup("Transaction History", result)
        else:
            self.show_popup("Error", "Incorrect PIN.", error=True)

    def ask_amount(self, action):
        """Prompts the user to enter an amount."""
        amount = self.ask_for_input(action, "Amount ($):")
        try:
            amount = float(amount)
            if amount > 0:
                return amount
            else:
                self.show_popup("Error", "Amount must be positive.", error=True)
                return None
        except ValueError:
            self.show_popup("Error", "Invalid amount. Please enter a valid number.", error=True)
            return None

    def ask_for_pin(self, action):
        """Prompts the user to enter a PIN."""
        pin = self.ask_for_input(action, "Enter PIN:")
        try:
            pin = int(pin)
            if len(str(pin)) == 4:
                return pin
            else:
                self.show_popup("Error", "PIN must be 4 digits.", error=True)
                return None
        except ValueError:
            self.show_popup("Error", "Invalid PIN. Please enter a numeric value.", error=True)
            return None

    def ask_for_input(self, action, prompt):
        """Creates a prompt to ask for user input."""
        input_window = tk.Toplevel(self.root)
        input_window.geometry("300x150")
        input_window.title(action)

        label = tk.Label(input_window, text=prompt, font=("Arial", 12), bg="#f0f0f0", fg="#333")
        label.pack(pady=10)

        entry = tk.Entry(input_window, width=20, font=("Arial", 12))
        entry.pack(pady=10)

        result = None

        def submit():
            nonlocal result
            result = entry.get()
            input_window.destroy()

        submit_button = ttk.Button(input_window, text="Submit", command=submit, width=20, style="TButton")
        submit_button.pack(pady=10)

        self.root.wait_window(input_window)
        return result

    def show_popup(self, title, message, error=False):
        """Displays a styled popup message."""
        if error:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)


if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()
