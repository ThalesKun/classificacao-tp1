#!/usr/bin/env python3
"""Gráficos do TP1 de ordenação a partir de resultados.csv.

Uso (na pasta do projeto):
    python3 analise.py resultados.csv

Dependências: pandas, numpy, matplotlib.
Cria/atualiza somente PNGs na pasta 'analise/' ao lado do CSV.
Não altera, descarta nem corrige tempos individuais.
"""

from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.lines import Line2D

COMPARACAO = ['bubbleSort', 'insertionSort', 'selectionSort', 'shellSort',
             'heapSort', 'mergeSort', 'quickSort']
NAO_COMPARATIVOS = ['countingSort', 'radixSort', 'bucketSort']
ALGORITMOS = COMPARACAO + NAO_COMPARATIVOS
ORDENS = ['crescente', 'decrescente', 'aleatorio']
ORDEM_NOME = {'crescente': 'Crescente', 'decrescente': 'Decrescente', 'aleatorio': 'Aleatório'}
NOME = {
    'bubbleSort': 'Bubble', 'insertionSort': 'Insertion',
    'selectionSort': 'Selection', 'shellSort': 'Shell',
    'heapSort': 'Heap', 'mergeSort': 'Merge', 'quickSort': 'Quick',
    'countingSort': 'Counting', 'radixSort': 'Radix', 'bucketSort': 'Bucket',
}
# Paleta com 10 cores de contraste forte. O nome de cada algoritmo aparece sempre:
# a interpretação não depende exclusivamente da percepção de cores.
COR = {
    'bubbleSort': '#C81E1E',      # vermelho
    'insertionSort': '#DF8400',   # laranja
    'selectionSort': '#7137B6',   # violeta
    'shellSort': '#0A63A5',       # azul
    'heapSort': '#208B46',        # verde
    'mergeSort': '#85510A',       # marrom
    'quickSort': '#D93F92',       # magenta
    'countingSort': '#079BAC',    # ciano
    'radixSort': '#738300',       # oliva
    'bucketSort': '#364152',      # grafite
}
# Identificadores adicionais para gráficos com curvas próximas.
MARCADORES = {'bubbleSort': 'o', 'insertionSort': '^', 'selectionSort': 's',
              'shellSort': 'D', 'heapSort': 'P', 'mergeSort': 'v',
              'quickSort': 'X', 'countingSort': 'h', 'radixSort': '*', 'bucketSort': '>'}
ESTILOS = {'bubbleSort': '-', 'insertionSort': '--', 'selectionSort': '-.',
           'shellSort': '-', 'heapSort': '--', 'mergeSort': '-.',
           'quickSort': '-', 'countingSort': '-', 'radixSort': '--', 'bucketSort': '-.'}
C_TEXTO = '#1B2838'
C_SUAVE = '#526174'
C_GRADE = '#DFE5EC'

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 12,
    'axes.titlesize': 14, 'axes.labelsize': 12,
    'xtick.labelsize': 10.5, 'ytick.labelsize': 11,
    'figure.facecolor': 'white', 'axes.facecolor': 'white',
    'savefig.facecolor': 'white',
    'text.color': C_TEXTO, 'axes.labelcolor': C_TEXTO,
    'xtick.color': C_SUAVE, 'ytick.color': C_TEXTO,
    'axes.edgecolor': '#CED7E2', 'axes.spines.top': False,
    'axes.spines.right': False,
})


def pt(x, casas=1):
    return f'{x:,.{casas}f}'.replace(',', '_').replace('.', ',').replace('_', '.')


def formatar_tempo(segundos):
    if segundos >= 1:
        return f'{pt(segundos, 2)} s'
    if segundos >= .001:
        return f'{pt(segundos * 1000, 2)} ms'
    return f'{pt(segundos * 1_000_000, 0)} µs'


