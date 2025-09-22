import pygame
import sys
from transition import FadeTransition, SlideTransition, CircleWipeTransition
from scene_manage import SceneManager
from scene import Scene


class MainMenuScene(Scene):
    def __init__(self):
        super().__init__("MainMenu")
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render("Main Menu - Press SPACE to Start", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(400, 300))

    def handle_events(self, events: list[pygame.event.Event]) -> str | None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return "GameScene"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "SettingMenu"
        return None

    def update(self, dt: float) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        screen.fill((50, 50, 100))
        screen.blit(self.text, self.text_rect)

class SettingMenuScene(Scene):
    def __init__(self):
        super().__init__("SettingMenu")
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render("Setting Menu - Press SPACE to Start", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(400, 300))

    def handle_events(self, events: list[pygame.event.Event]) -> str | None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "MainMenu"
        return None

    def update(self, dt: float) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        screen.fill((80, 150, 100))
        screen.blit(self.text, self.text_rect)

class GameScene(Scene):
    def __init__(self):
        super().__init__("GameScene")
        self.font = pygame.font.Font(None, 36)
        self.player_pos = [400, 300]
        self.player_speed = 300

    def handle_events(self, events: list[pygame.event.Event]) -> str | None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "MainMenu"
        return None

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_pos[0] -= self.player_speed * dt
        if keys[pygame.K_d]:
            self.player_pos[0] += self.player_speed * dt
        if keys[pygame.K_w]:
            self.player_pos[1] -= self.player_speed * dt
        if keys[pygame.K_s]:
            self.player_pos[1] += self.player_speed * dt

        self.player_pos[0] = max(25, min(800 - 25, self.player_pos[0]))
        self.player_pos[1] = max(25, min(600 - 25, self.player_pos[1]))

    def render(self, screen: pygame.Surface) -> None:
        screen.fill((100, 150, 50))
        pygame.draw.circle(screen, (255, 0, 0), (int(self.player_pos[0]), int(self.player_pos[1])), 25)
        instructions = self.font.render("Use Arrow Keys to Move. ESC to return to Menu.", True, (0, 0, 0))
        screen.blit(instructions, (50, 50))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Scene Manager Example")

    manager = SceneManager(screen)
    manager.add_scene("MainMenu", MainMenuScene())
    manager.add_scene("GameScene", GameScene())
    manager.add_scene("SettingMenu", SettingMenuScene())

    manager.register_default_transition(lambda: FadeTransition(0.8))
    manager.register_transition("MainMenu", "GameScene", lambda: SlideTransition(1.0))
    manager.register_transition("GameScene", "MainMenu", lambda: CircleWipeTransition(1.2))

    manager.run("MainMenu")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
