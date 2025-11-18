import argparse
import sqlite3
from datetime import datetime
import calendar

# Classe que representa as expenses
class Expense:
    def __init__(self, description, amount, category):
        self.description = description
        self.amount = amount
        self.category = category
        self.date = datetime.now()

# Constante que armazena uma string que representa o nome do banco de dados
EXPENSE_FILE = 'expense_storage.db'

# Aqui é feito uma conecxão com o banco de dados
# É a instrução with é usada para auxiliar a conecxão com o bd abrido e fechando a conecxão
with sqlite3.connect(EXPENSE_FILE) as connection:
    
    # essa variavel cursor é resposavel por fazer as ações de manipulação de dados detro do DB
    # ela um ponteiro para o DB e executamos ações no DB atraves desse ponteiro
    cursor = connection.cursor()

    # Aqui é criado uma query para criar uma tabela
    # Caso a table não exista ela é criada 
    created_table_query = """
    CREATE TABLE IF NOT EXISTS Expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        amount REAL,
        date TEXT,
        category TEXT
    );
    """
    # Aqui estamos executando o metodo execute() para executar a query dentro do DB o arquivo
    cursor.execute(created_table_query)

    # Essa instrução sala as alterações feitas.
    connection.commit()

# Função que insere uma expense no database
# Ela recebe um objeto expense
def insertion_expense(expense):
    """Insert a expense in the database

    :param expense: float - value of expense
    :return: None 
    """
    # Caso o valor da despesa seja negativo
    if expense.amount < 0:
        print("Invalid value")
        return
    
    # Instrução usada para fazer a conecxão com o DB
    with sqlite3.connect(EXPENSE_FILE) as connection:

        # Ponteito para o DB
        cursor = connection.cursor()

        # Query para inserir dados no DB
        insert_query = """
        INSERT INTO Expenses(description, amount, date, category)
        VALUES (?, ?, ?, ?);
        """
        # Aqui é obtido a data que a expense foi inserida na tabela
        # E também estamos formatando ela para o formato ISO
        current_datatime = expense.date.isoformat()

        # Aqui temos uma tupla com os dados da expenses
        expense_data = (expense.description, expense.amount, current_datatime, expense.category)

        # Executamos a query de inserção junto com os dados da expense que sera iserida no DB
        cursor.execute(insert_query, expense_data)

        # Fazemos o comite para salvar as alterações no DB
        connection.commit()

        print(f"Expense added successfully")

def get_all_expenses():
    """Obtains all expenses on the DB.

    :return: list - list of dictionary containing expense data 
    """
    with sqlite3.connect(EXPENSE_FILE) as connection:
        cursor = connection.cursor()
        select_query = """
        SELECT id, date, description, amount, category
        FROM Expenses;
        """
        cursor.execute(select_query)
        column_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(column_names, row)) for row in rows]

def list_expenses(category):
    """Display all expenses in formatted table

    :return: None
    """
    expenses = get_all_expenses()
    
    if not expenses:
        id_width = len('ID')
        date_width = len('Date')
        desc_width = len('Description')
        amount_width = len('Amount')
        ctg_width = len('Category')
    else:
        if category:
            expenses = [expense for expense in expenses if expense['category'] == category]
        
        id_width = max(len('ID'), max(len(str(exp['id'])) for exp in expenses))
        date_width = max(len('Date'), max(len(exp['date']) for exp in expenses))
        desc_width = max(len('Description'), max(len(exp['description']) for exp in expenses))
        amount_width = max(len('Amount'), max(len(f"${exp['amount']:.2f}") for exp in expenses))
        ctg_width = max(len('Category'), max(len(exp['category']) for exp in expenses))

    
    print(f"{'ID':<{id_width}} {'Date':<{date_width}} {'Description':<{desc_width}} {'Amount':<{amount_width}} {'Category':<{ctg_width}}")
    for expense in expenses:
        print(f"{expense['id']:<{id_width}} {expense['date']:<{date_width}} {expense['description']:<{desc_width}} {f'${expense['amount']:.2f}':<{amount_width}} {expense['category']:<{ctg_width}}")

def get_expense_by_id(expense_id):
    """Obtains a specific expense

    :param expense_id: int  - ID of expense
    :return: dict or None - expense data if found, None otherwise
    """

    with sqlite3.connect(EXPENSE_FILE) as connection:
        cursor = connection.cursor()
        select_query = """
        SELECT id, date, description, amount
        FROM Expenses
        WHERE id = ?
        """
        cursor.execute(select_query, (expense_id,))
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchone()
        return dict(zip(columns, data)) if data else None

