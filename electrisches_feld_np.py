# password: 31693169

import pygame
import numpy as np

pygame.init()

RED = (255, 0, 0)
GREY = (100, 100, 100)
BLUE = (0, 0, 255)
LIGHT_GREY = (128, 128, 128)
DARK_GREY = (20, 20, 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont('Comic Sans Ms', 15)


class Particle:
    def __init__(self, x, y, charge=0):
        self.x = x
        self.y = y
        self.charge = charge

    def show(self, screen):
        if self.charge < 0:
            pygame.draw.circle(screen, RED, (self.x, self.y), 20)
        elif self.charge > 0:
            pygame.draw.circle(screen, BLUE, (self.x, self.y), 20)
        else:
            pygame.draw.circle(screen, GREY, (self.x, self.y), 20)
        if self.charge > 0:
            text = FONT.render('+' + str(self.charge), True, WHITE)
        else:
            text = FONT.render(str(self.charge), True, WHITE)
        screen.blit(text, (self.x - text.get_width() / 2, self.y - text.get_height() / 2))

    def move(self, pos):
        self.x = pos[0]
        self.y = pos[1]


class Field:
    def __init__(self, screen: pygame.Surface, particles, vector_spacing=20):
        self.screen = screen
        self.raw_field = np.zeros((screen.get_height(), screen.get_width, 2))
        self.vector_spacing = vector_spacing
        self.particles = particles

    def compute(self, particles):
        h = self.screen.get_height()
        w = self.screen.get_width()
        if self.raw_field.shape != (h, w, 2):
            # Regenerate field
            self.raw_field = np.zeros((h, w, 2))
        x_f = np.array([list(range(w)) for _ in range(h)])
        y_f = np.array([[y for _ in range(w)] for y in range(h)])
        for particle in particles:
            dx = x_f - particle.x
            dy = y_f - particle.y
            # dists =

    def show_vectors(self, screen: pygame.Surface, particles):
        h = screen.get_height()
        w = screen.get_width()
        row = h // self.vector_spacing
        col = w // self.vector_spacing
        vertical_shift = (h / 2) % self.vector_spacing - self.vector_spacing // 2
        horizontal_shift = (w / 2) % self.vector_spacing - self.vector_spacing // 2
        for i in range(row + 1):
            y = vertical_shift + i * self.vector_spacing
            for j in range(col + 1):
                x = horizontal_shift + j * self.vector_spacing
                vector = calc_vector(x, y, particles)
                pygame.draw.line(screen, GREY, (x, y), (x + vector[0], y + vector[1]))
                length = (vector[0] * vector[0] + vector[1] * vector[1]) ** 0.5
                if length != 0:
                    x_unit = vector[0] * 5 / length
                    y_unit = vector[1] * 5 / length
                    pygame.draw.line(screen, GREY,
                                     (x + vector[0], y + vector[1]),
                                     (x + vector[0] - x_unit - y_unit, y + vector[1] - y_unit + x_unit)
                                     )
                    pygame.draw.line(screen, GREY,
                                     (x + vector[0], y + vector[1]),
                                     (x + vector[0] - x_unit + y_unit, y + vector[1] - y_unit - x_unit)
                                     )

    def show_vectors_with_color(self, screen: pygame.Surface, particles):
        h = screen.get_height()
        w = screen.get_width()
        row = h // self.vector_spacing
        col = w // self.vector_spacing
        vertical_shift = (h / 2) % self.vector_spacing - self.vector_spacing // 2
        horizontal_shift = (w / 2) % self.vector_spacing - self.vector_spacing // 2
        for i in range(row + 1):
            y = vertical_shift + i * self.vector_spacing
            for j in range(col + 1):
                x = horizontal_shift + j * self.vector_spacing
                vector = calc_vector(x, y, particles)
                length = (vector[0] * vector[0] + vector[1] * vector[1]) ** 0.5
                if length != 0:
                    x_unit = vector[0] * 5 / length
                    y_unit = vector[1] * 5 / length
                    color = (min(255, int(length * 5)), max(0, int(127 - length * 5)), 0)
                    pygame.draw.line(screen, color, (x, y), (x + 3 * x_unit, y + 3 * y_unit))
                    pygame.draw.line(screen, color,
                                     (x + 3 * x_unit, y + 3 * y_unit),
                                     (x + 2 * x_unit - y_unit, y + 2 * y_unit + x_unit)
                                     )
                    pygame.draw.line(screen, color,
                                     (x + 3 * x_unit, y + 3 * y_unit),
                                     (x + 2 * x_unit + y_unit, y + 2 * y_unit - x_unit)
                                     )


class UpperBar:
    def __init__(self, screen: pygame.Surface, height=30):
        self.height = height
        self.screen = screen
        self.items = []
        self.borders = []

    def add_items(self, *items):
        self.items += items

    def set_borders(self):
        pass

    def show(self):
        pygame.draw.rect(self.screen, GREY, (0, 0, self.screen.get_width(), self.height))
        x = 2
        for text in self.items:
            text_surface = FONT.render(text, True, WHITE)
            w = text_surface.get_width()
            pygame.draw.rect(self.screen, DARK_GREY, (x, 2, w + 4, self.height - 4))
            pygame.draw.rect(self.screen, LIGHT_GREY, (x + 1, 3, w + 2, self.height - 6))
            self.screen.blit(text_surface, (x + 1, 3))
            x += w + 6

    def get_clicked(self, mouse_pos):
        pass


def calc_vector(x, y, particles):
    total_x = 0
    total_y = 0
    for particle in particles:
        dx = x - particle.x
        dy = y - particle.y
        dist = (dx * dx + dy * dy) ** 0.5
        if dist < 20:
            return [0, 0]
        else:
            dist *= 0.25 / particle.charge
            dx /= dist
            dy /= dist
            factor = 1 / (dist * dist + 1.5)
        dx *= factor
        dy *= factor
        total_x += dx
        total_y += dy
    return [total_x, total_y]


stick_list = []


def add_stick(x, y, charge):
    for i in range(y, y + 20):
        new_particle = Particle(x, y + (10 * i), charge)
        stick_list.append(new_particle)
        i += 5


def main():
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

    field = Field(15)
    add_stick(100, 30, 5)
    add_stick(400, 30, -5)
    particles = [Particle(700, 300, 20), Particle(600, 150, 20), Particle(700, 150, -20)]
    particles += stick_list
    upper_bar = UpperBar(screen)
    upper_bar.add_items('text', 'text2', 'text3')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = upper_bar.get_clicked(pygame.mouse.get_pos())
        screen.fill(BLACK)
        # field.show_vectors(screen, particles)
        field.show_vectors_with_color(screen, particles)
        particles[0].move(pygame.mouse.get_pos())
        for particle in particles:
            particle.show(screen)
        upper_bar.show()
        pygame.display.update()


if __name__ == '__main__':
    main()
