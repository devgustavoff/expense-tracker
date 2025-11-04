import argparse
import sqlite3
from datetime import datetime
import pandas as pd
import calendar

# Classe que representa as expenses
class Expense:
    def __init__(self, description, amount):
        self.description = description
        self.amount = amount
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
        date TEXT
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
        INSERT INTO Expenses(description, amount, date)
        VALUES (?, ?, ?);
        """
        # Aqui é obtido a data que a expense foi inserida na tabela
        # E também estamos formatando ela para o formato ISO
        current_datatime = expense.date.isoformat()

        # Aqui temos uma tupla com os dados da expenses
        expense_data = (expense.description, expense.amount, current_datatime)

        # Executamos a query de inserção junto com os dados da expense que sera iserida no DB
        cursor.execute(insert_query, expense_data)

        # Fazemos o comite para salvar as alterações no DB
        connection.commit()

        print(f"Expense added successfully")


# Essa função mostra todas as expenses no DB
def list_expenses():
    """Display all expenses in formatted table

    :return: None
    """
    
    # Instrução que faz a conecxão com o DB
    with sqlite3.connect(EXPENSE_FILE) as connection:

        # Query que seleciona e motra as colunas expecificadas de Expenses
        select_query = "SELECT id, date, description, amount FROM Expenses;"

        # Aqui usamos a biblioteca pandas para criar um dataframe
        df = pd.read_sql_query(select_query, connection)

        # Instrução que renomeia o nome das colunas
        df = df.rename(columns={
            'id':'ID',
            'date':'Date',
            'description':'Description',
            'amount':'Amount'
        })

        # Converte a data para o formato YYYY/MM/DD
        df['Date'] = pd.to_datetime(df['Date']).dt.date

        # Esse instrunção transforma valores Null/NaN no formato 0.00
        df['Amount'] = df['Amount'].fillna(0.0)

        # Essa instrução aplica a função lambda em todos os valores da coluna amount
        # A expressão que a lambda recebe de conversão, essa expressão converte todo valor x em um valor com 2 casas decimais
        df['Amount'] = df['Amount'].apply(lambda x: f"${x:.2f}")

        # Imprime o dataframe no formato string, o index=Fales é para desativar os indices das linhas
        # não quero mostrar os idices das linhas
        print(df.to_string(index=False))


def update_expense(expense_id, amount):
    """Update an expense existente

    :param expense_id: int - id of expense.
    :param amount: float -  value of expense.
    """

    with sqlite3.connect(EXPENSE_FILE) as connection:

        cursor = connection.cursor()

        update_query = """
        UPDATE Expenses
        SET amount = ?
        WHERE id = ?;
        """
        cursor.execute(update_query, (amount, expense_id))

        connection.commit()

        print(f"Expense updated successfully (ID: {expense_id})")

def delete_expense(expense_id):
    """Delete an specific expense

    :param expense_id: int - ID of expense.
    :return: None
    """

    with sqlite3.connect(EXPENSE_FILE) as connection:

        cursor = connection.cursor()

        select_query = """
        SELECT 1
        FROM Expenses
        WHERE id = ?
        """

        cursor.execute(select_query, (expense_id,))

        aux = cursor.fetchone()

        if aux != None:

            delete_query = """
            DELETE FROM Expenses
            WHERE id = ?;
            """
            cursor.execute(delete_query, (expense_id,))

            connection.commit()

            print(f"Expense deleted successfully (ID: {expense_id})")
        else:
            print("Expense not found")


def summary_total():
    """Display summary total of expenses

    :return: None
    """

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
    """Display summary of a specific month

    :return: None
    """
    
    with sqlite3.connect(EXPENSE_FILE) as connection:

        cursor = connection.cursor()

        summary_month_query = """
        SELECT SUM(amount)
        FROM Expenses
        WHERE strftime('%m', date) = ?
        """

        cursor.execute(summary_month_query, (month,))

        month_expenses = cursor.fetchone()

        name_of_month = calendar.month_name[int(month)]

        try:
            print(f"Total expenses for {name_of_month} ${month_expenses[0]:.2f}")
        except TypeError:
            print(f"Date not found")

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

# Comando para listar todas as despesas
parser_list = subparsers.add_parser('list', help='List all expenses in lista of expenses')

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
    insertion_expense(Expense(description=args.description, amount=args.amount))
elif args.command == 'update':
    update_expense(args.id, args.amount)
elif args.command == 'delete':
    delete_expense(args.id)
elif args.command == 'list':
    list_expenses()
elif args.command == 'summary':
    if args.month:
        summary_month(args.month)
    else:
        summary_total()
