"""
smart_search.py — Search an Obsidian vault via CLI + Smart Connections

Two modes:
  - Semantic connections (via Smart Connections plugin)
  - Keyword search (via Obsidian CLI)

Setup:
  1. Install Smart Connections plugin in Obsidian.
  2. Install Obsidian CLI (ships with Obsidian 1.12.4+).
  3. Either set the OBSIDIAN_CLI env var to the path of the Obsidian binary,
     or edit the DEFAULT_OBSIDIAN_CLI dict below for your OS.

Usage:
  python smart_search.py --file "Command Center.md"           # Semantic connections
  python smart_search.py --file "Command Center.md" --cross    # Cross-domain only
  python smart_search.py --query "freeze patterns"             # Keyword search
  python smart_search.py --file X --limit 5                    # Limit results
  python smart_search.py --file X --json                       # Machine-readable output
"""

import json
import os
import re
import subprocess
import sys

# Default paths per platform. Override with the OBSIDIAN_CLI env var.
DEFAULT_OBSIDIAN_CLI = {
    "win32": r"C:\Users\<YOUR_USER>\AppData\Local\Programs\Obsidian\Obsidian.exe",
    "darwin": "/Applications/Obsidian.app/Contents/MacOS/Obsidian",
    "linux": "/usr/bin/obsidian",
}

OBSIDIAN_CLI = os.environ.get("OBSIDIAN_CLI") or DEFAULT_OBSIDIAN_CLI.get(sys.platform, "")

# Match any line that looks like an Obsidian startup log (date prefix YYYY-MM-DD).
_DATE_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2}")


def run_eval(js_code):
    """Run JavaScript via Obsidian CLI eval and return stdout."""
    try:
        result = subprocess.run(
            [OBSIDIAN_CLI, "eval", f"code={js_code}"],
            capture_output=True, text=True, timeout=30
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        print(f"Error: failed to invoke Obsidian CLI: {e}", file=sys.stderr)
        sys.exit(2)

    if result.returncode != 0:
        print(f"Error: Obsidian CLI returned exit code {result.returncode}", file=sys.stderr)
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        sys.exit(2)

    lines = result.stdout.strip().split("\n")
    # Strip Obsidian startup noise (any date-prefixed line, plus installer lines).
    clean = [l for l in lines if not _DATE_PREFIX.match(l) and "installer" not in l]
    return "\n".join(clean).strip()


def find_connections(file_key, limit=10, cross_domain=False):
    """Find semantically similar content for a given file."""
    # Use json.dumps to safely embed file_key into the JS source. This protects
    # against filenames containing apostrophes, backslashes, or other characters
    # that would break a naive f-string interpolation.
    fk_lit = json.dumps(file_key)
    fk_no_md = json.dumps(file_key.replace(".md", ""))
    js = f"""(async()=>{{
        const sc=app.plugins.plugins['smart-connections'];
        if(!sc||!sc.env){{console.log(JSON.stringify({{error:'Smart Connections not loaded'}}));return}}
        const sources=sc.env.smart_sources;
        let src=sources.get({fk_lit});
        if(!src){{
            const match=sources.keys.find(k=>k.includes({fk_no_md})||k.endsWith({fk_lit}));
            if(match)src=sources.get(match);
        }}
        if(!src){{console.log(JSON.stringify({{error:'File not found',searched:{fk_lit}}}));return}}
        const results=await src.find_connections({{limit:{max(limit * 3, 30)}}});
        const out=results.map(r=>({{key:r.item.key,score:parseFloat(r.score.toFixed(3))}}));
        console.log(JSON.stringify(out))
    }})()"""
    raw = run_eval(js)
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return [{"error": "Parse failed", "raw": raw}]
    if isinstance(data, dict) and "error" in data:
        return [data]

    if cross_domain:
        source_domain = file_key.split("/")[0]
        data = [d for d in data if not d["key"].startswith(source_domain + "/")]

    return data[:limit]


def search_query(query, limit=10):
    """Keyword search via Obsidian CLI search command with JSON output."""
    try:
        result = subprocess.run(
            [OBSIDIAN_CLI, "search", f"query={query}", f"limit={limit}", "format=json"],
            capture_output=True, text=True, timeout=30
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        print(f"Error: failed to invoke Obsidian CLI: {e}", file=sys.stderr)
        sys.exit(2)

    if result.returncode != 0:
        print(f"Error: Obsidian CLI returned exit code {result.returncode}", file=sys.stderr)
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        sys.exit(2)

    lines = result.stdout.strip().split("\n")
    json_start = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("[") or stripped.startswith("{"):
            json_start = i
            break
    if json_start is None:
        return []
    try:
        data = json.loads("\n".join(lines[json_start:]))
    except json.JSONDecodeError:
        return []
    # Data is a list of file paths
    return [{"key": f, "score": 0} for f in data[:limit]]


def main():
    args = sys.argv[1:]

    # Show usage when called with no args, before the config check, so a fresh
    # user gets help rather than a config error.
    if not args:
        print(__doc__)
        return

    if not OBSIDIAN_CLI or "<YOUR_USER>" in OBSIDIAN_CLI:
        print("Error: OBSIDIAN_CLI is not configured.", file=sys.stderr)
        print("Set the OBSIDIAN_CLI env var to your Obsidian binary path,", file=sys.stderr)
        print("or edit DEFAULT_OBSIDIAN_CLI at the top of this script.", file=sys.stderr)
        sys.exit(1)

    json_mode = "--json" in args
    cross_domain = "--cross" in args
    limit = 10

    if "--limit" in args:
        idx = args.index("--limit")
        limit = int(args[idx + 1])

    if "--file" in args:
        idx = args.index("--file")
        file_key = args[idx + 1]
        results = find_connections(file_key, limit=limit, cross_domain=cross_domain)
    elif "--query" in args:
        idx = args.index("--query")
        query = args[idx + 1]
        results = search_query(query, limit=limit)
    else:
        print(__doc__)
        return

    if json_mode:
        print(json.dumps(results, indent=2))
        return

    if not results:
        print("No results found.")
        return

    if isinstance(results[0], dict) and "error" in results[0]:
        print(f"Error: {results[0]['error']}", file=sys.stderr)
        sys.exit(2)

    for r in results:
        # Clean up block-level keys for readable output
        key = r["key"]
        parts = key.split("#")
        file_part = parts[0]
        section = parts[1] if len(parts) > 1 else ""
        score = r["score"]
        if section:
            print(f"  {score:.3f}  {file_part}  >  {section}")
        else:
            print(f"  {score:.3f}  {file_part}")


if __name__ == "__main__":
    main()
