#!/usr/bin/env python3
"""Add a song to Irish India Radio.

Usage:
    python add_song.py                      # asks you questions
    python add_song.py "C:\\path\\song.mp3"   # starts with this file
    python add_song.py --list               # show the playlist
    python add_song.py --remove 3           # remove song number 3
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PLAYLIST = ROOT / "playlist.json"
MUSIC = ROOT / "music"
MAX_MB = 95  # GitHub rejects files over 100 MB

LICENSES = {
    "1": ("CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/"),
    "2": ("CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0/"),
    "3": ("CC BY-NC 4.0", "https://creativecommons.org/licenses/by-nc/4.0/"),
    "4": ("CC BY-NC-SA 4.0", "https://creativecommons.org/licenses/by-nc-sa/4.0/"),
    "5": ("CC BY-ND 4.0", "https://creativecommons.org/licenses/by-nd/4.0/"),
    "6": ("CC BY-NC-ND 4.0", "https://creativecommons.org/licenses/by-nc-nd/4.0/"),
    "7": ("CC0 (public domain)", "https://creativecommons.org/publicdomain/zero/1.0/"),
    "8": ("Public domain", ""),
    "9": ("Used with the artist's written permission", ""),
}


def load():
    return json.loads(PLAYLIST.read_text(encoding="utf-8"))


def save(cfg):
    PLAYLIST.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def ask(prompt, default="", required=True):
    while True:
        hint = f" [{default}]" if default else ""
        val = input(f"{prompt}{hint}: ").strip()
        if val.startswith("& "):  # PowerShell drag-and-drop adds this
            val = val[2:].strip()
        val = val.strip('"').strip("'") or default
        if val or not required:
            return val
        print("  This one is needed.")


def safe_name(name):
    stem, ext = Path(name).stem, Path(name).suffix.lower()
    stem = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-").lower() or "song"
    return stem + ext


def list_songs(cfg):
    tracks = cfg.get("tracks", [])
    if not tracks:
        print("The playlist is empty.")
    for i, t in enumerate(tracks, 1):
        f = t.get("file")
        f = f[0] if isinstance(f, list) else f
        print(f"{i:>3}. {t.get('title')}, by {t.get('artist')} ({t.get('license')})  {f}")


def add(start_path=""):
    cfg = load()
    print("\nAdd a song to Irish India Radio")
    print("Only add music you are allowed to stream (Creative Commons, public domain, or with the artist's permission).\n")

    src = ask("Path to the MP3 file (you can drag the file into this window)", start_path)
    if src.startswith(("http://", "https://")):
        file_ref = src
    else:
        p = Path(src).expanduser()
        if not p.is_file():
            sys.exit(f"Can't find the file: {p}")
        if p.suffix.lower() not in (".mp3", ".m4a", ".ogg", ".wav"):
            sys.exit("Use an .mp3, .m4a, .ogg or .wav file.")
        size_mb = p.stat().st_size / 1_048_576
        if size_mb > MAX_MB:
            sys.exit(f"That file is {size_mb:.0f} MB. GitHub rejects files over 100 MB, so use a smaller file.")
        MUSIC.mkdir(exist_ok=True)
        dest = MUSIC / safe_name(p.name)
        if p.resolve() != dest.resolve():
            if dest.exists():
                sys.exit(f"music/{dest.name} already exists. Rename your file and try again.")
            shutil.copy2(p, dest)
            print(f"  Copied to music/{dest.name}")
        file_ref = f"music/{dest.name}"

    title = ask("Song title", Path(src).stem.replace("-", " ").replace("_", " ").title())
    artist = ask("Artist / composer")
    print("\nLicence:")
    for k, (name, _) in LICENSES.items():
        print(f"  {k}. {name}")
    choice = ask("Choose a number", "1")
    lic, lic_url = LICENSES.get(choice, (choice, ""))
    source = ask("Web page where you got the song (for the credits)", required=False)

    track = {"title": title, "artist": artist, "file": file_ref, "license": lic}
    if lic_url:
        track["license_url"] = lic_url
    if source:
        track["source_url"] = source
    cfg.setdefault("tracks", []).append(track)
    save(cfg)
    print(f"\nAdded \"{title}\". The playlist now has {len(cfg['tracks'])} song(s).")
    print("To put it online:  git add .  ->  git commit -m \"Add song\"  ->  git push")


def remove(n):
    cfg = load()
    tracks = cfg.get("tracks", [])
    if not 1 <= n <= len(tracks):
        sys.exit(f"There is no song number {n}. Run: python add_song.py --list")
    t = tracks.pop(n - 1)
    save(cfg)
    ref = t.get("file", "")
    ref = ref if isinstance(ref, str) else ""
    f = ROOT / ref
    if ref.startswith("music/") and f.is_file() and not any(x.get("file") == ref for x in tracks):
        f.unlink()
    print(f"Removed \"{t.get('title')}\".")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--list"]:
        list_songs(load())
    elif args[:1] == ["--remove"] and len(args) == 2 and args[1].isdigit():
        remove(int(args[1]))
    else:
        add(args[0] if args else "")
