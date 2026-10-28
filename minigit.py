from collections import deque


class MiniGit:
    """Representa um repositório Git simplificado baseado em grafo de commits.

    Armazena o histórico de commits, mensagens e branches utilizando dicionários,
    listas e tuplas, contabilizando os passos de cada operação executada.
    """

    __slots__ = (
        "__pais",
        "__mensagens",
        "__branches",
        "__branch_atual",
        "__contador",
        "__passos",
    )

    def __init__(self):
        """Inicializa o repositório vazio na branch 'main' sem commits."""
        self.__pais = {}
        self.__mensagens = {}
        self.__branches = {"main": None}
        self.__branch_atual = "main"
        self.__contador = 0
        self.__passos = 0

    @property
    def passos(self):
        """Devolve a quantidade de passos gastos pela última operação realizada."""
        return self.__passos

    @property
    def branch_atual(self):
        """Devolve o nome da branch atualmente ativa."""
        return self.__branch_atual

    def commitar(self, mensagem):
        """Cria um novo commit apontando para o commit atual da branch ativa.

        Contagem de passos: 2 passos fixos.
        - 1 passo para criar o nó do commit no dicionário.
        - 1 passo para mover o ponteiro da branch ativa para o novo nó.
        """
        if not mensagem:
            raise ValueError("A mensagem do commit não pode ser vazia.")

        self.__contador += 1
        identificador = f"c{self.__contador}"

        commit_pai = self.__branches[self.__branch_atual]
        lista_pais = []
        if commit_pai is not None:
            lista_pais.append(commit_pai)

        self.__pais[identificador] = lista_pais
        self.__mensagens[identificador] = mensagem
        self.__branches[self.__branch_atual] = identificador
        self.__passos = 2
        return identificador

    def mensagem(self, commit):
        """Devolve a mensagem associada ao identificador do commit informado.

        Contagem de passos: 1 passo fixo.
        - Acesso direto à chave no dicionário (busca por hash O(1)).
        """
        if commit not in self.__mensagens:
            raise ValueError(f"Commit '{commit}' não existe.")

        self.__passos = 1
        return self.__mensagens[commit]

    def pais(self, commit):
        """Devolve os identificadores dos pais do commit como uma tupla imutável.

        Contagem de passos: 1 passo fixo.
        - Acesso direto à chave no dicionário (busca por hash O(1)).
        """
        if commit not in self.__pais:
            raise ValueError(f"Commit '{commit}' não existe.")

        self.__passos = 1
        return tuple(self.__pais[commit])

    def criar_branch(self, nome):
        """Cria uma nova branch apontando para o commit atual da branch ativa.

        Contagem de passos: 1 passo fixo.
        - 1 passo para registrar a nova chave no dicionário de branches.
        """
        if nome in self.__branches:
            raise ValueError(f"Branch '{nome}' já existe.")

        commit_atual = self.__branches[self.__branch_atual]
        if commit_atual is None:
            raise ValueError("Não há commits para criar uma nova branch.")

        self.__branches[nome] = commit_atual
        self.__passos = 1

    def trocar_branch(self, nome):
        """Altera a branch ativa para a branch indicada.

        Contagem de passos: 1 passo fixo.
        - 1 passo para atualizar o nome da branch atual (ponteiro HEAD).
        """
        if nome not in self.__branches:
            raise ValueError(f"Branch '{nome}' não existe.")

        self.__branch_atual = nome
        self.__passos = 1

    def mesclar(self, nome):
        """Mescla a branch indicada na branch atual, gerando um commit com dois pais.

        Contagem de passos: 2 passos fixos.
        - 1 passo para criar o commit com os dois pais.
        - 1 passo para mover o ponteiro da branch ativa para o commit de mesclagem.
        """
        if nome not in self.__branches:
            raise ValueError(f"Branch '{nome}' não existe.")

        if nome == self.__branch_atual:
            raise ValueError("Não é possível mesclar a branch com ela mesma.")

        commit_atual = self.__branches[self.__branch_atual]
        commit_indicado = self.__branches[nome]

        self.__contador += 1
        identificador = f"c{self.__contador}"

        self.__pais[identificador] = [commit_atual, commit_indicado]
        self.__mensagens[identificador] = f"merge de {nome}"
        self.__branches[self.__branch_atual] = identificador
        self.__passos = 2
        return identificador

    def log(self):
        """Devolve os identificadores de todos os commits alcançáveis a partir da branch atual.

        Contagem de passos: 1 passo por commit visitado.
        - Percorre o grafo em largura usando uma fila (collections.deque).
        - Gasta a quantidade exata de commits retornados (0 se não houver commits).
        """
        commit_ponta = self.__branches[self.__branch_atual]
        if commit_ponta is None:
            self.__passos = 0
            return ()

        visitados = []
        fila = deque([commit_ponta])

        while len(fila) > 0:
            commit_atual = fila.popleft()
            if commit_atual in visitados:
                continue
            visitados.append(commit_atual)
            for pai in self.__pais[commit_atual]:
                fila.append(pai)

        self.__passos = len(visitados)
        return tuple(visitados)

    def buscar(self, texto):
        """Busca o primeiro commit, por ordem de criação, cuja mensagem contenha o texto indicado.

        Contagem de passos: 1 passo por commit examinado.
        - Itera sobre os commits na ordem em que foram criados até encontrar a ocorrência,
          ou percorre todos se nenhum contiver o texto.
        """
        passos_gastos = 0
        for identificador, mensagem in self.__mensagens.items():
            passos_gastos += 1
            if texto in mensagem:
                self.__passos = passos_gastos
                return identificador

        self.__passos = passos_gastos
        return None

    def merges(self):
        """Devolve uma tupla com os identificadores dos commits que possuem mais de um pai.

        Contagem de passos: 1 passo por commit existente no repositório.
        - Percorre todos os commits registrados verificando a quantidade de pais.
        """
        lista_merges = []
        for identificador, lista_pais in self.__pais.items():
            if len(lista_pais) > 1:
                lista_merges.append(identificador)

        self.__passos = len(self.__pais)
        return tuple(lista_merges)


