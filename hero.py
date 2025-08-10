from pgzero.actor import Actor


class Hero:
    def __init__(self, pos, speed=1.0, frame_speed=0.15):
        self.actor = Actor("d_hero_idle0", pos)
        self.speed = speed

        # Atributos para animação do personagem
        self.anim_speed = frame_speed
        self.current_frame = 0
        self.current_anim = "idle"
        self.last_anim = self.current_anim
        self.animation_frames = {
            "idle": ["d_hero_idle0", "d_hero_idle1", "d_hero_idle2", "d_hero_idle3"],
            "down_walk": [
                "d_hero_walk0",
                "d_hero_walk1",
                "d_hero_walk2",
                "d_hero_walk3",
                "d_hero_walk4",
                "d_hero_walk5",
            ],
            "left_walk": [
                "l_hero_walk0",
                "l_hero_walk1",
                "l_hero_walk2",
                "l_hero_walk3",
                "l_hero_walk4",
                "l_hero_walk5",
            ],
            "right_walk": [
                "r_hero_walk0",
                "r_hero_walk1",
                "r_hero_walk2",
                "r_hero_walk3",
                "r_hero_walk4",
                "r_hero_walk5",
            ],
            "up_walk": [
                "u_hero_walk0",
                "u_hero_walk1",
                "u_hero_walk2",
                "u_hero_walk3",
                "u_hero_walk4",
                "u_hero_walk5",
            ],
        }

    def move(self, keyboard, wall_limit, tile_size):
        future_x, future_y = self.actor.x, self.actor.y

        # Cada sala só possui as paredes externas
        # Então o limite pode ser calculado dessa forma
        wall_left = wall_limit[0]
        wall_right = wall_limit[1]
        wall_top = wall_limit[2]
        wall_bottom = wall_limit[3]

        # Sempre assume que o personagem está parado inicialmente
        self.current_anim = "idle"

        # Calcula a posição futura do personagem
        if keyboard.left:
            self.current_anim = "left_walk"
            future_x = self.actor.x - self.speed
        elif keyboard.right:
            self.current_anim = "right_walk"
            future_x = self.actor.x + self.speed
        elif keyboard.down:
            future_y = self.actor.y + self.speed
            self.current_anim = "down_walk"
        elif keyboard.up:
            self.current_anim = "up_walk"
            future_y = self.actor.y - self.speed

        # Necessário adicionar/subtrair a metade do tamanho do personagem
        # na conta já que seu ponto de ancoragem é o centro
        half_hero_size = tile_size // 2
        left_limit = wall_left + half_hero_size
        right_limit = wall_right - half_hero_size
        top_limit = wall_top + half_hero_size
        bottom_limit = wall_bottom - half_hero_size

        # Caso seja uma posição válida, se move até lá
        if future_x > left_limit and future_x < right_limit:
            self.actor.x = future_x
        if future_y > top_limit and future_y < bottom_limit:
            self.actor.y = future_y

    def animate(self):
        # Reseta o contador de frames quando a animação troca
        if self.last_anim != self.current_anim:
            self.current_frame = 0
            self.last_anim = self.current_anim

        # Executa a animação atual
        frames = self.animation_frames[self.current_anim]
        self.current_frame += self.anim_speed
        if self.current_frame >= len(frames):
            self.current_frame = 0
        self.actor.image = frames[int(self.current_frame)]

    def draw(self):
        self.actor.draw()
