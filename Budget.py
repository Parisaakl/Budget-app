class Category:
  # Initialize a category with a name and an empty ledger
  def __init__(self, category):
    self.category = category
    self.ledger = []

  # Define how the category should be represented as a string
  def __str__(self):
    s = self.category.center(30, "*") + "\n"

    # Loop through the ledger and format each item
    for item in self.ledger:
      temp = f"{item['description'][:23]:23}{item['amount']:7.2f}"
      s += temp + "\n"

    # Add the total balance at the end
    s += "Total: " + str(self.get_balance())
    return s

  # Add a deposit to the ledger with an optional description
  def deposit(self, amount, description=""):
    temp = {}
    temp['amount'] = amount
    temp['description'] = description
    self.ledger.append(temp)

  # Add a withdrawal to the ledger with an optional description
  def withdraw(self, amount, description=""):
    # Check if there are sufficient funds before adding the withdrawal
    if self.check_funds(amount):
      temp = {}
      temp['amount'] = 0 - amount
      temp['description'] = description
      self.ledger.append(temp)
      return True
    return False

  # Calculate and return the current balance
  def get_balance(self):
    balance = 0
    for item in self.ledger:
      balance += item['amount']
    return balance

  # Transfer funds from one category to another
  def transfer(self, amount, budget_cat):
    if self.check_funds(amount):
      self.withdraw(amount, "Transfer to " + budget_cat.category)
      budget_cat.deposit(amount, "Transfer from " + self.category)
      return True
    return False

  # Check if there are sufficient funds for a withdrawal or transfer
  def check_funds(self, amount):
    if amount > self.get_balance():
      return False
    return True

# Create a spending chart for a list of categories
def create_spend_chart(categories):
  spend = []
  
  # Calculate the total spent in each category
  for category in categories:
    temp = 0
    for item in category.ledger:
      if item['amount'] < 0:
        temp += abs(item['amount'])
    spend.append(temp)
  
  total = sum(spend)
  
  # Calculate the percentage spent in each category
  percentage = [i/total * 100 for i in spend]

  # Build the spending chart string
  s = "Percentage spent by category"
  for i in range(100, -1, -10):
    s += "\n" + str(i).rjust(3) + "|"
    for j in percentage:
      if j > i:
        s += " o "
      else:
        s += "   "
    s += " "  # Add spaces

  s += "\n    ----------"

  # Find the maximum length of category names
  cat_length = []
  for category in categories:
    cat_length.append(len(category.category))
  max_length = max(cat_length)

  # Add category names to the spending chart
  for i in range(max_length):
    s += "\n    "
    for j in range(len(categories)):
      if i < cat_length[j]:
        s += " " + categories[j].category[i] + " "
      else:
        s += "   "
    s += " "  # Add spaces

  return s
