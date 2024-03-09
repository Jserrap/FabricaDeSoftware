# Requerimentos
-django
-djangorestframework
-djangocorsheaders
-djangorestframework-simplejwt
...
(lista completa no requirements.txt)

# Objetivo da api:
Consumir uma API, e forneçer ao usuário alguns dados sobre lutadores de UFC (Ultimate Fighting Championship), provendo dados como, nome, quantidades de lutas, e resultado de sua ultima luta.

(!AVISO!) A API Utilizada para este projeto não aparenta estar completamente atualizada, de modo que lutas após o ufc 283 são visiveis, no entanto não possuem seu resultado atualizado.Infelizmente por ser a única API gratuita que eu encontrei que servisse para o propósito desse trabalho, decidi utiliza-la mesmo assim. Então, para resolver isso, criei a aplicação de uma maneira que qualquer luta que esteja desatualizada seja ignorado, então, apenas os dados pre UFC 283 estão de fato disponiveis.

# Como acessar?
A API pode ser acessada na url https:000.0.0.0000/api/lutador (zeros apenas placeholder para o endereço do server).

# GET, POST, PUT, DELETE
Ao utilizar o endereço acima no método GET, será retornado os registros dos lutadores ja existentes no banco de dados. 
Para adicionar um novo lutador via POST, basta adicionar uma barra ao final da url https:000.0.0.0000/api/lutador/ e passar o name "lutador" (sem aspas), e como seu respectivo valor, o nome do lutador, podendo receber na forma de JSON também. ex:

{
	"lutador":"Jon Jones"
}

Para realizar um DELETE basta passar o ID do lutador que você queira deletar do banco de dados na url, exemplo: https:000.0.0.0000/api/lutador/16/ e logo em seguida, ele será excluido da sua database.
Por fim, para realizar um PUT, basta passar o ID na url, semelhante ao exemplo acima, e passar o atributo do lutador que você gostaria de modificar e seu novo valor, tambem podendo receber na forma de JSON. Ex:

{
	"totalDeLutas":1000
}

# Autenticação
Para realizar a autenticação, para que você possa acessar a API de lutadores, basta visitar a url https:000.0.0.0000/token/ (POST), e passar as chaves "username" e "password", com os valores "cliente" e "123456", respectivamente, ex:

{
	"username":"cliente",
	"password":"123456"
}

Em seguida, a API retornará dois valores, um "refresh", e outro "access". A de "access" será adicionada ao seu header, com o nome do header sendo Authorization, e seu valor a palavra "Bearer", seguida da chave, da seguinte maneira:

Authorization           Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA5OTY4NTQzLCJpYXQiOjE3MDk5NjgyNDMsImp0aSI6ImQxNzU1NmM0Y2I5NDQzYTc4MzJkMjFkYTRlZTA4OGJiIiwidXNlcl9pZCI6Mn0.Q88sDlhyWXGh0jw0I3II00j4neexAIJduAyhcvmSQIw

Após isso ser feito, você poderá acessar https:000.0.0.0000/api/lutador, no entanto a chave eventualmente expirará. Quando isso ocorrer, você pode ou repetir o processo mencionado acima, ou então, utilizando a chave "refresh" retornada anteriormente, visitar https:000.0.0.0000/token/refresh/ (POST), e passar o, na chave "Refresh" o valor, que assim te gerará uma nova chave, que poderá ser utilizada no header novamente.

# Banco de Dados
O banco de dados utilizado para este projeto foi o PostgreSQL, os dados de sua configuração estão no arquivo settings, na parte de DATABASES = {}. Está configurado da seguinte forma:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Db_APIUFC',
        'USER': 'postgres',
        'PASSWORD' : 'senha123',
        'HOST' : 'localhost'
    }
}