import math
from pgzero.actor import Actor


class Orc:
    def __init__(self, pos, speed=0.7, frame_speed=0.15):
        self.actor = Actor("d_orc_walk0", pos)
        self.speed = speed

        # Atributos para animação
        self.anim_speed = frame_speed
        self.current_frame = 0
        self.current_anim = "down_walk"
        self.animation_frames = {
            "down_walk": [
                "d_orc_walk0",
                "d_orc_walk1",
                "d_orc_walk2",
                "d_orc_walk3",
                "d_orc_walk4",
                "d_orc_walk5",
            ]
        }

    def attack(self, hero):
        # Lógica pro inimigo perseguir o heroi
        dx = hero.actor.x - self.actor.x
        dy = hero.actor.y - self.actor.y
        dist = math.hypot(dx, dy)

        if dist > 0:
            dx /= dist
            dy /= dist
            self.actor.x += dx * self.speed
            self.actor.y += dy * self.speed

    def animate(self):
        # Executa a animação atual
        frames = self.animation_frames[self.current_anim]
        self.current_frame += self.anim_speed
        if self.current_frame >= len(frames):
            self.current_frame = 0
        self.actor.image = frames[int(self.current_frame)]

    def draw(self):
        self.actor.draw()


class Shooter:
    def __init__(
        self, pos, speed=0.7, bullet_speed=1, attack_cooldown=0.5, frame_speed=0.15
    ):
        self.actor = Actor("d_shooter_attack0", pos)
        self.speed = speed
        self.bullet_speed = bullet_speed
        self.attack_cooldown = attack_cooldown
        self.can_attack = True

        # Atributos para animação
        self.anim_speed = frame_speed
        self.current_frame = 0
        self.current_anim = "down_attack"
        self.last_anim = self.current_anim
        self.animation_frames = {
            "down_attack": [
                "d_shooter_attack0",
                "d_shooter_attack1",
                "d_shooter_attack2",
            ],
            "left_attack": [
                "l_shooter_attack0",
                "l_shooter_attack1",
                "l_shooter_attack2",
            ],
            "right_attack": [
                "r_shooter_attack0",
                "r_shooter_attack1",
                "r_shooter_attack2",
            ],
            "up_attack": [
                "u_shooter_attack0",
                "u_shooter_attack1",
                "u_shooter_attack2",
            ],
        }

    def attack(self, hero, bullets, clock):
        if not self.can_attack:
            return

        # Determina o ângulo em relação ao heroi
        angle_to_hero = self.actor.angle_to(hero.actor)

        # Normaliza os valores de angulo para serem entre 0-360
        if angle_to_hero < 0:
            angle_to_hero += 360

        # Determina qual lado atirar baseado no ângulo com o herói
        self.current_anim = "down_attack"

        if angle_to_hero >= 315 or angle_to_hero < 45:  # Direita
            self.current_anim = "right_attack"
            bullets.append((Actor("fireball", self.actor.pos), "x", self.bullet_speed))
        elif angle_to_hero >= 45 and angle_to_hero < 135:  # Cima
            self.current_anim = "up_attack"
            bullets.append((Actor("fireball", self.actor.pos), "y", -self.bullet_speed))
        elif angle_to_hero > 135 and angle_to_hero < 225:  # Esquerda
            self.current_anim = "left_attack"
            bullets.append((Actor("fireball", self.actor.pos), "x", -self.bullet_speed))
        else:  # Baixo
            self.current_anim = "down_attack"
            bullets.append((Actor("fireball", self.actor.pos), "y", self.bullet_speed))

        self.can_attack = False
        clock.schedule(self.reset_attack, self.attack_cooldown)

    def reset_attack(self):
        self.can_attack = True

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
