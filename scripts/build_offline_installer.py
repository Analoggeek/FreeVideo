"""Build a self-contained offline installer for the current platform and architecture.

Supports:
- Windows (x86_64 / AMD64 - Intel & AMD PC/Laptop) -> FreeVideo.exe
- macOS Apple Silicon (arm64) -> FreeVideo-Mac-arm64.dmg
- macOS Intel (x86_64) -> FreeVideo-Mac-x86_64.dmg
- Linux (x86_64 - Intel & AMD PC/Laptop) -> FreeVideo-Linux-x86_64.AppImage
"""

from __future__ import annotations

import argparse
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def detect_target() -> tuple[str, list[str]]:
    system = platform.system()
    machine = platform.machine().lower()

    if system == 'Windows':
        return 'windows-x86_64', [sys.executable, str(ROOT / 'scripts/build_windows.py')]
    if system == 'Darwin':
        if machine in ('arm64', 'aarch64'):
            return 'macos-arm64', [sys.executable, str(ROOT / 'scripts/build_macos.py'), '--arch', 'arm64']
        if machine in ('x86_64', 'amd64'):
            return 'macos-x86_64', [sys.executable, str(ROOT / 'scripts/build_macos.py'), '--arch', 'x86_64']
        raise SystemExit(f'Unsupported macOS architecture: {machine}')
    if system == 'Linux':
        if machine in ('x86_64', 'amd64'):
            return 'linux-x86_64', [sys.executable, str(ROOT / 'scripts/build_linux.py')]
        raise SystemExit(f'Unsupported Linux architecture: {machine}')
    raise SystemExit(f'Unsupported operating system: {system}')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / 'build/offline-installer')
    args = parser.parse_args()

    target, cmd = detect_target()
    out_dir = args.out.expanduser().resolve() / target
    cmd.extend(['--out', str(out_dir)])

    print(f'Building offline installer for {target} -> {out_dir}')
    subprocess.run(cmd, cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
