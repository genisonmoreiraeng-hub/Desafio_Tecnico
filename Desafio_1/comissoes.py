"""Calcula a comissão de cada vendedor a partir de um JSON de vendas.

Regras (aplicadas a cada venda):
  - valor < 100,00            -> sem comissão
  - 100,00 <= valor < 500,00  -> 1%
  - valor >= 500,00           -> 5%

Uso: python comissoes.py [caminho_do_json]
"""
import json
import sys
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

LIMITE_MINIMO = Decimal("100.00")
LIMITE_FAIXA_ALTA = Decimal("500.00")
TAXA_FAIXA_BAIXA = Decimal("0.01")
TAXA_FAIXA_ALTA = Decimal("0.05")
CENTAVOS = Decimal("0.01")


def calcular_comissao_venda(valor: Decimal) -> Decimal:
    """Retorna a comissão de uma única venda."""
    if valor < LIMITE_MINIMO:
        return Decimal("0")
    if valor < LIMITE_FAIXA_ALTA:
        return valor * TAXA_FAIXA_BAIXA
    return valor * TAXA_FAIXA_ALTA


def carregar_vendas(caminho: str) -> list[dict]:
    # parse_float=Decimal evita erros de ponto flutuante em valores monetários
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo, parse_float=Decimal)["vendas"]


def calcular_comissoes(vendas: list[dict]) -> dict[str, Decimal]:
    """Soma a comissão de todas as vendas de cada vendedor."""
    totais: dict[str, Decimal] = defaultdict(Decimal)
    for venda in vendas:
        totais[venda["vendedor"]] += calcular_comissao_venda(Decimal(venda["valor"]))
    return {nome: total.quantize(CENTAVOS, ROUND_HALF_UP) for nome, total in totais.items()}


def formatar_reais(valor: Decimal) -> str:
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def main() -> None:
    caminho = sys.argv[1] if len(sys.argv) > 1 else "vendas.json"
    comissoes = calcular_comissoes(carregar_vendas(caminho))

    for vendedor, total in comissoes.items():
        print(f"{vendedor}: {formatar_reais(total)}")


if __name__ == "__main__":
    main()
