from abc import ABC, abstractmethod
import pygame
import math

class Transition(ABC):
    """抽象过渡效果基类。"""
    
    def __init__(self, duration: float):
        self.duration = duration
        self.elapsed_time = 0.0
        self.is_complete = False

    @abstractmethod
    def update(self, dt: float) -> None:
        """更新过渡效果。
        
        参数:
            dt: 时间增量。
        """
        self.elapsed_time += dt
        if self.elapsed_time >= self.duration:
            self.is_complete = True

    @abstractmethod
    def render(self, screen: pygame.Surface, old_scene_surface: pygame.Surface, new_scene_surface: pygame.Surface) -> None:
        """渲染过渡效果。
        
        参数:
            screen: 主屏幕表面。
            old_scene_surface: 旧场景的渲染表面。
            new_scene_surface: 新场景的渲染表面。
        """
        pass

class FadeTransition(Transition):
    """淡入淡出过渡效果。"""

    def __init__(self, duration: float):
        super().__init__(duration)
        self.fade_surface = pygame.Surface((800, 600))
        self.fade_surface.fill((0, 0, 0))

    def update(self, dt: float) -> None:
        super().update(dt)

    def render(self, screen: pygame.Surface, old_scene_surface: pygame.Surface, new_scene_surface: pygame.Surface) -> None:
        progress = min(self.elapsed_time / self.duration, 1.0)

        if progress < 0.5:
            alpha = int((progress / 0.5) * 255)
            screen.blit(old_scene_surface, (0, 0))
            self.fade_surface.set_alpha(alpha)
            screen.blit(self.fade_surface, (0, 0))
        else:
            alpha = int(((1.0 - progress) / 0.5) * 255)
            screen.blit(new_scene_surface, (0, 0))
            self.fade_surface.set_alpha(alpha)
            screen.blit(self.fade_surface, (0, 0))

class SlideTransition(Transition):
    """滑动过渡效果。"""
    def __init__(self, duration: float):
        super().__init__(duration)

    def update(self, dt: float) -> None:
        super().update(dt)

    def render(self, screen: pygame.Surface, old_scene_surface: pygame.Surface, new_scene_surface: pygame.Surface) -> None:
        progress = self.elapsed_time / self.duration
        width = screen.get_width()

        old_x = -progress * width
        new_x = width - progress * width

        screen.blit(old_scene_surface, (old_x, 0))
        screen.blit(new_scene_surface, (new_x, 0))

class CircleWipeTransition(Transition):
    """圆形擦除过渡效果。"""
    def __init__(self, duration: float):
        super().__init__(duration)

    def update(self, dt: float) -> None:
        super().update(dt)

    def render(self, screen: pygame.Surface, old_scene_surface: pygame.Surface, new_scene_surface: pygame.Surface) -> None:
        progress = self.elapsed_time / self.duration
        width, height = screen.get_size()
        center = (width // 2, height // 2)

        max_radius = math.sqrt(center[0]**2 + center[1]**2)
        radius = progress * max_radius
        screen.blit(new_scene_surface, (0, 0))
        temp_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        temp_surf.blit(old_scene_surface, (0, 0))
        cover = pygame.Surface((width, height), pygame.SRCALPHA)
        cover.fill((255, 255, 255, 255))
        pygame.draw.circle(cover, (255, 255, 255, 0), center, radius)
        temp_surf.blit(cover, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(temp_surf, (0, 0))