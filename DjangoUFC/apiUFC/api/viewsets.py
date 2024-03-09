from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..models import LutadorModel
from .serializers import LutadorSerializer
import requests
import json

class LutadorViewset(ModelViewSet):
    queryset = LutadorModel.objects.all()
    serializer_class = LutadorSerializer

    def create(self, request):
        nome = request.data.get('lutador', 'Ben Askren')

        site = f'https://fightingtomatoes.com/UFC-data-endpoint.php?api_key=d3f7a17f3973584a40e4d500c958dd3f3a96f08f&year=Any&event=Any&fighter={nome.replace(' ', '+')}'
        
        requisicao = requests.get(site)
        textoRequisicao = requisicao.text
        inicioJSON = textoRequisicao.find("[{")
        finalJSON = textoRequisicao.find("}]")

        textoRequisicao = textoRequisicao[inicioJSON : finalJSON+2]

        requisicaoJSON = json.loads(textoRequisicao)
        lutas = 0

        for req in requisicaoJSON:
  
            lutas += 1

        requisicaoJSON = requisicaoJSON[0]

        print(requisicaoJSON['fighter_1'])

        print(requisicaoJSON)

        dados_recebidos = {
            "nome": nome,
            "totalDeLutas": lutas,
            "ultimaLuta": {
                "data" : requisicaoJSON['date'],
                "evento": requisicaoJSON['event'],
                "lutador1" : requisicaoJSON['fighter_1'],
                "lutador2" : requisicaoJSON['fighter_2'],
                "vencedor" : requisicaoJSON['winner'],
                "rounds" : requisicaoJSON['round'],
                "metodo" : requisicaoJSON['method'],
            }
        }

        meuserializer = LutadorSerializer(data=dados_recebidos)

        if  meuserializer.is_valid():
            
            lutadorPesquisar = LutadorModel.objects.filter(nome = nome)

            lutadorPesquisarExiste = lutadorPesquisar.exists()

            if lutadorPesquisarExiste:
                return Response({'Aviso': f"{nome} ja existe no banco de dados"})
            
            meuserializer.save()
            return Response(meuserializer.data)
        
        else:
            print(meuserializer.errors)
            return Response({'Aviso': 'Alguma coisa deu errado'})

