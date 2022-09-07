class DadosItens():
    def __init__(self, item_bd):
        self.id = item_bd.id
        self.autores = item_bd.autores
        self.categorias = item_bd.categorias
        self.subcategorias = item_bd.subcategorias
        self.niveis_ensino = item_bd.niveis_ensino

        self.nome_item = item_bd.nome_item
        self.descricao = item_bd.descricao

        self.imagem_apoio = item_bd.imagem_apoio
        self.arquivo_grt = item_bd.arquivo_grt
        self.data_upload = item_bd.data_upload