"""cd_ripper submodule that handles ripping .wav files off of CDs."""
import logging
import os
import pathlib
import shutil
import subprocess
import tempfile
from typing import Union, List

import plac

_logger_name = "cd_ripper.raw"
_logger = logging.getLogger(_logger_name)


def rip_cd_to_folder(folder: pathlib.Path) -> None:
    """Rip all tracks on the current CD into the provided folder."""
    if not folder.is_dir():
        raise FileNotFoundError(folder)

    pwd = os.getenv("PWD")
    # -X: abort on skip
    # -B: batch
    cdparanoia_command = (
        f"cd {folder.resolve()};"
        "cdparanoia -XB; "
        f"cd {pwd}")
    _logger.debug("Running command: %s", cdparanoia_command)
    subprocess.run(cdparanoia_command, shell=True, check=True)


def _set_up_logger(logger_name: Union[List, str], log_level: int) -> None:
    """Set up logging to terminal."""
    if isinstance(logger_name, str):
        loggers = [logger_name]

    else:
        loggers = logger_name

    for l in loggers:
        logger = logging.getLogger(l)
        h = logging.StreamHandler()
        f = logging.Formatter("%(message)s")
        h.setFormatter(f)
        logger.addHandler(h)

        logger.setLevel(logging.DEBUG)
        h.setLevel(log_level)


def move_wav_files_to_album(
    wav: pathlib.Path,
    album: pathlib.Path,
    initial_index: int = 0,
    prefix: str = "track",
    mock_run: bool = False,
) -> int:
    """Given a folder of .wav files, copy with rename into album/raw.

    Returns file count in album.
    """
    raw = album / "raw"
    for _file in wav.iterdir():
        name = _file.stem.split(".")[0]
        number = int(name[5:7]) + initial_index 
        target = raw / f"{prefix}{'0' if number < 10 else ''}{number}.wav"

        if mock_run:
            _logger.info("shutil.move(%s, %s)", _file, target)
        else:
            shutil.move(_file, target)

    return len(list(wav.iterdir()))

@plac.annotations(
    folder=plac.Annotation(
        "path to top-level folder for album", type=pathlib.Path),
    cd_count=plac.Annotation(
        "Number of cds in the album", kind="option", abbrev="n", type=int),
    mock_run=plac.Annotation(
        "Print actions instead of executing them", kind="flag",),
)
def rip_album_from_cd(folder: pathlib.Path, cd_count: int = 1, mock_run: bool = False) -> None:
    """Convert a CD in the disk drive into an Album in my Library."""
    # 1. Create folder and album structure
    raw_dir = folder / "raw"
    raw_dir.mkdir(exist_ok=True)

    # 2. Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = pathlib.Path(temp_dir)

        track_num = 0
        for n in range(1, cd_count + 1):
            input(f"Load CD {n}, then press <Enter>:")

            # Rip CD to temporary directory
            rip_cd_to_folder(temp_dir)

            prefix = f"cd0{n}track" if n < 9 else f"cd{n}track"
            track_num += move_wav_files_to_album(
                temp_dir, folder, track_num, prefix=prefix, mock_run=mock_run)


if __name__ == "__main__":
    _set_up_logger("cd_ripper.raw", logging.DEBUG)
    plac.call(rip_album_from_cd)
