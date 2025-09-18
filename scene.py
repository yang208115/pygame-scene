import pygame
from abc import ABC, abstractmethod

class Scene(ABC):
    """抽象场景基类，定义了所有场景必须实现的接口。"""
    
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> str | None:
        """处理用户输入和系统事件。
        
        参数:
            events: Pygame事件列表。
            
        返回:
            如果场景需要切换，返回目标场景的名称；否则返回None。
        """
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """更新场景逻辑和状态。
        
        参数:
            dt: 自上一帧以来的时间增量（秒）。
        """
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """将场景内容渲染到屏幕上。
        
        参数:
            screen: 主显示表面。
        """
        pass

    def on_enter(self, screen: pygame.Surface) -> None:
        """场景被激活时调用，用于初始化。"""
        pass

    def on_exit(self) -> None:
        """场景被切换出去时调用，用于清理。"""
        pass