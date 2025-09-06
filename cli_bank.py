from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

AGENCIA = "0001"  # Define a agência padrão


@dataclass
class Usuario:
    # Define a entidade usuário com os mesmos campos do desafio original
    nome: str
    data_nascimento: str
    cpf: str
    endereco: str  # Formato sugerido: logradouro, nro - bairro - cidade/UF


class Conta:
    # Representa conta com campos equivalentes ao desafio
    def __init__(self, agencia: str, numero_conta: int, usuario: Usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario

        # Mantém os mesmos nomes de campos
        self.saldo: float = 0.0
        self.limite: float = 500.0
        self.extrato: str = ""
        self.numero_saques: int = 0
        self.LIMITE_SAQUES: int = 3

    # Realiza depósito e registra no extrato
    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        self.saldo += valor
        self._adiciona_movimento(f"Depósito:\tR$ {valor:.2f}")
        print("Depósito realizado com sucesso!")
        return True

    # Realiza saque respeitando limite de valor e quantidade
    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False

        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
            return False
        if excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
            return False
        if excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            return False

        self.saldo -= valor
        self.numero_saques += 1
        self._adiciona_movimento(f"Saque:\t\tR$ {valor:.2f}")
        print("Saque realizado com sucesso!")
        return True

    # Exibe o extrato com o saldo atual
    def exibir_extrato(self) -> None:
        print("\n================ EXTRATO ================")
        if not self.extrato:
            print("Não foram realizadas movimentações.")
        else:
            print(self.extrato.strip())
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("=========================================\n")

    # Retorna uma representação simples da conta
    def resumo(self) -> str:
        return (
            f"Agência: {self.agencia} | Conta: {self.numero_conta:04d} | "
            f"Titular: {self.usuario.nome} | CPF: {self.usuario.cpf}"
        )

    # Registra movimento no extrato
    def _adiciona_movimento(self, linha: str) -> None:
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.extrato += f"{data} - {linha}\n"


class Banco:
    # Orquestra usuários e contas, mantendo nomes 'usuarios' e 'contas'
    def __init__(self):
        self.usuarios: List[Usuario] = []
        self.contas: List[Conta] = []
        self._sequencial_conta: int = 1

    # Cria usuário se CPF não existir
    def criar_usuario(self, *, nome: str, data_nascimento: str, cpf: str, endereco: str) -> Optional[Usuario]:
        if self.filtrar_usuario(cpf):
            print("Usuário já cadastrado!")
            return None
        usuario = Usuario(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
        self.usuarios.append(usuario)
        print("Usuário criado com sucesso!")
        return usuario

    # Retorna usuário pelo CPF
    def filtrar_usuario(self, cpf: str) -> Optional[Usuario]:
        for u in self.usuarios:
            if u.cpf == cpf:
                return u
        return None

    # Cria conta associada a um CPF existente
    def criar_conta(self, cpf: str) -> Optional[Conta]:
        usuario = self.filtrar_usuario(cpf)
        if not usuario:
            print("Usuário não encontrado! Cadastro necessário.")
            return None
        conta = Conta(AGENCIA, self._sequencial_conta, usuario)
        self.contas.append(conta)
        self._sequencial_conta += 1
        print("Conta criada com sucesso!")
        return conta

    # Lista as contas existentes
    def listar_contas(self) -> None:
        if not self.contas:
            print("Nenhuma conta cadastrada.")
            return
        for conta in self.contas:
            print(conta.resumo())

    # Retorna uma conta por número
    def obter_conta_por_numero(self, numero_conta: int) -> Optional[Conta]:
        for c in self.contas:
            if c.numero_conta == numero_conta:
                return c
        return None


def menu() -> str:
    # Exibe as opções do sistema
    return """\n
[d]\tDepositar
[s]\tSacar
[e]\tExtrato
[nu]\tNovo usuário
[nc]\tNova conta
[lc]\tListar contas
[lcx]\tListar contas com saldos
[q]\tSair
=> """.strip()


def seed_exemplos(banco: Banco) -> None:
    # Cria 3 usuários e 3 contas com depósitos iniciais
    u1 = banco.criar_usuario(
        nome="Ana Clara Souza",
        data_nascimento="01-01-1990",
        cpf="12345678901",
        endereco="Rua A, 100 - Centro - São Paulo/SP",
    )
    u2 = banco.criar_usuario(
        nome="Bruno Lima",
        data_nascimento="12-05-1985",
        cpf="98765432100",
        endereco="Av. Brasil, 200 - Jardim - Campinas/SP",
    )
    u3 = banco.criar_usuario(
        nome="Carla Menezes",
        data_nascimento="23-08-1992",
        cpf="11122233344",
        endereco="Alameda das Flores, 50 - Bela Vista - Piracicaba/SP",
    )

    c1 = banco.criar_conta("12345678901") if u1 else None
    c2 = banco.criar_conta("98765432100") if u2 else None
    c3 = banco.criar_conta("11122233344") if u3 else None

    if c1: c1.depositar(1500.00)
    if c2: c2.depositar(250.00)
    if c3: c3.depositar(800.00)

    print("\n=== Contas de exemplo criadas ===")
    banco.listar_contas()
    print("================================\n")


def main():
    # Controla o loop principal
    banco = Banco()
    seed_exemplos(banco)  # popula com 3 contas de exemplo

    while True:
        opcao = input(menu()).strip().lower()

        if opcao == "d":
            try:
                numero_conta = int(input("Informe o número da conta: "))
            except ValueError:
                print("Número de conta inválido.")
                continue
            conta = banco.obter_conta_por_numero(numero_conta)
            if not conta:
                print("Conta não encontrada.")
                continue
            try:
                valor = float(input("Informe o valor do depósito: ").replace(",", "."))
            except ValueError:
                print("Valor inválido.")
                continue
            conta.depositar(valor)

        elif opcao == "s":
            try:
                numero_conta = int(input("Informe o número da conta: "))
            except ValueError:
                print("Número de conta inválido.")
                continue
            conta = banco.obter_conta_por_numero(numero_conta)
            if not conta:
                print("Conta não encontrada.")
                continue
            try:
                valor = float(input("Informe o valor do saque: ").replace(",", "."))
            except ValueError:
                print("Valor inválido.")
                continue
            conta.sacar(valor)

        elif opcao == "e":
            try:
                numero_conta = int(input("Informe o número da conta: "))
            except ValueError:
                print("Número de conta inválido.")
                continue
            conta = banco.obter_conta_por_numero(numero_conta)
            if not conta:
                print("Conta não encontrada.")
                continue
            conta.exibir_extrato()

        elif opcao == "nu":
            nome = input("Nome completo: ").strip()
            data_nascimento = input("Data de nascimento (dd-mm-aaaa): ").strip()
            cpf = "".join(filter(str.isdigit, input("CPF (somente números): ").strip()))
            logradouro = input("Logradouro: ").strip()
            numero = input("Número: ").strip()
            bairro = input("Bairro: ").strip()
            cidade = input("Cidade: ").strip()
            uf = input("UF: ").strip().upper()
            endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{uf}"
            banco.criar_usuario(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

        elif opcao == "nc":
            cpf = "".join(filter(str.isdigit, input("Informe o CPF do usuário: ").strip()))
            conta = banco.criar_conta(cpf)
            if conta:
                print("Dados da conta:", conta.resumo())

        elif opcao == "lc":
            banco.listar_contas()

        elif opcao == "lcx":
            if not banco.contas:
                print("Nenhuma conta cadastrada.")
            else:
                for c in banco.contas:
                    print(f"{c.resumo()} | Saldo: R$ {c.saldo:.2f} | Saques: {c.numero_saques}/{c.LIMITE_SAQUES}")

        elif opcao == "q":
            print("Encerrando...")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
