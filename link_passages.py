#!/usr/bin/env python3
"""
Ergaenzt in den BEREITS angelegten Issues einen klickbaren Link auf den
zugehoerigen Abschnitt in recommendation.md.

Sicher gegen Doppellaeufe:
- Issues werden ueber ihren TITEL gefunden (nicht ueber Nummern).
- Ist der Link in einem Issue schon vorhanden, wird es uebersprungen.
Du kannst dieses Skript also mehrfach laufen lassen, ohne Schaden anzurichten.

Voraussetzungen
---------------
- Derselbe fine-grained Token wie zuvor (Issues: Read & Write, Metadata: Read).
- export GITHUB_TOKEN=github_pat_xxx
- issues.json liegt im selben Ordner.

Benutzung
---------
    python3 link_passages.py --dry-run     # zeigt nur, was geaendert wuerde
    python3 link_passages.py               # schreibt die Links in die Issues
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

OWNER = "nfdi-de"
REPO = "section-metadata-recommendation-re3data-curation"
API = "https://api.github.com"
THROTTLE = 1.1

# Abschnittsname (wie im Issue) -> GitHub-Ueberschriften-Anker in recommendation.md
SECTION_SLUGS = {
    "Rahmen und Grundlagen": "rahmen-und-grundlagen-der-empfehlung",
    "Zielgruppe": "zielgruppe",
    "Begriffsdefinitionen": "begriffsdefinitionen",
    "Hintergrund und Motivation": "hintergrund-und-motivation",
    "Zielsetzung": "zielsetzung",
    "Empfehlung": "empfehlung",
    "Erwartete Wirkung": "erwartete-wirkung",
}

TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "Content-Type": "application/json",
    "User-Agent": "nfdi-curation-link",
}


def _request(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read().decode() or "{}"), r.headers
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}"), e.headers


def fetch_all_issues():
    """Alle offenen Issues holen (ohne Pull Requests), als Titel -> Issue."""
    out = {}
    page = 1
    while True:
        url = f"{API}/repos/{OWNER}/{REPO}/issues?state=open&per_page=100&page={page}"
        status, data, _ = _request("GET", url)
        if status != 200:
            sys.exit(f"Fehler beim Laden der Issues ({status}): {data.get('message')}")
        if not data:
            break
        for it in data:
            if "pull_request" in it:      # PRs ausblenden
                continue
            out[it["title"].strip()] = it
        page += 1
    return out


def section_url(section):
    slug = SECTION_SLUGS.get(section)
    if not slug:
        return None
    return f"https://github.com/{OWNER}/{REPO}/blob/main/recommendation.md#{slug}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not TOKEN:
        sys.exit("Fehler: GITHUB_TOKEN ist nicht gesetzt.")

    here = os.path.dirname(os.path.abspath(__file__))
    issues_src = json.load(open(os.path.join(here, "issues.json"), encoding="utf-8"))

    live = fetch_all_issues()
    print(f"Gefundene offene Issues im Repo: {len(live)}\n")

    changed = skipped = missing = 0
    for entry in issues_src:
        title = entry["title"].strip()
        m = re.search(r"Abschnitt: _([^_]+)_", entry["body"])
        section = m.group(1) if m else None
        url = section_url(section)
        issue = live.get(title)

        if not issue:
            print(f"  ? nicht im Repo gefunden: {title}")
            missing += 1
            continue
        if not url:
            print(f"  ? unbekannter Abschnitt '{section}': {title}")
            missing += 1
            continue

        body = issue["body"] or ""
        if url in body:                       # schon verlinkt -> idempotent
            skipped += 1
            continue

        # "Abschnitt: _Name_"  ->  "Abschnitt: [Name](URL)"
        new_body, n = re.subn(
            r"Abschnitt: _" + re.escape(section) + r"_",
            f"Abschnitt: [{section}]({url})",
            body,
        )
        if n == 0:  # Zeile nicht gefunden -> Link anhaengen
            new_body = body + f"\n\n➡️ Passage im Dokument: [{section}]({url})"

        if args.dry_run:
            print(f"  [dry] #{issue['number']}: + Link -> {section}")
            changed += 1
            continue

        status, resp, _ = _request(
            "PATCH", f"{API}/repos/{OWNER}/{REPO}/issues/{issue['number']}",
            {"body": new_body},
        )
        if status == 200:
            print(f"  + #{issue['number']}: Link auf '{section}' ergaenzt")
            changed += 1
        else:
            print(f"  ! #{issue['number']} Fehler {status}: {resp.get('message')}")
        time.sleep(THROTTLE)

    print(f"\nFertig. Ergaenzt: {changed} | bereits vorhanden: {skipped} | nicht zugeordnet: {missing}")


if __name__ == "__main__":
    main()
