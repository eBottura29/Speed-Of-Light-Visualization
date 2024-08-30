# The idea of this simulation is to visualize how it would look like to pass the speed of light (example: you're in a space ship and you are observing a particle spinning)
# Moving faster than the speed of light is impossible in real life, since moving at the speed of light requires literally infinite energy, and you cant get more than infinite energy, actually, not even infinite energy is possible...

import pygame
from pg_utils import *

# Vector2 Setup
vector2 = Vector2()
vector2.init_vectors()

# Vector3 Setup
vector3 = Vector3()
vector3.init_vectors()

# Colors Setup
colors = Color()
colors.init_colors()

# PyGame Setup
pygame.init()

SCREEN = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN if FULLSCREEN else 0)
pygame.display.set_caption(WINDOW_NAME)
# pygame.display.set_icon(pygame.image.load(ICON_LOCATION))  # Uncomment if you have an icon

clock = pygame.time.Clock()
delta_time = 0.0

arial = pygame.font.SysFont("Arial", 32)

# C = speed of light
c = 10
threshold = 0.01

scale = 100 / 1


def sign(num):
    if abs(num) != num:
        return -1
    elif num == 0:
        return 0
    else:
        return 1


class Particle:
    def __init__(self, position, radius, mass, color):
        self.position = position
        self.radius = radius
        self.mass = mass
        self.color = color
        self.time_velocity = c
        self.t = 0
        self.angular_velocity = 0
        self.angle = 0
        self.distance = 200
        self.kinetic_energy = 0

    def update(self):
        self.angle += self.angular_velocity * delta_time

        self.spatial_speed = self.angular_velocity * self.distance

        if self.angular_velocity < c:
            self.time_velocity = math.sqrt(c**2 - self.angular_velocity**2)
        elif self.angular_velocity > c:
            self.time_velocity = -math.sqrt(self.angular_velocity**2 - c**2)
        else:
            self.time_velocity = 0

        self.t += self.time_velocity * delta_time

        self.position.x = (
            math.cos(self.angle * sign(self.time_velocity)) * self.distance
        )
        self.position.y = (
            math.sin(self.angle * sign(self.time_velocity)) * self.distance
        )

        self.velocity_meters_per_second = self.angular_velocity / scale
        self.c_meter_per_second = c / scale

        v = self.velocity_meters_per_second
        if v >= self.c_meter_per_second:
            self.kinetic_energy = float("inf")
        else:
            gamma = 1 / math.sqrt(1 - (v**2 / self.c_meter_per_second**2))
            self.kinetic_energy = (gamma - 1) * self.mass * self.c_meter_per_second**2

    def draw(self):
        screen_pos = (
            int(self.position.x + WIDTH // 2),
            int(self.position.y + HEIGHT // 2),
        )
        pygame.draw.circle(SCREEN, self.color.get_tup(), screen_pos, self.radius)


def main():
    global delta_time

    running = True
    get_ticks_last_frame = 0.0

    test_particle = Particle(Vector2(0, 0), 10, 1, colors.WHITE)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        SCREEN.fill(colors.BLACK.get_tup())

        test_particle.angular_velocity += delta_time / 2

        test_particle.update()
        test_particle.draw()

        t_time_velocity = Text(
            f"Time Vel: {test_particle.time_velocity:.2f}",
            arial,
            colors.WHITE.get_tup(),
            (WIDTH // 2, 48),
        )
        t_time_velocity.draw(SCREEN, t_time_velocity.center)

        t_time = Text(
            f"Time Elapsed: {test_particle.t:.2f}",
            arial,
            colors.WHITE.get_tup(),
            (WIDTH // 2, 48 * 2),
        )
        t_time.draw(SCREEN, t_time.center)

        t_velocity = Text(
            f"Velocity: {test_particle.angular_velocity:.2f} p/s",
            arial,
            colors.WHITE.get_tup(),
            (WIDTH // 2, 48 * 3),
        )
        t_velocity.draw(SCREEN, t_velocity.center)

        t_c_percent = Text(
            f"Speed of Light: {round((test_particle.angular_velocity/c)*100)}%",
            arial,
            colors.WHITE.get_tup(),
            (WIDTH // 2, 48 * 4),
        )
        t_c_percent.draw(SCREEN, t_c_percent.center)

        t_kinetic_energy = Text(
            f"Kinetic Energy: {test_particle.kinetic_energy:.2f} J",
            arial,
            colors.WHITE.get_tup(),
            (WIDTH // 2, 48 * 5),
        )
        t_kinetic_energy.draw(SCREEN, t_kinetic_energy.center)

        t_energy = Text(
            f"Energy: {test_particle.mass * (c**2):.2f} N",
            arial,
            colors.WHITE.get_tup(),
            (WIDTH // 2, 48 * 6),
        )
        t_energy.draw(SCREEN, t_energy.center)

        pygame.display.flip()

        get_ticks_last_frame, delta_time = manage_frame_rate(
            clock, get_ticks_last_frame
        )

    pygame.quit()


if __name__ == "__main__":
    main()
