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
        self.vector_spacing = vector_spacing
        self.particles = particles

    def compute(self, particles):
        h = self.screen.get_height()
        w = self.screen.get_width()
        self.raw_field = np.zeros((w, h, 2))
        y_f = np.array([list(range(h)) for _ in range(w)])
        x_f = np.array([[x for _ in range(h)] for x in range(w)])
        for particle in particles:
            dx = x_f - particle.x
            dy = y_f - particle.y
            dir_field = np.stack([dx, dy], axis=-1)
            dist_squared = (dx * dx) + (dy * dy)
            dist_squared_field = np.stack([dist_squared, dist_squared], axis=-1)
            dist_root = np.sqrt(dist_squared)
            norm_divider = np.stack([dist_root, dist_root], axis=-1)
            norm_field = dir_field / norm_divider
            force = (4 * particle.charge) / (dist_squared_field + 1.5)
            intensities_normal = (4 * particle.charge) / (dist_squared + 1.5)
            force = np.stack([intensities_normal, intensities_normal], axis=-1)
            self.intensities = np.abs(intensities_normal)
            force_field = norm_field * force
            self.raw_field += force_field

    def show_vectors(self, screen: pygame.Surface, particles):
        h = screen.get_height()
        w = screen.get_width()
        row = h // self.vector_spacing
        col = w // self.vector_spacing
        vertical_shift = (h / 2) % self.vector_spacing - self.vector_spacing // 2
        horizontal_shift = (w / 2) % self.vector_spacing - self.vector_spacing // 2
        self.compute(particles)
        for i in range(row + 1):
            y = vertical_shift + i * self.vector_spacing
            for j in range(col + 1):
                x = horizontal_shift + j * self.vector_spacing
                vector_x = self.raw_field[int(x), int(y), 0]
                vector_y = self.raw_field[int(x), int(y), 1]
                pygame.draw.line(screen, GREY, (x, y), (x + vector_x, y + vector_y))
                length = self.intensities[int(x)][int(y)]
                if length != 0:
                    x_unit = vector_x * 5 / length
                    y_unit = vector_y * 5 / length
                    pygame.draw.line(screen, GREY,
                                     (x + vector_x, y + vector_y),
                                     (x + vector_x - x_unit - y_unit, y + vector_y - y_unit + x_unit)
                                     )
                    pygame.draw.line(screen, GREY,
                                     (x + vector_x, y + vector_y),
                                     (x + vector_x - x_unit + y_unit, y + vector_y - y_unit - x_unit)
                                     )

    def show_vectors_with_color(self, screen: pygame.Surface, particles):
        h = screen.get_height()
        w = screen.get_width()
        row = h // self.vector_spacing
        col = w // self.vector_spacing
        vertical_shift = (h / 2) % self.vector_spacing - self.vector_spacing // 2
        horizontal_shift = (w / 2) % self.vector_spacing - self.vector_spacing // 2
        self.compute(particles)
        for i in range(row + 1):
            y = vertical_shift + i * self.vector_spacing
            for j in range(col + 1):
                x = horizontal_shift + j * self.vector_spacing
                vector_x = self.raw_field[int(x), int(y), 0]
                vector_y = self.raw_field[int(x), int(y), 1]
                length = self.intensities[int(x)][int(y)]
                print(length)
                if length != 0:
                    x_unit = vector_x * 5 / length
                    y_unit = vector_y * 5 / length
                    print(x_unit, y_unit)
                    color = (min(255, int(length * 5)), max(0, int(127 - length * 5)), 0)
                    #despaghettify
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


stick_list = []


def add_stick(x, y, charge):
    for i in range(y, y + 20):
        new_particle = Particle(x, y + (10 * i), charge)
        stick_list.append(new_particle)
        i += 5


def main():
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

    add_stick(100, 30, 5)
    add_stick(400, 30, -5)
    particles = [Particle(700, 300, 20), Particle(600, 150, 20), Particle(700, 150, -20)]
    particles += stick_list
    field = Field(screen, particles, vector_spacing=15)
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
