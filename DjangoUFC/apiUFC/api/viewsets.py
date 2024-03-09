from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import LutadorModel
from .serializers import LutadorSerializer
import requests
import json

class LutadorViewset(ModelViewSet):
    permission_classes = (IsAuthenticated, )

    queryset = LutadorModel.objects.all()
    serializer_class = LutadorSerializer

    def create(self, request):
        # Valor realiza request, definindo como valor default Ben Askren
        nome = request.data.get('lutador', 'Ben Askren')

        # Site utilizado
        site = f'https://fightingtomatoes.com/UFC-data-endpoint.php?api_key=d3f7a17f3973584a40e4d500c958dd3f3a96f08f&year=Any&event=Any&fighter={nome.replace(' ', '+')}'
        
        # Request sendo feita
        requisicao = requests.get(site)
        textoRequisicao = requisicao.text

        # Infelizmente tive um problema com a api utilizada. Ao invés dela retornar um JSON, ela retornava o HTML completo da página, isso gerava o problema que eu não 
        # conseguia utilizar o .json() do requests, a solução para isso foi utilizar a livraria json do python. O que eu fiz foi, recebi o conteudo inteiro da pagina na forma 
        # html, e primeiramente verifiquei se de fato possuia o JSON, ou a mensagem de erro. Caso possuisse a mensagem de erro, caia na condicional a baixo e retornava a mensagem
        # de lutador não encontrado. Caso fosse de fato o JSON, utilizaria as strings '[{' '}]' para delimitar o inicio e final da parte JSON do arquivo HTML, e, utilizando
        # a biblioteca json e convertia-o para json.
        
        # Verifica se é json ou não
        if(textoRequisicao.find('[{') == -1):
            return Response({'Aviso': 'Lutador não encontrado. Caso necessário, visite a documentação'})

        else:
            # Delimita o json por meio dos caracteres '[{' '}]'
            inicioJSON = textoRequisicao.find("[{")
            finalJSON = textoRequisicao.find("}]")
            textoRequisicao = textoRequisicao[inicioJSON : finalJSON+2]

            # Converte para json
            requisicaoJSON = json.loads(textoRequisicao)

            # Quantidade total de lutas
            lutas = 0

            # Itera sobre o JSON que contem todas as lutas, e para cada luta presente, + 1 no contador
            for req in requisicaoJSON:
    
                lutas += 1

            # Seleciona a primeira luta (mais recente)
            requisicaoJSON = requisicaoJSON[0]

            # Associa cada falor do JSON a um valor que será salvo no db e retornado para o user
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

            # Caso seja valido:
            if  meuserializer.is_valid():
                
                lutadorPesquisar = LutadorModel.objects.filter(nome = nome)

                lutadorPesquisarExiste = lutadorPesquisar.exists()

                # Caso ja exista no db exibe a mensagem, caso não exista, salva no db e exibe os dados do lutador
                if lutadorPesquisarExiste:
                    return Response({'Aviso': f"{nome} ja existe no banco de dados"})
                
                meuserializer.save()
                return Response(meuserializer.data)
            # Exibe mensagem de erro
            else:
                print(meuserializer.errors)
                return Response({'Aviso': 'Alguma coisa deu errado'})

