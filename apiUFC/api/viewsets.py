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
            cartel = [0,0,0]
            ultimaLuta = ''

            # Itera sobre o JSON que contem todas as lutas, e para cada luta QUE ESTEJA ATUALIZADA calcula cartel e + 1 no contador de lutas
            for req in requisicaoJSON:

                # Apenas lutas com resultados atualizados contam
                if req['winner'] != '':

                    # Salva a ultima luta
                    if lutas == 0:
                        ultimaLuta = req

                    lutas += 1

                    #Checa se o lutador salvo foi quem ganhou

                    # Tive que incluir .strip() para remover espaços no inicil e no final das strings, devido a erros de formatação na API utilizada
                    if req['winner'].strip() == nome.strip():
                        cartel [0] += 1
                    elif req ['winner'].strip() == 'none':
                        cartel [2] += 1
                    else:
                        cartel [1] += 1

            # Seleciona a primeira luta (mais recente)
                    
            if (ultimaLuta == ''):
                # Para evitar erros, caso o lutador não possua nenhuma luta válida dentro da organização, para não retornar uma string vazia, retorna:
                ultimaLuta = {
                    "date": "",
                    "event": "",
                    "fighter_1": "",
                    "fighter_2": "",
                    "winner": "",
                    "round": "",
                    "method": ""
                }

            # Associa cada falor do JSON a um valor que será salvo no db e retornado para o user
            dados_recebidos = {
                "nome": nome,
                "cartelNoUFC": f"{cartel[0]} - {cartel[1]} - {cartel[2]}",
                "totalDeLutas": lutas,
                "ultimaLuta": {
                    "data" : ultimaLuta['date'],
                    "evento": ultimaLuta['event'],
                    "lutador1" : ultimaLuta['fighter_1'],
                    "lutador2" : ultimaLuta['fighter_2'],
                    "vencedor" : ultimaLuta['winner'],
                    "rounds" : ultimaLuta['round'],
                    "metodo" : ultimaLuta['method'],
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

