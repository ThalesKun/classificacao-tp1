# TP1 - Algoritmos e Classificação de Dados

Implementação e análise de desempenho de 10 algoritmos de ordenação em Java.

## Estrutura

- `Ordenadores.java` — implementação dos 10 algoritmos (7 de comparação + 3 de tempo linear)
- `TesteCorretude.java` — verificação de corretude (vetores pequenos, compara com `Arrays.sort()`)
- `ExperimentoDesempenho.java` — mede o tempo de execução e gera `resultados.csv`
- `analise.py` — lê `resultados.csv` e gera estatísticas + gráficos
- `resultados.csv` — tempos individuais de todas as execuções
- `analise/` — saída do `analise.py` (estatísticas e gráficos)

## 1. Verificar corretude dos algoritmos

```bash
javac *.java
java TesteCorretude
```

## 2. Rodar os experimentos de desempenho

```bash
javac *.java
java ExperimentoDesempenho
```

Gera/sobrescreve `resultados.csv` (tempos em nanossegundos).

**Para mudar os tamanhos testados**, edite em `ExperimentoDesempenho.java`:
```java
private static final int[] TAMANHOS = {1_000, 10_000, 100_000, 1_000_000};
```

Em 100.000 elementos ou menos, roda 30 repetições por configuração; em 1.000.000,
10 repetições (os algoritmos O(n²) ficam lentos nesse tamanho). Para pular alguma
combinação específica que estiver demorando demais, adicione em `PULAR`:
```java
PULAR.add("bubbleSort:1000000");
```

O CSV grava (com flush) a cada repetição — pode interromper com `Ctrl+C` a qualquer
momento sem perder o que já rodou.

## 3. Gerar estatísticas e gráficos

Precisa de `pandas` e `matplotlib`:
```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas matplotlib
```

Depois, sempre que quiser gerar os gráficos:
```bash
source venv/bin/activate
python3 analise.py resultados.csv
```

Gera em `analise/`:
- `estatisticas.csv` — média, mediana, mínimo, máximo e desvio-padrão por configuração
- `dispersao_tempo_vs_tamanho.png` — tempo médio vs. tamanho (log-log)
- `barras_tempo_medio.png` — comparação entre algoritmos no maior tamanho testado
- `boxplot_tempo.png` — distribuição dos tempos no maior tamanho testado