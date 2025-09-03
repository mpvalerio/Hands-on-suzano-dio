#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Bancário v2 (CLI)
- Modularizado por funções.
- Depósito, Saque (limite por operação e por dia), Extrato.
- Cadastro de Usuário (CPF único).
- Cadastro e listagem de Contas.
"""

from __future__ import annotations
import textwrap
from typing import Dict, List, Optional

# ===== Configurações/Constantes =====
LIMITE_SAQUE_POR_OP = 500.00
LIMITE_SAQUES_DIA = 3
AGENCIA_PADRAO = "0001"

# ===== Estado simples em memória =====
saldo = 0.0
extrato = ""  # string com linhas
numero_saques = 0

usuarios: List[Dict] = []    # [{"nome":..., "cpf":..., "data_nascimento":..., "endereco":..., "bairro":..., "cidade":..., "estado":...}]
contas: List[Dict] = []      # [{"agencia":..., "numero":..., "usuario": <dict_usuario>}]
proximo_numero_conta = 1


# ===== Utilidades =====
def menu() -> str:
    """Exibe o menu e retorna a escolha do usuário."""
    opcoes = """
    --------------- MENU ----------------
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo Usuário
    [nc] Nova Conta
    [lc] Listar Contas
    [q] Sair
    => """
    return input(textwrap.dedent(opcoes)).strip().lower()


def ler_valor_rotulo(rotulo: str) -> float:
    """Lê um valor monetário (aceita vírgula ou ponto)."""
    while True:
        bruto = input(f"{rotulo}: ").strip().replace(",", ".")
        try:
            valor = float(bruto)
            return valor
        except ValueError:
            print("Entrada inválida. Use apenas números (ex.: 1500.45 ou 1500,45).")


# ===== Operações financeiras =====
def depositar(saldo: float, valor: float, extrato: str):
    """Deposita 'valor' (>0) no saldo e registra no extrato."""
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\nDepósito realizado.")
    else:
        print("\nOperação inválida (valor deve ser positivo).")
    return saldo, extrato


def sacar(*, saldo: float, valor: float, extrato: str, limite: float,
          num_saques: int, limite_saques: int):
    """
    Saque com verificações de saldo, limite por operação e limite de saques.
    Parâmetros keyword-only (conforme otimização do artigo).
    Retorna (saldo, extrato, num_saques).
    """
    sem_saldo = valor > saldo
    sem_limite = valor > limite
    sem_saque = num_saques >= limite_saques

    if sem_saldo:
        print("\nSaldo insuficiente.")
    elif sem_limite:
        print(f"\nValor excede o limite por saque (R$ {limite:.2f}).")
    elif sem_saque:
        print("\nNúmero de saques diários excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:    R$ {valor:.2f}\n"
        num_saques += 1
        print("\nSaque realizado.")
    else:
        print("\nOperação inválida (valor deve ser positivo).")

    return saldo, extrato, num_saques


def exibir_extrato(saldo: float, *, extrato: str):
    """Mostra o histórico de transações e o saldo atual (extrato pode estar vazio)."""
    print("\n---------------------- EXTRATO ----------------------")
    print("Não foram realizadas movimentações." if not extrato else extrato, end="")
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("----------------------------------------------------")


# ===== Usuários =====
def filtrar_usuario(cpf: str, usuarios: List[Dict]) -> Optional[Dict]:
    """Retorna o usuário com o CPF informado ou None."""
    filtrados = [u for u in usuarios if u["cpf"] == cpf]
    return filtrados[0] if filtrados else None


def novo_usuario(usuarios: List[Dict]) -> None:
    """Cadastra um novo usuário (CPF único)."""
    cpf = input("CPF (somente números): ").strip()
    if filtrar_usuario(cpf, usuarios):
        print("\nUsuário já cadastrado.")
        return

    nome = input("Nome completo: ").strip()
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input("Endereço (logradouro e número): ").strip()
    bairro = input("Bairro: ").strip()
    cidade = input("Cidade: ").strip()
    estado = input("UF: ").strip().upper()

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco,
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado,
    })
    print("\nUsuário cadastrado com sucesso.")


# ===== Contas =====
def nova_conta(agencia: str, numero: int, usuarios: List[Dict]) -> Optional[Dict]:
    """Cria uma nova conta vinculada a um usuário existente (por CPF)."""
    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("\nUsuário não encontrado. Cadastre-o antes (opção [nu]).")
        return None

    conta = {"agencia": agencia, "numero": f"{numero:06d}", "usuario": usuario}
    print(f"\nConta criada: Agência {conta['agencia']}  Número {conta['numero']}  Titular: {usuario['nome']}")
    return conta


def listar_contas(contas: List[Dict]) -> None:
    """Lista todas as contas cadastradas."""
    if not contas:
        print("\nNão há contas cadastradas.")
        return

    print("\n------------------- CONTAS -------------------")
    for c in contas:
        print(f"Agência: {c['agencia']} | Número: {c['numero']} | Titular: {c['usuario']['nome']} (CPF {c['usuario']['cpf']})")
    print("----------------------------------------------")


# ===== Loop principal =====
def main():
    global saldo, extrato, numero_saques, proximo_numero_conta

    while True:
        opcao = menu()

        if opcao == "d":
            valor = ler_valor_rotulo("Valor do depósito")
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = ler_valor_rotulo("Valor do saque")
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=LIMITE_SAQUE_POR_OP,
                num_saques=numero_saques,
                limite_saques=LIMITE_SAQUES_DIA,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            novo_usuario(usuarios)

        elif opcao == "nc":
            conta = nova_conta(AGENCIA_PADRAO, proximo_numero_conta, usuarios)
            if conta:
                contas.append(conta)
                proximo_numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Encerrando. Obrigado por utilizar o sistema.")
            break

        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    main()
