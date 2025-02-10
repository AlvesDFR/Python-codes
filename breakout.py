import turtle
import random

# Configuração da tela
screen = turtle.Screen()
screen.title("Breakout Game")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)  # Desativa atualização automática da tela

# Score e Vidas
score = 0
lives = 3

# Placar (score e vidas)
score_display = turtle.Turtle()
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(250, 260)  # Posição no canto superior direito
score_display.write(f"Score: {score}  Vidas: {lives}", align="left", font=("Arial", 16, "bold"))


# Atualizar placar
def update_score():
    score_display.clear()
    score_display.write(f"Score: {score}\n Vidas: {lives}", align="left", font=("Arial", 16, "bold"))


# Criando a raquete (paddle)
paddle = turtle.Turtle()
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=6)
paddle.penup()
paddle.goto(0, -250)


# Movimento da raquete
def move_left():
    x = paddle.xcor() - 30
    if x > -350:
        paddle.setx(x)


def move_right():
    x = paddle.xcor() + 30
    if x < 350:
        paddle.setx(x)


screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")

# Criando a bola
ball = turtle.Turtle()
ball.shape("circle")
ball.color("red")
ball.penup()
ball.speed(40)
ball.goto(0, -100)
ball.dx = random.choice([-1, 1])  # Velocidade inicial reduzida
ball.dy = 1

# Criando blocos (bricks)
bricks = []


def create_bricks(rows, cols):
    colors = ["red", "orange", "yellow", "green", "blue"]
    for row in range(rows):
        for col in range(cols):
            brick = turtle.Turtle()
            brick.shape("square")
            brick.color(colors[row % len(colors)])
            brick.shapesize(stretch_wid=1, stretch_len=2)
            brick.penup()
            x = -290 + (col * 65)
            y = 200 - (row * 30)
            brick.goto(x, y)
            bricks.append(brick)


create_bricks(5, 10)  # 5 linhas, 10 colunas de blocos

# Loop principal do jogo
running = True


while running:
    screen.update()

    # Movimento da bola
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Colisão com as bordas
    if ball.xcor() > 390 or ball.xcor() < -390:
        ball.dx *= -1  # Inverter direção horizontal

    if ball.ycor() > 290:
        ball.dy *= -1  # Inverter direção vertical

    # Se a bola cair para fora do campo (perde uma vida)
    if ball.ycor() < -290:
        lives -= 1
        update_score()
        if lives == 0:
            print(f"Game Over! Seu score final: {score}")
            running = False
        else:
            ball.goto(0, -100)
            ball.dy *= -1

    # Colisão com a raquete
    if (ball.ycor() < -240 and ball.ycor() > -250) and \
            (paddle.xcor() - 60 < ball.xcor() < paddle.xcor() + 60):
        ball.dy *= -1

    # Colisão com os blocos
    for brick in bricks:
        if brick.distance(ball) < 25:
            ball.dy *= -1
            brick.goto(1000, 1000)  # Remove o bloco da tela
            bricks.remove(brick)  # Remove da lista
            score += 10
            update_score()

    # Se todos os blocos forem destruídos (vitória)
    if not bricks:
        print(f"Parabéns! Você venceu! Score final: {score}")
        running = False

screen.mainloop()
