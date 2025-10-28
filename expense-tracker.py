import argparse
import sqlite3
from datetime import datetime
import pandas as pd

class Expense:
    def __init__(self, description, amount):
        self.description = description
        self.amount = amount
        self.date = datetime.now()

EXPENSE_FILE = 'expense_storage.db'

with sqlite3.connect(EXPENSE_FILE) as connection:
    
    cursor = connection.cursor()

    created_table_query = """
    CREATE TABLE IF NOT EXISTS Expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        amount REAL,
        date TEXT
    );
    """
    cursor.execute(created_table_query)

    connection.commit()

def insertion_expense(expense):
    
    with sqlite3.connect(EXPENSE_FILE) as connection:

        cursor = connection.cursor()
        insert_query = """
        INSERT INTO Expenses(description, amount, date)
        VALUES (?, ?, ?);
        """
    
        current_datatime = expense.date.isoformat()

        expense_data = (expense.description, expense.amount, current_datatime)

        cursor.execute(insert_query, expense_data)

        connection.commit()

# Me explique essa função
def list_expenses():
    
    with sqlite3.connect(EXPENSE_FILE) as connection:

        select_query = "SELECT id, date, description, amount FROM Expenses;"

        df = pd.read_sql_query(select_query, connection)

        df = df.rename(columns={
            'id':'ID',
            'date':'Date',
            'description':'Description',
            'amount':'Amount'
        })
        # Formatar exibição da data
        print(df.to_string(index=False, formatters={'Amount': '${:.2f}'.format}))

def update_expense(expense_id, amount):

    with sqlite3.connect(EXPENSE_FILE) as connection:

        cursor = connection.cursor()

        update_query = """
        UPDATE Expenses
        SET amount = ?
        WHERE id = ?;
        """
        cursor.execute(update_query, (amount, expense_id))

        connection.commit()

        print(f"Update amount for {expense_id} to {amount}")

def delete_expense(expense_id):
    
    with sqlite3.connect(EXPENSE_FILE) as connection:

        cursor = connection.cursor()

        delete_query = """
        DELETE FROM Expenses
        WHERE id = ?;
        """
        cursor.execute(delete_query, (expense_id,))

        connection.commit()

        print("Expense deleted successfully")

def summary_total():
    
    with sqlite3.connect(EXPENSE_FILE) as connection:

        cursor = connection.cursor()

        summary_total_query = """
        SELECT SUM(amount)
        FROM Expenses
        """

        cursor.execute(summary_total_query)

        total_expenses = cursor.fetchone()

        print(f"Total expenses: ${total_expenses[0]:.2f}")

def summary_month(month):
    
    with sqlite3.connect(EXPENSE_FILE) as connection:

        cursor = connection.cursor()

        summary_month_query = """
        SELECT SUM(amount)
        FROM Expenses
        WHERE strftime('%m', date) = ?
        """

        cursor.execute(summary_month_query, (month,))

        month_expenses = cursor.fetchone()

        print(month_expenses)

parser = argparse.ArgumentParser(description='Manage expenses')
subparsers = parser.add_subparsers(dest='command', required=True)

# Argumentos para adicionar uma despesa
parser_add = subparsers.add_parser('add', help='Add a new expense')
parser_add.add_argument('--description', action='store', help='Description of expense')
parser_add.add_argument('--amount', type=float, action='store', help='Amount of expense')

# Argumento para listar as despesa
parser_list = subparsers.add_parser('list', help='List all expenses in lista of expenses')

# Argumento para atualizar despesa
parser_update = subparsers.add_parser('update', help='Update the amount of expense')
parser_update.add_argument('--expense', type=int, action='store', help='ID of expense')
parser_update.add_argument('--amount', type=float, action='store', help='New amount')

# Agumento para deletar despesa
parser_delete = subparsers.add_parser('delete', help="Delete a expense")
parser_delete.add_argument('--expense', type=int, action='store', help='ID of expense')

# Argumento para mostrar o total das despesas
parser_summary = subparsers.add_parser('summary', help="Show the total of expenses")
parser_summary.add_argument('--month', type=str, action='store', help="Show the total of expense for a specific month")

args = parser.parse_args()

if args.command == 'add':
    insertion_expense(Expense(description=args.description, amount=args.amount))
elif args.command == 'update':
    update_expense(args.expense, args.amount)
elif args.command == 'delete':
    delete_expense(args.expense)
elif args.command == 'list':
    list_expenses()
elif args.command == 'summary':
    if args.month:
        summary_month(args.month)
    else:
        summary_total()
