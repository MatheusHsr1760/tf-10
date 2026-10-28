# TF 10 - Estrutura de Dados: MiniGit

Implementação de um simulador simplificado do Git (`MiniGit`) com foco na análise de complexidade e contagem de passos de operações de **leitura** versus **escrita** em estruturas de dados (dicionários, listas, tuplas e filas).

---

## Tabela de Medição: Leitura x Escrita

Abaixo estão os resultados obtidos pela função `medir()` executando 10, 100 e 1000 commits consecutivos:

```
commits   passos do commitar   passos do log
10        2                    10
100       2                    100
1000      2                    1000
```

| Commits | Passos do commitar | Passos do log |
| :---: | :---: | :---: |
| 10 | 2 | 10 |
| 100 | 2 | 100 |
| 1000 | 2 | 1000 |

---

## Respostas às Questões

### 1. Por que o commitar gasta sempre 2 passos, e o log gasta mais conforme o histórico cresce? (leitura x escrita)
O `commitar` é uma operação de escrita de custo constante: apenas cria o nó no dicionário e atualiza o ponteiro da branch, gastando sempre 2 passos. Já o `log` realiza uma leitura que percorre o histórico em largura, precisando visitar e enfileirar cada commit ancestral individualmente; por isso, quanto mais commits existem no histórico, mais passos são necessários para percorrê-los.

### 2. Por que mensagem(commit) gasta 1 passo e buscar(texto) pode gastar muitos? O que o dicionario ganha quando se procura pela chave, e o que ele não ajuda quando se procura pelo valor?
A busca por chave em `mensagem(commit)` utiliza a função de hash do dicionário para acessar o endereço exato do registro em 1 passo direto. Já a busca por conteúdo em `buscar(texto)` não se beneficia do espalhamento da chave, exigindo uma busca linear que inspeciona commit por commit até encontrar a ocorrência ou percorrer todos.

### 3. Por que o merge é um commit com dois pais, e por que isso faz do histórico um grafo, e não uma lista?
O merge unifica duas frentes de desenvolvimento distintas, registrando como pais tanto a branch ativa quanto a branch incorporada. A presença de múltiplos pais promove pontos de convergência além das ramificações, transformando o histórico em um grafo direcionado acíclico (DAG) em vez de uma sequência estritamente linear.

### 4. Por que o método pais devolve uma tupla, e não a lista que está guardada dentro do dicionário?
A tupla é uma estrutura de dados imutável em Python, diferentemente da lista interna utilizada pela classe. Ao devolver uma tupla, evitamos que referências externas alterem os elementos da coleção por acidente ou malícia, garantindo o encapsulamento e a imutabilidade do histórico do Git.
