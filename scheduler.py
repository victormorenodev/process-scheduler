# lê o arquivo de configuração e retorna o quantum e o aging
def config_file_reader(file_url):
    with open(file_url, 'r') as file:
        configs = file.read()
        print(configs)
        quantum, aging = map(lambda c: c.split(':')[1], configs.split('\n'))
        return quantum, aging

print(config_file_reader('teste.txt'))

# FCFS
# Shorted Job First
# Shortest Remaining Time First
# Round-Robin