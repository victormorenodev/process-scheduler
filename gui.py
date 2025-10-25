import tkinter as tk
from tkinter import filedialog, messagebox
from scheduler import Process, load_processes_from_file
from algorithms import execute_algorithm

# Variáveis globais
processes = []

def add_process():
    try:
        creation = int(entry_creation.get())
        burst = int(entry_burst.get())
        priority = int(entry_priority.get())

        p = Process(creation, burst, priority)
        processes.append(p)

        # adiciona na lista
        process_listbox.insert(tk.END, f"P{len(processes)}: t={creation}, d={burst}, p={priority}")

        # limpa campos
        entry_creation.delete(0, tk.END)
        entry_burst.delete(0, tk.END)
        entry_priority.delete(0, tk.END)

    except:
        messagebox.showerror("Erro", "Valores inválidos")

def load_file():
    global processes
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            processes = load_processes_from_file(file_path)
            process_listbox.delete(0, tk.END)

            for i, p in enumerate(processes):
                process_listbox.insert(tk.END, f"P{i+1}: t={p.creation_date}, d={p.burst_time}, p={p.priority}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")

def clear_processes():
    global processes
    processes = []
    process_listbox.delete(0, tk.END)
    text_result.delete(1.0, tk.END)
    label_tt.config(text="-")
    label_tw.config(text="-")
    label_cs.config(text="-")

def run_simulation():
    if not processes:
        messagebox.showwarning("Aviso", "Adicione processos primeiro")
        return

    # pega configurações
    quantum = int(entry_quantum.get())
    aging = int(entry_aging.get())

    # pega algoritmo selecionado e converte para código
    alg_name = algorithm_var.get()

    # mapeia nome para código
    alg_map = {
        "FCFS": "fcfs",
        "SJF": "sjf",
        "SRTF": "srtf",
        "Prioridade (sem preempção)": "priority",
        "Prioridade (com preempção)": "priority_preemptive",
        "Round-Robin": "round_robin",
        "Round-Robin com Prioridade": "round_robin_priority"
    }

    alg = alg_map[alg_name]

    # executa
    try:
        execution = execute_algorithm(processes, alg, quantum, aging)

        # mostra resultados
        label_tt.config(text=f"{execution.tt:.2f}s")
        label_tw.config(text=f"{execution.tw:.2f}s")
        label_cs.config(text=str(execution.context_swaps))

        # mostra diagrama
        text_result.delete(1.0, tk.END)
        text_result.insert(1.0, execution.execution_diagram)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro na simulação: {str(e)}")

# Janela principal
root = tk.Tk()
root.title("Simulador de Escalonamento")
root.geometry("1000x700")

# Frame esquerdo
frame_left = tk.Frame(root)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Configurações
frame_config = tk.LabelFrame(frame_left, text="Configurações", padx=10, pady=10)
frame_config.pack(fill=tk.X, pady=5)

tk.Label(frame_config, text="Quantum:").grid(row=0, column=0, sticky=tk.W)
entry_quantum = tk.Entry(frame_config, width=10)
entry_quantum.insert(0, "2")
entry_quantum.grid(row=0, column=1)

tk.Label(frame_config, text="Aging:").grid(row=1, column=0, sticky=tk.W)
entry_aging = tk.Entry(frame_config, width=10)
entry_aging.insert(0, "1")
entry_aging.grid(row=1, column=1)

tk.Label(frame_config, text="Algoritmo:").grid(row=2, column=0, sticky=tk.W)
algorithm_var = tk.StringVar(value="FCFS")
algorithms = [
    "FCFS",
    "SJF",
    "SRTF",
    "Prioridade (sem preempção)",
    "Prioridade (com preempção)",
    "Round-Robin",
    "Round-Robin com Prioridade"
]

menu_alg = tk.OptionMenu(frame_config, algorithm_var, *algorithms)
menu_alg.grid(row=2, column=1, sticky=tk.W)

# Adicionar processo
frame_add = tk.LabelFrame(frame_left, text="Adicionar Processo", padx=10, pady=10)
frame_add.pack(fill=tk.X, pady=5)

tk.Label(frame_add, text="Tempo de Criação:").grid(row=0, column=0)
entry_creation = tk.Entry(frame_add, width=10)
entry_creation.grid(row=0, column=1)

tk.Label(frame_add, text="Duração:").grid(row=1, column=0)
entry_burst = tk.Entry(frame_add, width=10)
entry_burst.grid(row=1, column=1)

tk.Label(frame_add, text="Prioridade:").grid(row=2, column=0)
entry_priority = tk.Entry(frame_add, width=10)
entry_priority.grid(row=2, column=1)

tk.Button(frame_add, text="Adicionar", command=add_process).grid(row=3, column=0, columnspan=2, pady=5)

# Carregar arquivo
frame_file = tk.LabelFrame(frame_left, text="Carregar Arquivo", padx=10, pady=10)
frame_file.pack(fill=tk.X, pady=5)

tk.Button(frame_file, text="Selecionar Arquivo de Input", command=load_file).pack()

# Lista de processos
frame_list = tk.LabelFrame(frame_left, text="Processos", padx=10, pady=10)
frame_list.pack(fill=tk.BOTH, expand=True, pady=5)

process_listbox = tk.Listbox(frame_list, height=10)
process_listbox.pack(fill=tk.BOTH, expand=True)

# Botões
frame_buttons = tk.Frame(frame_left)
frame_buttons.pack(fill=tk.X, pady=5)

tk.Button(frame_buttons, text="Executar", command=run_simulation, bg="green", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="Limpar", command=clear_processes, bg="red", fg="white").pack(side=tk.LEFT, padx=5)

# Frame direito - Resultados
frame_right = tk.Frame(root)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Métricas
frame_metrics = tk.LabelFrame(frame_right, text="Métricas", padx=10, pady=10)
frame_metrics.pack(fill=tk.X, pady=5)

tk.Label(frame_metrics, text="Tempo Médio de Vida:").grid(row=0, column=0)
label_tt = tk.Label(frame_metrics, text="-", font=("Arial", 12, "bold"))
label_tt.grid(row=0, column=1)

tk.Label(frame_metrics, text="Tempo Médio de Espera:").grid(row=1, column=0)
label_tw = tk.Label(frame_metrics, text="-", font=("Arial", 12, "bold"))
label_tw.grid(row=1, column=1)

tk.Label(frame_metrics, text="Trocas de Contexto:").grid(row=2, column=0)
label_cs = tk.Label(frame_metrics, text="-", font=("Arial", 12, "bold"))
label_cs.grid(row=2, column=1)

# Diagrama
frame_diagram = tk.LabelFrame(frame_right, text="Diagrama de Execução", padx=10, pady=10)
frame_diagram.pack(fill=tk.BOTH, expand=True, pady=5)

text_result = tk.Text(frame_diagram, font=("Courier", 9), wrap=tk.NONE)
text_result.pack(fill=tk.BOTH, expand=True)

scrollbar_y = tk.Scrollbar(frame_diagram, command=text_result.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
text_result.config(yscrollcommand=scrollbar_y.set)

scrollbar_x = tk.Scrollbar(frame_diagram, command=text_result.xview, orient=tk.HORIZONTAL)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
text_result.config(xscrollcommand=scrollbar_x.set)

root.mainloop()
