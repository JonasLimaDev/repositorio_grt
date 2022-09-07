from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class Autor(models.Model):
    nome_autor = models.CharField(max_length=150, null=False, blank=False,unique=True)
    vinculo = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.nome_autor

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ('nome_autor',)

class Categoria(models.Model):
    nome_categoria = models.CharField(max_length=150, null=False, blank=False, unique=True, verbose_name="Nome da Categoria")
    descricao = models.CharField(max_length=250, null=True, blank=True)
    imagem_capa = models.ImageField(upload_to="Categorias", null=True, blank=True)

    def __str__(self):
        return self.nome_categoria

    class Meta:
        ordering = ('nome_categoria',)




class Subcategoria(models.Model):
    nome_subcategoria = models.CharField(max_length=150, unique=True, null=False, blank=False, verbose_name="Nome da Subcategoria")

    def __str__(self):
        return self.nome_subcategoria


class NivelEnsino(models.Model):
    nivel = models.CharField(max_length=150,unique=True, null=False, blank=False, verbose_name="Nivel de Ensino")

    def __str__(self):
        return self.nivel

    class Meta:
        verbose_name = "Nível de Ensino"
        verbose_name_plural = "Níveis de Ensino"


class Item(models.Model):
    autores = models.ManyToManyField("Autor")
    categorias = models.ManyToManyField("Categoria")
    subcategorias = models.ManyToManyField("Subcategoria")
    niveis_ensino = models.ManyToManyField("NivelEnsino")

    nome_item = models.CharField(max_length=150, null=False, blank=False, verbose_name="Nome do Item")
    descricao = models.CharField(max_length=150, null=True, blank=True, verbose_name="Descrição")

    imagem_apoio = models.ImageField(verbose_name="Imagem de Apoio", upload_to="Items")
    arquivo_grt = models.FileField(upload_to="Items")
    data_upload = models.DateField(auto_now=True)


    def __str__(self):
        return self.nome_item

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Itens"
        ordering = ('nome_item', 'data_upload')
