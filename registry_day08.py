from abc import ABC, abstractmethod


class Account(ABC):

    def __init__(self, owner, number, phone, branch, account_type, balance=0):
        self.owner = owner
        self.account_number = number
        self.phone = phone
        self.branch = branch
        self.account_type = account_type
        self._balance = balance
        self.bank = "Abyssinia Bank"
        self.status = "Active"
        self.history = []

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
        else:
            self._balance += amount
            self.history.append({
                'type': 'deposit',
                'amount': amount,
                'balance_before': self._balance - amount
            })
            print(f"Deposited {amount} ETB")
            print(f"New Balance: {self._balance} ETB")

    @abstractmethod
    def withdraw(self, amount):
        pass

    def undo_last(self):
        if not self.history:
            print(f"  No transactions to undo for account {self.account_number}")
            return False

        last_tx = self.history.pop()

        if last_tx['type'] == 'deposit':
            self._balance -= last_tx['amount']
            print(f"  UNDO: Removed deposit of {last_tx['amount']} ETB from account {self.account_number}")
        else:
            self._balance += last_tx['amount']
            print(f"  UNDO: Restored withdrawal of {last_tx['amount']} ETB to account {self.account_number}")

        return True

    def statement(self):
        print("\n--- Account Statement ---")
        print(f"Bank: {self.bank}")
        print(f"Owner: {self.owner}")
        print(f"Account Number: {self.account_number}")
        print(f"Account Type: {self.account_type}")
        print(f"Status: {self.status}")
        print(f"Balance: {self._balance} ETB")

    def __repr__(self):
        return f"Account({self.account_number}, {self.owner}, Balance: {self._balance} ETB)"


class SavingsAccount(Account):

    def __init__(self, owner, number, phone, branch, balance=0, interest_rate=0.05):
        super().__init__(owner, number, phone, branch, "Savings", balance)
        self.interest_rate = interest_rate

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount")
        elif amount > self._balance - 50:
            print("Savings account must keep minimum 50 ETB")
        else:
            self._balance -= amount
            self.history.append({
                'type': 'withdraw',
                'amount': amount,
                'balance_before': self._balance + amount
            })
            print(f"Withdrawn {amount} ETB from Savings Account")

    def statement(self):
        super().statement()
        print(f"Interest Rate: {self.interest_rate * 100}%")
        print("------------------------")


