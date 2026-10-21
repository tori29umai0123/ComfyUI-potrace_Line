"""Retrace line art with Potrace and rasterize its curves.

SPDX-License-Identifier: GPL-2.0-or-later
"""

import aggdraw
import numpy as np
import potrace
import torch
from PIL import Image, ImageFilter


class PotraceLineArt:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "image": ("IMAGE",),
            "threshold": ("FLOAT", {"default": 0.70, "min": 0.0, "max": 1.0, "step": 0.001}),
            "despeckle": ("INT", {"default": 3, "min": 0, "max": 100, "step": 1}),
            "smoothness": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.34, "step": 0.05}),
            "antialias": ("INT", {"default": 3, "min": 1, "max": 4, "step": 1}),
            "pre_blur": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 4.0, "step": 0.1}),
            "median_filter": ("BOOLEAN", {"default": False}),
            "output_scale": ("INT", {"default": 1, "min": 1, "max": 4, "step": 1}),
            "transparent_background": ("BOOLEAN", {"default": True}),
        }}

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "trace"
    CATEGORY = "image/potrace"

    def trace(self, image, threshold, despeckle, smoothness, antialias,
              pre_blur=0.0, median_filter=False, output_scale=1,
              transparent_background=True):
        frames = []
        for frame in image.detach().cpu().numpy():
            height, width = frame.shape[:2]
            rgb = Image.fromarray(np.rint(np.clip(frame[..., :3], 0, 1) * 255).astype(np.uint8), "RGB")
            gray = rgb.convert("L")
            if median_filter:
                gray = gray.filter(ImageFilter.MedianFilter(3))
            if pre_blur > 0:
                gray = gray.filter(ImageFilter.GaussianBlur(pre_blur))
            binary = Image.fromarray(
                np.where(np.asarray(gray) < threshold * 255, 0, 255).astype(np.uint8), "L"
            )
            curves = potrace.Bitmap(binary).trace(
                turdsize=despeckle, alphamax=smoothness,
                opticurve=True, opttolerance=0.2,
            )

            path = aggdraw.Path()
            for curve in curves:
                start = curve.start_point
                path.moveto(start.x * antialias, start.y * antialias)
                for segment in curve.segments:
                    if segment.is_corner:
                        corner, end = segment.c, segment.end_point
                        path.lineto(corner.x * antialias, corner.y * antialias)
                        path.lineto(end.x * antialias, end.y * antialias)
                    else:
                        c1, c2, end = segment.c1, segment.c2, segment.end_point
                        path.curveto(
                            c1.x * antialias, c1.y * antialias,
                            c2.x * antialias, c2.y * antialias,
                            end.x * antialias, end.y * antialias,
                        )
                path.close()

            render = Image.new("RGB", (width * antialias, height * antialias), "white")
            if curves:
                draw = aggdraw.Draw(render)
                draw.path(path, aggdraw.Brush("black"))
                draw.flush()
            if antialias != output_scale:
                render = render.resize((width * output_scale, height * output_scale), Image.Resampling.LANCZOS)
            if transparent_background:
                alpha = Image.fromarray(255 - np.asarray(render.convert("L")), "L")
                render = Image.new("RGBA", render.size, (0, 0, 0, 0))
                render.putalpha(alpha)
            frames.append(np.asarray(render, dtype=np.float32) / 255.0)
        return (torch.from_numpy(np.stack(frames)),)
