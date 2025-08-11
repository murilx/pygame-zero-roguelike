from enemy import Orc, Shooter
from hero import Hero
from menu_button import Button

# Dimensões da tela (Jogo com 16x16 tiles, cada tile com 16x18 pixels)
TILE_SIZE = 18
WIDTH = TILE_SIZE * 16
HEIGHT = TILE_SIZE * 16

game_state = "menu"  # Estados do jogo: menu, playing, defeat
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
    global bullets, enemies
    hero = Hero((WIDTH // 2, HEIGHT // 2))
    enemies = [Orc((36, HEIGHT // 2)), Shooter((WIDTH // 2, 36))]
    bullets = []
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


def draw_end_screen(message):
    message_fontsize = 32
    subtitle_fontsize = 16

    message_pos = (WIDTH // 2, 16)
    subtitle_pos = (WIDTH // 2, 16 + message_fontsize)

    screen.clear()
    screen.draw.text(message, midtop=message_pos, fontsize=message_fontsize)
    screen.draw.text(
        "Clique em qualquer lugar da tela para sair",
        midtop=subtitle_pos,
        fontsize=subtitle_fontsize,
    )


def on_mouse_down(pos):
    if game_state == "menu":
        for button in menu_buttons:
            button.check_click(pos)
    if game_state == "defeat":
        on_exit()  # Fecha o jogo


def update_bullets():
    for bullet in bullets:
        future_x, future_y = bullet[0].x, bullet[0].y
        if bullet[1] == "x":
            future_x = bullet[0].x + bullet[2]
        else:
            future_y = bullet[0].y + bullet[2]

        # Verifica a colisão das balas com paredes
        left_limit = TILE_SIZE
        right_limit = WIDTH - TILE_SIZE
        top_limit = TILE_SIZE
        bottom_limit = HEIGHT - TILE_SIZE

        if future_x < left_limit or future_x > right_limit:
            bullets.remove(bullet)
            continue

        if future_y < top_limit or future_y > bottom_limit:
            bullets.remove(bullet)
            continue

        # Caso a bala vá para uma posição válida, atualiza
        bullet[0].x = future_x
        bullet[0].y = future_y


def check_collisions():
    global game_state
    for enemy in enemies:
        if hero.actor.colliderect(enemy.actor):
            game_state = "defeat"

    for bullet in bullets:
        if hero.actor.colliderect(bullet[0]):
            game_state = "defeat"


def draw():
    if game_state == "menu":
        draw_menu()
    if game_state == "playing":
        screen.clear()
        hero.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet in bullets:
            bullet[0].draw()
    if game_state == "defeat":
        draw_end_screen("Derrota")


def update():
    if game_state == "playing":
        hero.animate()
        hero.move(
            keyboard,
            (TILE_SIZE, WIDTH - TILE_SIZE, TILE_SIZE, HEIGHT - TILE_SIZE),
            TILE_SIZE,
        )
        for enemy in enemies:
            if isinstance(enemy, Orc):
                enemy.attack(hero)
            elif isinstance(enemy, Shooter):
                enemy.attack(hero, bullets, clock)
            enemy.animate()
        update_bullets()
        check_collisions()
