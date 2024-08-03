OPTIONS_SCHEMA = {
    "type": "object",
    "properties": {
        "series_id": {"type": "integer"},
        "season_number": {"type": "integer"},
        "language": {"type": "string"},
        "video_size": {
            "type": "object",
            "properties": {"width": {"type": "integer"}, "height": {"type": "integer"}},
        },
        "episodes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "episode_number": {"type": "integer"},
                    "input_filename": {"type": "string"},
                },
            },
            "minItems": 1,
            "uniqueItems": True,
        },
        "chapter_format": {"type": "string"},
        "output_filename": {"type": "string"},
    },
}
