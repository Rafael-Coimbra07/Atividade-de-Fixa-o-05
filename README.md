Projeto Fintech - Análise de Transações

Projeto desenvolvido para o exercício de Ciência de Dados.

A aplicação trabalha com os dados de transações gerados pelo arquivo criar_dados.py. Os dados são tratados com Pandas e depois apresentados em uma aplicação feita com Streamlit.

Como funciona

Primeiro é necessário gerar os arquivos de dados:

python criar_dados.py

O script irá gerar:

transacoes.csv
cotacoes.csv

Depois, para executar a aplicação:

pip install -r requirements.txt
streamlit run app.py
O que foi feito

No arquivo app.py foram realizados os tratamentos pedidos na atividade:

leitura do arquivo de transações usando latin1;
preenchimento dos valores vazios pela mediana de cada estado;
criação da coluna plataforma;
conversão da data para datetime e uso do fuso America/Sao_Paulo;
criação das informações de dia da semana e mês;
remoção dos registros duplicados;
filtro das transações de setembro dos estados SP e RJ acima de R$ 5.000;
associação do nível de risco de cada cliente;
criação da tabela dinâmica por mês e risco;
cálculo do Z-Score por estado;
identificação das transações com Z-Score acima de 2,5;
gráfico do total diário e da média móvel de 7 dias.
Arquivos
app.py
criar_dados.py
transacoes.csv
cotacoes.csv
requirements.txt
README.md
.gitignore
Tecnologias utilizadas
Python
Pandas
NumPy
Matplotlib
Streamlit
