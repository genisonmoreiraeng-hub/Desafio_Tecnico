from datetime import date, datetime
from typing import Dict, Union


class CalculadoraJuros:
    """Calcula multas e juros por atraso no pagamento de títulos/boletos."""

    PERCENTUAL_MULTA_DIARIA: float = 0.025  # 2.5% ao dia

    def __init__(self, taxa_multa_diaria: float = PERCENTUAL_MULTA_DIARIA):
        if taxa_multa_diaria < 0:
            raise ValueError("A taxa de multa diária não pode ser negativa.")
        self.taxa_multa_diaria = taxa_multa_diaria

    def calcular_pagamento(
        self,
        valor_original: float,
        data_vencimento: Union[date, str],
        data_referencia: date = date.today()
    ) -> Dict[str, Union[float, int, str]]:
        """Calcula o valor atualizado do título com base na data de referência (padrão: hoje).

        :param valor_original: Valor inicial do título.
        :param data_vencimento: Data de vencimento (objeto date ou string 'YYYY-MM-DD').
        :param data_referencia: Data do cálculo/pagamento (padrão é hoje).
        :return: Dicionário com o resumo completo dos cálculos.
        """
        if valor_original <= 0:
            raise ValueError("O valor original deve ser maior que zero.")

        data_venc_obj = self._converter_para_date(data_vencimento)

        dias_atraso = (data_referencia - data_venc_obj).days

        # Se não houver atraso (pago em dia ou antecipado), não há juros
        if dias_atraso <= 0:
            return {
                "valor_original": round(valor_original, 2),
                "dias_atraso": 0,
                "taxa_diaria_percentual": self.taxa_multa_diaria * 100,
                "valor_juros": 0.0,
                "valor_total": round(valor_original, 2),
                "status": "Em dia / Sem juros"
            }

        # Cálculo proporcional: valor * (taxa * dias)
        percentual_total_juros = self.taxa_multa_diaria * dias_atraso
        valor_juros = valor_original * percentual_total_juros
        valor_total = valor_original + valor_juros

        return {
            "valor_original": round(valor_original, 2),
            "dias_atraso": dias_atraso,
            "taxa_diaria_percentual": self.taxa_multa_diaria * 100,
            "valor_juros": round(valor_juros, 2),
            "valor_total": round(valor_total, 2),
            "status": "Em atraso"
        }

    @staticmethod
    def _converter_para_date(data_val: Union[date, str]) -> date:
        """Auxiliar para converter string 'YYYY-MM-DD' em objeto date, se necessário."""
        if isinstance(data_val, str):
            try:
                return datetime.strptime(data_val, "%Y-%m-%d").date()
            except ValueError as err:
                raise ValueError(
                    f"Formato de data inválido: '{data_val}'. Use o formato 'YYYY-MM-DD'."
                ) from err
        if isinstance(data_val, date):
            return data_val

        raise TypeError("A data de vencimento deve ser um objeto date ou string 'YYYY-MM-DD'.")


# ==========================================
# Exemplo de Uso / Testes
# ==========================================

if __name__ == "__main__":
    calculadora = CalculadoraJuros()

    # Exemplo 1: Título vencido há alguns dias
    valor = 1000.00
    vencimento = "2026-10-01"  # Data no passado relativa a hoje

    resultado = calculadora.calcular_pagamento(
        valor_original=valor,
        data_vencimento=vencimento
    )

    print("=== DEMONSTRATIVO DE CÁLCULO DE JUROS ===")
    print(f"Valor Original: R$ {resultado['valor_original']:.2f}")
    print(f"Dias de Atraso: {resultado['dias_atraso']} dia(s)")
    print(f"Taxa Diária: {resultado['taxa_diaria_percentual']}% ao dia")
    print(f"Valor dos Juros/Multa: R$ {resultado['valor_juros']:.2f}")
    print(f"Valor Total Atualizado: R$ {resultado['valor_total']:.2f}")
    print(f"Status: {resultado['status']}")