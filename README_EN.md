# ComfyUI-potrace_Line

## Before and after

The supplied `新規キャンバス6.png` and the ComfyUI output `potrace_line_art_white_00010_.png` are included under simpler names. The after image has a white background (`transparent_background=false`) and matches the 1024×1536 input dimensions.

| Input | Processed (white background preview) |
| :---: | :---: |
| <img src="examples/example_lineart.png" alt="Original line art" width="350"> | <img src="examples/example_lineart_processed_white.png" alt="Line art processed with Potrace on white" width="350"> |

The same 300×300 pixel area around the face is cropped from each image and enlarged 3× to show the lines clearly.

| Before, enlarged | After, enlarged |
| :---: | :---: |
| <img src="docs/images/example_face_before.png" alt="Face detail before processing" width="350"> | <img src="docs/images/example_face_after.png" alt="Face detail after processing" width="350"> |

[日本語](README.md)

A ComfyUI custom node that retraces black and white line art with [Potrace](https://potrace.sourceforge.net/) and rasterizes the curves into an antialiased image. The default output has a transparent background and the same width and height as the input. Batch images are supported.

## Installation

1. Place this folder at `ComfyUI/custom_nodes/ComfyUI-potrace_Line`.
2. Install dependencies **using the Python environment that runs ComfyUI**:

   On Windows with `C:\ComfyUI\.venv`:

   ```powershell
   C:\ComfyUI\.venv\Scripts\python.exe -m pip install -r C:\ComfyUI\custom_nodes\ComfyUI-potrace_Line\requirements.txt
   ```

   In other environments:

   ```bash
   python -m pip install -r ComfyUI/custom_nodes/ComfyUI-potrace_Line/requirements.txt
   ```

3. Restart ComfyUI.

The requirements file installs the existing pure Python [`potracer`](https://pypi.org/project/potracer/) library and the [`aggdraw`](https://pypi.org/project/aggdraw/) curve renderer. Neither implementation is bundled here. Install `potracer`, not `pypotrace`.
If the node shows `IMPORT FAILED`, check that both packages are installed in the Python environment used to launch ComfyUI.

## Usage

Connect `Load Image` → `Potrace Line Art / 線画を整える` → `Save Image`. Use black lines on a white background. By default, the node returns black lines on transparent RGBA, and `Save Image` writes a transparent PNG. Disable `transparent_background` to return a white background RGB image. Grayscale or color input is binarized using Pillow's luminance conversion.

| Input | Description |
| --- | --- |
| `threshold` | Pixels darker than this value become ink. The default is `0.70`. Increase it if pale lines disappear. |
| `despeckle` | Potrace area threshold for removing small spots. Lower it if details disappear. |
| `smoothness` | Potrace curve smoothing. `0` preserves corners; higher values round them. |
| `antialias` | Internal curve rendering scale. The default is `3`; this is separate from output size. |
| `pre_blur` | Gaussian blur radius after median filtering and before binarization. Disabled by default. |
| `median_filter` | Applies a 3×3 median filter to suppress small noise. Disabled by default; leave it off if fine lines disappear. |
| `output_scale` | Output width and height multiplier. The default `1` preserves input dimensions. `2` turns 1024×1536 into 2048×3072. |
| `transparent_background` | When `true`, removes the white background and converts line darkness to alpha. Defaults to `true`. |

The default `threshold=0.70` and `median_filter=false` were chosen by comparing images with both bold and fine lines. If fine lines disappear, raise `threshold` or lower `despeckle`.

Examples: [transparent background (default)](examples/potrace_line_art.json) / [white background](examples/potrace_line_art_white.json). Copy the [input image](examples/example_lineart.png) to `ComfyUI/input/` before opening the workflow, or choose your own image in `Load Image`. The [white background output](examples/example_lineart_processed_white.png) uses the latter workflow settings.

Potrace retraces the binarized shape. It cannot infer detail lost in a low resolution image or reconnect broken lines. The pure Python implementation can be slow on large or complex images. A 2× output uses four times as many pixels as the input, so allow for the additional memory use.

## License

This node is licensed under [GNU GPL-2.0-or-later](LICENSE). Its `potracer` dependency is also GPL-2.0-or-later. Follow both licenses when redistributing.
