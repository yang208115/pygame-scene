import pygame
from scene import Scene
from transition import Transition
from typing import Callable

class SceneManager:
    """场景管理器，负责协调场景的切换和生命周期。"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.scenes: dict[str, Scene] = {}
        self.transition_map: dict[tuple[str, str], Callable[[], Transition]] = {}
        self.current_scene: Scene | None = None
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.in_transition = False
        self.transition: Transition | None = None
        self.next_scene_name: str | None = None
        self.old_scene_surface = pygame.Surface(screen.get_size())
        self.new_scene_surface = pygame.Surface(screen.get_size())
        self.default_transition: Callable[[], Transition] | None = None

    def add_scene(self, name: str, scene: Scene) -> None:
        """注册一个场景到管理器中。

        参数:
            name: 场景的唯一名称。
            scene: 场景实例。
        """
        self.scenes[name] = scene

    def switch_scene(self, name: str) -> None:
        """切换到指定名称的场景。

        参数:
            name: 目标场景的名称。

        抛出:
            ValueError: 如果目标场景未注册。
        """
        if name not in self.scenes:
            raise ValueError(f"Scene '{name}' not found.")

        if self.current_scene:
            self.current_scene.on_exit()

        self.current_scene = self.scenes[name]
        self.current_scene.on_enter(self.screen)

    def run(self, initial_scene: str) -> None:
        """启动游戏主循环，支持过渡效果。"""
        self.switch_scene(initial_scene)

        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            if self.in_transition and self.transition:
                self.transition.update(dt)
                self.transition.render(self.screen, self.old_scene_surface, self.new_scene_surface)
                if self.transition.is_complete:
                    if self.current_scene:
                        self.current_scene.on_exit()
                    self.current_scene = self.scenes[self.next_scene_name]
                    self.in_transition = False
                    self.transition = None
            else:
                if self.current_scene:
                    next_scene = self.current_scene.handle_events(events)
                    if next_scene:
                        key = (self.current_scene.name, next_scene)
                        transition_factory = self.transition_map.get(key) or self.default_transition
                        if transition_factory:
                            self.switch_scene_with_transition(next_scene, transition_factory)
                        else:
                            self.switch_scene(next_scene)
                    else:
                        self.current_scene.update(dt)
                        self.current_scene.render(self.screen)

            pygame.display.flip()

    def switch_scene_with_transition(self, name: str, transition_factory: Callable[[], Transition]) -> None:
        if name not in self.scenes:
            raise ValueError(f"Scene '{name}' not found.")

        self.old_scene_surface = pygame.Surface(self.screen.get_size())
        if self.current_scene:
            self.current_scene.render(self.old_scene_surface)

        next_scene = self.scenes[name]
        next_scene.on_enter(self.screen)
        next_scene.update(0)
        self.new_scene_surface = pygame.Surface(self.screen.get_size())
        next_scene.render(self.new_scene_surface)

        self.transition = transition_factory()
        self.in_transition = True
        self.next_scene_name = name

    def register_transition(self, from_scene: str, to_scene: str, factory: Callable[[], Transition]):
        """注册从 from_scene 切换到 to_scene 时使用的过渡效果"""
        self.transition_map[(from_scene, to_scene)] = factory

    def register_default_transition(self, factory: Callable[[], Transition]):
        """注册一个默认的过渡效果，用于所有未指定过渡的场景切换。"""
        self.default_transition = factory
