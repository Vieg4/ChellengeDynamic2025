import random
import time
import tracemalloc
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from functools import lru_cache

# ---------- Modelo simples ----------
class Insumo:
    """Classe que representa um insumo com nome, quantidade e validade."""
    def __init__(self, nome: str, quantidade: int, validade: int):
        self.nome = nome
        self.quantidade = quantidade
        self.validade = validade

# ---------- Algoritmos de ordenação ----------
def merge_sort(lista, chave):
    """Merge Sort recursivo."""
    if len(lista) <= 1:
        return lista
    meio = len(lista) // 2
    esq = merge_sort(lista[:meio], chave)
    dir = merge_sort(lista[meio:], chave)
    return merge(esq, dir, chave)

def merge(esq, dir, chave):
    """Mescla duas listas ordenadas."""
    res, i, j = [], 0, 0
    while i < len(esq) and j < len(dir):
        if chave(esq[i]) <= chave(dir[j]):
            res.append(esq[i])
            i += 1
        else:
            res.append(dir[j])
            j += 1
    res.extend(esq[i:])
    res.extend(dir[j:])
    return res

def quick_sort(lista, chave):
    """Quick Sort recursivo (não in-place)."""
    if len(lista) <= 1:
        return lista
    pivo = lista[len(lista)//2]
    iguais  = [x for x in lista if chave(x) == chave(pivo)]
    menores = [x for x in lista if chave(x) <  chave(pivo)]
    maiores = [x for x in lista if chave(x) >  chave(pivo)]
    return quick_sort(menores, chave) + iguais + quick_sort(maiores, chave)

# ---------- Funções auxiliares ----------
def gerar_dados(n):
    """Gera uma lista de n objetos Insumo com valores aleatórios."""
    return [Insumo(f"Item{i}", random.randint(1, 100), random.randint(1, 30)) for i in range(n)]

def medir_tempo_mem(func, lista, chave):
    """Mede tempo de execução e pico de memória de uma função de ordenação."""
    tracemalloc.start()
    t0 = time.perf_counter()
    func(lista, chave)
    tempo = time.perf_counter() - t0
    mem_atual, mem_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return tempo, mem_pico / 1024  # KB

# ---------- Função do gráfico com caching ----------
@lru_cache(maxsize=None)
def gerar_grafico_interativo():
    """
    Gera gráfico 3D interativo comparando Merge Sort e Quick Sort.
    Usa programação dinâmica (cache) para não recalcular resultados repetidos.
    """
    tamanhos = [100, 500, 1000, 2000]
    resultados = []

    # Cache para não recalcular tempos/memórias do mesmo tamanho
    resultados_cache = {}

    for n in tamanhos:
        if n not in resultados_cache:
            base = gerar_dados(n)
            for nome_alg, alg in [("merge_sort", merge_sort), ("quick_sort", quick_sort)]:
                # Executa 3 vezes e tira média usando list comprehension
                tempos, mems = zip(*[
                    medir_tempo_mem(alg, base[:], lambda x: x.quantidade) for _ in range(3)
                ])
                resultados_cache[n] = resultados_cache.get(n, []) + [(nome_alg, n, np.mean(tempos), np.mean(mems))]
        # Adiciona os resultados do cache à lista principal
        resultados.extend(resultados_cache[n])

    # Transformar em DataFrame para Plotly
    df = pd.DataFrame(resultados, columns=["Algoritmo", "Tamanho", "Tempo", "Memoria"])

    # Criar figura 3D interativa
    fig = go.Figure()
    cores = {"merge_sort": "limegreen", "quick_sort": "orange"}

    for alg in df["Algoritmo"].unique():
        sub = df[df["Algoritmo"] == alg]
        fig.add_trace(go.Scatter3d(
            x=sub["Tamanho"],
            y=sub["Tempo"],
            z=sub["Memoria"],
            mode="lines+markers",
            name=alg,
            line=dict(color=cores[alg], width=4),
            marker=dict(size=6, color=cores[alg]),
            hovertemplate="Algoritmo: %{text}<br>Tamanho: %{x}<br>Tempo: %{y:.5f}s<br>Memória: %{z:.2f} KB",
            text=[alg]*len(sub)
        ))

    # Layout com fundo azul escuro
    fig.update_layout(
        title="Comparativo de Algoritmos (3D Interativo)",
        scene=dict(
            xaxis_title="Tamanho da Lista (n)",
            yaxis_title="Tempo (s)",
            zaxis_title="Memória Pico (KB)",
            bgcolor="#0F103B"  # fundo interno
        ),
        paper_bgcolor="#0F103B",  # fundo externo
        legend=dict(bgcolor="rgba(255,255,255,0.1)", font=dict(color="white")),
        font=dict(color="white")
    )

    fig.show()
