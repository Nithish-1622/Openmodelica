"""
Theme Manager for the OpenModelica Simulation Studio.

Provides a centralized, singleton-style theme controller that loads
QSS stylesheets, emits change signals, and supplies consistent
matplotlib plot color palettes for both dark and light modes.
"""

from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMainWindow


# ── QSS file locations ─────────────────────────────────────────
_STYLE_DIR = Path(__file__).resolve().parent / "styles"
_DARK_QSS_PATH = _STYLE_DIR / "dark_theme.qss"
_LIGHT_QSS_PATH = _STYLE_DIR / "light_theme.qss"


# ── Plot color palettes ────────────────────────────────────────
_DARK_PLOT_COLORS: dict[str, str] = {
    "bg": "#1E1E1E",
    "card": "#252526",
    "grid": "#333333",
    "text": "#C5C5C5",
    "text_dim": "#969696",
    "border": "#444444",
    "title": "#FFFFFF",
    "marker_bg": "#1E1E1E",
    "accent": "#007ACC",
    "line": "#58A6FF",
}

_LIGHT_PLOT_COLORS: dict[str, str] = {
    "bg": "#E0F2FE",     # Sky Blue 100
    "card": "#F0F9FF",   # Sky Blue 50
    "grid": "#BAE6FD",   # Sky Blue 200
    "text": "#0F172A",   # Slate 900
    "text_dim": "#475569", # Slate 600
    "border": "#7DD3FC", # Sky Blue 300
    "title": "#0C4A6E",  # Sky Blue 900
    "marker_bg": "#E0F2FE",
    "accent": "#0369A1", # Sky Blue 700
    "line": "#0284C7",   # Sky Blue 600
}


def _load_qss(path: Path) -> str:
    """Load a QSS file and return its content as a string.

    Args:
        path: Path to the .qss stylesheet file.

    Returns:
        Contents of the QSS file, or empty string on error.
    """
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


class ThemeManager(QObject):
    """Centralized theme controller for the Simulation Studio.

    Emits ``themeChanged`` whenever the active theme is switched,
    allowing all connected components (panels, plots, etc.) to
    react accordingly without hard-coded color logic.

    Signals:
        themeChanged (str): Emitted with ``"dark"`` or ``"light"``.
    """

    themeChanged = pyqtSignal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._current: str = "light"  # default branded theme
        self._dark_qss: str = _load_qss(_DARK_QSS_PATH)
        self._light_qss: str = _load_qss(_LIGHT_QSS_PATH)

    # ── Public API ──────────────────────────────────────────────

    @property
    def current_theme(self) -> str:
        """Return the current theme name (``"dark"`` or ``"light"``)."""
        return self._current

    def is_dark(self) -> bool:
        """Return ``True`` if the current theme is dark."""
        return self._current == "dark"

    def switch_theme(self, theme: str) -> None:
        """Disabled: Branded Sky Blue theme is now mandatory."""
        pass

    def toggle(self) -> None:
        """Disabled: Branded Sky Blue theme is now mandatory."""
        pass

    def apply(self, window: QMainWindow) -> None:
        """Apply the branded Sky Blue stylesheet to a QMainWindow."""
        window.setStyleSheet(self._light_qss)

    def get_plot_colors(self) -> dict[str, str]:
        """Return the matplotlib color palette for the active theme.

        Returns:
            A dict with keys: bg, card, grid, text, text_dim,
            border, title, marker_bg, accent, line.
        """
        return dict(_DARK_PLOT_COLORS if self.is_dark() else _LIGHT_PLOT_COLORS)

    def get_qss(self) -> str:
        """Return the raw QSS string for the active theme."""
        return self._dark_qss if self.is_dark() else self._light_qss

    def reload(self) -> None:
        """Reload QSS files from disk (useful during development)."""
        self._dark_qss = _load_qss(_DARK_QSS_PATH)
        self._light_qss = _load_qss(_LIGHT_QSS_PATH)
