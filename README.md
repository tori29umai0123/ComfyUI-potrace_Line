# ComfyUI-potrace_Line

[English](README_EN.md)

白黒線画を [Potrace](https://potrace.sourceforge.net/) でなぞり直し、曲線をアンチエイリアス付きの白背景画像として出力する ComfyUI カスタムノードです。標準設定では入力と同じ縦横サイズで出力します。画像のバッチ入力にも対応します。

## インストール

1. このフォルダを `ComfyUI/custom_nodes/ComfyUI-potrace_Line` に置きます。
2. **ComfyUI が使用する Python 環境で**依存ライブラリをインストールします。

   Windows で `C:\ComfyUI\.venv` を使っている場合:

   ```powershell
   C:\ComfyUI\.venv\Scripts\python.exe -m pip install -r C:\ComfyUI\custom_nodes\ComfyUI-potrace_Line\requirements.txt
   ```

   それ以外の環境:

   ```bash
   python -m pip install -r ComfyUI/custom_nodes/ComfyUI-potrace_Line/requirements.txt
   ```

3. ComfyUI を再起動します。

`requirements.txt` は既存の純 Python ライブラリ [`potracer`](https://pypi.org/project/potracer/) と曲線描画ライブラリ [`aggdraw`](https://pypi.org/project/aggdraw/) をインストールします。これらの実装はこのリポジトリに同梱していません。`pypotrace` ではなく `potracer` が必要です。
`IMPORT FAILED` と表示される場合は、ComfyUI を起動する Python に両方が入っているか確認してください。

## 使い方

`Load Image` → `Potrace Line Art / 線画を整える` → `Save Image` の順につなぎます。黒線・白背景の画像を入力してください。標準出力は黒線だけの RGBA 画像で、`Save Image` が透過PNGとして保存します。`transparent_background` を無効にすると RGB の白背景画像になります。グレーやカラーの入力は Pillow の輝度変換で二値化します。

| 入力 | 説明 |
| --- | --- |
| `threshold` | これより暗い画素を線とみなします。標準値は `165/255 ≒ 0.647`。薄い線が消える場合は上げます。 |
| `despeckle` | 小さな点を除去する Potrace の面積しきい値。細部が消える場合は下げます。 |
| `smoothness` | Potrace の曲線化の強さ。`0` は角を残し、値を上げると滑らかになります。 |
| `antialias` | 曲線を描画する内部倍率。標準値は `3`。出力サイズとは別です。 |
| `pre_blur` | メディアン処理後、二値化前のガウスぼかし半径。標準では無効です。 |
| `median_filter` | 3×3 メディアンフィルターで細かなノイズを抑えます。標準で有効です。 |
| `output_scale` | 出力の縦横倍率。標準値 `1` は入力と同じサイズ。`2` なら 904×1740 入力から 1808×3480 を出力します。 |
| `transparent_background` | `true` で白背景を透明にし、線の濃さをアルファに変換します。標準は `true`。 |

標準設定は `Artwork_potrace_smooth.png` を作成した検証スクリプトと同じ前処理・曲線描画を使い、出力を1倍の透過PNGにしています。検証画像と同じ白背景・2倍出力が必要な場合は `transparent_background=false`、`output_scale=2` にしてください。細線が消える場合は `despeckle` または `threshold` を下げてください。

サンプル: [透過背景（標準）](examples/potrace_line_art.json) / [白背景](examples/potrace_line_art_white.json)。付属の [example_lineart.png](examples/example_lineart.png) を `ComfyUI/input/` にコピーしてからワークフローを読み込むか、`Load Image` で手持ちの線画を選んでください。

Potrace は二値化後の形をなぞります。低解像度で潰れた細部や、途切れた線を推測して復元するものではありません。純 Python 実装のため、大きな画像や複雑な線画は処理に時間がかかります。2倍出力は元画像の4倍の画素数を使います。

## ライセンス

このノードは [GNU GPL-2.0-or-later](LICENSE) です。依存する `potracer` も GPL-2.0-or-later です。配布時はそれぞれのライセンス条件を守ってください。
