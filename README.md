# Expense Tracker CLI

Ferramenta de linha de comando para gerenciamento financeiro pessoal, construída em Python com persistência de dados em SQLite.

Project URL: https://github.com/devgustavoff/expense-tracker

## 🚀 Tecnologias

- **Python 3.x**
- **SQLite** - Banco de dados relacional
- **Pandas** - Manipulação e formatação de dados
- **argparse** - Interface de linha de comando

## 📋 Funcionalidades

- ✅ Adicionar despesas com descrição e valor
- ✅ Listar todas as despesas em formato de tabela
- ✅ Atualizar valor de despesas existentes
- ✅ Deletar despesas
- ✅ Visualizar resumo total de gastos
- ✅ Visualizar resumo de gastos por mês específico

## 🔧 Instalação

### Pré-requisitos
- Python 3.7 ou superior

### Instalar dependências
```bash
pip install pandas
```

## 💻 Como usar

### Adicionar uma despesa
```bash
python expense-tracker.py add --description "Almoço" --amount 25.50
```

### Listar todas as despesas
```bash
python expense-tracker.py list
```

### Atualizar uma despesa
```bash
python expense-tracker.py update --id 1 --amount 30.00
```

### Deletar uma despesa
```bash
python expense-tracker.py delete --id 1
```

### Ver resumo total de despesas
```bash
python expense-tracker.py summary
```

### Ver resumo de um mês específico
```bash
python expense-tracker.py summary --month 01
```
*Formato do mês: 01 para Janeiro, 02 para Fevereiro, etc.*

## 🗂️ Estrutura do Projeto

- **SQLite** para persistência de dados com schema bem definido
- **Interface CLI** profissional usando argparse com comandos e subcomandos
- **Formatação de dados** com Pandas para visualização clara
- **Arquitetura modular** com funções separadas para cada operação CRUD

## 📊 Exemplo de Saída
```
ID  Date        Description    Amount
1   2024-11-01  Almoço        $25.50
2   2024-11-02  Transporte    $15.00
3   2024-11-03  Mercado       $120.75
```

## 🎯 Projeto desenvolvido como parte do portfólio

Este projeto demonstra habilidades em:
- Desenvolvimento de aplicações CLI
- Trabalho com bancos de dados relacionais (SQLite)
- Manipulação de dados com Pandas
- Programação Orientada a Objetos (POO)
- Persistência e gerenciamento de dados

---

**Desenvolvido por Gustavo Fernandes**