def formatar_fator(fator):
    if fator >= 1_000_000:
        return f'{pt(fator / 1_000_000, 2)} mi×'
    if fator >= 10_000:
        return f'{pt(fator / 1_000, 1)} mil×'
    if fator >= 100:
        return f'{pt(fator, 0)}×'
    if fator >= 10:
        return f'{pt(fator, 1)}×'
    return f'{pt(fator, 2)}×'


def estrutura(ax, eixo='x'):
    ax.set_axisbelow(True)
    ax.grid(axis=eixo, color=C_GRADE, linewidth=.8)
    ax.tick_params(axis='both', length=0, pad=7)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#CAD3DC')


def salvar(fig, pasta, nome):
    # Nenhum SVG, PDF, CSV de auditoria ou arquivo adicional é criado.
    destino = pasta / f'{nome}.png'
    fig.savefig(destino, dpi=260, facecolor='white')
    plt.close(fig)
    print(f'  {destino.name}')


def titulo(fig, principal, apoio, rodape=''):
    fig.text(.06, .967, principal, size=21, weight='bold', va='top')
    fig.text(.06, .915, apoio, size=11, color=C_SUAVE, va='top')
    if rodape:
        fig.text(.06, .027, rodape, size=9.5, color=C_SUAVE, va='bottom')


def ler_csv(caminho):
    dados = pd.read_csv(caminho)
    colunas = ['algoritmo', 'tamanho', 'ordenacao', 'repeticao', 'tempo_ns']
    faltantes = sorted(set(colunas) - set(dados.columns))
    if faltantes:
        raise ValueError('Colunas ausentes: ' + ', '.join(faltantes))
    if dados.empty or dados[colunas].isna().any().any():
        raise ValueError('CSV vazio ou com valores obrigatórios ausentes.')
    for coluna in ['tamanho', 'repeticao', 'tempo_ns']:
        valores = pd.to_numeric(dados[coluna], errors='raise')
        if not np.isfinite(valores).all() or (valores <= 0).any() or (valores % 1 != 0).any():
            raise ValueError(f'Valores inválidos em {coluna}.')
        dados[coluna] = valores.astype('int64')
    for coluna in ['algoritmo', 'ordenacao']:
        dados[coluna] = dados[coluna].astype(str).str.strip()
    if dados.duplicated(['algoritmo', 'tamanho', 'ordenacao', 'repeticao']).any():
        raise ValueError('Existem repetições duplicadas na mesma configuração.')
    if not set(dados.algoritmo).issubset(ALGORITMOS) or not set(dados.ordenacao).issubset(ORDENS):
        raise ValueError('Algoritmo ou ordenação desconhecidos no CSV.')
    dados['tempo_s'] = dados['tempo_ns'] / 1_000_000_000
    return dados


def estatisticas(dados):
    return (dados.groupby(['algoritmo', 'tamanho', 'ordenacao'])['tempo_s']
            .agg(media='mean', mediana='median', maximo='max', minimo='min',
                 repeticoes='count').reset_index())


