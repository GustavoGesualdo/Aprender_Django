from django.db import models

'''
class Pessoa(models.Model):
    nome = models.CharField(max_length=50)
    idade = models.IntegerField()

    def __str__(self) -> str:
        return self.nome
'''

class NovaPessoa(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(default="2000-01-01")  # Agora você armazena a data de nascimento
    rua = models.CharField(max_length=100)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=100)
    nome_responsavel = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome

    @property
    def idade(self):
        # Aqui você pode calcular a idade com base na data de nascimento
        from datetime import date
        today = date.today()
        idade = today.year - self.data_nascimento.year
        if today.month < self.data_nascimento.month or (today.month == self.data_nascimento.month and today.day < self.data_nascimento.day):
            idade -= 1
        return idade
    
class Doador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    # Adicione outros campos necessários, como CPF, tipo sanguíneo, etc.

    def __str__(self):
        return self.nome