import json
import os
from datetime import datetime
from typing import Any


class BankAccount:
    MAX_PIN_ATTEMPTS = 3

    def __init__(
        self,
        account_number: str,
        holder_name: str,
        pin: str,
        balance: float = 0.0,
        status: str = "Active",
        failed_attempts: int = 0,
        transactions: list[dict[str, Any]] | None = None,
    ):
        if not account_number.strip():
            raise ValueError("Account number cannot be empty.")

        if not holder_name.strip():
            raise ValueError("Account holder name cannot be empty.")

        if not pin.isdigit() or len(pin) != 4:
            raise ValueError("PIN must contain exactly four digits.")

        if balance < 0:
            raise ValueError("Opening balance cannot be negative.")

        if status not in ["Active", "Locked"]:
            raise ValueError("Account status must be Active or Locked.")

        self.account_number = account_number.strip()
        self.holder_name = holder_name.strip()

        # Private account data
        self.__pin = pin
        self.__balance = float(balance)

        self.status = status
        self.failed_attempts = failed_attempts
        self.__transactions = transactions or []

        if not self.__transactions and balance > 0:
            self.__record_transaction(
                transaction_type="Opening balance",
                amount=balance,
                description="Account created",
            )

    def authenticate(self, entered_pin: str) -> bool:
        """Validate the entered PIN and apply lockout rules."""
        if self.status == "Locked":
            print("This account is locked.")
            return False

        if entered_pin == self.__pin:
            self.failed_attempts = 0
            return True

        self.failed_attempts += 1

        attempts_remaining = (
            self.MAX_PIN_ATTEMPTS - self.failed_attempts
        )

        if self.failed_attempts >= self.MAX_PIN_ATTEMPTS:
            self.status = "Locked"
            print("Too many incorrect attempts. Account locked.")
        else:
            print(
                "Incorrect PIN. "
                f"Attempts remaining: {attempts_remaining}"
            )

        return False

    def get_balance(self) -> float:
        """Return the current account balance."""
        return self.__balance

    def deposit(self, amount: float) -> bool:
        """Deposit money into the account."""
        if self.status != "Active":
            print("Transactions are unavailable because the account is locked.")
            return False

        if amount <= 0:
            print("Deposit amount must be greater than zero.")
            return False

        self.__balance += amount

        self.__record_transaction(
            transaction_type="Deposit",
            amount=amount,
            description="Cash deposit",
        )

        print(f"£{amount:.2f} deposited successfully.")
        return True

    def withdraw(self, amount: float) -> bool:
        """Withdraw money while preventing a negative balance."""
        if self.status != "Active":
            print("Transactions are unavailable because the account is locked.")
            return False

        if amount <= 0:
            print("Withdrawal amount must be greater than zero.")
            return False

        if amount > self.__balance:
            print("Insufficient balance.")
            return False

        self.__balance -= amount

        self.__record_transaction(
            transaction_type="Withdrawal",
            amount=amount,
            description="Cash withdrawal",
        )

        print(f"£{amount:.2f} withdrawn successfully.")
        return True

    def transfer(
        self,
        target_account: "BankAccount",
        amount: float,
    ) -> bool:
        """Transfer money to another account."""
        if self.status != "Active":
            print("Your account is locked.")
            return False

        if target_account.status != "Active":
            print("The target account is locked.")
            return False

        if target_account is self:
            print("You cannot transfer to the same account.")
            return False

        if amount <= 0:
            print("Transfer amount must be greater than zero.")
            return False

        if amount > self.__balance:
            print("Insufficient balance.")
            return False

        self.__balance -= amount
        target_account.__balance += amount

        self.__record_transaction(
            transaction_type="Transfer sent",
            amount=amount,
            description=(
                f"Transferred to {target_account.account_number}"
            ),
        )

        target_account.__record_transaction(
            transaction_type="Transfer received",
            amount=amount,
            description=(
                f"Received from {self.account_number}"
            ),
        )

        print(
            f"£{amount:.2f} transferred successfully to "
            f"{target_account.holder_name}."
        )

        return True

    def change_pin(
        self,
        current_pin: str,
        new_pin: str,
    ) -> bool:
        """Change the PIN after validating the current PIN."""
        if self.status != "Active":
            print("The account is locked.")
            return False

        if current_pin != self.__pin:
            print("Current PIN is incorrect.")
            return False

        if not new_pin.isdigit() or len(new_pin) != 4:
            print("New PIN must contain exactly four digits.")
            return False

        if new_pin == self.__pin:
            print("New PIN must be different from the current PIN.")
            return False

        self.__pin = new_pin

        self.__record_transaction(
            transaction_type="PIN change",
            amount=0.0,
            description="PIN changed successfully",
        )

        print("PIN changed successfully.")
        return True

    def unlock_account(self) -> None:
        """Administrative helper for the simulation."""
        self.status = "Active"
        self.failed_attempts = 0

    def __record_transaction(
        self,
        transaction_type: str,
        amount: float,
        description: str,
    ) -> None:
        """Store a transaction in the private ledger."""
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "description": description,
            "balance_after": self.__balance,
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
        }

        self.__transactions.append(transaction)

    def show_mini_statement(self) -> None:
        """Display the last five transactions."""
        if not self.__transactions:
            print("No transactions found.")
            return

        print("\n--- Mini-Statement ---")
        print(f"Account: {self.account_number}")
        print(f"Holder: {self.holder_name}")

        recent_transactions = self.__transactions[-5:]

        for transaction in recent_transactions:
            print(
                f"\n{transaction['timestamp']}\n"
                f"Type: {transaction['type']}\n"
                f"Amount: £{transaction['amount']:.2f}\n"
                f"Details: {transaction['description']}\n"
                f"Balance: £{transaction['balance_after']:.2f}"
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert the account object into JSON-compatible data."""
        return {
            "account_number": self.account_number,
            "holder_name": self.holder_name,
            "pin": self.__pin,
            "balance": self.__balance,
            "status": self.status,
            "failed_attempts": self.failed_attempts,
            "transactions": self.__transactions,
        }


class Bank:
    def __init__(self, filename: str = "accounts.json"):
        self.filename = filename
        self.accounts: dict[str, BankAccount] = {}
        self.load_accounts()

    def add_account(self, account: BankAccount) -> bool:
        """Add a new bank account."""
        if account.account_number in self.accounts:
            print("An account with this number already exists.")
            return False

        self.accounts[account.account_number] = account
        self.save_accounts()

        print("Account added successfully.")
        return True

    def find_account(
        self,
        account_number: str,
    ) -> BankAccount | None:
        """Find an account by its account number."""
        return self.accounts.get(account_number.strip())

    def save_accounts(self) -> None:
        """Save all account data to JSON."""
        data = {
            account_number: account.to_dict()
            for account_number, account in self.accounts.items()
        }

        try:
            with open(
                self.filename,
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(data, file, indent=4)

        except OSError as error:
            print(f"Could not save account data: {error}")

    def load_accounts(self) -> None:
        """Restore account objects from JSON."""
        if not os.path.exists(self.filename):
            self.accounts = {}
            return

        try:
            with open(
                self.filename,
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            self.accounts = {}

            for account_number, account_data in data.items():
                account = BankAccount(
                    account_number=account_data["account_number"],
                    holder_name=account_data["holder_name"],
                    pin=account_data["pin"],
                    balance=account_data["balance"],
                    status=account_data.get("status", "Active"),
                    failed_attempts=account_data.get(
                        "failed_attempts",
                        0,
                    ),
                    transactions=account_data.get(
                        "transactions",
                        [],
                    ),
                )

                self.accounts[account_number] = account

        except json.JSONDecodeError:
            print("The account data file is damaged.")
            self.accounts = {}

        except (KeyError, TypeError, ValueError) as error:
            print(f"Invalid account data: {error}")
            self.accounts = {}

        except OSError as error:
            print(f"Could not load account data: {error}")
            self.accounts = {}


class ATM:
    def __init__(self, bank: Bank):
        self.bank = bank
        self.current_account: BankAccount | None = None

    def get_numeric_amount(self, prompt: str) -> float | None:
        """Accept and validate a currency amount."""
        raw_value = input(prompt).strip()

        try:
            amount = float(raw_value)

            if amount <= 0:
                print("Amount must be greater than zero.")
                return None

            return round(amount, 2)

        except ValueError:
            print("Please enter a valid numeric amount.")
            return None

    def login(self) -> bool:
        """Authenticate an account holder."""
        account_number = input(
            "Enter account number: "
        ).strip()

        account = self.bank.find_account(account_number)

        if account is None:
            print("Account not found.")
            return False

        if account.status == "Locked":
            print("This account is locked.")
            return False

        pin = input("Enter your four-digit PIN: ").strip()

        if not pin.isdigit():
            print("PIN must contain digits only.")
            return False

        authenticated = account.authenticate(pin)
        self.bank.save_accounts()

        if authenticated:
            self.current_account = account
            print(f"\nWelcome, {account.holder_name}.")
            return True

        return False

    def show_menu(self) -> None:
        print("\n--- ATM Menu ---")
        print("1. Check balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Mini-statement")
        print("6. Change PIN")
        print("7. Logout")

    def handle_deposit(self) -> None:
        if self.current_account is None:
            return

        amount = self.get_numeric_amount(
            "Enter deposit amount: £"
        )

        if amount is None:
            return

        if self.current_account.deposit(amount):
            self.bank.save_accounts()

    def handle_withdrawal(self) -> None:
        if self.current_account is None:
            return

        amount = self.get_numeric_amount(
            "Enter withdrawal amount: £"
        )

        if amount is None:
            return

        if self.current_account.withdraw(amount):
            self.bank.save_accounts()

    def handle_transfer(self) -> None:
        if self.current_account is None:
            return

        target_number = input(
            "Enter target account number: "
        ).strip()

        target_account = self.bank.find_account(target_number)

        if target_account is None:
            print("Target account not found.")
            return

        amount = self.get_numeric_amount(
            "Enter transfer amount: £"
        )

        if amount is None:
            return

        if self.current_account.transfer(
            target_account,
            amount,
        ):
            self.bank.save_accounts()

    def handle_pin_change(self) -> None:
        if self.current_account is None:
            return

        current_pin = input(
            "Enter current PIN: "
        ).strip()

        new_pin = input(
            "Enter new four-digit PIN: "
        ).strip()

        if self.current_account.change_pin(
            current_pin,
            new_pin,
        ):
            self.bank.save_accounts()

    def account_session(self) -> None:
        """Run the ATM menu after successful login."""
        while self.current_account is not None:
            self.show_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                balance = self.current_account.get_balance()
                print(f"Current balance: £{balance:.2f}")

            elif choice == "2":
                self.handle_deposit()

            elif choice == "3":
                self.handle_withdrawal()

            elif choice == "4":
                self.handle_transfer()

            elif choice == "5":
                self.current_account.show_mini_statement()

            elif choice == "6":
                self.handle_pin_change()

            elif choice == "7":
                print("You have been logged out.")
                self.current_account = None

            else:
                print("Enter a valid option from 1 to 7.")

    def run(self) -> None:
        """Start the ATM application."""
        while True:
            print("\n--- Professional ATM Simulation ---")
            print("1. Login")
            print("2. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                if self.login():
                    self.account_session()

            elif choice == "2":
                print("Thank you for using the ATM.")
                break

            else:
                print("Enter either 1 or 2.")


def create_sample_accounts(bank: Bank) -> None:
    """Create demonstration accounts on the first run."""
    if bank.accounts:
        return

    account1 = BankAccount(
        account_number="1001",
        holder_name="Sriharsh",
        pin="1234",
        balance=5000,
    )

    account2 = BankAccount(
        account_number="1002",
        holder_name="Rahul",
        pin="5678",
        balance=3000,
    )

    bank.add_account(account1)
    bank.add_account(account2)


def main() -> None:
    bank = Bank()
    create_sample_accounts(bank)

    atm = ATM(bank)
    atm.run()


if __name__ == "__main__":
    main()