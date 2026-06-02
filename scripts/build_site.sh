#!/usr/bin/env bash

set -euo pipefail

serve=false
port=8000

while [[ $# -gt 0 ]]; do
	case "$1" in
		--serve)
			serve=true
			shift
			;;
		--port)
			port="$2"
			shift 2
			;;
		*)
			echo "Usage: $0 [--serve] [--port PORT]" >&2
			exit 1
			;;
	esac
done

repo_root=$(cd "$(dirname "$0")/.." && pwd)
output_dir="$repo_root/_site/calendars"
events_file="$repo_root/calendars/stadtbibliothek.yaml"

rm -rf "$repo_root/_site"
mkdir -p "$output_dir"
uv run yaml2ics "$events_file" > "$output_dir/stadtbibliothek.ics"
uv run "$repo_root/scripts/generate_website.py"

if [[ "$serve" == true ]]; then
	echo "Serving $repo_root/_site at http://127.0.0.1:$port/calendars/"
	exec uv run python -m http.server "$port" --directory "$repo_root/_site"
fi
