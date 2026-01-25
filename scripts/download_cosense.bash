#!/usr/bin/env bash
set -euo pipefail
set -xv

PROJECT="watarukura"

#page=1
#curl -sL "https://scrapbox.io/api/pages/$PROJECT/" >"articles$page"
#count=$(jq .count "articles$page")
#limit=$(jq .limit "articles$page")
#while ((count > limit)); do
#  count=$((count - limit))
#  skip=$((page * limit))
#  page=$((page + 1))
#  curl -sL "https://scrapbox.io/api/pages/$PROJECT/?skip=$skip" >"articles$page"
#done
#
#mkdir -p scrapbox
#cat articles* |
#  jq -r '.pages[].title' |
#  sed -e 's;/;%2F;g' -e 's/ /_/g' |
#  while read -r title; do
#    curl -sL "https://scrapbox.io/api/pages/$PROJECT/$title/text" >"scrapbox/$title".sb
#  done

mkdir -p markdown
cat articles* |
  jq -r '.pages[].title' |
  sed -e 's;/;%2F;g' -e 's/ /_/g' |
  while read -r title; do
    uv run sb2md.py "scrapbox/$title".sb >"markdown/$title".md
  done
