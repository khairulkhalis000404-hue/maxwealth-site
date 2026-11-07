#!/bin/zsh
# Rebuild and copy the site to the scratchpad the preview server serves (the launcher can't read Desktop)
cd "${0:A:h}/.." && python3 tools/build.py && rsync -a --delete docs/ /private/tmp/claude-501/-Users-khrlkhls-Desktop-AI-Video-Editor/cf607fba-db98-46f5-a945-3bed1a28cd19/scratchpad/mw-preview/
