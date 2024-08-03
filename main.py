import itertools
import json
import shutil
from datetime import datetime, date, time, timedelta
from pathlib import Path

from jsonschema import validate

from config import OPTIONS_SCHEMA
from utils import (
    get_episodes_name,
    get_video_duration,
    generate_single_chapter,
    edit_prop_video_size,
    merge_videos,
)

options_path = Path("./input/options.json")
episodes_path = Path("./output/episodes.json")
chapters_path = Path("./output/chapters.txt")
movies_path = Path("./output/movies")

# 0. clean output folder
if any(Path("./output").iterdir()):
    print("Output folder is not empty")
    user_input = input("Do you want to clean the output folder? (y/n) ")
    if user_input.lower() == "y":
        shutil.rmtree("./output")
        Path("./output").mkdir()

# 1-a. read options.json file and validate schema
print("I'm checking if options.json file is valid...")
if not options_path.exists():
    raise FileNotFoundError(f"{options_path} not found")

options = json.load(options_path.open(encoding="utf-8"))
validate(instance=options, schema=OPTIONS_SCHEMA)

# 1-b. check if input_filename exist for every episode
for opt_episode in options.get("episodes", []):
    input_filename = opt_episode.get("input_filename")
    if not Path("./input/" + input_filename).exists():
        raise FileNotFoundError(f"{"./input/" + input_filename} not found")

# 2. request themoviedb.org to get episodes names
print("I'm getting episodes names from themoviedb.org...")
episodes = dict()
if episodes_path.exists():
    episodes = json.load(episodes_path.open(encoding="utf-8"))
else:
    print("themov")
    response = get_episodes_name(
        options["series_id"], options["season_number"], options["language"]
    )
    if response.ok:
        episodes = response.json()
        episodes_path.write_text(json.dumps(episodes))

# 3-a. zip information about episodes
print("I'm gathering all information about episodes...")
option2episode_list = list()
timeline = time(minute=0, second=0, microsecond=0)

for option, episode in itertools.zip_longest(
    sorted(options.get("episodes", []), key=lambda x: x["episode_number"]),
    sorted(episodes.get("episodes", []), key=lambda x: x["episode_number"]),
):
    if not option or not episode:
        break
    if option["episode_number"] == episode["episode_number"]:
        data = {
            "id": episode["id"],
            "name": episode["name"],
            "number": episode["episode_number"],
            "duration": timeline,
            "filepath": Path("./input/" + option["input_filename"]),
        }

        # 3-b. calculate duration for each video
        video_duration = get_video_duration(data["filepath"])
        duration = timedelta(seconds=video_duration)
        timeline = (datetime.combine(date.today(), timeline) + duration).time()

        option2episode_list.append(data)

# 3-c. generate chapter file and show it
print("I'm generating chapters file...")
if chapters_path.exists():
    pass
else:
    chapters = list()
    for data in option2episode_list:
        chapter_format = options.get("chapter_format", "{name}")
        chapter_name = chapter_format.format(
            id=data["id"],
            name=data["name"],
            number=data["number"],
            duration=data["duration"],
            filename=data["filepath"].name,
        )
        chapter_str = generate_single_chapter(
            data["number"], chapter_name, data["duration"]
        )

        chapters.append(chapter_str)

    chapters_path.write_text("\n".join(chapters), encoding="utf-8")

# 4. ask user before proceed
print("Look at this chapter file content:")
print(chapters_path.read_text(encoding="utf-8"))
user_input = input("Do you want to proceed? (y/n) ")
if user_input.lower() == "n":
    exit()

# 5. clone videos in output folder
print("I'm cloning videos...")
if not movies_path.exists():
    movies_path.mkdir()

for data in option2episode_list:
    data["filepath"] = shutil.copy(
        data["filepath"], Path("./output/movies/" + data["filepath"].name)
    )

# 6. resize videos
print("I'm resizing videos... (fastboi)")
for data in option2episode_list:
    data["is_ready"] = edit_prop_video_size(
        data["filepath"],
        options.get("video_size.width", 1920),
        options.get("video_size.height", 1080),
    )

# 7. merge videos
print("It's time to merge videos...")
if not all(data["is_ready"] for data in option2episode_list):
    print("Some videos are not ready")
    exit()

final_result = merge_videos(
    str(Path("./output/" + options.get("output_filename", "output.mkv"))),
    str(chapters_path),
    list(str(filepath) for filepath in movies_path.glob("*")),
)
if final_result:
    print("Done!")
else:
    print("Something went wrong")
