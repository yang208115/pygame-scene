# 🎮 Pygame Scene Manager

A **lightweight, modular** Pygame scene management framework designed for game developers, supporting **scene switching lifecycle management** and **smooth transition animations**. Suitable for various game scenes like menus, levels, and settings pages.

[简体中文](README_CN.md)

---

## ✨ Features

- 🧩 **Modular Architecture**: Based on abstract base classes, easy to extend.
- 🎞️ **Transition Animation Support**: Built-in effects like fade, slide, and circle wipe, with support for custom transitions.
- 🚀 **Simplified Registration**: Set a default transition for all scenes and override specific ones as needed.
- 🧵 **Non-blocking Transitions**: The main loop is not blocked during transitions.
- 🧪 **Easy to Debug**: Clear scene lifecycle hooks (`on_enter`, `on_exit`).
- 📦 **Zero Dependencies**: Relies only on Pygame itself.

---

## 🚀 Quick Start

### Install Dependencies

```bash
pip install pygame
```

### Run the Demo

```bash
python main.py
```

> The demo includes three scenes: Main Menu, Game Scene and SettingMenu Scene. Press SPACE to start the game, ESC to return to the menu.

---

## 📁 Project Structure

```
pygame-scene-manager/
├── main.py              # Demo entry point
├── scene.py             # Abstract scene base class
├── scene_manage.py      # Scene manager
├── transition.py        # Abstract transition base class
└── README.md
```

---

## 🧱 Core Concepts

### 1. Scene

All scenes must inherit from the `Scene` abstract class and implement the following methods:

| Method          | Description                                         |
|-----------------|-----------------------------------------------------|
| `handle_events` | Handle events, return target scene name (optional)  |
| `update`        | Update logic                                        |
| `render`        | Render graphics                                     |
| `on_enter`      | Called when the scene is activated (optional)       |
| `on_exit`       | Called when the scene is switched out (optional)    |

#### Example: Main Menu Scene

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
                return "GameScene"  # Switch to the game scene
        return None

    def render(self, screen):
        screen.fill((50, 50, 100))
        screen.blit(self.text, self.text_rect)
```

---

### 2. SceneManager

Responsible for registering scenes, switching scenes, and managing transition animations.

#### Register Scenes

```python
manager = SceneManager(screen)
manager.add_scene("MainMenu", MainMenuScene())
manager.add_scene("GameScene", GameScene())
```

#### Register Transitions

You can set a default transition or register specific transitions between scenes.

```python
# Set a default transition
manager.register_default_transition(lambda: FadeTransition(0.8))

# Override with a specific transition
manager.register_transition("MainMenu", "GameScene", lambda: SlideTransition(1.0))
```

#### Start the Game

```python
manager.run("MainMenu")
```

---

### 3. Transition

All transitions must inherit from the `Transition` abstract class.

#### Built-in Effects

- **FadeTransition**: Fades the old scene out and the new scene in.
- **SlideTransition**: Slides the new scene in over the old one.
- **CircleWipeTransition**: Reveals the new scene with a circular wipe effect.

#### Example: Custom Slide Transition

```python
class SlideTransition(Transition):
    def render(self, screen, old_surface, new_surface):
        progress = self.elapsed_time / self.duration
        offset = int(progress * 800)
        screen.blit(old_surface, (-offset, 0))
        screen.blit(new_surface, (800 - offset, 0))
```

---

## 🧪 Extension Guide

### ✅ Custom Scene

```python
class SettingsScene(Scene):
    def __init__(self):
        super().__init__("Settings")
        # Initialize UI elements

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "MainMenu"
        return None

    def render(self, screen):
        screen.fill((30, 30, 30))
        # Draw settings options
```

---

## 🧑‍💻 Developer Tips

- **Unique Scene Names**: Scene names must be unique for switching and registering transitions.
- **Use Lambda for Factories**: Use `lambda: YourTransition(1.0)` to avoid premature instantiation.
- **Lifecycle Hooks**:
  - `on_enter()`: Good for loading resources, playing music, resetting state.
  - `on_exit()`: Good for saving data, stopping sounds, releasing resources.

---

## 📄 License

LGPL-3.0 License - see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Issues and Pull Requests are welcome. Let's make this project better together!

---

## 🔗 Related Links

- [Pygame Official Documentation](https://www.pygame.org/docs/)
- [Python Game Development Community](https://www.reddit.com/r/pygame/)
- [This Project's GitHub Repository](https://github.com/your-username/pygame-scene-manager)

---

⭐ If you find this project helpful, don't forget to give it a **Star**!
