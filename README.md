# 🎮 Pygame Scene Manager

一个**轻量级、模块化**的 Pygame 场景管理框架，专为游戏开发者设计，支持**场景切换生命周期管理**与**平滑过渡动画**。适用于菜单、关卡、设置页等多种游戏场景。

---

## ✨ 特性

- 🧩 **模块化架构**：基于抽象基类设计，易于扩展
- 🎞️ **过渡动画支持**：内置淡入淡出效果，支持自定义过渡
- 🧵 **非阻塞切换**：过渡期间不阻塞主循环
- 🧪 **易于调试**：清晰的场景生命周期钩子（`on_enter`, `on_exit`）
- 📦 **零依赖**：仅依赖 Pygame 本体

---

## 🚀 快速开始

### 安装依赖

```bash
pip install pygame
```

### 运行演示

```bash
python main.py
```

> 演示包含两个场景：主菜单 和 游戏场景，按空格键开始游戏，ESC 返回菜单。

---

## 📁 项目结构

```
pygame-scene-manager/
├── main.py              # 演示入口
├── scene.py             # 抽象场景基类
├── scene_manage.py      # 场景管理器
├── transition.py        # 抽象过渡基类
└── README.md
```

---

## 🧱 核心概念

### 1. 场景（Scene）

所有场景必须继承自 `Scene` 抽象类，并实现以下方法：

| 方法名         | 用途说明                         |
|----------------|----------------------------------|
| `handle_events`| 处理事件，返回目标场景名（可选）|
| `update`       | 更新逻辑                         |
| `render`       | 渲染画面                         |
| `on_enter`     | 场景被激活时调用（可选）         |
| `on_exit`      | 场景被切换时调用（可选）         |

#### 示例：主菜单场景

```python
class MainMenuScene(Scene):
    def __init__(self):
        super().__init__("MainMenu")
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render("Press SPACE to Start", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(400, 300))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return "GameScene"  # 切换到游戏场景
        return None

    def render(self, screen):
        screen.fill((50, 50, 100))
        screen.blit(self.text, self.text_rect)
```

---

### 2. 场景管理器（SceneManager）

负责注册场景、切换场景、管理过渡动画。

#### 注册场景

```python
manager = SceneManager(screen)
manager.add_scene("MainMenu", MainMenuScene())
manager.add_scene("GameScene", GameScene())
```

#### 注册过渡效果

```python
manager.register_transition("MainMenu", "GameScene", lambda: FadeTransition(1.0))
```

#### 启动游戏

```python
manager.run("MainMenu")
```

---

### 3. 过渡效果（Transition）

所有过渡效果必须继承自 `Transition` 抽象类。

#### 内置效果：淡入淡出（FadeTransition）

```python
class FadeTransition(Transition):
    def render(self, screen, old_surface, new_surface):
        progress = min(self.elapsed_time / self.duration, 1.0)
        if progress < 0.5:
            # 淡出旧场景
            alpha = int((progress / 0.5) * 255)
            screen.blit(old_surface, (0, 0))
            self.fade_surface.set_alpha(alpha)
            screen.blit(self.fade_surface, (0, 0))
        else:
            # 淡入新场景
            alpha = int(((1.0 - progress) / 0.5) * 255)
            screen.blit(new_surface, (0, 0))
            self.fade_surface.set_alpha(alpha)
            screen.blit(self.fade_surface, (0, 0))
```

---

## 🧪 扩展指南

### ✅ 自定义场景

```python
class SettingsScene(Scene):
    def __init__(self):
        super().__init__("Settings")
        # 初始化UI元素

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "MainMenu"
        return None

    def render(self, screen):
        screen.fill((30, 30, 30))
        # 绘制设置选项
```

### ✅ 自定义过渡效果

```python
class SlideTransition(Transition):
    def render(self, screen, old_surface, new_surface):
        progress = self.elapsed_time / self.duration
        offset = int(progress * 800)
        screen.blit(old_surface, (-offset, 0))
        screen.blit(new_surface, (800 - offset, 0))
```

---

## 🧑‍💻 开发者提示

- **场景名必须唯一**，用于切换与注册过渡
- **过渡工厂使用 lambda**：`lambda: YourTransition(1.0)`，避免提前实例化
- **生命周期钩子**适合用于：
  - `on_enter()`：加载资源、播放音乐、重置状态
  - `on_exit()`：保存数据、停止音效、释放资源

---

## 📄 开源协议

LGPL-3.0 License - 详见 [LICENSE](LICENSE)

---

## 🤝 贡献欢迎

欢迎提交 Issue 与 Pull Request，一起让这个项目更好！

---

## 🔗 相关链接

- [Pygame 官方文档](https://www.pygame.org/docs/)
- [Python 游戏开发社区](https://www.reddit.com/r/pygame/)
- [本项目 GitHub 仓库](https://github.com/your-username/pygame-scene-manager)

---

⭐ 如果这个项目对你有帮助，别忘了点个 **Star**！