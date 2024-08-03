from datetime import time
from subprocess import run

import requests

from secret import THEMOVIEDB_API_KEY


def get_episodes_name(
    series_id: int, season_number: int, language: str
) -> requests.Response:
    base_url = f"https://api.themoviedb.org/3/tv/{series_id}/season/{season_number}?language={language}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {api_key}".format(api_key=THEMOVIEDB_API_KEY),
    }
    return requests.get(base_url, headers=headers)


def get_video_duration(filepath: str) -> float:
    process = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            filepath,
        ],
        capture_output=True,
    )

    return float(process.stdout.decode())


def generate_single_chapter(number: int, name: str, duration: time) -> str:
    d = time.strftime(duration, "%H:%M:%S.%f")
    return f"""CHAPTER{number:>03}={d[:-3]}
CHAPTER{number:>03}NAME={name}"""


def resize_video(filepath: str, width: int, height: int, output: str) -> bool:
    process = run(
        [
            "ffmpeg",
            "-i",
            filepath,
            "-vf",
            f"scale={width}:{height}",
            "-c:a",
            "copy",
            output,
        ],
        capture_output=True,
    )

    return process.returncode == 0


def edit_prop_video_size(filepath: str, width: int, height: int) -> bool:
    process = run(
        [
            "mkvpropedit",
            filepath,
            "--edit",
            "track:1",
            "--set",
            f"pixel-width={width}",
            "--set",
            f"pixel-height={height}",
            "--quiet",
        ],
        capture_output=True,
    )

    return process.returncode == 0


def merge_videos(output: str, chapters_file: str, videos: list[str]) -> bool:
    process = run(
        [
            "mkvmerge",
            "--output",
            output,
            "--chapter-charset",
            "utf-8",
            "--chapters",
            chapters_file,
            *" +".join(videos).split(),
            "--quiet",
        ],
    )

    return process.returncode == 0
