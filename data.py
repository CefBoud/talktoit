import glob
import os
import shutil
import tempfile
from pathlib import Path
from typing import List

import conf


def get_indexable_data() -> List[str]:
    data_path = Path(conf.DATA_DIR)
    return [
        f.name
        for f in os.scandir(data_path)
        if f.is_dir() and len(glob.glob1(f, "*")) > 0
    ]


def upload_files(
    files: List[tempfile._TemporaryFileWrapper], data_label: str
) -> List[str]:
    data_dir = Path(f"{conf.DATA_DIR}/{data_label}")
    data_dir.mkdir(exist_ok=True)
    file_paths = []

    for f in files:
        # f.name is the absolute path. Path(f.name).name is the filename
        shutil.copy(f.name, data_dir / Path(f.name).name)
        file_paths.append(f.name)
    return file_paths
