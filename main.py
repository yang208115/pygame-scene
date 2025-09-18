import pygame
import sys


from scene_manage import SceneManager
from scene import Scene
from transition import Transition

class FadeTransition(Transition):
    """淡入淡出过渡效果。"""
    
    def __init__(self, duration: float):
        super().__init__(duration)  # 过渡时间
        self.fade_surface = pygame.Surface((800, 600)) # 假设屏幕大小
        self.fade_surface.fill((0, 0, 0))

    def update(self, dt: float) -> None:
        super().update(dt)

    def render(self, screen: pygame.Surface, old_scene_surface: pygame.Surface, new_scene_surface: pygame.Surface) -> None:
        progress = min(self.elapsed_time / self.duration, 1.0)
        
        # 淡出阶段 (0.0 to 0.5)
        if progress < 0.5:
            alpha = int((progress / 0.5) * 255)
            screen.blit(old_scene_surface, (0, 0))
            self.fade_surface.set_alpha(alpha)
            screen.blit(self.fade_surface, (0, 0))
        # 淡入阶段 (0.5 to 1.0)
        else:
            alpha = int(((1.0 - progress) / 0.5) * 255)
            screen.blit(new_scene_surface, (0, 0))
            self.fade_surface.set_alpha(alpha)
            screen.blit(self.fade_surface, (0, 0))

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
        return None

    def update(self, dt: float) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        screen.fill((50, 50, 100))
        screen.blit(self.text, self.text_rect)

class GameScene(Scene):
    def __init__(self):
        super().__init__("GameScene")
        self.font = pygame.font.Font(None, 36)
        self.player_pos = [400, 300]
        self.player_speed = 300 # 像素/秒

    def handle_events(self, events: list[pygame.event.Event]) -> str | None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "MainMenu"
        return None

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_pos[0] -= self.player_speed * dt
        if keys[pygame.K_RIGHT]:
            self.player_pos[0] += self.player_speed * dt
        if keys[pygame.K_UP]:
            self.player_pos[1] -= self.player_speed * dt
        if keys[pygame.K_DOWN]:
            self.player_pos[1] += self.player_speed * dt

        # 边界检查
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

    manager.register_transition("MainMenu", "GameScene", lambda: FadeTransition(1.0))
    manager.register_transition("GameScene", "MainMenu", lambda: FadeTransition(0.8))
    
    manager.run("MainMenu")
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()