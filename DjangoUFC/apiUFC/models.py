from django.db import models


# Modelo que contem dados do lutador, e os dados da sua ultima luta como JSON
class LutadorModel(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(verbose_name="Nome do lutador", max_length=100, null=True, blank=True)
    #cartel do lutador
    cartelNoUFC = models.CharField(verbose_name="Cartel do lutador no UFC: v-d-nc", max_length=50, null=True, blank=True)
    # Total de lutas
    totalDeLutas = models.IntegerField(null=True, blank=True)
    # Contem a ultima luta
    ultimaLuta = models.JSONField(verbose_name="ultimaLuta", max_length=500, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.nome

