from subprocess import run

import requests

from secret import THEMOVIEDB_API_KEY


def test_mkvtoolnix_installed():
    p = run(["mkvpropedit", "-V"])
    assert p.returncode == 0

    p = run(["mkvmerge", "-V"])
    assert p.returncode == 0


def test_ffmpeg_installed():
    p = run(["ffmpeg", "-version"])
    assert p.returncode == 0

    p = run(["ffprobe", "-version"])
    assert p.returncode == 0


def test_themoviedb_valid_apikey():
    url = "https://api.themoviedb.org/3/authentication"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {THEMOVIEDB_API_KEY}",
    }

    response = requests.get(url, headers=headers)
    assert response.ok
    assert response.status_code == 200
