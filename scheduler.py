# classe processo
class Process: # Um processo possui data de criação, duração do processo e prioridade, nessa ordem
    def __init__(self, creation_date, burst_time, priority):
        self.creation_date = creation_date
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time # inicialmente o tempo restante é igual à duração do processo

'''
    classe que irá guardar as informações da execução dos escaladores
    proccesses_executions é uma lista de listas, em que cada linha é um instante da execução,
    e cada linha da execução é o estado do processo. -1 significa que ele ainda não entrou na fila
    de espera, 0 significa que ele está suspensão e 1 significa ativo. tt é tempo médio de vida, tw é
    tempo médio de espera e context_swaps é o número de trocas de contexto
'''
class Execution:
    def __init__(self, processes_executions: list[list[int]], tt = 0, tw = 0, context_swaps = 0):
        self.tt = tt
        self.tw = tw
        self.context_swaps = context_swaps
        self.processes = processes
        self.processes_executions = processes_executions
        
        # Criando primeira linha do diagrama de execução
        first_line = 'tempo   '
        for i in range(len(processes_executions[0])):
            first_line = first_line + f' P{i+1}'
        self.execution_diagram = first_line

    def generate_statistics(self): # gera todos os dados de saídas necessários
        
        # constrói o diagrama de execução
        for i in range(len(self.processes_executions)):
            current_line = ['##' if (p == 1) else '--' if (p == 0) else '  ' for p in self.processes_executions[i]]
            self.execution_diagram += f'\n{i}- {i+1}     ' + (' ').join(current_line)
        print(self.execution_diagram)

# lê o arquivo de configuração e retorna o quantum e o aging
def read_config_file_reader(file_url) -> (int, int):
    with open(file_url, 'r') as file:
        configs = file.read()
    quantum, aging = map(lambda c: int(c.split(':')[1]), configs.split('\n'))
    return quantum, aging

# lê o arquivo de entrada e retorna os processos na forma [Processo 1, Processo 2..., Processo N]
def read_input_file(file_url) -> list[Process]:
    with open(file_url, 'r') as file:
        input = file.read()
    processes = list(map(lambda p: p.split(' '), input.split('\n')))
    return list(map(lambda p: Process(p[0], p[1], p[2]), processes))

# função que recebe a lista de processos e o algoritmo de execução
def execute(processes, alg = ""):
    processes_executions = [[1, -1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    execution = Execution(processes_executions)
    execution.generate_statistics()

processes = read_input_file('input.txt')

execute(processes)