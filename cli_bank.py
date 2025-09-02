# -*- coding: utf-8 -*-
"""
Sistema Bancário
Operações: depósito, saque e extrato.
- Depósito: apenas valores positivos.
- Saque: até R$ 500,00 por operação e no máximo 3 saques por dia.
- Extrato: lista todas as movimentações; se vazio, informa ausência.
Obs.: Entrada de valores aceita vírgula ou ponto como separador decimal.
"""

from datetime import datetime, date
from typing import List, Dict

# Constantes de regra de negócio
LIMITE_SAQUE = 500.00
LIMITE_SAQUES_DIARIOS = 3

# Estado simples em memória
saldo: float = 0.0
movimentos: List[Dict] = []  # cada item: {"tipo": "DEPÓSITO"|"SAQUE", "valor": float, "data": datetime}


def formatar_moeda(valor: float) -> str:
    """Formata valores no padrão exigido: R$ xxx.xx (ponto como separador decimal)."""
    return f"R$ {valor:.2f}"


def contar_saques_hoje() -> int:
    """Conta quantos saques já foram feitos na data de hoje."""
    hoje = date.today()
    return sum(1 for m in movimentos if m["tipo"] == "SAQUE" and m["data"].date() == hoje)


def input_valor(acao: str) -> float:
    """
    Lê um valor do usuário para a ação informada (ex.: 'depósito' ou 'saque').
    Aceita vírgula ou ponto. Garante retorno >= 0 (senão, retorna 0).
    """
    while True:
        bruto = input(f"Informe o valor para {acao}: ").strip()
        try:
            # Permite vírgula como decimal
            valor = float(bruto.replace(",", "."))
            if valor < 0:
                print("Valor negativo não é permitido. Tente novamente.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite apenas números (ex.: 1500.45 ou 1500,45).")


def depositar():
    """Executa um depósito se o valor for positivo."""
    global saldo
    valor = input_valor("depósito")
    if valor <= 0:
        print("Depósitos devem ser maiores que zero.")
        return
    saldo += valor
    movimentos.append({"tipo": "DEPÓSITO", "valor": valor, "data": datetime.now()})
    print(f"Depósito realizado com sucesso: {formatar_moeda(valor)}. Saldo atual: {formatar_moeda(saldo)}")


def sacar():
    """Executa um saque respeitando limite por operação e limite diário, além do saldo disponível."""
    global saldo
    if contar_saques_hoje() >= LIMITE_SAQUES_DIARIOS:
        print("Limite diário de saques atingido (3 por dia).")
        return

    valor = input_valor("saque")

    if valor <= 0:
        print("Saques devem ser maiores que zero.")
        return
    if valor > LIMITE_SAQUE:
        print(f"O valor máximo por saque é {formatar_moeda(LIMITE_SAQUE)}.")
        return
    if valor > saldo:
        print("Saldo insuficiente para realizar o saque.")
        return

    saldo -= valor
    movimentos.append({"tipo": "SAQUE", "valor": valor, "data": datetime.now()})
    restantes = LIMITE_SAQUES_DIARIOS - contar_saques_hoje()
    print(f"Saque realizado: {formatar_moeda(valor)}. Saldo atual: {formatar_moeda(saldo)}. "
          f"Saques restantes hoje: {restantes}")


def extrato():
    """Exibe todas as movimentações e, ao final, o saldo atual."""
    print("\n=== EXTRATO ===")
    if not movimentos:
        print("Não foram realizadas movimentações.")
        print(f"Saldo atual: {formatar_moeda(saldo)}")
        print("===============")
        return

    for m in movimentos:
        data_hora = m["data"].strftime("%d/%m/%Y %H:%M:%S")
        print(f"{data_hora} - {m['tipo']}: {formatar_moeda(m['valor'])}")

    print("-----------------------------")
    print(f"Saldo atual: {formatar_moeda(saldo)}")
    print("===============")


def menu():
    """Menu principal simples."""
    opcoes = {
        "d": ("Depositar", depositar),
        "s": ("Sacar", sacar),
        "e": ("Extrato", extrato),
        "q": ("Sair", None),
    }
    print("\nBem-vindo ao Sistema Bancário")
    while True:
        print("\nEscolha uma opção:")
        for k, (nome, _) in opcoes.items():
            print(f"[{k}] {nome}")
        escolha = input("> ").strip().lower()

        if escolha == "q":
            print("Encerrando. Obrigado por utilizar o sistema.")
            break
        if escolha in opcoes and opcoes[escolha][1] is not None:
            opcoes[escolha][1]()  # chama a função associada
        else:
            print("Opção inválida. Tente novamente.")


def main():
    menu()


if __name__ == "__main__":
    main()