def tentar(acao):
    """Executa uma ação e captura possíveis exceções ValueError."""
    try:
        acao()
    except ValueError as erro:
        print("erro:", erro)


def medir(quantidade):
    """Mede os passos de escrita (commitar) e leitura (log) para uma quantidade de commits."""
    git_medicao = MiniGit()
    for numero in range(quantidade):
        git_medicao.commitar(f"commit {numero}")
    passos_commitar = git_medicao.passos
    git_medicao.log()
    passos_log = git_medicao.passos
    return passos_commitar, passos_log


if __name__ == "__main__":
    git = MiniGit()
    git.commitar("primeiro commit")
    print(git.passos)
    git.commitar("segundo commit")
    git.criar_branch("feature")
    print(git.passos)
    git.commitar("terceiro commit")
    git.trocar_branch("feature")
    git.commitar("quarto commit")
    git.trocar_branch("main")
    git.mesclar("feature")
    print(git.pais("c5"))
    print(git.log(), git.passos)
    print(git.mensagem("c3"), git.passos)
    print(git.buscar("quarto"), git.passos)
    print(git.merges())
    git.trocar_branch("feature")
    print(git.log(), git.passos)
    git.trocar_branch("main")

    tentar(lambda: git.trocar_branch("inexistente"))
    tentar(lambda: git.criar_branch("main"))
    tentar(lambda: git.mesclar("main"))
    tentar(lambda: git.pais("c99"))

    print("commits   passos do commitar   passos do log")
    for quantidade in (10, 100, 1000):
        passos_commitar, passos_log = medir(quantidade)
        print(f"{quantidade:<10}{passos_commitar:<21}{passos_log}")
