"""Build the public book and browser-based notebook environment."""

from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent
PUBLIC_DIRS = ("lectures 1", "lectures 2", "exercises 1", "exercises 2")


def run(*command, cwd=HERE):
    subprocess.run(command, cwd=cwd, check=True)


def sync_content():
    for name in PUBLIC_DIRS:
        source = SOURCE / name
        target = HERE / name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(
            source,
            target,
            ignore=shutil.ignore_patterns(".DS_Store", ".ipynb_checkpoints", ".mypy_cache", "__pycache__"),
        )


def main():
    sync_content()
    bin_dir = Path(sys.executable).parent
    book = bin_dir / "jupyter-book"
    jupyter = bin_dir / "jupyter"
    if not book.exists() or not jupyter.exists():
        raise SystemExit("Install requirements into this Python environment first; see README.md.")

    run(str(book), "clean", ".")
    run(str(book), "build", ".")

    with tempfile.TemporaryDirectory(prefix="neu715-lite-") as temporary:
        lite_dir = Path(temporary)
        files = lite_dir / "files"
        files.mkdir()
        shutil.copy2(HERE / "jupyter-lite.json", lite_dir)
        for name in PUBLIC_DIRS:
            shutil.copytree(HERE / name, files / name)
        run(
            str(jupyter),
            "lite",
            "build",
            "--output-dir",
            str(HERE / "_build/html/lite"),
            cwd=lite_dir,
        )

    notebooks = list(HERE.glob("* */*.ipynb"))
    assert len(notebooks) == 17, f"expected 17 public notebooks, found {len(notebooks)}"
    assert (HERE / "_build/html/index.html").is_file()
    assert (HERE / "_build/html/lite/lab/index.html").is_file()
    lite_config = json.loads((HERE / "_build/html/lite/jupyter-lite.json").read_text())
    packages = lite_config["jupyter-config-data"]["litePluginSettings"][
        "@jupyterlite/pyodide-kernel-extension:kernel"
    ]["loadPyodideOptions"]["packages"]
    assert "pillow" in packages, "JupyterLite must preload Pillow for Dungeon Escape"
    assert not any((HERE / name).exists() for name in ("tests", "instructor 1", "instructor 2"))
    print("Built _build/html with 17 notebooks; no tests or instructor files included.")


if __name__ == "__main__":
    main()
