"""Thread-safe grid state manager for WebSocket broadcasting."""

import threading
from typing import Optional, Callable

_lock = threading.RLock()
_grid_state = {}  # Key: "page/row/col", Value: (r, g, b)
_broadcast_callback: Optional[Callable[[int, int, int, tuple], None]] = None


def set_broadcast_callback(callback: Callable[[int, int, int, tuple], None]) -> None:
    """Set the callback function to broadcast grid updates."""
    global _broadcast_callback
    with _lock:
        _broadcast_callback = callback


def update_button(page: int, row: int, col: int, color: tuple) -> None:
    """Update a button's color and broadcast to WebSocket clients."""
    key = f"{page}/{row}/{col}"
    with _lock:
        _grid_state[key] = color
        if _broadcast_callback:
            _broadcast_callback(page, row, col, color)


def get_grid_state(page: int = 1) -> dict:
    """Get the current state of the grid for a specific page."""
    with _lock:
        result = {}
        for key, color in _grid_state.items():
            p, r, c = key.split("/")
            if int(p) == page:
                result[f"{r}/{c}"] = color
        return result


def clear_grid() -> None:
    """Clear all grid state."""
    with _lock:
        _grid_state.clear()
