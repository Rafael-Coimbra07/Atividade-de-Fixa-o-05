# Fintech Analytics — Pipeline de Dados e Detecção de Anomalias

Aplicação acadêmica desenvolvida para uma Fintech com Pandas, NumPy, Matplotlib e Streamlit.

## 1. Requisitos atendidos

- Leitura de `transacoes.csv` com `encoding="latin1"`.
- Imputação de `valor` ausente pela mediana por estado.
- Criação da coluna `plataforma = "Mobile"`.
- Conversão de `data_transacao` para datetime e localização em `America/Sao_Paulo`.
- Criação de `dia_semana` e `mes` usando `.dt`.
- Remoção de duplicidades mantendo a primeira ocorrência.
- Filtro de setembro, SP/RJ e valor maior que R$ 5.000 usando `&` e `|`.
- Mapeamento de risco com `.map()`.
- Criação de `pivot_table` por mês e nível de risco com `margins=True`.
- Cálculo do Z-Score por estado sem utilizar laços `for`.
- Identificação de possíveis anomalias com `Z > 2.5`.
- Gráfico utilizando a API orientada a objetos do Matplotlib.
- Total diário das transações.
- Média móvel de 7 dias.
- Eixo Y iniciado em zero com `ax.set_ylim(bottom=0)`.

## 2. Estrutura do projeto

fintech_analytics/
├── app.py
├── criar_dados.py
├── requirements.txt
├── README.md
├── .gitignore
├── transacoes.csv
└── cotacoes.csv

## 3. Como executar

### Windows

Primeiro, crie o ambiente virtual:

python -m venv .venv

Ative o ambiente:

.venv\Scripts\activate

Instale as bibliotecas:

pip install -r requirements.txt

Gere os arquivos de dados:

python criar_dados.py

Depois execute a aplicação:

streamlit run app.py

A aplicação será aberta no navegador pelo endereço mostrado no terminal.

## 4. Tecnologias utilizadas

- Python
- Pandas
- NumPy
- Matplotlib
- Streamlit

## 5. Entrega pelo GitHub

Para enviar o projeto para o GitHub:

git init
git add .
git commit -m "Entrega projeto Fintech"
git branch -M main
git remote add origin URL_DO_SEU_REPOSITORIO
git push -u origin main

Substitua URL_DO_SEU_REPOSITORIO pelo endereço do seu repositório no GitHub.

## 6. Observação

O arquivo `criar_dados.py` faz parte do projeto porque é o script disponibilizado para gerar os dados utilizados pela aplicação.
