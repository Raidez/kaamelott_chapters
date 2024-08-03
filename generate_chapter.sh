#!/usr/bin/env bash
# TODO: check bin (mkvtoolnix) before
# TODO: show file order and ask to proceed before execution
# TODO: transform constants to arguments
# TODO: search serie with name
# TODO: show a progress bar

THEMOVIEDB_API_KEY=
SERIES_ID=11466
SEASON_NUMBER=4
LANGUAGE=fr-FR
VIDEO_PIXEL_SIZE=(1920 1080)
OUTPUT_FILENAME="Kaamelott - Livre IV.mkv"
FILE_LIST=()

i=0
timeline=0.0

# request themoviedb.org to get episodes names
curl --request GET \
     --url "https://api.themoviedb.org/3/tv/${SERIES_ID}/season/${SEASON_NUMBER}?language=${LANGUAGE}" \
     --header "Authorization: Bearer ${THEMOVIEDB_API_KEY}" \
     --header 'accept: application/json' \
     --silent > names.json

# process all mkv file
for file in *.mkv
do
  # change video pixel size
  flatpak run org.bunkus.mkvtoolnix-gui propedit $file --edit track:1 --set pixel-width=${VIDEO_PIXEL_SIZE[0]} --set pixel-height=${VIDEO_PIXEL_SIZE[1]} --quiet

  # extract chapter name from json
  chapter_name=$(cat names.json | jq -r .episodes[$i].name)

  # generate chapter file
  cat >> chapters.txt << EOL
CHAPTER$(printf %02d $((i + 1)))=$(date -d@$timeline -u +%H:%M:%S.%N)
CHAPTER$(printf %02d $((i + 1)))NAME=Épisode $((i + 1)) - $chapter_name
EOL

  # extract duration from file and calc the next chapter segment
  duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $file)
  timeline=$(bc -l <<< "${timeline} + ${duration}")

  FILE_LIST+=($file)
  i=$((i + 1))
done

# generate list of file
FILE_LIST=$(printf "%s +" "${FILE_LIST[@]}")

# merge episodes
flatpak run org.bunkus.mkvtoolnix-gui merge --output "${OUTPUT_FILENAME}" --chapters chapters.txt ${FILE_LIST} --quiet

# clean previous data
rm -f names.json chapters.txt