def grafico_setas(stats, pasta):
    fatia = stats[stats.tamanho == 100_000].copy()
    ordens = [o for o in ORDENS if o in fatia.ordenacao.values]
    if not ordens:
        return
    referencia = fatia.groupby('ordenacao').maximo.min()
    fatia['vezes'] = fatia.maximo / fatia.ordenacao.map(referencia)

    fig, eixos = plt.subplots(1, len(ordens), figsize=(22, 9.2), squeeze=False)
    titulo(fig, '100 mil elementos  |  Comparação relativa dos tempos máximos',
           'Cada seta parte de 1× e termina em quantas vezes o algoritmo foi mais lento que o melhor da MESMA entrada.',
           '10 execuções por algoritmo • Eixo logarítmico • Os valores são máximos individuais, não tempos médios.')
    for ax, ordem in zip(eixos[0], ordens):
        bloco = fatia[fatia.ordenacao == ordem].sort_values('vezes', ascending=False)
        maior = float(bloco.vezes.max())
        for pos, (_, r) in enumerate(bloco.iterrows()):
            fator = float(r.vezes)
            cor = COR[r.algoritmo]
            ax.plot([1, fator], [pos, pos], color=cor, lw=2.8,
                    solid_capstyle='round', zorder=3)
            ax.scatter([fator], [pos], marker='>', s=100, color=cor,
                       edgecolors='white', linewidths=.65, zorder=5)
            ax.annotate(formatar_fator(fator), (fator, pos), xytext=(7, 0),
                        textcoords='offset points', ha='left', va='center',
                        fontsize=10, color=C_TEXTO, weight='bold')
        ax.set_yticks(range(len(bloco)), [NOME[a] for a in bloco.algoritmo], fontsize=11)
        ax.invert_yaxis()
        ax.axvline(1, color=C_SUAVE, linestyle=(0, (3, 3)), lw=1.3)
        ax.set_xscale('log')
        ax.set_xlim(.87, maior * 4.7)
        ax.set_title(ORDEM_NOME[ordem], loc='left', fontsize=15,
                     weight='bold', pad=14)
        ax.set_xlabel('Razão em relação ao menor máximo (×)', labelpad=12, fontsize=10.5)
        ax.xaxis.set_major_locator(mticker.LogLocator(base=10, numticks=8))
        ax.xaxis.set_minor_formatter(mticker.NullFormatter())
        estrutura(ax)
    fig.subplots_adjust(left=.09, right=.985, top=.82, bottom=.135, wspace=.48)
    salvar(fig, pasta, '01_setas_100mil')


def grafico_barras_maximos(stats, pasta):
    """Uma única escala por painel: horizontal LOG, sem divisão em faixas artificiais."""
    fatia = stats[stats.tamanho == 100_000]
    ordens = [o for o in ORDENS if o in fatia.ordenacao.values]
    if not ordens:
        return
    fig, eixos = plt.subplots(1, len(ordens), figsize=(22, 9.2), squeeze=False)
    titulo(fig, '100 mil elementos  |  Maior tempo registrado por algoritmo',
           'Uma barra por algoritmo, mostrando o MAIOR tempo entre as 10 execuções de cada entrada.',
           'Escala logarítmica em segundos: leia os valores nas barras; o comprimento NÃO é proporcional ao tempo.')
    for ax, ordem in zip(eixos[0], ordens):
        bloco = fatia[fatia.ordenacao == ordem].sort_values('maximo', ascending=False)
        minimo = float(bloco.maximo.min())
        maximo = float(bloco.maximo.max())
        inicio = 10 ** np.floor(np.log10(minimo / 1.5))
        ys = np.arange(len(bloco))
        valores = bloco.maximo.to_numpy(dtype=float)
        # Toda barra começa na mesma referência POSITIVA, necessária em escala log.
        ax.barh(ys, valores - inicio, left=inicio, height=.61,
                color=[COR[a] for a in bloco.algoritmo],
                edgecolor='#FFFFFF', linewidth=.65, zorder=3)
        for yi, v in enumerate(valores):
            ax.annotate(formatar_tempo(v), (v, yi), xytext=(8, 0),
                        textcoords='offset points', ha='left', va='center',
                        fontsize=10, weight='bold', color=C_TEXTO)
        ax.set_yticks(ys, [NOME[a] for a in bloco.algoritmo], fontsize=11)
        ax.invert_yaxis()
        ax.set_xscale('log')
        ax.set_xlim(inicio * .85, maximo * 5.0)
        ax.set_title(ORDEM_NOME[ordem], loc='left', fontsize=15, weight='bold', pad=14)
        ax.set_xlabel('Tempo máximo por execução (s, escala log)', fontsize=10.5, labelpad=12)
        ax.xaxis.set_major_locator(mticker.LogLocator(base=10, numticks=9))
        ax.xaxis.set_minor_formatter(mticker.NullFormatter())
        estrutura(ax)
    fig.subplots_adjust(left=.09, right=.985, top=.82, bottom=.135, wspace=.46)
    salvar(fig, pasta, '02_barras_maximos_100mil')


