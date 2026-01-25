#!/usr/bin/env bash
set -euo pipefail
set -xv

PROJECT="watarukura"

usage() {
  echo "Usage: $0 [-d YYYY-MM-DD|--since YYYY-MM-DD] [--skip-download]" >&2
  exit 2
}

since_date=""
skip_download=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    -d|--since)
      [[ $# -ge 2 ]] || usage
      since_date="$2"
      shift 2
      ;;
    --since=*)
      since_date="${1#*=}"
      shift
      ;;
    -h|--help)
      usage
      ;;
    --skip-download)
      skip_download=1
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      ;;
  esac
done

since_epoch=""
if [[ -n "$since_date" ]]; then
  if date -j -f "%Y-%m-%d" "$since_date" "+%s" >/dev/null 2>&1; then
    since_epoch=$(date -j -f "%Y-%m-%d" "$since_date" "+%s")
  else
    since_epoch=$(date -d "$since_date" "+%s")
  fi
fi

title_filter='.pages[].title'
jq_args=()
if [[ -n "$since_epoch" ]]; then
  title_filter='.pages[] | select(.updated >= $since_epoch) | .title'
  jq_args=(--argjson since_epoch "$since_epoch")
fi

page=1
if [[ "$skip_download" -eq 0 ]]; then
  curl -sL "https://scrapbox.io/api/pages/$PROJECT?sort=updated" >"articles$page"
  count=$(jq -r .count "articles$page")
  limit=$(jq -r .limit "articles$page")
  if [[ "$count" == "null" || "$limit" == "null" ]]; then
    echo "Failed to read page metadata from scrapbox API." >&2
    exit 1
  fi
  while ((count > limit)); do
    count=$((count - limit))
    skip=$((page * limit))
    page=$((page + 1))
    curl -sL "https://scrapbox.io/api/pages/$PROJECT?sort=updated&skip=$skip" >"articles$page"
  done
fi

if [[ "$skip_download" -eq 0 ]]; then
  mkdir -p scrapbox
  cat articles* |
    jq -r "${jq_args[@]}" "$title_filter" |
    sed -e 's;/;%2F;g' -e 's/ /_/g' |
    while read -r title; do
      curl -sL "https://scrapbox.io/api/pages/$PROJECT/$title/text" >"scrapbox/$title".sb
    done
fi

mkdir -p markdown
cat articles* |
  jq -r "${jq_args[@]}" "$title_filter" |
  sed -e 's;/;%2F;g' -e 's/ /_/g' |
  while read -r title; do
    uv run sb2md.py "scrapbox/$title".sb >"markdown/$title".md
  done
