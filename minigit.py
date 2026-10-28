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

        Gasta 2 passos: 1 para criar o registro do commit e 1 para mover
        o ponteiro da branch atual para o novo commit.
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

        Gasta 1 passo: consulta direta por chave no dicionário (O(1)).
        """
        if commit not in self.__mensagens:
            raise ValueError(f"Commit '{commit}' não existe.")

        self.__passos = 1
        return self.__mensagens[commit]

    def pais(self, commit):
        """Devolve os identificadores dos pais do commit como uma tupla imutável.

        Gasta 1 passo: consulta direta por chave no dicionário (O(1)).
        """
        if commit not in self.__pais:
            raise ValueError(f"Commit '{commit}' não existe.")

        self.__passos = 1
        return tuple(self.__pais[commit])

    def criar_branch(self, nome):
        """Cria uma nova branch apontando para o commit atual da branch ativa.

        Gasta 1 passo: cria um novo ponteiro no dicionário de branches.
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

        Gasta 1 passo: atualiza o ponteiro que indica a branch atual.
        """
        if nome not in self.__branches:
            raise ValueError(f"Branch '{nome}' não existe.")

        self.__branch_atual = nome
        self.__passos = 1

    def mesclar(self, nome):
        """Mescla a branch indicada na branch atual, gerando um commit com dois pais.

        Gasta 2 passos: 1 para criar o commit com os dois pais e 1 para mover
        o ponteiro da branch atual para o commit de mesclagem.
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
