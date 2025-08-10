from hero import Hero
from menu_button import Button

# Dimensões da tela (Jogo com 16x16 tiles, cada tile com 16x18 pixels)
TILE_SIZE = 18
WIDTH = TILE_SIZE * 16
HEIGHT = TILE_SIZE * 16

game_state = "menu"  # Estados do jogo: menu, playing
sound_on = True
sounds.background.play(-1)
menu_buttons = []
mouse_position = (0, 0)


# Mantem a posição do mouse atualizada
# Necessário já que não temos acesso a pygame.mouse.get_pos
def on_mouse_move(pos):
    global mouse_position
    mouse_position = pos


# Cria os objetos para um jogo novo e atualiza o game state
def on_start():
    global game_state, hero
    hero = Hero((WIDTH // 2, HEIGHT // 2), 1)
    game_state = "playing"
    print("[DEBUG] game_state:", game_state)


def on_exit():
    print("[DEBUG] fechando o jogo")
    exit()


def toggle_sound():
    global sound_on
    sound_on = not sound_on
    print("[DEBUG] sound_on:", sound_on)
    if sound_on:
        sounds.background.play(-1)
    else:
        sounds.background.stop()


def draw_menu():
    global menu_buttons
    title_fontsize = 32
    subtitle_fontsize = 16

    CENTER = WIDTH // 2, HEIGHT // 2
    title_pos = (CENTER[0], 16)
    subtitle_pos = (CENTER[0], 16 + title_fontsize)
    init_pos = (CENTER[0], CENTER[1] - 40)
    sound_pos = (CENTER[0], CENTER[1])
    exit_pos = (CENTER[0], CENTER[1] + 40)

    menu_buttons = [
        Button("Iniciar", init_pos, on_click=on_start),
        Button(
            f"Som: {'LIGADO' if sound_on else 'DESLIGADO'}",
            sound_pos,
            on_click=toggle_sound,
        ),
        Button("Sair", exit_pos, on_click=on_exit),
    ]

    screen.clear()
    screen.draw.text("Roguelike", midtop=title_pos, fontsize=title_fontsize)
    screen.draw.text(
        "Derrote dos monstros e encontre o tesouro",
        midtop=subtitle_pos,
        fontsize=subtitle_fontsize,
    )
    for button in menu_buttons:
        button.draw(screen, mouse_position)


def on_mouse_down(pos):
    if game_state == "menu":
        for button in menu_buttons:
            button.check_click(pos)


def draw():
    if game_state == "menu":
        draw_menu()
    if game_state == "playing":
        screen.clear()
        hero.draw()


def update():
    if game_state == "playing":
        hero.animate()
        hero.move(
            keyboard,
            (TILE_SIZE, WIDTH - TILE_SIZE, TILE_SIZE, HEIGHT - TILE_SIZE),
            TILE_SIZE,
        )