def grafico_crescimento(stats, pasta, algoritmos, principal, arquivo):
    ordens = [o for o in ORDENS if o in stats.ordenacao.values]
    if not ordens:
        return
    fig, eixos = plt.subplots(1, len(ordens), figsize=(21.5, 8.1), squeeze=False)
    titulo(fig, principal, 'Tempo mediano (10 ou 30 execuções, dependendo do tamanho) • Eixos em escala log-log.',
           'Curvas terminam no último tamanho realmente medido. Sem ponto significa teste não realizado.')
    for ax, ordem in zip(eixos[0], ordens):
        for alg in algoritmos:
            d = stats[(stats.algoritmo == alg) & (stats.ordenacao == ordem)].sort_values('tamanho')
            if d.empty:
                continue
            ax.plot(d.tamanho.to_numpy(), d.mediana.to_numpy() * 1_000,
                    color=COR[alg], linestyle=ESTILOS[alg], marker=MARCADORES[alg],
                    lw=2.5, ms=7, markeredgecolor='white', markeredgewidth=.8, zorder=3)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ns = sorted(stats.tamanho.unique())
        ax.set_xticks(ns)
        ax.set_xticklabels([('1 mil' if n == 1_000 else '10 mil' if n == 10_000
                            else '100 mil' if n == 100_000 else '1 milhão' if n == 1_000_000
                            else f'{n:,}') for n in ns], rotation=20)
        ax.set_ylabel('Tempo mediano (ms)' if ax is eixos[0, 0] else '')
        ax.set_xlabel('Elementos por vetor')
        ax.set_title(ORDEM_NOME[ordem], loc='left', fontsize=15, weight='bold', pad=14)
        estrutura(ax, 'both')
        ax.grid(which='minor', color='#F0F3F7', lw=.5)
    handles = [Line2D([], [], label=NOME[alg], color=COR[alg], lw=2.5,
                      ls=ESTILOS[alg], marker=MARCADORES[alg], ms=7)
               for alg in algoritmos if alg in stats.algoritmo.values]
    fig.legend(handles=handles, loc='lower center', bbox_to_anchor=(.53, .12),
               ncol=len(handles), frameon=False, fontsize=12, columnspacing=2.1)
    fig.subplots_adjust(left=.064, right=.98, top=.79, bottom=.245, wspace=.24)
    salvar(fig, pasta, arquivo)


def grafico_milhao(stats, pasta):
    fatia = stats[stats.tamanho == 1_000_000]
    ordens = [o for o in ORDENS if o in fatia.ordenacao.values]
    if not ordens:
        return
    fig, eixos = plt.subplots(1, len(ordens), figsize=(21, 8.4), squeeze=False)
    titulo(fig, '1 milhão de elementos  |  Tempo médio dos algoritmos executados',
           'Média das 10 execuções por configuração • Barras horizontais em escala LINEAR comum.',
           'Bubble, Insertion e Selection não foram executados em 1 milhão de elementos.')
    limite = float(fatia.media.max()) * 1.21
    for ax, ordem in zip(eixos[0], ordens):
        d = fatia[fatia.ordenacao == ordem].sort_values('media', ascending=False)
        ys = np.arange(len(d))
        ax.barh(ys, d.media, color=[COR[a] for a in d.algoritmo], height=.6,
                edgecolor='white', linewidth=.7, zorder=3)
        for yi, (_, r) in enumerate(d.iterrows()):
            ax.text(float(r.media) + limite*.018, yi, formatar_tempo(float(r.media)),
                    va='center', ha='left', fontsize=10.5, weight='bold')
        ax.set_yticks(ys, [NOME[a] for a in d.algoritmo], fontsize=11.5)
        ax.invert_yaxis()
        ax.set_xlim(0, limite)
        ax.set_title(ORDEM_NOME[ordem], loc='left', fontsize=15, weight='bold', pad=14)
        ax.set_xlabel('Tempo médio por execução (s)', labelpad=12)
        estrutura(ax)
    fig.subplots_adjust(left=.105, right=.985, top=.81, bottom=.14, wspace=.44)
    salvar(fig, pasta, '05_barras_media_1milhao')


