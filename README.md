# Kaamelott Chapters
Recently I downloaded (totally legally) the tv show, Kaamelott.
But each episode was splitted, it was a pain in the ass to watch.

So I made a shell script at first to merge all the videos together and use themoviedb.org api to get the title of each episode.

And I switched back to Windows ... so the script wasn't very useful anymore.

## How to cook your merged video
Need an input and output folder, in the input, I put a options.json file, like this :
```json
{
    "series_id": 11466,
    "season_number": 1,
    "language": "fr-FR",
    "video_size": {
        "width": 1920,
        "height": 1080
    },
    "episodes": [
        {
            "episode_number": 1,
            "input_filename": "movies/Kaamelott.S01E001.Heat.mkv"
        },
        {
            "episode_number": 2,
            "input_filename": "movies/Kaamelott.S01E002.Les_Tartes_aux_Myrtilles.mkv"
        },
        {
            "episode_number": 3,
            "input_filename": "movies/Kaamelott.S01E003.La_Table_de_Breccan.mkv"
        },
        {
            "episode_number": 4,
            "input_filename": "movies/Kaamelott.S01E004.Le_Chevalier_Mystere.mkv"
        },
        {
            "episode_number": 5,
            "input_filename": "movies/Kaamelott.S01E005.Le_Fleau_de_Dieu.mkv"
        },
        {
            "episode_number": 6,
            "input_filename": "movies/Kaamelott.S01E006.Le_Garde_du_Corps.mkv"
        },
        {
            "episode_number": 7,
            "input_filename": "movies/Kaamelott.S01E007.Des_nouvelles_du_Monde.mkv"
        }
    ],
    "chapter_format": "Épisode {number} - {name}",
    "output_filename": "Kaamelott.S01E001-007.mkv"
}
```