import textwrap  # Biblioteca padrão para manipular texto formatado
from abc import ABC, abstractmethod  # Para criar classes abstratas
from datetime import datetime  # Para registrar data/hora nas transações

# Classe base genérica — usada como superclasse
# OOP: Herança — outras classes herdam seus atributos e métodos
class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []  # OOP: Composição — Cliente tem uma lista de contas

    def perform_transaction(self, account, transaction):
        # OOP: Polimorfismo — aceita objetos de diferentes tipos (Deposit ou Withdrawal)
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)


# Classe especializada que herda de Client
# OOP: Herança — reaproveita e estende atributos
class Individual(Client):
    def __init__(self, name, birth_date, cpf, address):
        super().__init__(address)  # Python: chama construtor da superclasse
        self.name = name
        self.birth_date = birth_date
        self.cpf = cpf


# Classe base para contas bancárias
class Account:
    def __init__(self, number, client):
        self._balance = 0  # OOP: Encapsulamento — atributo protegido
        self._number = number
        self._agency = "0001"
        self._client = client
        self._history = History()  # OOP: Composição — conta contém histórico

    @classmethod
    def new_account(cls, client, number):
        # Python: método de classe — usa cls ao invés de self
        return cls(number, client)

    # Pythonic way de acessar atributos privados
    # OOP: Encapsulamento via @property
    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def agency(self):
        return self._agency

    @property
    def client(self):
        return self._client

    @property
    def history(self):
        return self._history

    def withdraw(self, amount):
        if amount > self.balance:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif amount > 0:
            self._balance -= amount
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False


# Classe especializada para conta corrente
class CheckingAccount(Account):
    def __init__(self, number, client, limit=500, withdraw_limit=3):
        super().__init__(number, client)  # Herda da Account
        self._limit = limit
        self._withdraw_limit = withdraw_limit

    def withdraw(self, amount):
        # Filtra transações do tipo Withdrawal usando compreensão de listas (Pythonic)
        num_withdrawals = len([
            t for t in self.history.transactions if t["type"] == Withdrawal.__name__
        ])
        if amount > self._limit:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif num_withdrawals >= self._withdraw_limit:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().withdraw(amount)
        return False

    def __str__(self):
        # Python: método especial para representar objetos como string formatada
        return f"""\n\
            Agência:\t{self.agency}
            C/C:\t\t{self.number}
            Titular:\t{self.client.name}
        """


# Classe que representa o histórico de uma conta
class History:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        # datetime.now() → captura o momento da transação
        self._transactions.append({
            "type": transaction.__class__.__name__,  # Polimorfismo: tipo dinâmico
            "value": transaction.value,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })


# Classe abstrata para definir estrutura de transações
# OOP: Abstração — define uma interface comum
class Transaction(ABC):  # ABC = Abstract Base Class (Python)
    @property
    @abstractmethod
    def value(self):
        pass  # Python: método obrigatório em subclasses

    @abstractmethod
    def register(self, account):
        pass


