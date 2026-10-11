"""
AuraBeats - Color Themes
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

THEMES = {
    "default": {
        "label": "🎨 Default (Purple)",
        "primary": "#a855f7",
        "secondary": "#06b6d4",
        "accent": "#ec4899",
    },
    "dark": {
        "label": "🌙 Dark Mode",
        "primary": "#1a1a2e",
        "secondary": "#16213e",
        "accent": "#e94560",
    },
    "sakura": {
        "label": "🌸 Sakura",
        "primary": "#ff69b4",
        "secondary": "#ffb6c1",
        "accent": "#ff1493",
    },
    "ocean": {
        "label": "🌊 Ocean",
        "primary": "#0077b6",
        "secondary": "#00b4d8",
        "accent": "#03045e",
    },
    "fire": {
        "label": "🔥 Fire",
        "primary": "#ff4500",
        "secondary": "#ff6347",
        "accent": "#ffd700",
    },
    "forest": {
        "label": "🌲 Forest",
        "primary": "#2d6a4f",
        "secondary": "#52b788",
        "accent": "#95d5b2",
    },
    "royal": {
        "label": "👑 Royal Gold",
        "primary": "#ffd700",
        "secondary": "#daa520",
        "accent": "#b8860b",
    },
    "neon": {
        "label": "⚡ Neon",
        "primary": "#ff00ff",
        "secondary": "#00ffff",
        "accent": "#ffff00",
    },
}


def get_theme(name: str) -> dict:
    """Get theme by name"""
    return THEMES.get(name.lower(), THEMES["default"])


def list_themes() -> list:
    """List all themes"""
    return [
        {"name": name, "label": data["label"]}
        for name, data in THEMES.items()
    ]
