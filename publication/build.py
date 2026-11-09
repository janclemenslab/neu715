"""Build the public book and browser-based notebook environment."""

from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent
PUBLIC_DIRS = ("lectures 1", "lectures 2", "lectures 3", "exercises 1", "exercises 2", "exercises 3")
WEEK4_FILES = {
    "lectures 4": ("4.01_files_batch_analysis.ipynb", "4.02_distributions_summary_stats.ipynb", "4.04_statistical_tests.ipynb", "fig", "data/independent.csv", "data/paired.csv", "behavioral_data", "format_examples", "4.01_files_data.zip"),
    "exercises 4": ("4.01_files_batch_analysis_exercises.ipynb", "training_data", "4.01_files_exercises_data.zip", "5.01_probabilities_exercise.ipynb", "5.02_descriptive_stats_exercise.ipynb", "5.03_inferential_stats_exercise.ipynb", "5.01_probabilities_exercise.npz", "5.01_probabilities_exercise4.png", "5.01_probabilities_exercise5.png", "5.01_probabilities_exercise_raster.npz", "5.01_probabilities_exercise_raster.png", "5.03_inferential_stats_exercise.npy", "5.03_inferential_stats_exercise_multi.npy", "ncb.mplstyle", "statistics_exercises_data.zip"),
}
WEEK5_FILES = {
    "lectures 5": ("5.01_linear_regression.ipynb", "5.02_nonlinear_regression.ipynb", "5.01_linear_regression.npz", "5.02_nonlinear_regression.npz", "fig", "week_5_plan.md"),
    "exercises 5": ("5.01_linear_regression_exercises.ipynb", "5.02_nonlinear_regression_exercises.ipynb", "5.01_linear_regression_exercises_1.npz", "5.01_linear_regression_exercises_2.npz", "5.02_nonlinear_regression_exercises_1.npz", "5.02_nonlinear_regression_exercises_2.npz"),
}
WEEK5_ARCHIVES = {"lectures 5": "week_5_lectures.zip", "exercises 5": "week_5_exercises.zip"}


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
            if source.suffix == ".ipynb" and source.name.startswith("4.01_"):
                notebook = json.loads(destination.read_text())
                archive = next(name for name in paths if name.endswith(".zip"))
                for cell in notebook["cells"]:
                    if cell["cell_type"] == "code":
                        cell["outputs"] = []
                        cell["execution_count"] = None
                    elif cell["cell_type"] == "markdown":
                        text = "".join(cell["source"])
                        text = text.replace(f"**`{archive}`**", f"[**{archive}**]({archive})")
                        if "conda install openpyxl" in text and "browser version and get this error" not in text:
                            text += "\n\nIf you are using the browser version and get this error, run `%pip install openpyxl` in a new code cell, then rerun the loading cell."
                        cell["source"] = text.splitlines(keepends=True)
                destination.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")

    for folder, paths in WEEK5_FILES.items():
        target = HERE / folder
        if target.exists():
            shutil.rmtree(target)
        for path in paths:
            source = SOURCE / folder / path
            destination = target / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, destination, ignore=shutil.ignore_patterns(".DS_Store", ".ipynb_checkpoints"))
            else:
                shutil.copy2(source, destination)
            if source.suffix == ".ipynb":
                notebook = json.loads(destination.read_text())
                first = next(cell for cell in notebook["cells"] if cell["cell_type"] == "markdown")
                first["source"] = ("".join(first["source"]).rstrip() +
                    f"\n\n**Download for local use:** [{WEEK5_ARCHIVES[folder]}]({WEEK5_ARCHIVES[folder]}). "
                    "Extract the bundle to keep the notebooks and their data together. "
                    "The lecture bundle also includes the figures and week plan.\n").splitlines(keepends=True)
                destination.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")

    plan = HERE / "lectures 5/week_5_plan.md"
    plan.write_text(plan.read_text() + "\n## Downloads\n\n"
        "- [Lecture notebooks, data, figures, and week plan](week_5_lectures.zip)\n"
        "- [Exercise notebooks and data](../exercises%205/week_5_exercises.zip)\n\n"
        "Extract each ZIP into a folder before opening its notebooks. "
        "The notebooks and data are also included in the browser environment.\n")
    for folder, archive in WEEK5_ARCHIVES.items():
        target = HERE / folder
        files = sorted(path for path in target.rglob("*") if path.is_file())
        with zipfile.ZipFile(target / archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
            for path in files:
                bundle.write(path, path.relative_to(target))


def main():
    sync_content()
    bin_dir = Path(sys.executable).parent
    book = bin_dir / "jupyter-book"
    jupyter = bin_dir / "jupyter"
    if not book.exists() or not jupyter.exists():
        raise SystemExit("Install requirements into this Python environment first; see README.md.")

    run(str(book), "clean", ".")
    run(str(book), "build", ".")
    for folder, paths in WEEK4_FILES.items():
        for path in paths:
            if path.endswith(".zip"):
                shutil.copy2(HERE / folder / path, HERE / "_build/html" / folder / path)
    # Keep individual Week 5 data/figure assets and both bundles downloadable.
    for folder in WEEK5_FILES:
        for source in (HERE / folder).rglob("*"):
            if source.is_file() and source.suffix not in (".ipynb", ".md"):
                target = HERE / "_build/html" / folder / source.relative_to(HERE / folder)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

    with tempfile.TemporaryDirectory(prefix="neu715-lite-") as temporary:
        lite_dir = Path(temporary)
        files = lite_dir / "files"
        files.mkdir()
        shutil.copy2(HERE / "jupyter-lite.json", lite_dir)
        for name in (*PUBLIC_DIRS, *WEEK4_FILES, *WEEK5_FILES):
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
    assert len(notebooks) == 36, f"expected 36 public notebooks, found {len(notebooks)}"
    for folder, paths in WEEK4_FILES.items():
        assert sorted(p.name for p in (HERE / folder).glob("*.ipynb")) == sorted(p for p in paths if p.endswith(".ipynb"))
        for path in paths:
            assert (HERE / "_build/html/lite/files" / folder / path).exists()
    for folder, paths in WEEK5_FILES.items():
        assert sorted(p.name for p in (HERE / folder).glob("*.ipynb")) == sorted(p for p in paths if p.endswith(".ipynb"))
        for source in (HERE / folder).rglob("*"):
            if not source.is_file():
                continue
            relative = source.relative_to(HERE / folder)
            assert (HERE / "_build/html/lite/files" / folder / relative).is_file()
            if source.suffix in (".ipynb", ".md"):
                assert (HERE / "_build/html" / folder / relative.with_suffix(".html")).is_file()
            else:
                assert (HERE / "_build/html" / folder / relative).is_file()
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
    print("Built _build/html with 36 notebooks, including Week 5 and its download bundles; no tests or instructor files included.")


if __name__ == "__main__":
    main()
