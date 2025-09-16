from collections import deque
import random
import time
import tracemalloc

# -------------------------
# Módulo: simulação de consumo de insumos
# -------------------------
# Este módulo define:
# - a classe Insumo (registro de um insumo consumido)
# - funções para gerar dados simulados
# - implementações de fila e pilha (exibição)
# - buscas (sequencial e binária) com saída explicada
# - algoritmos de ordenação (merge sort e quick sort)
# - um decorator para medir tempo e memória das operações


# -------------------------
# Classe Insumo
# -------------------------
class Insumo:
    """
    Representa um insumo consumido.
    Atributos:
    - nome: nome do insumo (string)
    - quantidade: quantidade consumida (int)
    - validade: dias restantes até a validade (int)
    """
    def __init__(self, nome, quantidade, validade):
        self.nome = nome
        self.quantidade = quantidade
        self.validade = validade

    def __repr__(self):
        # Representação legível do objeto para impressão
        return f"{self.nome} | Qtd: {self.quantidade} | Val: {self.validade}"


# -------------------------
# Funções auxiliares
# -------------------------
def gerar_consumo():
    """
    Gera uma lista de objetos Insumo com valores aleatórios.
    Retorna uma lista com 10 entradas por padrão.
    """
    nomes_insumos = ["Reagente A", "Reagente B", "Reagente C", "Descartavel X", "Descartavel Y"]
    return [
        # random.choice escolhe um nome aleatório da lista;
        # random.randint gera quantidade e validade aleatórias.
        Insumo(random.choice(nomes_insumos), random.randint(1, 50), random.randint(1, 30))
        for _ in range(10)
    ]


def mostrar_lista(lista):
    """
    Imprime cada item da lista em uma linha.
    Útil para exibir o conteúdo atual (lista de insumos).
    """
    for item in lista:
        print(item)


# -------------------------
# Decorador: medir performance
# -------------------------
def medir_performance(func):
    """
    Decorator que mede tempo de execução e uso de memória da função decorada.
    - usa tracemalloc para medir memória alocada durante a execução
    - usa time.perf_counter() para medir tempo com alta resolução
    Ao final, imprime o tempo e a memória (atual e pico).
    """
    def wrapper(*args, **kwargs):
        tracemalloc.start()                      # inicia rastreamento de memória
        inicio_tempo = time.perf_counter()       # marca o tempo inicial

        resultado = func(*args, **kwargs)       # executa a função decorada

        fim_tempo = time.perf_counter()         # marca o tempo final
        memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()                      # para o rastreamento de memória

        # imprime métricas de performance
        print(f"\n⏱ Tempo de execução: {fim_tempo - inicio_tempo:.6f} s")
        print(f"💾 Memória usada: {memoria_atual / 1024:.2f} KB | Pico: {memoria_pico / 1024:.2f} KB")
        return resultado
    return wrapper


# -------------------------
# FILA
# -------------------------
@medir_performance
def mostrar_fila(consumo_diario):
    """
    Demonstra comportamento de FILA (FIFO).
    - cria um deque a partir da lista de consumo
    - vai 'retirando' elementos com popleft (ordem cronológica)
    """
    fila = deque(consumo_diario)  # deque permite popleft eficiente
    print("\n--- FILA (Ordem cronológica) ---")
    while fila:
        # cada popleft representa o próximo consumido (mais antigo primeiro)
        print("Consumido:", fila.popleft())


# -------------------------
# PILHA
# -------------------------
@medir_performance
def mostrar_pilha(consumo_diario):
    """
    Demonstra comportamento de PILHA (LIFO).
    - converte a lista para uma pilha (list)
    - usa pop() para retirar o último elemento (último consumo primeiro)
    """
    pilha = list(consumo_diario)
    print("\n--- PILHA (Últimos consumos primeiro) ---")
    while pilha:
        # pop retira o último item inserido => LIFO
        print("Consumido:", pilha.pop())


