from pathlib import Path
import zipfile

import pytest

from flowlens.extractor import InputError, solution_directory


def test_directory_is_returned(tmp_path: Path):
    with solution_directory(tmp_path) as root:
        assert root == tmp_path.resolve()


def test_zip_slip_is_rejected(tmp_path: Path):
    archive = tmp_path / "bad.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("../escape.txt", "no")
    with pytest.raises(InputError, match="Unsafe archive entry"):
        with solution_directory(archive):
            pass
