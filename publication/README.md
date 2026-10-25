# Course website publication

This folder builds the published course website. The build copies only lectures
and exercises from Weeks 1–3; tests and local review files are excluded.

[Published course](https://janclemenslab.org/neu715/). Week 3 covers Monday to
Wednesday; Thursday remains open.

From this folder:

```sh
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python build.py
.venv/bin/python -m http.server 8000 --directory _build/html
```

Then open <http://localhost:8000>. Stop the server with Control-C.

The **Run all notebooks directly in your browser** link opens JupyterLite. Its
first start downloads the browser-based Python runtime and may take a moment.
Test the plotting, Dungeon Escape, and NumPy image/audio notebooks as well as
a simple Week 1 notebook. SciPy is preloaded for WAV loading; the image and
audio assets are bundled beside the exercise notebook. Nothing in this workflow publishes or uploads files.

The repository URL and Binder/Colab settings are configured in `_config.yml`.
The live site is served from `main` → `docs/` in `janclemenslab/neu715`.