def update_expense(expense_id, amount):
    """Update an expense existente

    :param expense_id: int - id of expense.
    :param amount: float -  value of expense.
    """
    
    expense = get_expense_by_id(expense_id)
    if expense:
        with sqlite3.connect(EXPENSE_FILE) as connection:
            cursor = connection.cursor()
            update_query = """
            UPDATE Expenses
            SET amount = ?
            WHERE id = ?;
            """
            cursor.execute(update_query, (amount, expense_id))
            print(f"Expense updated successfully")
    else:
        print("Invalid ID")

def delete_expense(expense_id):
    """Delete an specific expense

    :param expense_id: int - ID of expense.
    :return: None
    """

    expense = get_expense_by_id(expense_id)
    if expense:
        with sqlite3.connect(EXPENSE_FILE) as connection:
            cursor = connection.cursor()
            delete_query = """
            DELETE
            FROM Expenses 
            WHERE id = ?
            """
            cursor.execute(delete_query, (expense_id,))
            print("Expense deleted successfully")
    else:
        print("Invalid ID")

def get_total_expenses():
    """Sum the total amount of all expenses

    :return: float - the total of colum amount
    """

    with sqlite3.connect(EXPENSE_FILE) as connection:
        cursor = connection.cursor()
        sum_query = """
        SELECT SUM(amount)
        FROM Expenses
        """
        cursor.execute(sum_query)
        result = cursor.fetchone()
        return result[0] if result[0] is not None else 0.0

def get_month_total(month):
    """Sum the total of all expenses of specific month

    :param month: string - number of month
    :return: float - total of expenses of specific month
    """
    
    month = str(month).zfill(2)
    
    with sqlite3.connect(EXPENSE_FILE) as connection:
        cursor = connection.cursor()
        sum_query = """
        SELECT SUM(amount)
        FROM Expenses
        WHERE strftime('%m', date) = ?
        """
        cursor.execute(sum_query, (month,))
        result = cursor.fetchone()
        return result[0] if result[0] is not None else 0.0

def summary_total():
    """Display summary total of expenses

    :return: None
    """

    print(f"Total expenses: ${get_total_expenses():.2f}")

def summary_month(month):
    """Display summary of a specific month

    :return: None
    """
    try:
        print(f"Total expenses for {calendar.month_name[int(month)]}: ${get_month_total(month):.2f}")
    except (IndexError, ValueError):
        print("Invalid month")

# Instanciamos um objeto analisador sintatico 
parser = argparse.ArgumentParser(description='Manage expenses')

# É criado um subanalisador sintatico
subparsers = parser.add_subparsers(dest='command', required=True)

# Comando para adicionar uma despesa
parser_add = subparsers.add_parser('add', help='Add a new expense')

# Argumento opcional para adcionar uma descrição a despesa
parser_add.add_argument('--description', action='store', help='Description of expense')

# Argumento opcional para adcionar o valor da despesa
parser_add.add_argument('--amount', type=float, action='store', help='Amount of expense')

parser_add.add_argument('--category', type=str, action='store', help='Category of expense')

# Comando para listar todas as despesas
parser_list = subparsers.add_parser('list', help='List all expenses in lista of expenses')

parser_list.add_argument('--category', type=str, action='store', help='Name of category')

# Comando para atualizar uma despesa especifica
parser_update = subparsers.add_parser('update', help='Update the amount of expense')

# Argumento opcional para especificar o ID da despesa
parser_update.add_argument('--id', type=int, action='store', help='ID of expense')

# Argumento opcional para especificar o novo valor da despesa
parser_update.add_argument('--amount', type=float, action='store', help='New amount')

# Comando para deletar uma despesa especifica
parser_delete = subparsers.add_parser('delete', help="Delete a expense")

# Argumento opcional que especifica o ID da despesa a ser deletada
parser_delete.add_argument('--id', type=int, action='store', help='ID of expense')

# Coamndo para mostrar a soma total das despesas
parser_summary = subparsers.add_parser('summary', help="Show the total of expenses")

# Argumento opcional caso queria saber o total das despesas de um mês especifico
parser_summary.add_argument('--month', type=str, action='store', help="Show the total of expense for a specific month")

# Nessa linha esta sendo executado o nalaisador sintatico
# Os dados são inseriodos em args
args = parser.parse_args()

if args.command == 'add':
    insertion_expense(Expense(description=args.description, amount=args.amount, category=args.category))
elif args.command == 'update':
    update_expense(args.id, args.amount)
elif args.command == 'delete':
    delete_expense(args.id)
elif args.command == 'list':
    list_expenses(category=args.category)
elif args.command == 'summary':
    if args.month:
        summary_month(args.month)
    else:
        summary_total()
