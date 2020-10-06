#### Introdução

A Flora Energia é uma empresa de tecnologia energética, sustentável e acessível a todos. A Flora gera energia em suas fazendas sustentáveis e injeta na rede elétrica, recebendo em troca créditos da distribuidora. O público alvo da Flora são os consumidores de baixa tensão com contas até R$ 50.000,00 reais, tipicamente o consumo residencial, que ao aderir à solução passa a ter descontos na conta de Energia Elétrica e a pagar uma parte de serviço à Flora de forma que a soma dos pagamentos sempre resulte menor que a fatura normal do consumidor. Para que o cliente (consumidor que se enquadra no público alvo) faça adesão à solução ou mesmo solicite informações sobre quais serão seus descontos, é necessário que a Flora conheça seu perfil de consumo entre outras informações constantes na fatura desse cliente.

**A estória de usuário enxergada para esse projeto é:
Preciso de uma aplicação para extrair dados de campos específicos da fatura e disponibilizar os dados em um banco que pode ser acessado via uma API(Application Programming Interface).**
Dessa forma, como trata-se de uma solução tipificada como varejo, a quantidade de clientes e potenciais clientes que terão suas faturas analisadas é absurdamente alta, fazendo-se necessário um processo automatizado que elimine desperdícios de tempo e dinheiro. Outro ponto importantíssimo é proporcionar uma boa experiência ao cliente por meio de um processo simples e rápido solicitação de informações e a adesão facilitada. Uma possível limitação na automação desse processo é a qualidade do artefato enviado pelo cliente, no caso, a fatura de Energia Elétrica.

#### Linguagens, Frameworks e Infraestrutura

* A linguagem escolhida foi o Python, por ser a linguagem mais consagrada no quesito extração e tratamento de dados.
* Foi adotado o Framework Flask, uma vez que a forma mais evidente de entregar a solução proposta é via WEB.
* A extração de dados via OCR(Optical Character Recognition) foi feita usando a API do google conhecida como Vision. A escolha foi feita por conta de sua precisão, uma vez erros de leitura em valores podem ter alto impacto no negócio. Precificação de uso da API Vision em https://cloud.google.com/vision/pricing#example .
* O Banco de Dados escolhido foi o MongoDB, por proporcionar alta velocidade de leitura/gravação e facilitar a expansão da solução depois que ela já estiver em produção. Em um momento futuro, pode-se considerar a indexação do MongoDB com Elasticsearch, para buscas mais rápidas e inteligentes.
* Apesar de ser um MVP(Minimum Viable Product), no quesito infraestrutura, esse projeto é pensado para em um momento posterior, ser implantado em soluções nativas de nuvem, baseada em microsserviços, usando soluções escaláveis e de alta performance, como é o caso de containers em kubernetes preferencialmente em nuvem pública.

#### Especificações

A solução foi solicitada no modelo de API, dessa forma os serviços podem ser consumidos por aplicações WEB, aplicativos Mobile (smartphones etc) e inclusive sistemas integrados corporativos(ERPs). O microsserviço tratado por esse MVP é responsável por receber  de forma eletrônica a fatura do cliente, extrair os dados necessários usando tecnologia OCR e gravar esses dados em um banco de dados NoSQL, no caso o MongoDB.
##### Demonstração
Para facilitar a demonstração, foi disponibilizada uma interface web para upload da fatura e verificação dos dados extraídos. Como o objetivo é apenas teste, não foram aplicados efeitos visuais nem folhas de estilo. Não foi implantado o mecanismo de autenticação.

#### Código Fonte

##### Estrutura de pastas e arquivos

O projeto foi escrito tendo como objetivo a simplicidade, com uma visão minimalista. A estrutura de arquivos e pastas foi definida para a pasta **templates** abrigar a página de teste de envio de arquivos (apesar de isso poder ser feito pelo Postman por exemplo). A Pasta conta-images, guarda localmente uma cópia do arquivo enviado. O arquivo **db.py**, contém as informações para conexão com o banco de dados MongoDB, que está online no AtlasDB usando o free Tier. O arquivo googlekey.json contém as credenciais da service account utilizada para autorizar o uso da API Vision do google, nesse caso, foi criada a conta de e-mail xxxxxx@gmail.com e configurado o período de avaliação gratuito de 90 dias do GCP(Google Cloud Platform). O requirements.txt contém os requisitos para o projeto funcionar. Por último, mas não menos importante, o **server.py**, que é o arquivo principal onde estão as rotas e a lógica da API (não foi aplicado o padrão MVC).

