from datetime import datetime  # Importa a biblioteca datetime para manipulação de datas e horas.

# Constantes do sistema (valores que não mudam durante a execução):
WITHDRAWAL_LIMIT = 3  # Limite máximo de saques por dia.
WITHDRAWAL_VALUE_LIMIT = 500.00  # Valor máximo permitido por saque.
DAILY_TRANSACTION_LIMIT = 10  # Limite máximo de transações diárias (depósitos + saques).

# Menu de opções apresentado ao usuário:
MENU = """
============BANCO============
ESCOLHA UMA OPERAÇÃO:
[a] DEPÓSITO
[b] SAQUE
[c] EXTRATO
[d] SAIR
=============================
"""

# Variáveis do sistema (valores que podem mudar durante a execução):
datetime_format = "%d/%m/%Y %H:%M"  # Formato de data/hora para exibição.
balance = 0  # Saldo inicial da conta.
statement = [f"Saldo inicial: R$ {balance:.2f}"]  # Lista que armazena o histórico de transações.
withdrawal_count = 0  # Contador de saques diários.
daily_transactions = 0  # Contador de transações diárias (depósitos e saques).
today = datetime.today().strftime("%d/%m/%Y")  # Data atual no formato dia/mês/ano.

# Função para realizar depósitos:
def deposit(amount, balance, statement, daily_transactions):
    balance += amount  # Adiciona o valor ao saldo atual.
    print(f"O valor de R${amount:.2f} foi depositado com sucesso.")
    timestamp = datetime.now()  # Obtém a data e hora atuais.
    # Adiciona uma entrada ao extrato com o valor depositado e a data/hora da transação:
    statement.append(f"R$ {amount:.2f} depositados - {timestamp.strftime(datetime_format)}")
    daily_transactions += 1  # Incrementa o contador de transações.
    return balance, statement, daily_transactions  # Retorna os novos valores de saldo, extrato e transações.

# Função para realizar saques:
def withdraw(amount, balance, withdrawal_count, statement, daily_transactions):

    if amount > balance:
        print("Saldo insuficiente para o saque.")  # Verifica se o saldo é suficiente.
    elif amount > WITHDRAWAL_VALUE_LIMIT:
        print(f"Valor informado é maior que o limite de R${WITHDRAWAL_VALUE_LIMIT:.2f} para saques.")  # Verifica se o valor está acima do permitido.
    else:
        balance -= amount  # Subtrai o valor do saldo.
        withdrawal_count += 1  # Incrementa o contador de saques.
        print(f"Retire o valor de R${amount:.2f} da máquina.")
        timestamp = datetime.now()  # Obtém a data e hora atuais.
        # Adiciona uma entrada ao extrato com o valor sacado e a data/hora da transação:
        statement.append(f"-R$ {amount:.2f} sacados - {timestamp.strftime(datetime_format)}")
        daily_transactions += 1  # Incrementa o contador de transações.
    return balance, statement, withdrawal_count, daily_transactions  # Retorna os novos valores.

# Função para imprimir o extrato:
def print_statement(statement, balance):
    print("\n===== EXTRATO =====")
    for item in statement:  # Percorre a lista de transações e imprime cada item.
        print(item)
    print(f"Saldo atual: R$ {balance:.2f}")  # Imprime o saldo atual da conta.
    print("====================\n")

# Loop principal do programa (exibe o menu e processa as opções do usuário):
while True:
    # Verifica se o dia mudou (para resetar os contadores diários):
    if today != datetime.today().strftime("%d/%m/%Y"):
        daily_transactions = 0  # Reseta o número de transações diárias.
        withdrawal_count = 0  # Reseta o número de saques diários.
        today = datetime.today().strftime("%d/%m/%Y")  # Atualiza a data.

    # Verifica se o limite de transações diárias foi alcançado:
    if daily_transactions >= DAILY_TRANSACTION_LIMIT:
        print("Limite de transações diárias alcançado!")
        print_statement(statement, balance)  # Imprime o extrato e finaliza o programa.
        break

    option = input(MENU).lower()  # Exibe o menu e recebe a opção do usuário.

    if option == "d":
        print("Obrigado por utilizar nossos serviços.")
        break  # Encerra o programa.

    elif option == "a":  # Depósito:
        deposit_value = float(input("Valor a ser depositado: R$"))
        if deposit_value > 0:
            # Chama a função de depósito e atualiza as variáveis:
            balance, statement, daily_transactions = deposit(deposit_value, balance, statement, daily_transactions)
        else:
            print("Apresente um valor válido.")  # Valida se o valor informado é positivo.

    elif option == "b":  # Saque:

        if withdrawal_count >= WITHDRAWAL_LIMIT:
            print("Você atingiu o limite de saques diários.")  # Verifica se o limite de saques foi atingido.
        else:
            withdrawal_value = float(input("Valor a ser sacado: R$"))
            if withdrawal_value > 0:
                # Chama a função de saque e atualiza as variáveis:
                balance, statement, withdrawal_count, daily_transactions = withdraw(withdrawal_value, balance, withdrawal_count, statement, daily_transactions)
            else:
                print("Apresente um valor válido.")  # Valida se o valor informado é positivo.

    elif option == "c":  # Imprimir extrato:
        print_statement(statement, balance)

    else:
        print("Opção inválida, tente novamente.")  # Mensagem de erro para opções inválidas.
