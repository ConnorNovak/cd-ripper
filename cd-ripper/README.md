# Installation

1. Run the installation script.
```
./install.sh
```

# Usage
```
poetry run python -m cd_ripper -h
```

# Information

## Tools Used

1. `ffmpeg`: generate .mp3 files from .wav files

2. `mid3v2`: add audio tags to .mp3 files (mutagen-based)

3. `cdparanoia`: rip high-quality .wav files from audio CDs

## Useful Workflow
```
# Make folder for album
cd ~/Library/Music/Albums
mkdir -p ALBUM_NAME/raw

# Rip .wav files from CD
cd ALBUM_NAME/raw
cdparanoia -B && rename 's/\.cdda//' *.wav

# Convert .wav to mp3
cd ~/Workspace/mp3-player-tooling/cd-ripper
poetry run python -m cd_ripper ~/Library/Music/Albums/ALBUM_NAME/raw -od ~/Library/Music/Albums/ALBUM_NAME
```
