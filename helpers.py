import pygame

COLOUR_INACTIVE = pygame.Color('lightskyblue3')
COLOUR_ACTIVE = pygame.Color('dodgerblue2')


class InputTextBox:
    def __init__(self, x, y, w, h, title, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.border_color = COLOUR_INACTIVE
        self.border_width = 2
        self._font_title = pygame.font.Font(None, int(h*1.2))
        self._font_text = pygame.font.Font(None, h)
        self.title = self._font_title.render(title, True, "white")
        self.text = text
        self.txt_surface = self._font_text.render(text, True, self.border_color)

        self.border_rect = pygame.Rect(x, y, w, h)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True

            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    self.text += event.unicode

                self.txt_surface = self._font_text.render(self.text, True, "black")

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        if self.active:
            self.border_color = COLOUR_ACTIVE
            self.border_rect = pygame.Rect(
                self.rect.x - 1,
                self.rect.y - 1,
                self.rect.w + 2,
                self.rect.h + 2
            )
        else:
            self.border_color = COLOUR_INACTIVE
            self.border_rect = self.rect

    def draw(self, screen):
        screen.fill("white", self.rect)
        screen.blit(self.txt_surface, (self.rect.x+3, self.rect.y+4))
        screen.blit(self.title, (self.rect.x-self.title.get_width()-10, self.rect.y+5))
        pygame.draw.rect(screen, self.border_color, self.border_rect, self.border_width)


class TextBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


class Graph:
    def __init__(self):
        pass

def draw_arrow(screen, points, double_ended=False, color="white"):
    pygame.draw.lines(screen, color, True, points=points)


    pygame.draw.line(screen, color, points[1], (points[1], 880))
    pygame.draw.line(screen, color, points[1], (1490, 860))

    if double_ended:
        pygame.draw.line(screen, color, points[0], (1490, 880))
        pygame.draw.line(screen, color, points[0], (1490, 860))