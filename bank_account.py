class BankAccount: 
    def __init__(self, account_holder: str, initial_balance: float = 0.0):
        self.account_holder = account_holder
        self.__balance = initial_balance
        self.__transactions = []
        
    
    def get_balance(self) -> float: 
        return self.__balance

    
    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than 0")
            return False

        self.__balance += amount
        print(f"${amount:.2f} deposited successfully") 
        print(f"balance is now {self.__balance:.2f}")
        return True 

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Withrawal amount must be positive")
        elif amount > self.__balance:
            raise ValueError("Cannot withdraw more than balance")
            return False 

        self.__balance -= amount
        print(f"${amount:.2f} withdrawn successfully")
        print(f"balance is now: {self.__balance}")
        return True 

    def transfer(self, target_account, amount: float) -> bool:
            if amount > self.__balance: 
                raise ValueError("Not enough balance")
            if amount <= 0:
                raise ValueError("Transfer amount must be greater than zero.")

            self.withdraw(amount)
            target_account.deposit(amount)
            print(f"${amount:.2f} transferred successfully to {target_account.account_holder}")
        
            return True 



account = BankAccount("Sriharsh", 1000)
print(account.account_holder)
print(account.get_balance())

account2 = BankAccount("John", 500)


account.deposit(500)
account.withdraw(200)
print(f"${account.get_balance()}")
account.transfer(account2, 300)    