class CurrentAccount(Account):

    def __init__(self, owner, number, phone, branch, balance=0, overdraft_limit=2000):
        super().__init__(owner, number, phone, branch, "Current", balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount")
        elif amount > self._balance + self.overdraft_limit:
            print("Overdraft limit exceeded")
        else:
            self._balance -= amount
            self.history.append({
                'type': 'withdraw',
                'amount': amount,
                'balance_before': self._balance + amount
            })
            print(f"Withdrawn {amount} ETB from Current Account")

    def statement(self):
        super().statement()
        print(f"Overdraft Limit: {self.overdraft_limit} ETB")
        print("------------------------")


class AccountRegistry:

    def __init__(self):
        self.by_number = {}
        self.order = []

    def add(self, acc):
        self.by_number[acc.account_number] = acc
        self.order.append(acc.account_number)

    def find(self, number):
        return self.by_number.get(number)

    def list_all(self):
        return [self.by_number[num] for num in self.order]

    def top_by_balance(self, n):
        all_accounts = list(self.by_number.values())
        sorted_accounts = sorted(all_accounts, key=lambda acc: acc.balance, reverse=True)
        return sorted_accounts[:n]

    def _get_sorted_numbers(self):
        return sorted(self.order)

    def binary_search(self, number):
        sorted_numbers = self._get_sorted_numbers()
        low, high = 0, len(sorted_numbers) - 1

        while low <= high:
            mid = (low + high) // 2
            mid_number = sorted_numbers[mid]

            if mid_number == number:
                return self.by_number[mid_number]
            elif mid_number < number:
                low = mid + 1
            else:
                high = mid - 1

        return None

    def find_by_number(self, number):
        return self.binary_search(number)

    def total_transactions(self, acc, index=0):
        if isinstance(acc, str):
            acc = self.find(acc)
            if acc is None:
                return 0

        if index >= len(acc.history):
            return 0

        return acc.history[index]['amount'] + self.total_transactions(acc, index + 1)

    def undo_last(self, account_number):
        account = self.find(account_number)
        if account is None:
            print(f"Account {account_number} not found")
            return False
        return account.undo_last()


if __name__ == "__main__":
    print("=" * 60)
    print("DAY 8: SORT & SEARCH THE REGISTRY")
    print("=" * 60)

    registry = AccountRegistry()

    accounts = [
        SavingsAccount("Amen", "123456", "+251987654321", "Sarbet", 1000),
        CurrentAccount("Kirubel", "654321", "+251911223344", "Bole", 1000),
        SavingsAccount("Charlie", "111111", "+251922334455", "Piassa", 2500, 0.07),
        CurrentAccount("Diana", "222222", "+251933445566", "Merkato", 750, 3000),
        SavingsAccount("Eve", "333333", "+251944556677", "Bole", 3000, 0.04),
    ]

    for acc in accounts:
        registry.add(acc)

    print("\n=== Running Transactions ===")
    for account in accounts:
        account.deposit(200)
        account.withdraw(1100)
        account.statement()

    print("\n" + "=" * 60)
    print("STEP 2: top_by_balance(n)")
    print("=" * 60)
    print("Top 3 accounts by balance:")
    top3 = registry.top_by_balance(3)
    for i, acc in enumerate(top3, 1):
        print(f"  {i}. {acc.account_number} — {acc.owner}: {acc.balance} ETB")

    print("\nTop 5 (all):")
    top5 = registry.top_by_balance(5)
    for i, acc in enumerate(top5, 1):
        print(f"  {i}. {acc.account_number} — {acc.owner}: {acc.balance} ETB")

    print("\n" + "=" * 60)
    print("STEP 3: binary_search(number)")
    print("=" * 60)

    result = registry.find_by_number("123456")
    print(f"find_by_number('123456'): {result}")

    result = registry.find_by_number("999999")
    print(f"find_by_number('999999'): {result}")

    print("\nComparison:")
    print(f"  O(1) find('654321'):       {registry.find('654321')}")
    print(f"  O(log n) find_by_number('654321'): {registry.find_by_number('654321')}")

    print("\n" + "=" * 60)
    print("STEP 4: total_transactions(acc, index)")
    print("=" * 60)

    amen = registry.find("123456")
    print(f"\nAccount 123456 ({amen.owner}) history:")
    for i, tx in enumerate(amen.history):
        print(f"  [{i}] {tx['type']}: {tx['amount']} ETB")

    total = registry.total_transactions(amen)
    print(f"Total transaction amount: {total} ETB")

    kirubel = registry.find("654321")
    print(f"\nAccount 654321 ({kirubel.owner}) history:")
    for i, tx in enumerate(kirubel.history):
        print(f"  [{i}] {tx['type']}: {tx['amount']} ETB")

    total = registry.total_transactions("654321")
    print(f"Total transaction amount: {total} ETB")

    print("\n" + "=" * 60)
    print("UNDO DEMO")
    print("=" * 60)

    print(f"\nBefore undo: {amen.owner} balance = {amen.balance} ETB")
    registry.undo_last("123456")
    print(f"After undo:  {amen.owner} balance = {amen.balance} ETB")

    print("\n" + "=" * 60)
    print("BIG-O COMPLEXITY SUMMARY")
    print("=" * 60)
    print("  add(acc)              → O(1)")
    print("  find(number)          → O(1)")
    print("  list_all()            → O(n)")
    print("  top_by_balance(n)     → O(n log n)")
    print("  find_by_number()      → O(log n)")
    print("  total_transactions()  → O(m)")
    print("  undo_last()           → O(1)")
