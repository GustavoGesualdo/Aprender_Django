from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from .models import NovaPessoa, Doador
from .serializers import NovaPessoaSerializer, DoadorSerializer


@extend_schema_view(
    list=extend_schema(summary='Listar crianças', tags=['Crianças']),
    retrieve=extend_schema(summary='Detalhar criança', tags=['Crianças']),
    create=extend_schema(summary='Cadastrar criança', tags=['Crianças']),
    update=extend_schema(summary='Atualizar criança', tags=['Crianças']),
    partial_update=extend_schema(summary='Atualização parcial da criança', tags=['Crianças']),
    destroy=extend_schema(summary='Remover criança', tags=['Crianças']),
)
class NovaPessoaViewSet(viewsets.ModelViewSet):
    queryset = NovaPessoa.objects.all().order_by('nome')
    serializer_class = NovaPessoaSerializer


@extend_schema_view(
    list=extend_schema(summary='Listar doadores', tags=['Doadores']),
    retrieve=extend_schema(summary='Detalhar doador', tags=['Doadores']),
    create=extend_schema(summary='Cadastrar doador', tags=['Doadores']),
    update=extend_schema(summary='Atualizar doador', tags=['Doadores']),
    partial_update=extend_schema(summary='Atualização parcial do doador', tags=['Doadores']),
    destroy=extend_schema(summary='Remover doador', tags=['Doadores']),
)
class DoadorViewSet(viewsets.ModelViewSet):
    queryset = Doador.objects.all().order_by('nome')
    serializer_class = DoadorSerializer
