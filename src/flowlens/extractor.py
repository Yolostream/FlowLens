from contextlib import contextmanager
from pathlib import Path
import shutil
import tempfile
import zipfile


class InputError(ValueError):
    pass


def _safe_extract(archive: zipfile.ZipFile, target: Path) -> None:
    root = target.resolve()
    for entry in archive.infolist():
        destination = (target / entry.filename).resolve()
        if destination != root and root not in destination.parents:
            raise InputError(f"Unsafe archive entry: {entry.filename}")
    archive.extractall(target)


@contextmanager
def solution_directory(source: Path):
    source = source.expanduser().resolve()
    if source.is_dir():
        yield source
        return
    if not source.exists():
        raise InputError(f"Input does not exist: {source}")
    if source.suffix.lower() != ".zip":
        raise InputError("Input must be a solution ZIP file or an extracted directory")

    temp = Path(tempfile.mkdtemp(prefix="flowlens-"))
    try:
        try:
            with zipfile.ZipFile(source) as archive:
                _safe_extract(archive, temp)
        except zipfile.BadZipFile as exc:
            raise InputError(f"Invalid ZIP file: {source}") from exc
        yield temp
    finally:
        shutil.rmtree(temp, ignore_errors=True)
