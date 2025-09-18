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
        self.switch_scene(initial_scene)  # 初始化并切换到初始场景

        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0  # 控制帧率，获取每帧耗时（秒）

            events = pygame.event.get()  # 获取所有事件
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False  # 处理窗口关闭事件，终止主循环

            # ----- 过渡状态 -----
            if self.in_transition and self.transition:
                self.transition.update(dt)  # 更新过渡动画状态
                self.transition.render(self.screen, self.old_scene_surface, self.new_scene_surface)  # 渲染过渡效果
                if self.transition.is_complete:
                    # 真正完成场景切换
                    if self.current_scene:
                        self.current_scene.on_exit()  # 退出当前场景
                    self.current_scene = self.scenes[self.next_scene_name]  # 切换到新场景
                    self.in_transition = False  # 结束过渡状态
                    self.transition = None      # 清除过渡对象
            # ----- 正常运行 -----
            else:
                if self.current_scene:
                    next_scene = self.current_scene.handle_events(events)  # 处理当前场景事件，返回下一个场景名（如有）
                    if next_scene:
                        key = (self.current_scene.name, next_scene)
                        if key in self.transition_map:
                            # 如果有注册过渡效果，则使用过渡切换
                            self.switch_scene_with_transition(next_scene, self.transition_map[key])
                        else:
                            # 否则直接切换场景
                            self.switch_scene(next_scene)
                    else:
                        self.current_scene.update(dt)      # 更新当前场景逻辑
                        self.current_scene.render(self.screen)  # 渲染当前场景

            pygame.display.flip()  # 刷新屏幕显示

    def switch_scene_with_transition(self, name: str, transition_factory: Callable[[], Transition]) -> None:
        if name not in self.scenes:
            raise ValueError(f"Scene '{name}' not found.")

        # 保存当前场景图像
        self.old_scene_surface = pygame.Surface(self.screen.get_size())
        if self.current_scene:
            self.current_scene.render(self.old_scene_surface)  # 渲染当前场景到 old_scene_surface

        # 初始化新场景并渲染一帧
        next_scene = self.scenes[name]
        next_scene.on_enter(self.screen)  # 初始化新场景
        next_scene.update(0)              # 更新新场景（dt=0）
        self.new_scene_surface = pygame.Surface(self.screen.get_size())
        next_scene.render(self.new_scene_surface)  # 渲染新场景到 new_scene_surface

        # 启动过渡
        self.transition = transition_factory()  # 创建过渡对象
        self.in_transition = True               # 标记进入过渡状态
        self.next_scene_name = name             # 记录下一个场景名

    def register_transition(self, from_scene: str, to_scene: str, factory: Callable[[], Transition]):
        """注册从 from_scene 切换到 to_scene 时使用的过渡效果"""
        self.transition_map[(from_scene, to_scene)] = factory