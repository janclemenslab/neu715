# Course website publication

This folder builds the published course website. The build copies only lectures
and exercises from Weeks 1–3, the files lecture/exercise from Week 4, and the
descriptive and inferential statistics lectures with their figures and data.
Week 4 uses an explicit file list so later topics, tests, and local review files
are excluded.

[Published course](https://janclemenslab.org/neu715/).

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
a simple Week 1 notebook. SciPy is preloaded for WAV and MATLAB loading;
pandas is preloaded for the Week 4 Excel examples. If Excel loading reports a
missing reader, the notebook notes explain how to install openpyxl in JupyterLite.
The 4.01 notebooks link to separate lecture and exercise data ZIPs; extracted
input files are also included for browser use. Their published copies have saved
execution outputs cleared. The image and
audio assets are bundled beside the exercise notebook. Nothing in this workflow publishes or uploads files.

The repository URL is configured in `_config.yml`.
The live site is served from `main` → `docs/` in `janclemenslab/neu715`.
