from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def obter_conta(self):
        return self.contas[0] if self.contas else None
    
class pessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento):
        super().__init__(nome, cpf)
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self.agencia = "0001"
        self.numero = numero
        self.cliente = cliente
        self.saldo = 0
        self.historico = Historico()

    def sacar(self, valor):
        if valor > self.saldo:
            print("Saldo insuficiente!")
            return False
        self.saldo -= valor
        self.historico.adicionar_transacao(Saque(valor))
        print("Saque Realizado com sucesso!")
        return True
    
    def depositar(self, valor):
        if valor < 0:
            print("valor Ivalido pra o Desposito")
            return False
        self.saldo += valor
        self.historico.adicionar_transacao(Deposito(valor))
        print("Valor Depositado com Sucesso!")
        return True
    
    def exibir_extrato(self):
        print(f"\nExtrato da Conta {self.numero} - Cliente: {self.cliente.nome}")
        if not self.historico.transacoes:
            print("Nenhums Movimentocoes Registrada!")
        else:
            for transacao in self.historico.transacoes:
                print(f"{transacao.data} - {transacao.tipo}: R$ {transacao.valor:.2f}")
            print(f"Saldo Atual:R$ {self.saldo:.2f}\n")

class ContaCorrente(Conta):
    def __init__(self, numero,cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque
        self.saques_realizados = 0
    
    def sacar(self, valor):
        if self.saques_realizados >= self.limite_saque:
            print("Limite de Saque Diario Antingido!")
            return False
        if valor > (self.saldo + self.limite):
            print("Saque insuficiente Pra o Saque")
            return False
        self.saques_realizados += 1
        return super().sacar(valor)
    

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Transacao(ABC):
    def __init__(self, valor):
        self.valor = valor
        self.data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        @property
        @abstractmethod
        def tipo(self):
            pass

class Saque(Transacao):
        @property
        
        def tipo(self):
            return "Saque"

class Deposito(Transacao):
    @property
    def tipo(self):
        return "Deposito"
    

def criar_cliente():
    nome = input("Digite o nome: ")
    cpf = input("digite o CPF: ")
    data_nascimento = input("Digit a data de Nascimento (dd/mm/aaaa): ")
    cliente = pessoaFisica(nome, cpf, data_nascimento)
    return cliente

def criar_conta(numero,cliente):
    conta = ContaCorrente(numero, cliente)
    cliente.adicionar_conta(conta)
    print("\n=== Conta crianda com sucesso! ===")
    return conta


def main():
    clientes = []
    contas = []
    numero_conta = 1
    while True:
        print("""

=====================
    MENU
=====================
              
[1] Depositar
[2] Sacar
[3] Extrato
[4] Nova Conta
[5] Listar Cliente
[6] Novo Cliente
[0] Sair

""")
        
        opcao = input("=>")

        if opcao == "1":
            cpf = input("digite o CPF do cliente : ")
            cliente = next((cli for cli in clientes if cli.cpf== cpf),None)

            if cliente:
                conta = cliente.obter_conta()
                if conta:
                    valor = float(input("Digite o valor pra o Depositar"))
                    conta.depositar(valor)
                else:
                    print("Cliente na possui Conta")     
            else:
                print("Cliente nao Cadastrado")

        elif opcao == "2":
            cpf = input("Digite o cpf do cliente: ")
            cliente = next((cli for cli in clientes if cli.cpf == cpf), None)

            if cliente:
                conta = cliente.obter_conta()
                if conta:
                    valor = float(input("Digite o valor pra Sacar: "))
                    conta.sacar(valor)
                else:
                    print("cliente nao possui Conta")
            else:
                print("Cliente nao encontrado")
        elif opcao == "3":
            cpf = input("Digite o CPF do cliente: ")

            cliente = next((cli for cli in clientes  if cli.cpf == cpf), None)
            if cliente:
                conta = cliente.obter_conta()
                if conta:
                    conta.exibir_extrato()
                else:
                    print("Cliente nao possoui conta")
            else:
                print("Cliente nao encontrado!")
        elif opcao == "4":
            cpf = input("Digite o CPF do cliente: ")
            cliente = next((cli for cli in clientes if cli.cpf == cpf), None)
            if cliente:
                conta = criar_conta(numero_conta, cliente)

                contas.append(conta)
                numero_conta += 1
            else:
                print("Cliente nao encontrado!")

        elif opcao == "5":
            for conta in contas:
                print(f"\nAgencia: {conta.agencia}")
                print(f"C/C: {conta.numero}")
                print(f"Titular: {conta.cliente.nome}")

        elif opcao == "6":
            cliente = criar_cliente()
            clientes.append(cliente)
            print("\n=== Cliente criado com sucesso! ===")
        
        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opcao ivalida, siga o menu!")

if __name__ == "__main__":
    main()