# -------------------------
# BUSCAS (saída explicada)
# -------------------------
@medir_performance
def busca_sequencial(lista, nome):
    """
    Busca sequencial (linear) numa lista não ordenada.
    Imprime informações explicativas:
    - qual lista foi usada (original)
    - tamanho, alvo, número de comparações, resultado e registro encontrado.
    Retorna tuple (índice, objeto) ou (-1, None) se não encontrado.
    """
    print("\n🔎 Busca Sequencial")
    print("- Lista usada: original (não ordenada)")
    print(f"- Tamanho da lista: {len(lista)}")
    print(f"- Alvo: '{nome}'")

    comparacoes = 0
    # percorre cada elemento e compara o campo nome
    for i, insumo in enumerate(lista):
        comparacoes += 1
        if insumo.nome == nome:
            # encontrado: imprime detalhes e retorna
            print(f"- Comparações realizadas: {comparacoes}")
            print(f"- Resultado: ENCONTRADO no índice {i} da lista original.")
            print(f"- Registro: {insumo}")
            return i, insumo

    # não encontrado após percorrer toda a lista
    print(f"- Comparações realizadas: {comparacoes}")
    print("- Resultado: NÃO ENCONTRADO")
    return -1, None


@medir_performance
def busca_binaria(lista_ordenada, nome, lista_original=None):
    """
    Busca binária em lista ordenada por nome (crescente).
    Parâmetros:
    - lista_ordenada: lista previamente ordenada (por exemplo: sorted(lista, key=lambda x: x.nome))
    - nome: string com o nome buscado
    - lista_original: lista não ordenada (opcional). Se fornecida, tentamos localizar
      a posição correspondente na lista original usando identidade do objeto (is),
      já que sorted preserva referências aos mesmos objetos.
    Saída:
    - imprime número de iterações, comparações e posição na lista ordenada
    - se lista_original fornecida, também imprime a posição correspondente nela (se encontrada)
    - retorna (índice_na_lista_ordenada, objeto) ou (-1, None)
    """
    print("\n🔎 Busca Binária")
    print("- Lista usada: ORDENADA por nome (crescente)")
    print(f"- Tamanho da lista: {len(lista_ordenada)}")
    print(f"- Alvo: '{nome}'")

    esquerda, direita = 0, len(lista_ordenada) - 1
    iteracoes = 0
    comp_igualdade = 0  # conta comparações de igualdade (==)
    comp_ordem = 0      # conta comparações de ordem (< ou >)

    while esquerda <= direita:
        iteracoes += 1
        meio = (esquerda + direita) // 2
        nome_meio = lista_ordenada[meio].nome

        comp_igualdade += 1
        if nome_meio == nome:
            # encontrado no meio
            item = lista_ordenada[meio]
            idx_ordenada = meio
            idx_original = None

            # se o usuário passou a lista original, procuramos a posição correspondente
            # obs: sorted() mantém as mesmas referências aos objetos, logo podemos comparar por identidade (is)
            if lista_original is not None:
                for i, obj in enumerate(lista_original):
                    if obj is item:
                        idx_original = i
                        break

            # imprime resultados detalhados
            print(f"- Iterações: {iteracoes}")
            print(f"- Comparações de igualdade: {comp_igualdade} | de ordem: {comp_ordem}")
            print(f"- Resultado: ENCONTRADO na posição {idx_ordenada} da lista ORDENADA.")
            if idx_original is not None:
                print(f"- Posição correspondente na lista ORIGINAL: {idx_original}")
            print(f"- Registro: {item}")
            return idx_ordenada, item

        # se não igual, ajusta intervalo de busca
        comp_ordem += 1
        if nome_meio < nome:
            esquerda = meio + 1
        else:
            direita = meio - 1

    # não encontrado
    print(f"- Iterações: {iteracoes}")
    print(f"- Comparações de igualdade: {comp_igualdade} | de ordem: {comp_ordem}")
    print("- Resultado: NÃO ENCONTRADO")
    return -1, None


# -------------------------
# ORDENAÇÃO
# -------------------------
def merge_sort(lista, chave):
    """
    Implementação recursiva de Merge Sort.
    - lista: lista de objetos
    - chave: função que extrai o valor de comparação (ex.: lambda x: x.quantidade)
    Retorna uma nova lista ordenada.
    """
    if len(lista) <= 1:
        return lista
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio], chave)
    direita = merge_sort(lista[meio:], chave)
    return merge(esquerda, direita, chave)


