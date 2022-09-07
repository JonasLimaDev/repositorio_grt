from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

from .models import *
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .classes_dados import DadosItens

class CategoriasPageView(ListView):
    template_name = 'repositorio_pages/categorias.html'
    model = Categoria


class ItensPageView(ListView):
    template_name = 'repositorio_pages/lista_itens.html'
    model = Item
    context_object_name = 'lista_itens'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['autores'] = Autor.objects.all()
        context['niveis'] = NivelEnsino.objects.all()
        autor_filtro = self.request.GET.get('autor')
        if autor_filtro:
            context['autor_filtro'] = int(autor_filtro) if autor_filtro != "0" else None
        nivel_filtro = self.request.GET.get('nivel')
        if nivel_filtro:
            context['nivel_filtro'] = int(nivel_filtro) if nivel_filtro != "0" else None
        context['categoria'] = get_object_or_404(Categoria, id=self.kwargs['pk'])
        return context

    def get_queryset(self):
        self.categoria = get_object_or_404(Categoria, id=self.kwargs['pk'])
        autor_id = self.request.GET.get('autor') if self.request.GET.get('autor') != "0" else None
        nivel_id = self.request.GET.get('nivel') if self.request.GET.get('nivel') != "0" else None
        if autor_id and nivel_id:
            itens = Item.objects.filter(categorias=self.categoria,autores__id=autor_id, niveis_ensino__id=nivel_id)
        elif autor_id and not nivel_id:
            itens = Item.objects.filter(categorias=self.categoria, autores__id=autor_id)
        elif not autor_id and nivel_id:
            itens = Item.objects.filter(categorias=self.categoria, niveis_ensino__id=nivel_id)
        else:
            itens = Item.objects.filter(categorias=self.categoria)
        return itens



class SingleItemPageView(TemplateView):
    template_name = 'repositorio_pages/item.html'

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Item, id=self.kwargs['pk'])
        categoria_bd = None
        try:
            categoria_bd = Categoria.objects.get(id=self.kwargs['cat'])
        except:
            print(item.categorias)
            for categoria in item.categorias.all():
                categoria_bd = categoria
                break

        return render(request, self.template_name, {'item':item,'categoria':categoria_bd})




class HomePageView(TemplateView):
    template_name = 'base.html'
    def get(self, request, *args, **kwargs):
        dados = {}
        return render(request, self.template_name, {'dados': dados})



class SearchPageView(TemplateView):
    template_name = 'repositorio_pages/buscas.html'
    def get(self, request, *args, **kwargs):
        dados = {}
        return render(request, self.template_name, {'dados': dados})

    def post(self, request, *args, **kwargs):
        dados = {}
        #print(self.request.POST)

        objeto_busca = self.request.POST['busca']
        tipo_resultado, itens_busca = self.get_results_search(objeto_busca)
        return render(request, self.template_name, {'dados': dados, 'objeto_busca':objeto_busca,
                                                    'tipo_resultado':tipo_resultado,"itens_busca":itens_busca})

    def get_results_search(self, objeto_busca):
        tipo_busca = None
        resultados = []
        lista_ids = []
        if Item.objects.filter(nome_item__contains=objeto_busca) and not resultados:
            itens = Item.objects.filter(nome_item__contains=objeto_busca)
            for item in itens:
                item_class = DadosItens(item)
                if item_class not in resultados and item_class.id not in lista_ids:
                    resultados.append(item_class)
                    lista_ids.append(item_class.id)
            tipo_busca = "Nome do Item"
        if Item.objects.filter(descricao__contains=objeto_busca) and not resultados:
            itens = Item.objects.filter(descricao__contains=objeto_busca)
            for item in itens:
                item_class = DadosItens(item)
                if item_class not in resultados and item_class.id not in lista_ids:
                    resultados.append(item_class)
                    lista_ids.append(item_class.id)
            tipo_busca = "Descrição"

        if Autor.objects.filter(nome_autor__contains=objeto_busca) and not resultados:
            autores = Autor.objects.filter(nome_autor__contains=objeto_busca)
            for autor in autores:
                itens = Item.objects.filter(autores__id=autor.id)
                for item in itens:
                    item_class = DadosItens(item)
                    if item_class not in resultados and item_class.id not in lista_ids:
                        resultados.append(item_class)
                        lista_ids.append(item_class.id)
            tipo_busca = "Autor"
            # itens = Item.objects.filter(autores=autores)

        if NivelEnsino.objects.filter(nivel__contains=objeto_busca) and not resultados:
            niveis = NivelEnsino.objects.filter(nivel__contains=objeto_busca)
            for nivel in niveis:
                itens = Item.objects.filter(niveis_ensino__id=nivel.id)
                for item in itens:
                    item_class = DadosItens(item)
                    if item_class not in resultados and item_class.id not in lista_ids:
                        resultados.append(item_class)
                        lista_ids.append(item_class.id)
            tipo_busca = "Nivel de Ensino"
        if Categoria.objects.filter(nome_categoria__contains=objeto_busca) and not resultados:
            categorias = Categoria.objects.filter(nome_categoria__contains=objeto_busca)
            for categoria in categorias:
                itens = Item.objects.filter(categorias__id=categoria.id)
                for item in itens:
                    item_class = DadosItens(item)
                    if item_class not in resultados and item_class.id not in lista_ids:
                        resultados.append(item_class)
                        lista_ids.append(item_class.id)
            tipo_busca = "Categoria"
            # itens = Item.objects.filter(autores=autores)
        if Subcategoria.objects.filter(nome_subcategoria__contains=objeto_busca) and not resultados:
            subcategorias = Subcategoria.objects.filter(nome_subcategoria__contains=objeto_busca)
            for subcategoria in subcategorias:
                itens = Item.objects.filter(subcategorias__id=subcategoria.id)
                for item in itens:
                    item_class = DadosItens(item)
                    if item_class not in resultados and item_class.id not in lista_ids:
                        resultados.append(item_class)
                        lista_ids.append(item_class.id)
            tipo_busca = "Subcategoria"
            # itens = Item.objects.filter(autores=autores)
        else:
            print("Não Tem")
        return tipo_busca, resultados