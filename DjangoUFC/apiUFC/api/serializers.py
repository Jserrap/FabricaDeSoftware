from rest_framework.serializers import ModelSerializer
from ..models import LutadorModel

class LutadorSerializer(ModelSerializer):
    class Meta:
        model = LutadorModel
        fields = ['id', 'nome', 'totalDeLutas', 'ultimaLuta'] 
