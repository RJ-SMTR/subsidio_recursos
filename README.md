# subsidio_recursos

Repositório de avaliação de recursos solicitados quanto ao pagamento de
subsídio do sistema de ônibus convencionais do Rio de Janeiro (SPPO).

## Organização dos recursos

Cada pasta contém a avaliação de um único recurso aberto na plataforma
do MoviDesk. As pastas devem ser nomeadas conforme abaixo:

```
[numero_recurso]_[servico_recurso]_[data_abertura]
```

> Exemplo: `SMTR202212006611_010_2022-12-16`

### Estrutura da pasta

```
├── README.md                  <- Descrição do resumo da análise
├── data
│   ├── output                 <- Dados finais (tabelas de resumo e afins)
│   ├── treated                <- Dados tratados
│   ├── figures                <- Imagens geradas da analise
│   └── raw                    <- Dados brutos
├── notebooks                  <- Jupyter notebooks
│   ├── analise_exploratoria   <- Análise do problema apresentado
│   ├── teste_amostral         <- Testes com a amostra enviada
│   ├── reprocessamento        <- Reprocessamento do período completo, com resultados de antes/depois
│   └── raw                    <- Dados brutos
├── scripts                    <- Scripts Python/R
└── requirements.txt           <- Pacotes específicos da análise
```

## Método de avaliação

[TODO: adicionar infos de observação dos mapas, etc]

- Análise exploratória:
- Teste amostral:
- Reprocessamento:
