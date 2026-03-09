from rest_framework import serializers
from .models import NovaPessoa, Doador


class NovaPessoaSerializer(serializers.ModelSerializer):
    idade = serializers.IntegerField(read_only=True)

    class Meta:
        model = NovaPessoa
        fields = [
            'id',
            'nome',
            'data_nascimento',
            'idade',
            'rua',
            'numero',
            'bairro',
            'nome_responsavel',
            'telefone',
            'latitude',
            'longitude',
        ]


class DoadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doador
        fields = ['id', 'nome', 'email', 'telefone']
