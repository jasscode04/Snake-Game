from tkinter import *
import random
import os

# Constants
GAME_WIDTH = 600
GAME_HEIGHT = 600
SPEED = 170
SPACE_SIZE = 17
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
HIGHSCORE_FILE = "highscore.txt"

# Globals
score = 0
high_score = 0
direction = 'down'
paused = False
game_running = True

# Initialize the window
window = Tk()
window.title("Snake Game with High Score")
window.resizable(False, False)

# High Score Functions
def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as file:
            return int(file.read())
    return 0

def save_high_score(score):
    with open(HIGHSCORE_FILE, "w") as file:
        file.write(str(score))

# UI Elements
high_score = load_high_score()
label = Label(window, text=f"Score: {score}   High Score: {high_score}", font=('consolas', 25))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

retry_btn = Button(window, text="Retry", font=('consolas', 20), command=lambda: retry_game())
exit_btn = Button(window, text="Exit", font=('consolas', 20), command=lambda: window.destroy())

# Centering the window
window.update()
x = (window.winfo_screenwidth() // 2) - (window.winfo_width() // 2)
y = (window.winfo_screenheight() // 2) - (window.winfo_height() // 2)
window.geometry(f"{window.winfo_width()}x{window.winfo_height()}+{x}+{y}")

# Snake Class
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [[0, 0] for _ in range(BODY_PARTS)]
        self.squares = []

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# Food Class
class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Game Logic
def next_turn(snake, food):
    if not game_running or paused:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score, high_score
        score += 1
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        update_score()
        canvas.delete("food")
        food.__init__()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def update_score():
    label.config(text=f"Score: {score}   High Score: {high_score}")

def game_over():
    global game_running
    game_running = False
    canvas.delete("all")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 50, font=('consolas', 50), text="GAME OVER", fill="red")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 10, font=('consolas', 20),
                       text="Press 'R' to Retry or 'E' to Exit", fill="white")
    retry_btn.pack(pady=10)
    exit_btn.pack(pady=5)

def retry_game():
    global score, direction, paused, game_running, snake, food

    retry_btn.pack_forget()
    exit_btn.pack_forget()

    canvas.delete("all")
    score = 0
    direction = "down"
    paused = False
    game_running = True

    snake = Snake()
    food = Food()
    update_score()
    next_turn(snake, food)

def toggle_pause(event=None):
    global paused
    paused = not paused
    if paused:
        canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, font=('consolas', 40), text="PAUSED", fill="yellow", tag="pause")
    else:
        canvas.delete("pause")
        next_turn(snake, food)

# Controls
window.bind('<Left>', lambda e: change_direction('left'))
window.bind('<Right>', lambda e: change_direction('right'))
window.bind('<Up>', lambda e: change_direction('up'))
window.bind('<Down>', lambda e: change_direction('down'))
window.bind('r', lambda e: retry_game())
window.bind('e', lambda e: window.destroy())
window.bind('p', toggle_pause)

# Start game
snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()
