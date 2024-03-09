from rest_framework.serializers import ModelSerializer
from ..models import LutadorModel

class LutadorSerializer(ModelSerializer):
    class Meta:
        model = LutadorModel
        # Rows da tabela lutadorModel
        fields = ['id', 'nome', 'totalDeLutas', 'ultimaLuta'] 
