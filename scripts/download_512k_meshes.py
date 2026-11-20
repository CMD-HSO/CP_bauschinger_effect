"""Download the 80^3 (512k element) meshes of the mesh sensitivity study from Zenodo.

The two directories Mesh3_512k and Mesh3_512k_conforming are too large for Git.
This script downloads Dataset.zip from https://doi.org/10.5281/zenodo.21869496,
verifies its MD5 checksum and extracts only these two directories into
data/Models/.

Usage (from the repository root):
    python scripts/download_512k_meshes.py [--keep-zip]

Requires Python >= 3.8, standard library only.
"""

import argparse
import hashlib
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

URL = "https://zenodo.org/api/records/21869496/files/Dataset.zip/content"
MD5 = "e34b4076804c708f3f303e3566c183ef"
TARGET_DIRS = ("Mesh3_512k", "Mesh3_512k_conforming")

REPO_ROOT = Path(__file__).resolve().parent.parent
DEST = REPO_ROOT / "data" / "Models"


def download(url: str, dest: Path) -> None:
    print(f"Downloading {url}")
    with urllib.request.urlopen(url) as response, open(dest, "wb") as out:
        total = int(response.headers.get("Content-Length", 0))
        done = 0
        while chunk := response.read(1 << 20):
            out.write(chunk)
            done += len(chunk)
            if total:
                print(f"\r  {done / 1e6:6.1f} / {total / 1e6:.1f} MB", end="")
    print()


def md5sum(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extract(zip_path: Path, dest: Path) -> int:
    """Extract all members below a TARGET_DIRS component into dest."""
    count = 0
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            parts = PurePosixPath(info.filename.replace("\\", "/")).parts
            hits = [i for i, p in enumerate(parts) if p in TARGET_DIRS]
            if not hits:
                continue
            rel = Path(*parts[hits[0]:])
            if ".." in rel.parts:
                raise RuntimeError(f"Unsafe path in archive: {info.filename}")
            out = dest / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, open(out, "wb") as dst:
                shutil.copyfileobj(src, dst)
            count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--keep-zip", action="store_true",
                        help="keep Dataset.zip in data/ after extraction")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / "Dataset.zip"
        download(URL, zip_path)

        checksum = md5sum(zip_path)
        if checksum != MD5:
            print(f"MD5 mismatch: expected {MD5}, got {checksum}", file=sys.stderr)
            return 1
        print("MD5 checksum OK")

        n = extract(zip_path, DEST)
        if n == 0:
            print(f"No files below {TARGET_DIRS} found in archive", file=sys.stderr)
            return 1
        print(f"Extracted {n} files to {DEST}")

        if args.keep_zip:
            shutil.copy2(zip_path, REPO_ROOT / "data" / "Dataset.zip")
    return 0


if __name__ == "__main__":
    sys.exit(main())
