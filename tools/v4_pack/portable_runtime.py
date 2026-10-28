"""Build an isolated Python runtime for the bundled PTSL scripts."""
from pathlib import Path
import importlib.metadata
import shutil
import sys
import zipfile


def copy_runtime(destination):
    destination = Path(destination)
    if destination.exists():
        raise FileExistsError(destination)
    destination.mkdir(parents=True)
    base = Path(sys.base_prefix)
    for pattern in ("python*.exe", "*.dll", "LICENSE.txt"):
        for source in base.glob(pattern):
            shutil.copy2(source, destination / source.name)
    shutil.copytree(base / "DLLs", destination / "DLLs",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pdb"))
    library = base / "Lib"
    with zipfile.ZipFile(destination / "stdlib.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for source in sorted(library.rglob("*.py")):
            relative = source.relative_to(library)
            if any(part in {"site-packages", "__pycache__", "test", "tests", "idlelib", "tkinter", "ensurepip"} for part in relative.parts):
                continue
            archive.write(source, relative.as_posix())
    packages = destination / "packages"
    packages.mkdir()
    for name in ("py-ptsl", "grpcio", "protobuf", "typing-extensions"):
        distribution = importlib.metadata.distribution(name)
        for relative in distribution.files or ():
            if ".." in relative.parts or "__pycache__" in relative.parts or str(relative).endswith((".pyc", ".pyo")):
                continue
            source = Path(distribution.locate_file(relative))
            if source.is_file():
                target = packages / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
    version = f"{sys.version_info.major}{sys.version_info.minor}"
    (destination / f"python{version}._pth").write_text(
        "stdlib.zip\n.\nDLLs\npackages\nimport site\n", encoding="utf-8")
