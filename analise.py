#!/usr/bin/env python3
"""
Analise de desempenho dos algoritmos de ordenacao - TP1 ACD.

Le o CSV gerado por ExperimentoDesempenho.java
(algoritmo,tamanho,ordenacao,repeticao,tempo_ns), calcula estatisticas
(media, mediana, minimo, maximo, desvio-padrao) por configuracao, e gera
os graficos pedidos no enunciado: dispersao, barras e boxplot.

Uso:
    python3 analise.py [caminho_do_csv]

    (se nao for informado, usa "resultados.csv" no diretorio atual)

Saida (na pasta "analise/"):
    estatisticas.csv               - tabela com media/mediana/min/max/desvio por config.
    dispersao_tempo_vs_tamanho.png - tempo medio vs tamanho, log-log, por ordenacao
    barras_tempo_medio.png         - tempo medio por algoritmo no maior tamanho disponivel
    boxplot_tempo.png              - distribuicao dos tempos individuais no maior tamanho

Pode ser rodado varias vezes conforme novos tamanhos forem sendo adicionados
ao resultados.csv (ele se adapta automaticamente aos tamanhos/ordenacoes presentes).
"""

import sys
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# Configuracao
# ---------------------------------------------------------------
ALGORITMOS_COMPARACAO = ["bubbleSort", "insertionSort", "selectionSort",
                          "shellSort", "heapSort", "mergeSort", "quickSort"]
ALGORITMOS_LINEARES = ["countingSort", "radixSort", "bucketSort"]
TODOS_ALGORITMOS = ALGORITMOS_COMPARACAO + ALGORITMOS_LINEARES

ORDEM_ORDENACOES = ["crescente", "decrescente", "aleatorio"]

# cor fixa por algoritmo (paleta qualitativa, nunca reciclada entre algoritmos,
# consistente em todos os graficos gerados)
_PALETA = plt.get_cmap("tab10").colors
CORES = {alg: _PALETA[i % len(_PALETA)] for i, alg in enumerate(TODOS_ALGORITMOS)}

PASTA_SAIDA = "analise"


def carregar_dados(caminho_csv):
    df = pd.read_csv(caminho_csv)
    df["tempo_ms"] = df["tempo_ns"] / 1e6
    return df


def calcular_estatisticas(df):
    agrupado = df.groupby(["algoritmo", "tamanho", "ordenacao"])["tempo_ms"]
    stats = agrupado.agg(
        media="mean",
        mediana="median",
        minimo="min",
        maximo="max",
        desvio_padrao="std",
        n_execucoes="count",
    ).reset_index()
    return stats


def grafico_dispersao(stats, caminho_saida):
    """Tempo medio vs tamanho, uma linha por algoritmo, escala log-log.
    2 linhas (comparacao / linear) x N colunas (ordenacoes presentes)."""
    ordenacoes = [o for o in ORDEM_ORDENACOES if o in stats["ordenacao"].unique()]
    grupos = [("Comparacao", ALGORITMOS_COMPARACAO),
              ("Tempo linear", ALGORITMOS_LINEARES)]

    fig, eixos = plt.subplots(len(grupos), len(ordenacoes),
                               figsize=(5.2 * len(ordenacoes), 4.3 * len(grupos)),
                               squeeze=False)

    for linha, (titulo_grupo, algoritmos) in enumerate(grupos):
        for coluna, ordenacao in enumerate(ordenacoes):
            ax = eixos[linha][coluna]
            subset = stats[stats["ordenacao"] == ordenacao]
            for alg in algoritmos:
                dados_alg = subset[subset["algoritmo"] == alg].sort_values("tamanho")
                if dados_alg.empty:
                    continue
                ax.plot(dados_alg["tamanho"], dados_alg["media"],
                        marker="o", markersize=5, linewidth=1.8,
                        color=CORES[alg], label=alg)

            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_xlabel("Tamanho do vetor (log)")
            if coluna == 0:
                ax.set_ylabel(f"{titulo_grupo}\nTempo medio (ms, log)")
            ax.set_title(ordenacao.capitalize())
            ax.grid(True, which="both", linestyle="--", linewidth=0.4, alpha=0.5)
            if coluna == len(ordenacoes) - 1:
                ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1.02, 1))

    fig.suptitle("Tempo medio de execucao vs. tamanho do vetor (escala log-log)", fontsize=13)
    fig.tight_layout(rect=[0, 0, 0.90, 0.95])
    fig.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    plt.close(fig)