def grafico_boxplot(dados, pasta):
    """Gráfico extra: a dispersão real esclarece picos que distorcem os máximos."""
    fatia = dados[dados.tamanho == 100_000]
    ordens = [o for o in ORDENS if o in fatia.ordenacao.values]
    if not ordens:
        return
    fig, eixos = plt.subplots(1, len(ordens), figsize=(22, 9.2), squeeze=False)
    titulo(fig, '100 mil elementos  |  Variação entre as 10 execuções',
           'Boxplots horizontais: mediana, quartis e valores individuais fora dos limites usuais do boxplot.',
           'O eixo é logarítmico. Ponto isolado não prova erro experimental; ele merece investigação.')
    for ax, ordem in zip(eixos[0], ordens):
        d = fatia[fatia.ordenacao == ordem]
        algos = [a for a in ALGORITMOS if a in set(d.algoritmo)]
        series = [d[d.algoritmo == alg].tempo_s.to_numpy() for alg in algos]
        b = ax.boxplot(series, vert=False, positions=np.arange(len(algos)),
                       widths=.57, patch_artist=True, showfliers=True,
                       medianprops={'color': '#14171C', 'linewidth': 2},
                       whiskerprops={'color': C_SUAVE, 'linewidth': 1.2},
                       capprops={'color': C_SUAVE, 'linewidth': 1.2},
                       flierprops={'marker': 'o', 'markersize': 5,
                                   'markerfacecolor': 'white', 'markeredgecolor': '#B22737',
                                   'markeredgewidth': 1.25})
        for caixa, alg in zip(b['boxes'], algos):
            caixa.set_facecolor(COR[alg])
            caixa.set_alpha(.72)
        ax.set_yticks(range(len(algos)), [NOME[a] for a in algos])
        ax.invert_yaxis()
        ax.set_xscale('log')
        ax.set_xlabel('Tempo individual (segundos, log)', labelpad=12)
        ax.set_title(ORDEM_NOME[ordem], loc='left', fontsize=15, weight='bold', pad=14)
        estrutura(ax)
    fig.subplots_adjust(left=.09, right=.985, top=.82, bottom=.135, wspace=.45)
    salvar(fig, pasta, '06_boxplot_100mil')


def main():
    caminho = Path(sys.argv[1]) if len(sys.argv) >= 2 else Path('resultados.csv')
    if not caminho.is_file():
        print(f'Arquivo não encontrado: {caminho}', file=sys.stderr)
        return 1
    pasta = caminho.resolve().parent / 'analise'
    pasta.mkdir(parents=True, exist_ok=True)
    try:
        dados = ler_csv(caminho)
        stats = estatisticas(dados)
    except (ValueError, pd.errors.ParserError) as e:
        print(f'Erro no CSV: {e}', file=sys.stderr)
        return 1
    print(f'Medições carregadas: {len(dados)}. Gerando gráficos PNG:')
    grafico_setas(stats, pasta)
    grafico_barras_maximos(stats, pasta)
    grafico_crescimento(stats, pasta, COMPARACAO,
                       'Crescimento dos algoritmos por comparação', '03_crescimento_comparacao')
    grafico_crescimento(stats, pasta, NAO_COMPARATIVOS,
                       'Crescimento dos algoritmos não comparativos', '04_crescimento_nao_comparativos')
    grafico_milhao(stats, pasta)
    grafico_boxplot(dados, pasta)
    print(f'Concluído. Imagens PNG em: {pasta}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
