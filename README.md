# Fintech Analytics — Pipeline de Dados e Detecção de Anomalias

Aplicação acadêmica desenvolvida para uma Fintech com **Pandas, NumPy, Matplotlib e Streamlit**.

## 1. Requisitos atendidos

- Leitura de `transacoes.csv` com `encoding="latin1"`.
- Imputação de `valor` ausente pela mediana por estado.
- Criação da coluna `plataforma = "Mobile"`.
- Conversão de `data_transacao` para datetime e localização em `America/Sao_Paulo`.
- Criação de `dia_semana` e `mes` usando `.dt`.
- Remoção de duplicidades mantendo a primeira ocorrência.
- Filtro de setembro, SP/RJ e valor > R$ 5.000 usando `&` e `|`.
- Mapeamento de risco com `.map()`.
- `pivot_table` por mês e nível de risco com `margins=True`.
- Z-Score vetorizado por estado, sem laços `for`.
- Detecção de anomalias com `Z > 2.5`.
- Gráfico Matplotlib pela API orientada a objetos (`fig, ax = plt.subplots()`).
- Total diário e média móvel de 7 dias.
- Eixo Y iniciado em zero com `ax.set_ylim(bottom=0)`.

## 2. Estrutura

```text
fintech_analytics/
├── app.py
├── criar_dados.py
├── requirements.txt
├── README.md
├── .gitignore
└── transacoes.csv
