"""Build the public book and browser-based notebook environment."""

from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent
PUBLIC_DIRS = ("lectures 1", "lectures 2", "lectures 3", "exercises 1", "exercises 2", "exercises 3")
WEEK4_FILES = {
    "lectures 4": ("4.01_files_batch_analysis.ipynb", "4.02_distributions_summary_stats.ipynb", "4.04_statistical_tests.ipynb", "fig", "data/independent.csv", "data/paired.csv", "data/demo_sessions", "data/demo_mouse_A.xlsx", "data/demo_mouse_A.mat", "data/README.md"),
    "exercises 4": ("4.01_files_batch_analysis_exercises.ipynb", "data/behavioral_data", "data/README.md"),
}


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
    # Week 4 is released one topic at a time; copy only the listed materials.
    for folder, paths in WEEK4_FILES.items():
        target = HERE / folder
        if target.exists():
            shutil.rmtree(target)
        for path in paths:
            source = SOURCE / folder / path
            destination = target / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, destination, ignore=shutil.ignore_patterns(".DS_Store", "scores.png"))
            else:
                shutil.copy2(source, destination)


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
        for name in (*PUBLIC_DIRS, *WEEK4_FILES):
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
    assert len(notebooks) == 29, f"expected 29 public notebooks, found {len(notebooks)}"
    for folder, paths in WEEK4_FILES.items():
        assert sorted(p.name for p in (HERE / folder).glob("*.ipynb")) == sorted(p for p in paths if p.endswith(".ipynb"))
        for path in paths:
            assert (HERE / "_build/html/lite/files" / folder / path).exists()
    assert (HERE / "_build/html/index.html").is_file()
    assert (HERE / "_build/html/lite/lab/index.html").is_file()
    lite_config = json.loads((HERE / "_build/html/lite/jupyter-lite.json").read_text())
    packages = lite_config["jupyter-config-data"]["litePluginSettings"][
        "@jupyterlite/pyodide-kernel-extension:kernel"
    ]["loadPyodideOptions"]["packages"]
    assert "pillow" in packages, "JupyterLite must preload Pillow for Dungeon Escape"
    assert "scipy" in packages, "JupyterLite must preload SciPy for WAV loading"
    assert "pandas" in packages, "JupyterLite must preload pandas for the Excel example"
    assert not any((HERE / name).exists() for name in ("tests", "instructor 1", "instructor 2", "instructor 3", "instructor_week4", "draft_preview_week3", "draft_preview_week4"))
    for folder, asset in (("lectures 3", "coffee.png"), ("exercises 3", "astronaut.png"), ("exercises 3", "fly.png"), ("exercises 3", "fly_source.png"), ("exercises 3", "speech.wav")):
        assert (HERE / "_build/html/lite/files" / folder / "assets" / asset).is_file()
    print("Built _build/html with 29 notebooks; no tests or instructor files included.")


if __name__ == "__main__":
    main()