# Subclasse concreta de Transaction para Saques
class Withdrawal(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        if account.withdraw(self.value):
            account.history.add_transaction(self)


# Subclasse concreta de Transaction para Depósitos
class Deposit(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        if account.deposit(self.value):
            account.history.add_transaction(self)

# Função para exibir o menu principal formatado
# Python: uso do textwrap.dedent para remover indentação do menu
def main_menu():
    menu = """\n
    ================ MENU ================
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [log]\tLogin na conta
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))  # Python: entrada de dados com prompt formatado

# Função para exibir o menu de operações da conta
def account_menu():
    menu = """\n
    ================ CONTA ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [q]\tSair
    =>"""
    return input(textwrap.dedent(menu))


# Busca cliente pelo CPF
# Python: list comprehension + operador ternário
def find_client_by_cpf(cpf, clients):
    filtered = [c for c in clients if c.cpf == cpf]  # Pythonic: filtragem com list comprehension
    return filtered[0] if filtered else None  # Retorna o primeiro ou None


# Realiza login e mostra o menu de operações da conta
# OOP: Encapsulamento e composição ao acessar conta e transações
def login(clients):
    cpf = input("Informe o CPF do cliente: ")
    client = find_client_by_cpf(cpf, clients)

    if client:
        print(f"\n=== Bem-vindo(a), {client.name}! ===")
        account = get_client_account(client)  # Python: função isolada para obter conta
        if not account:
            return

        while True:
            option = account_menu()
            if option == "d":
                value = float(input("Informe o valor do depósito: "))
                client.perform_transaction(account, Deposit(value))  # OOP: Polimorfismo
            elif option == "s":
                value = float(input("Informe o valor do saque: "))
                client.perform_transaction(account, Withdrawal(value))
            elif option == "e":
                show_statement(account)
            elif option == "q":
                break
            else:
                print("\n@@@ Operação inválida. @@@")
    else:
        print("\n@@@ Cliente não encontrado! @@@")


# Recupera uma conta do cliente
# Se houver apenas uma, retorna direto; senão, permite escolher
def get_client_account(client):
    if not client.accounts:
        print("\n@@@ Cliente não possui conta! @@@")
        return
    if len(client.accounts) == 1:
        return client.accounts[0]
    
    # Python: enumerate para exibir opções numeradas
    print("\nSelecione a conta:")
    for i, acc in enumerate(client.accounts, 1):
        print(f"{i} - Conta {acc.number}, Agência {acc.agency}")
    
    index = int(input("\nDigite o número da conta desejada: "))
    return client.accounts[index - 1]  # Acesso direto à lista


# Mostra o extrato da conta com base no histórico de transações
def show_statement(account):
    print("\n================ EXTRATO ================")
    if not account.history.transactions:
        print("Não foram realizadas movimentações.")
    else:
        for t in account.history.transactions:
            print(f"\n{t['type']}:\n\tR$ {t['value']:.2f}")  # Python: f-string formatado
    print(f"\nSaldo:\n\tR$ {account.balance:.2f}")
    print("==========================================")


# Cria um novo cliente (Individual)
def create_client(clients):
    cpf = input("Informe o CPF (somente número): ")
    if find_client_by_cpf(cpf, clients):  # Evita duplicidade
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return
    
    name = input("Informe o nome completo: ")
    birth_date = input("Informe a data de nascimento (dd-mm-aaaa): ")
    address = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    clients.append(Individual(name, birth_date, cpf, address))  # OOP: Criação de objeto Individual
    print("\n=== Cliente criado com sucesso! ===")


# Cria uma nova conta corrente para cliente existente
def create_account(account_number, clients, accounts):
    cpf = input("Informe o CPF do cliente: ")
    client = find_client_by_cpf(cpf, clients)
    
    if not client:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    account = CheckingAccount.new_account(client, account_number)  # OOP: Método de classe para criação
    accounts.append(account)
    client.add_account(account)  # OOP: Composição
    print("\n=== Conta criada com sucesso! ===")


# Lista todas as contas criadas
def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))  # Usa __str__ da classe CheckingAccount


# ======================= SIGLAS DO MENU =======================
# Menu Principal:
# [nu] -> Novo usuário (criar cliente)
# [nc] -> Nova conta
# [lc] -> Listar contas
# [log] -> Login na conta
# [q] -> Sair do programa

# Menu da Conta (após login):
# [d] -> Depositar
# [s] -> Sacar
# [e] -> Exibir extrato
# [q] -> Sair da conta (volta para o menu principal)
# ==============================================================


# Função principal do sistema bancário
# Ponto de entrada da aplicação
def main():
    clients = []  # Lista que armazena os objetos do tipo Client
    accounts = []  # Lista que armazena objetos Account

    while True:
        option = main_menu()
        if option == "nu":
            create_client(clients)
        elif option == "nc":
            create_account(len(accounts) + 1, clients, accounts)
        elif option == "lc":
            list_accounts(accounts)
        elif option == "log":
            login(clients)
        elif option == "q":
            break
        else:
            print("\n@@@ Operação inválida. @@@")


# Condição padrão para execução direta (boilerplate Python)
if __name__ == "__main__":
    main()
