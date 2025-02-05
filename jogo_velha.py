import random


# Função para limpar a tela (funciona apenas no terminal)
def clear():
    print("\n" * 50)


# Variáveis globais
player_card = "X"
computer_card = "O"
positions = [str(i) for i in range(1, 10)]  # Lista de posições disponíveis
board = [" "] * 9  # Representação do tabuleiro


# Função para exibir o tabuleiro
def display_board():
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")


# Função para verificar se há um vencedor
def check_winner(mark):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
        [0, 4, 8], [2, 4, 6]  # Diagonais
    ]
    return any(all(board[i] == mark for i in condition) for condition in win_conditions)


# Função para verificar empate
def is_draw():
    return " " not in board


# Função para o jogador fazer uma jogada
def player_move():
    while True:
        move = input("Escolha uma posição (1-9): ")
        if move in positions and board[int(move) - 1] == " ":
            board[int(move) - 1] = player_card
            positions.remove(move)
            break
        else:
            print("Movimento inválido! Escolha um número disponível.")


# Função para a jogada do computador
def computer_move():
    move = random.choice([i for i in range(9) if board[i] == " "])
    board[move] = computer_card


# Loop principal do jogo
def play_game():
    clear()
    display_board()

    while True:
        player_move()
        clear()
        display_board()

        if check_winner(player_card):
            print("Parabéns! Você venceu! 🎉")
            break
        if is_draw():
            print("Empate! 🤝")
            break

        print("Vez do computador...")
        computer_move()
        display_board()

        if check_winner(computer_card):
            print("O computador venceu! 😢")
            break
        if is_draw():
            print("Empate! 🤝")
            break


# Iniciar o jogo
if __name__ == "__main__":
    play_game()
