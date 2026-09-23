# Local website preview

This folder is the publication candidate. The build copies only lectures and
exercises from the parent folder; tests and instructor files are excluded.

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
Test the plotting and Dungeon Escape notebooks as well as a simple Week 1
notebook. Nothing in this workflow publishes or uploads files.

Before publication, add the final GitHub repository URL and enable the Binder
and Colab settings in `_config.yml`.
