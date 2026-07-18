class Account:
    """A simple bank account with balance and transaction history."""
    def __init__(self, account_number, owner_name, initial_balance=0.0):
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = initial_balance
        self.history = []  

    def deposit(self, amount):
        """Deposit money and push record to history stack."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self.history.append({
            'type': 'deposit',
            'amount': amount,
            'balance_before': self.balance - amount
        })

    def withdraw(self, amount):
        """Withdraw money and push record to history stack."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.history.append({
            'type': 'withdraw',
            'amount': amount,
            'balance_before': self.balance + amount
        })

    def undo_last(self):
        """Pop the most recent transaction and reverse its effect."""
        if not self.history:
            print(f"  No transactions to undo for account {self.account_number}")
            return False

        last_tx = self.history.pop()

        if last_tx['type'] == 'deposit':
            self.balance -= last_tx['amount']
            print(f"  UNDO: Removed deposit of {last_tx['amount']:.2f} from account {self.account_number}")
        else:
            self.balance += last_tx['amount']
            print(f"  UNDO: Restored withdrawal of {last_tx['amount']:.2f} to account {self.account_number}")

        return True

    def __repr__(self):
        return f"Account({self.account_number}, {self.owner_name}, Balance: {self.balance:.2f})"


class AccountRegistry:
  
    def __init__(self):
        self.by_number = {}   
        self.order = []       

    def add(self, acc):
        """Add an account to the registry. O(1) time."""
        self.by_number[acc.account_number] = acc
        self.order.append(acc.account_number)

    def find(self, number):
        """Find an account by number. O(1) time."""
        return self.by_number.get(number)

    def list_all(self):
        """Return all accounts in insertion order. O(n) time."""
        return [self.by_number[num] for num in self.order]

    def top_by_balance(self, n):
        all_accounts = list(self.by_number.values())
        sorted_accounts = sorted(all_accounts, key=lambda acc: acc.balance, reverse=True)
        return sorted_accounts[:n]

    def _get_sorted_numbers(self):
        """Return account numbers sorted for binary search."""
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
        """Undo the most recent transaction on a specific account."""
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

    acc1 = Account("ACC-001", "Alice", 1000.0)
    acc2 = Account("ACC-002", "Bob", 500.0)
    acc3 = Account("ACC-003", "Charlie", 2500.0)
    acc4 = Account("ACC-004", "Diana", 750.0)
    acc5 = Account("ACC-005", "Eve", 3000.0)

    for acc in [acc1, acc2, acc3, acc4, acc5]:
        registry.add(acc)

    acc1.deposit(500.0)
    acc1.withdraw(200.0)
    acc1.deposit(300.0)

    acc3.deposit(1000.0)
    acc3.withdraw(500.0)

    print("\n--- STEP 2: top_by_balance(n) ---")
    print("Top 3 accounts by balance:")
    top3 = registry.top_by_balance(3)
    for i, acc in enumerate(top3, 1):
        print(f"  {i}. {acc.account_number} — {acc.owner_name}: {acc.balance:.2f}")

    print("\nTop 5 (all):")
    top5 = registry.top_by_balance(5)
    for i, acc in enumerate(top5, 1):
        print(f"  {i}. {acc.account_number} — {acc.owner_name}: {acc.balance:.2f}")

   
    print("\n--- STEP 3: binary_search(number) ---")

    result = registry.find_by_number("ACC-003")
    print(f"find_by_number('ACC-003'): {result}")

    result = registry.find_by_number("ACC-999")
    print(f"find_by_number('ACC-999'): {result}")
    print("\nComparison:")
    print(f"  O(1) find('ACC-004'):       {registry.find('ACC-004')}")
    print(f"  O(log n) find_by_number('ACC-004'): {registry.find_by_number('ACC-004')}")
    print("\n--- STEP 4: total_transactions(acc, index) ---")
    total1 = registry.total_transactions(acc1)
    print(f"ACC-001 total transaction amount: {total1:.2f}")
    print(f"  (History: deposit 500 + withdraw 200 + deposit 300 = {total1:.2f})")
    total3 = registry.total_transactions("ACC-003")
    print(f"\nACC-003 total transaction amount: {total3:.2f}")
    print(f"  (History: deposit 1000 + withdraw 500 = {total3:.2f})")

    total2 = registry.total_transactions(acc2)
    print(f"\nACC-002 total transaction amount: {total2:.2f}")
    print(f"  (No transactions yet)")
    print("\n" + "=" * 60)
    print("BIG-O COMPLEXITY SUMMARY (DAY 8)")
    print("=" * 60)
    print("  add(acc)              → O(1)")
    print("  find(number)          → O(1)   — dict lookup")
    print("  list_all()            → O(n)")
    print("  top_by_balance(n)     → O(n log n) — sorting")
    print("  find_by_number()      → O(log n) — binary search")
    print("  total_transactions()  → O(m)   — m = history length, recursive")
    print("  undo_last()           → O(1)")
