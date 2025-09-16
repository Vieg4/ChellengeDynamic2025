# Dynamic Programming - Gestão de Consumo de Insumos

## Descrição do Projeto
Este projeto tem como objetivo organizar e gerenciar o consumo diário de insumos (reagentes e descartáveis) em unidades de diagnóstico, onde o registro não é feito com precisão.  
Para isso, simulamos dados de consumo diário e aplicamos **estruturas de dados** e **algoritmos clássicos** para facilitar o controle de estoque e previsão de reposição.

---

## Funcionalidades Implementadas

### 1. Fila e Pilha
- **Fila:** Registra o consumo diário de insumos em ordem cronológica, permitindo acompanhar a sequência correta de uso.
- **Pilha:** Simula consultas em ordem inversa, mostrando os últimos consumos primeiro, útil para auditorias ou análises recentes.

### 2. Estruturas de Busca
- **Busca Sequencial:** Procura um insumo específico percorrendo a lista completa, ideal para pequenos volumes de dados.
- **Busca Binária:** Localiza rapidamente um insumo em listas ordenadas, aumentando a eficiência em grandes volumes.

### 3. Ordenação
- **Merge Sort e Quick Sort:** Organizam os insumos por quantidade consumida ou validade, garantindo que o estoque mais crítico seja identificado rapidamente.

### 4. Relatório
- Todo o código está disponível neste repositório no GitHub.
- Explicações detalhadas de cada estrutura e algoritmo estão comentadas no código, mostrando como foram aplicados no contexto do problema.

---

## Tecnologias Utilizadas
- Python 3.x
- Estruturas de dados: listas, filas e pilhas
- Algoritmos: Merge Sort, Quick Sort, Busca Sequencial e Binária
- Simulação de dados de consumo

---

- Caso o grafico interativo de erro para rodar tente executar o codigo abaixo no terminal em python.

from grafico import gerar_grafico_interativo

gerar_grafico_interativo()

- Caso precise abrir o grafico mais de uma vez abra outro terminal em python e escreva novamente o codigo