def grafico_barras(stats, caminho_saida):
    """Tempo medio por algoritmo no MAIOR tamanho disponivel, um subplot por ordenacao."""
    maior_tamanho = stats["tamanho"].max()
    ordenacoes = [o for o in ORDEM_ORDENACOES if o in stats["ordenacao"].unique()]

    fig, eixos = plt.subplots(1, len(ordenacoes), figsize=(5.2 * len(ordenacoes), 5), squeeze=False)
    eixos = eixos[0]

    for i, ordenacao in enumerate(ordenacoes):
        ax = eixos[i]
        subset = stats[(stats["tamanho"] == maior_tamanho) & (stats["ordenacao"] == ordenacao)]
        subset = subset.set_index("algoritmo").reindex(TODOS_ALGORITMOS).dropna(subset=["media"])

        cores_barras = [CORES[alg] for alg in subset.index]
        ax.bar(subset.index, subset["media"], color=cores_barras)
        ax.set_yscale("log")
        if i == 0:
            ax.set_ylabel("Tempo medio (ms, log)")
        ax.set_title(ordenacao.capitalize())
        ax.tick_params(axis="x", rotation=60)
        ax.grid(True, axis="y", which="both", linestyle="--", linewidth=0.4, alpha=0.5)

    titulo_tamanho = f"{int(maior_tamanho):,}".replace(",", ".")
    fig.suptitle(f"Tempo medio por algoritmo - tamanho = {titulo_tamanho}", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    plt.close(fig)


def grafico_boxplot(df, caminho_saida):
    """Distribuicao dos tempos individuais por algoritmo, no maior tamanho, por ordenacao."""
    maior_tamanho = df["tamanho"].max()
    ordenacoes = [o for o in ORDEM_ORDENACOES if o in df["ordenacao"].unique()]

    fig, eixos = plt.subplots(1, len(ordenacoes), figsize=(5.2 * len(ordenacoes), 5), squeeze=False)
    eixos = eixos[0]

    for i, ordenacao in enumerate(ordenacoes):
        ax = eixos[i]
        subset = df[(df["tamanho"] == maior_tamanho) & (df["ordenacao"] == ordenacao)]
        algoritmos_presentes = [a for a in TODOS_ALGORITMOS if a in subset["algoritmo"].unique()]
        dados_box = [subset[subset["algoritmo"] == a]["tempo_ms"].values for a in algoritmos_presentes]

        try:
            caixas = ax.boxplot(dados_box, tick_labels=algoritmos_presentes, patch_artist=True)
        except TypeError:
            # compatibilidade com versoes mais antigas do matplotlib
            caixas = ax.boxplot(dados_box, labels=algoritmos_presentes, patch_artist=True)
        for caixa, alg in zip(caixas["boxes"], algoritmos_presentes):
            caixa.set_facecolor(CORES[alg])
            caixa.set_alpha(0.7)

        ax.set_yscale("log")
        if i == 0:
            ax.set_ylabel("Tempo (ms, log)")
        ax.set_title(ordenacao.capitalize())
        ax.tick_params(axis="x", rotation=60)
        ax.grid(True, axis="y", which="both", linestyle="--", linewidth=0.4, alpha=0.5)

    titulo_tamanho = f"{int(maior_tamanho):,}".replace(",", ".")
    fig.suptitle(f"Distribuicao dos tempos de execucao - tamanho = {titulo_tamanho}", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    caminho_csv = sys.argv[1] if len(sys.argv) > 1 else "resultados.csv"
    if not os.path.exists(caminho_csv):
        print(f"Arquivo nao encontrado: {caminho_csv}")
        sys.exit(1)

    os.makedirs(PASTA_SAIDA, exist_ok=True)

    print(f"Lendo {caminho_csv}...")
    df = carregar_dados(caminho_csv)
    print(f"{len(df)} execucoes carregadas.")
    print(f"Tamanhos: {sorted(df['tamanho'].unique())}")
    print(f"Ordenacoes: {sorted(df['ordenacao'].unique())}")
    print(f"Algoritmos: {sorted(df['algoritmo'].unique())}")

    stats = calcular_estatisticas(df)
    caminho_stats = os.path.join(PASTA_SAIDA, "estatisticas.csv")
    stats.to_csv(caminho_stats, index=False, float_format="%.4f")
    print(f"\nEstatisticas salvas em {caminho_stats}")

    print("Gerando graficos...")
    grafico_dispersao(stats, os.path.join(PASTA_SAIDA, "dispersao_tempo_vs_tamanho.png"))
    grafico_barras(stats, os.path.join(PASTA_SAIDA, "barras_tempo_medio.png"))
    grafico_boxplot(df, os.path.join(PASTA_SAIDA, "boxplot_tempo.png"))

    print(f"\nConcluido. Arquivos em '{PASTA_SAIDA}/':")
    print("  - estatisticas.csv")
    print("  - dispersao_tempo_vs_tamanho.png")
    print("  - barras_tempo_medio.png")
    print("  - boxplot_tempo.png")


if __name__ == "__main__":
    main()
