"""SPDX-License-Identifier: GPL-2.0-or-later"""

from .nodes import PotraceLineArt

NODE_CLASS_MAPPINGS = {"PotraceLineArt": PotraceLineArt}
NODE_DISPLAY_NAME_MAPPINGS = {"PotraceLineArt": "Potrace Line Art / 線画を整える"}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
