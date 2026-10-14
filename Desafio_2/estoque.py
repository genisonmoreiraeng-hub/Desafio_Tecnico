import uuid
from enum import Enum
from typing import Dict, List, Optional, Tuple


class TipoMovimentacao(Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class MovimentacaoEstoque:
    def __init__(
        self,
        codigo_produto: int,
        tipo: TipoMovimentacao,
        quantidade: int,
        descricao: str
    ):
        if quantidade <= 0:
            raise ValueError("A quantidade movimentada deve ser maior que zero.")

        self.id_movimentacao: str = str(uuid.uuid4())
        self.codigo_produto: int = codigo_produto
        self.tipo: TipoMovimentacao = tipo
        self.quantidade: int = quantidade
        self.descricao: str = descricao

    def __repr__(self) -> str:
        return (
            f"Movimentacao(id='{self.id_movimentacao}', produto={self.codigo_produto}, "
            f"tipo={self.tipo.value}, qtd={self.quantidade}, desc='{self.descricao}')"
        )


class GerenciadorEstoque:
    def __init__(self, dados_iniciais: dict):
        self._produtos: Dict[int, dict] = {
            item["codigoProduto"]: {
                "descricaoProduto": item["descricaoProduto"],
                "estoque": item["estoque"]
            }
            for item in dados_iniciais.get("estoque", [])
        }
        self._historico_movimentacoes: List[MovimentacaoEstoque] = []

    def buscar_produto(self, codigo_produto: int) -> Optional[dict]:
        return self._produtos.get(codigo_produto)

    def lancar_movimentacao(
        self,
        codigo_produto: int,
        tipo: TipoMovimentacao,
        quantidade: int,
        descricao: str
    ) -> Tuple[MovimentacaoEstoque, int]:
        produto = self.buscar_produto(codigo_produto)
        if not produto:
            raise ValueError(f"Produto com código {codigo_produto} não encontrado.")

        if tipo == TipoMovimentacao.SAIDA and produto["estoque"] < quantidade:
            raise ValueError(
                f"Estoque insuficiente para '{produto['descricaoProduto']}'. "
                f"Estoque atual: {produto['estoque']}, Solicitado: {quantidade}."
            )

        # Atualiza o saldo do estoque
        if tipo == TipoMovimentacao.ENTRADA:
            produto["estoque"] += quantidade
        elif tipo == TipoMovimentacao.SAIDA:
            produto["estoque"] -= quantidade

        # Registra a movimentação
        movimentacao = MovimentacaoEstoque(
            codigo_produto=codigo_produto,
            tipo=tipo,
            quantidade=quantidade,
            descricao=descricao
        )
        self._historico_movimentacoes.append(movimentacao)

        return movimentacao, produto["estoque"]


# ==========================================
# Exemplo de Uso
# ==========================================

dados_json = {
    "estoque": [
        {"codigoProduto": 101, "descricaoProduto": "Caneta Azul", "estoque": 150},
        {"codigoProduto": 102, "descricaoProduto": "Caderno Universitário", "estoque": 75},
        {"codigoProduto": 103, "descricaoProduto": "Borracha Branca", "estoque": 200},
        {"codigoProduto": 104, "descricaoProduto": "Lápis Preto HB", "estoque": 320},
        {"codigoProduto": 105, "descricaoProduto": "Marcador de Texto Amarelo", "estoque": 90}
    ]
}

if __name__ == "__main__":
    gerenciador = GerenciadorEstoque(dados_json)

    print("--- Lançando Movimentações ---")

    # 1. Entrada de 50 Canetas Azuis (Código 101)
    mov1, estoque_final1 = gerenciador.lancar_movimentacao(
        codigo_produto=101,
        tipo=TipoMovimentacao.ENTRADA,
        quantidade=50,
        descricao="Recebimento de lote do fornecedor A"
    )
    print(f"ID Movimentação: {mov1.id_movimentacao}")
    print(f"Descrição: {mov1.descricao}")
    print(f"Estoque Final do Produto 101: {estoque_final1}\n")

    # 2. Saída de 10 Cadernos Universitários (Código 102)
    mov2, estoque_final2 = gerenciador.lancar_movimentacao(
        codigo_produto=102,
        tipo=TipoMovimentacao.SAIDA,
        quantidade=10,
        descricao="Venda Pedido #1042"
    )
    print(f"ID Movimentação: {mov2.id_movimentacao}")
    print(f"Descrição: {mov2.descricao}")
    print(f"Estoque Final do Produto 102: {estoque_final2}\n")