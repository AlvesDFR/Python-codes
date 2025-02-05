import tkinter as tk
import random
import time

# Lista de palavras para o teste
WORDS = ["palavra", "casa", "bola", "carro", "escola", "mesa", "cadeira", "livro", "janela", "gato",
"cachorro", "passarinho", "sol", "lua", "estrela", "água", "terra", "fogo", "vento", "chuva",
"mar", "rio", "montanha", "pedra", "areia", "flor", "árvore", "folha", "céu", "nuvem",
"relógio", "sapato", "roupa", "telefone", "música", "filme", "comida", "fruta", "doce", "salgado",
"alegria", "tristeza", "raiva", "medo", "sorriso", "choro", "abraço", "beijo", "amigo", "amiga",
"pai", "mãe", "irmão", "irmã", "tio", "tia", "avô", "avó", "primo", "prima",
"caderno", "lápis", "borracha", "caneta", "mochila", "dinheiro", "banco", "mercado", "loja", "brinquedo",
"tempo", "relógio", "calor", "frio", "neve", "praia", "campo", "cidade", "vila", "ponte",
"barco", "avião", "trem", "bicicleta", "ônibus", "estrada", "viagem", "mapa", "trabalho", "descanso",
"sono", "sonho", "pesadelo", "história", "verdade", "mentira", "segredo", "força", "coragem", "sorte"]

def start_test():
    global start_time, typed_words, correct_count, word_list, current_word, displayed_words
    start_button.config(state=tk.DISABLED)
    input_entry.config(state=tk.NORMAL)
    input_entry.focus()
    typed_words = []
    correct_count = 0
    start_time = time.time()
    update_timer()
    word_list = random.sample(WORDS, 70)  # Sorteia 70 palavras e mantém fixas
    displayed_words = " ".join(word_list)  # Texto fixo para exibição
    words_display.config(text=displayed_words)
    current_word = ""
    next_word()

def update_timer():
    elapsed = time.time() - start_time
    remaining_time = 60 - int(elapsed)
    timer_label.config(text=f"Tempo: {remaining_time}s")
    if remaining_time > 0:
        root.after(1000, update_timer)
    else:
        end_test()

def next_word():
    global current_word
    if word_list:
        current_word = word_list.pop(0)
        word_label.config(text=current_word, font=("Arial", 16, "bold"))
    else:
        end_test()
    input_entry.delete(0, tk.END)

def check_word(event):
    global correct_count
    typed_word = input_entry.get().strip()
    if typed_word == current_word:
        correct_count += 1
        word_label.config(fg="green")
    else:
        word_label.config(fg="red")
    typed_words.append(typed_word)
    next_word()

def end_test():
    input_entry.config(state=tk.DISABLED)
    start_button.config(state=tk.NORMAL)
    accuracy = (correct_count / len(typed_words) * 100) if typed_words else 0
    word_label.config(text=f"Fim! Score: {correct_count} | Precisão: {accuracy:.2f}%", fg="black")
    timer_label.config(text="Tempo: 0s")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Teste de Velocidade de Digitação")
root.geometry("600x400")

welcome_label = tk.Label(root, text="Bem-vindo ao teste de velocidade de digitação\nby Douglas F. R. Alves\n\nMaximize a janela\nA cada palavra digitada, pressione 'Enter'", font=("Arial", 12), justify="center")
welcome_label.pack(pady=10)

words_display = tk.Label(root, text="", font=("Arial", 12), wraplength=550, justify="center")
words_display.pack(pady=10)

word_label = tk.Label(root, text="Clique em Iniciar", font=("Arial", 16))
word_label.pack(pady=10)

timer_label = tk.Label(root, text="Tempo: 60s", font=("Arial", 14))
timer_label.pack()

input_entry = tk.Entry(root, font=("Arial", 14))
input_entry.pack(pady=10)
input_entry.bind("<Return>", check_word)
input_entry.config(state=tk.DISABLED)

start_button = tk.Button(root, text="Iniciar", font=("Arial", 14), command=start_test)
start_button.pack(pady=20)

root.mainloop()
