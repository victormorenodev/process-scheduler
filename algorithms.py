from scheduler import Process, Execution
import copy

def execute_algorithm(processes, algorithm, quantum=2, aging=1):
    # faz cópia para não alterar os originais
    procs = copy.deepcopy(processes)

    if algorithm == "fcfs":
        return fcfs(procs)
    elif algorithm == "sjf":
        return sjf(procs)
    elif algorithm == "srtf":
        return srtf(procs)
    elif algorithm == "priority":
        return priority_non_preemptive(procs)
    elif algorithm == "priority_preemptive":
        return priority_preemptive(procs)
    elif algorithm == "round_robin":
        return round_robin(procs, quantum)
    elif algorithm == "round_robin_priority":
        return round_robin_priority(procs, quantum, aging)

def fcfs(processes):
    # ordena por tempo de chegada
    processes.sort(key=lambda p: p.creation_date)

    n = len(processes)
    execution_matrix = []
    waiting_times = []
    turnaround_times = []
    context_swaps = 0

    max_time = max(p.creation_date for p in processes) + sum(p.burst_time for p in processes)
    current_process = None

    for t in range(max_time + 1):
        time_slot = [-1] * n

        # marca processos que já chegaram
        for i in range(n):
            if processes[i].creation_date <= t:
                if processes[i].remaining_time > 0:
                    time_slot[i] = 0
                else:
                    time_slot[i] = 0

        # escolhe próximo processo se não tem nenhum executando
        if current_process is None:
            for i in range(n):
                if processes[i].creation_date <= t and processes[i].remaining_time > 0:
                    current_process = i
                    context_swaps += 1
                    break

        # executa processo atual
        if current_process is not None and processes[current_process].remaining_time > 0:
            time_slot[current_process] = 1
            processes[current_process].remaining_time -= 1

            # se terminou
            if processes[current_process].remaining_time == 0:
                turnaround = t + 1 - processes[current_process].creation_date
                waiting = turnaround - processes[current_process].burst_time
                turnaround_times.append(turnaround)
                waiting_times.append(waiting)
                current_process = None

        execution_matrix.append(time_slot)

    avg_tt = sum(turnaround_times) / n
    avg_tw = sum(waiting_times) / n

    execution = Execution(execution_matrix, avg_tt, avg_tw, context_swaps)
    execution.generate_statistics()
    return execution

def sjf(processes):
    # shortest job first (não preemptivo)
    n = len(processes)
    execution_matrix = []
    waiting_times = []
    turnaround_times = []
    context_swaps = 0

    max_time = max(p.creation_date for p in processes) + sum(p.burst_time for p in processes)
    current_process = None
    completed = 0

    for t in range(max_time + 1):
        time_slot = [-1] * n

        for i in range(n):
            if processes[i].creation_date <= t:
                time_slot[i] = 0

        # escolhe processo com menor burst time
        if current_process is None:
            min_burst = 999999
            next_proc = None
            for i in range(n):
                if processes[i].creation_date <= t and processes[i].remaining_time > 0:
                    if processes[i].remaining_time < min_burst:
                        min_burst = processes[i].remaining_time
                        next_proc = i

            if next_proc is not None:
                current_process = next_proc
                context_swaps += 1

        # executa
        if current_process is not None and processes[current_process].remaining_time > 0:
            time_slot[current_process] = 1
            processes[current_process].remaining_time -= 1

            if processes[current_process].remaining_time == 0:
                turnaround = t + 1 - processes[current_process].creation_date
                waiting = turnaround - processes[current_process].burst_time
                turnaround_times.append(turnaround)
                waiting_times.append(waiting)
                current_process = None
                completed += 1

        execution_matrix.append(time_slot)

        if completed == n:
            break

    avg_tt = sum(turnaround_times) / n
    avg_tw = sum(waiting_times) / n

    execution = Execution(execution_matrix, avg_tt, avg_tw, context_swaps)
    execution.generate_statistics()
    return execution

