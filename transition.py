from abc import ABC, abstractmethod
import pygame

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