def merge(esq, dir, chave):
    """
    Função auxiliar para mesclar duas listas já ordenadas (esq e dir).
    Usa a função 'chave' para comparar elementos.
    """
    resultado = []
    i = j = 0
    while i < len(esq) and j < len(dir):
        if chave(esq[i]) <= chave(dir[j]):
            resultado.append(esq[i]); i += 1
        else:
            resultado.append(dir[j]); j += 1
    # anexar o restante de uma das listas
    resultado.extend(esq[i:]); resultado.extend(dir[j:])
    return resultado


def quick_sort(lista, chave):
    """
    Implementação de Quick Sort (versão funcional / não in-place).
    - escolhe um pivô (meio) e particiona em menores/iguais/maiores
    - concatena recursivamente
    Nota: esta implementação cria listas adicionais (não é in-place),
    mas é simples e didática.
    """
    if len(lista) <= 1:
        return lista
    pivo = lista[len(lista) // 2]
    iguais  = [x for x in lista if chave(x) == chave(pivo)]
    menores = [x for x in lista if chave(x) <  chave(pivo)]
    maiores = [x for x in lista if chave(x) >  chave(pivo)]
    return quick_sort(menores, chave) + iguais + quick_sort(maiores, chave)


@medir_performance
def ordenar_merge(consumo_diario):
    """
    Wrapper para ordenar por quantidade usando Merge Sort.
    Decorado para medir performance.
    """
    return merge_sort(consumo_diario, lambda x: x.quantidade)


@medir_performance
def ordenar_quick(consumo_diario):
    """
    Wrapper para ordenar por validade usando Quick Sort.
    Decorado para medir performance.
    """
    return quick_sort(consumo_diario, lambda x: x.validade)


# -------------------------
# MENU INTERATIVO
# -------------------------
def menu():
    """
    Menu interativo em loop.
    - permite gerar dados simulados
    - escolher operações: exibir, fila, pilha, buscas, ordenações
    - cada operação usa as funções definidas acima
    """
    consumo_diario = gerar_consumo()  # gera dados iniciais
    while True:
        # imprime opções do menu
        print("\n=== MENU ===")
        print("1 - Mostrar dados simulados")
        print("2 - Fila (ordem cronológica)")
        print("3 - Pilha (últimos consumos)")
        print("4 - Busca Sequencial (explicada)")
        print("5 - Busca Binária (explicada)")
        print("6 - Ordenar por quantidade (Merge Sort)")
        print("7 - Ordenar por validade (Quick Sort)")
        print("8 - Gerar novos dados simulados")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\n--- Dados simulados ---")
            mostrar_lista(consumo_diario)

        elif opcao == "2":
            mostrar_fila(consumo_diario)

        elif opcao == "3":
            mostrar_pilha(consumo_diario)

        elif opcao == "4":
            # busca sequencial (usa lista original)
            nome = input("Digite o nome do insumo para buscar: ")
            idx, item = busca_sequencial(consumo_diario, nome)
            print(f"\n↩️ Retorno da função: {(idx, item)}")

        elif opcao == "5":
            # busca binária: precisa ordenar por nome antes de chamar
            nome = input("Digite o nome do insumo para buscar: ")
            lista_ordenada = sorted(consumo_diario, key=lambda x: x.nome)
            idx, item = busca_binaria(lista_ordenada, nome, lista_original=consumo_diario)
            print(f"\n↩️ Retorno da função (índice na lista ORDENADA, objeto): {(idx, item)}")

        elif opcao == "6":
            print("\n--- Ordenado por quantidade (Merge Sort) ---")
            ordenado = ordenar_merge(consumo_diario)
            mostrar_lista(ordenado)

        elif opcao == "7":
            print("\n--- Ordenado por validade (Quick Sort) ---")
            ordenado = ordenar_quick(consumo_diario)
            mostrar_lista(ordenado)

        elif opcao == "8":
            consumo_diario = gerar_consumo()
            print("\n✅ Novos dados simulados gerados!")

        elif opcao == "0":
            print("Encerrando...")
            break

        else:
            print("Opção inválida. Tente novamente.")