def srtf(processes):
    # shortest remaining time first (preemptivo)
    n = len(processes)
    execution_matrix = []
    waiting_times = []
    turnaround_times = []
    context_swaps = 0

    max_time = max(p.creation_date for p in processes) + sum(p.burst_time for p in processes)
    current_process = None
    completed = 0

    for t in range(max_time + 1):
        time_slot = [-1] * n

        for i in range(n):
            if processes[i].creation_date <= t:
                time_slot[i] = 0

        # escolhe processo com menor tempo restante
        min_remaining = 999999
        next_proc = None
        for i in range(n):
            if processes[i].creation_date <= t and processes[i].remaining_time > 0:
                if processes[i].remaining_time < min_remaining:
                    min_remaining = processes[i].remaining_time
                    next_proc = i
                elif processes[i].remaining_time == min_remaining and i == current_process:
                    next_proc = current_process

        if next_proc is not None and next_proc != current_process:
            context_swaps += 1
            current_process = next_proc

        # executa
        if current_process is not None and processes[current_process].remaining_time > 0:
            time_slot[current_process] = 1
            processes[current_process].remaining_time -= 1

            if processes[current_process].remaining_time == 0:
                turnaround = t + 1 - processes[current_process].creation_date
                waiting = turnaround - processes[current_process].burst_time
                turnaround_times.append(turnaround)
                waiting_times.append(waiting)
                completed += 1

        execution_matrix.append(time_slot)

        if completed == n:
            break

    avg_tt = sum(turnaround_times) / n
    avg_tw = sum(waiting_times) / n

    execution = Execution(execution_matrix, avg_tt, avg_tw, context_swaps)
    execution.generate_statistics()
    return execution

def priority_non_preemptive(processes):
    # por prioridade sem preempção (menor número = maior prioridade)
    n = len(processes)
    execution_matrix = []
    waiting_times = []
    turnaround_times = []
    context_swaps = 0

    max_time = max(p.creation_date for p in processes) + sum(p.burst_time for p in processes)
    current_process = None
    completed = 0

    for t in range(max_time + 1):
        time_slot = [-1] * n

        for i in range(n):
            if processes[i].creation_date <= t:
                time_slot[i] = 0

        # escolhe processo com maior prioridade (menor valor)
        if current_process is None:
            min_priority = 999999
            next_proc = None
            for i in range(n):
                if processes[i].creation_date <= t and processes[i].remaining_time > 0:
                    if processes[i].priority < min_priority:
                        min_priority = processes[i].priority
                        next_proc = i
                    elif processes[i].priority == min_priority:
                        if next_proc is None or processes[i].remaining_time < processes[next_proc].remaining_time:
                            next_proc = i

            if next_proc is not None:
                current_process = next_proc
                context_swaps += 1

        # executa
        if current_process is not None and processes[current_process].remaining_time > 0:
            time_slot[current_process] = 1
            processes[current_process].remaining_time -= 1

            if processes[current_process].remaining_time == 0:
                turnaround = t + 1 - processes[current_process].creation_date
                waiting = turnaround - processes[current_process].burst_time
                turnaround_times.append(turnaround)
                waiting_times.append(waiting)
                current_process = None
                completed += 1

        execution_matrix.append(time_slot)

        if completed == n:
            break

    avg_tt = sum(turnaround_times) / n
    avg_tw = sum(waiting_times) / n

    execution = Execution(execution_matrix, avg_tt, avg_tw, context_swaps)
    execution.generate_statistics()
    return execution

def priority_preemptive(processes):
    # por prioridade com preempção
    n = len(processes)
    execution_matrix = []
    waiting_times = []
    turnaround_times = []
    context_swaps = 0

    max_time = max(p.creation_date for p in processes) + sum(p.burst_time for p in processes)
    current_process = None
    completed = 0

    for t in range(max_time + 1):
        time_slot = [-1] * n

        for i in range(n):
            if processes[i].creation_date <= t:
                time_slot[i] = 0

        # escolhe processo com maior prioridade
        min_priority = 999999
        next_proc = None
        for i in range(n):
            if processes[i].creation_date <= t and processes[i].remaining_time > 0:
                if processes[i].priority < min_priority:
                    min_priority = processes[i].priority
                    next_proc = i
                elif processes[i].priority == min_priority:
                    if i == current_process:
                        next_proc = current_process
                    elif next_proc != current_process and processes[i].remaining_time < processes[next_proc].remaining_time:
                        next_proc = i

        if next_proc is not None and next_proc != current_process:
            context_swaps += 1
            current_process = next_proc

        # executa
        if current_process is not None and processes[current_process].remaining_time > 0:
            time_slot[current_process] = 1
            processes[current_process].remaining_time -= 1

            if processes[current_process].remaining_time == 0:
                turnaround = t + 1 - processes[current_process].creation_date
                waiting = turnaround - processes[current_process].burst_time
                turnaround_times.append(turnaround)
                waiting_times.append(waiting)
                completed += 1

        execution_matrix.append(time_slot)

        if completed == n:
            break

    avg_tt = sum(turnaround_times) / n
    avg_tw = sum(waiting_times) / n

    execution = Execution(execution_matrix, avg_tt, avg_tw, context_swaps)
    execution.generate_statistics()
    return execution

def round_robin(processes, quantum):
    # round-robin sem prioridade
    n = len(processes)
    execution_matrix = []
    waiting_times = []
    turnaround_times = []
    context_swaps = 0

    max_time = max(p.creation_date for p in processes) + sum(p.burst_time for p in processes) + n * quantum

    ready_queue = []
    current_process = None
    quantum_left = 0
    completed = 0
    added = [False] * n

    for t in range(max_time + 1):
        time_slot = [-1] * n

        # adiciona processos que chegaram na fila
        for i in range(n):
            if processes[i].creation_date == t and not added[i]:
                ready_queue.append(i)
                added[i] = True

        for i in range(n):
            if processes[i].creation_date <= t:
                time_slot[i] = 0

        # se quantum acabou, devolve processo pra fila
        if current_process is not None and quantum_left == 0:
            if processes[current_process].remaining_time > 0:
                ready_queue.append(current_process)
            current_process = None

        # pega próximo processo da fila
        if current_process is None and ready_queue:
            current_process = ready_queue.pop(0)
            quantum_left = quantum
            context_swaps += 1

        # executa
        if current_process is not None and processes[current_process].remaining_time > 0:
            time_slot[current_process] = 1
            processes[current_process].remaining_time -= 1
            quantum_left -= 1

            if processes[current_process].remaining_time == 0:
                turnaround = t + 1 - processes[current_process].creation_date
                waiting = turnaround - processes[current_process].burst_time
                turnaround_times.append(turnaround)
                waiting_times.append(waiting)
                current_process = None
                quantum_left = 0
                completed += 1

        execution_matrix.append(time_slot)

        if completed == n:
            break

    avg_tt = sum(turnaround_times) / n
    avg_tw = sum(waiting_times) / n

    execution = Execution(execution_matrix, avg_tt, avg_tw, context_swaps)
    execution.generate_statistics()
    return execution

def round_robin_priority(processes, quantum, aging):
    # round-robin com prioridade e envelhecimento
    n = len(processes)
    execution_matrix = []
    waiting_times = []
    turnaround_times = []
    context_swaps = 0

    max_time = max(p.creation_date for p in processes) + sum(p.burst_time for p in processes) + n * quantum

    ready_queue = []
    current_process = None
    quantum_left = 0
    completed = 0
    added = [False] * n

    # prioridades dinâmicas
    dynamic_priority = [p.priority for p in processes]

    for t in range(max_time + 1):
        time_slot = [-1] * n

        # adiciona processos que chegaram
        for i in range(n):
            if processes[i].creation_date == t and not added[i]:
                ready_queue.append(i)
                added[i] = True

        for i in range(n):
            if processes[i].creation_date <= t:
                time_slot[i] = 0

        # se quantum acabou
        if current_process is not None and quantum_left == 0:
            # aplica aging nos processos da fila
            for idx in ready_queue:
                dynamic_priority[idx] = max(1, dynamic_priority[idx] - aging)

            if processes[current_process].remaining_time > 0:
                # processo volta com prioridade original (estática)
                dynamic_priority[current_process] = processes[current_process].priority
                ready_queue.append(current_process)
            current_process = None

        # escolhe próximo processo por prioridade
        if current_process is None and ready_queue:
            # ordena por prioridade dinâmica (menor prioridade primeiro)
            # em caso de empate, mantém ordem FIFO (primeiro da fila)
            ready_queue.sort(key=lambda i: dynamic_priority[i])
            current_process = ready_queue.pop(0)
            quantum_left = quantum
            context_swaps += 1

        # executa
        if current_process is not None and processes[current_process].remaining_time > 0:
            time_slot[current_process] = 1
            processes[current_process].remaining_time -= 1
            quantum_left -= 1

            if processes[current_process].remaining_time == 0:
                turnaround = t + 1 - processes[current_process].creation_date
                waiting = turnaround - processes[current_process].burst_time
                turnaround_times.append(turnaround)
                waiting_times.append(waiting)
                current_process = None
                quantum_left = 0
                completed += 1

        execution_matrix.append(time_slot)

        if completed == n:
            break

    avg_tt = sum(turnaround_times) / n
    avg_tw = sum(waiting_times) / n

    execution = Execution(execution_matrix, avg_tt, avg_tw, context_swaps)
    execution.generate_statistics()
    return execution
