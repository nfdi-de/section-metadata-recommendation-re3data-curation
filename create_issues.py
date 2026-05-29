#!/usr/bin/env python3
"""
Bestueckt das Kuratierungs-Repo mit Labels und Issues aus der
Community-Kommentierungsphase.

Voraussetzungen
---------------
- Python 3.8+, `pip install requests`
- Ein fine-grained Personal Access Token mit Resource Owner = nfdi-de und den
  Permissions:  Issues: Read & Write,  Metadata: Read
  (fuer --project zusaetzlich:  Organization > Projects: Read & Write)
- Token als Umgebungsvariable:  export GITHUB_TOKEN=github_pat_xxx

Benutzung
---------
    python create_issues.py --dry-run          # zeigt nur, was passieren wuerde
    python create_issues.py                     # legt Labels + Issues an
    python create_issues.py --project 7         # zusaetzlich aufs Project-Board #7

Die Dateien labels.json und issues.json muessen im selben Verzeichnis liegen.
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error

OWNER = "nfdi-de"
REPO = "section-metadata-recommendation-re3data-curation"
API = "https://api.github.com"
GRAPHQL = "https://api.github.com/graphql"
THROTTLE = 1.1  # Sekunden zwischen schreibenden Requests (Secondary Rate Limit)

TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "Content-Type": "application/json",
    "User-Agent": "nfdi-curation-import",
}


def _request(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            body = r.read().decode()
            return r.status, (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def ensure_labels(labels, dry):
    for lb in labels:
        if dry:
            print(f"  [dry] Label: {lb['name']}")
            continue
        status, resp = _request("POST", f"{API}/repos/{OWNER}/{REPO}/labels", lb)
        if status == 201:
            print(f"  + Label angelegt: {lb['name']}")
        elif status == 422:
            # existiert bereits -> Farbe/Beschreibung aktualisieren
            _request("PATCH", f"{API}/repos/{OWNER}/{REPO}/labels/{lb['name']}",
                     {"new_name": lb["name"], "color": lb["color"],
                      "description": lb.get("description", "")})
            print(f"  = Label aktualisiert: {lb['name']}")
        else:
            print(f"  ! Label '{lb['name']}' Fehler {status}: {resp.get('message')}")
        time.sleep(THROTTLE)


def create_issue(issue, dry):
    if dry:
        print(f"  [dry] Issue: {issue['title']}  {issue['labels']}"
              + (f"  (+{len(issue['seed_comments'])} Antwort)" if issue.get("seed_comments") else ""))
        return None
    payload = {"title": issue["title"], "body": issue["body"], "labels": issue["labels"]}
    status, resp = _request("POST", f"{API}/repos/{OWNER}/{REPO}/issues", payload)
    if status != 201:
        print(f"  ! Issue '{issue['title']}' Fehler {status}: {resp.get('message')}")
        return None
    num, node_id = resp["number"], resp["node_id"]
    print(f"  + #{num}: {issue['title']}")
    time.sleep(THROTTLE)
    for sc in issue.get("seed_comments", []):
        _request("POST", f"{API}/repos/{OWNER}/{REPO}/issues/{num}/comments", {"body": sc})
        time.sleep(THROTTLE)
    return node_id


def resolve_project_id(project_number):
    q = ("query($org:String!,$num:Int!){organization(login:$org)"
         "{projectV2(number:$num){id}}}")
    status, resp = _request("POST", GRAPHQL,
                            {"query": q, "variables": {"org": OWNER, "num": project_number}})
    try:
        return resp["data"]["organization"]["projectV2"]["id"]
    except (KeyError, TypeError):
        print(f"  ! Project #{project_number} nicht gefunden: {resp}")
        return None


def add_to_project(project_id, issue_node_id):
    m = ("mutation($p:ID!,$c:ID!){addProjectV2ItemById(input:{projectId:$p,contentId:$c})"
         "{item{id}}}")
    _request("POST", GRAPHQL,
             {"query": m, "variables": {"p": project_id, "c": issue_node_id}})
    time.sleep(THROTTLE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="nichts anlegen, nur anzeigen")
    ap.add_argument("--project", type=int, default=None,
                    help="Project-(v2)-Nummer, auf die Issues gelegt werden sollen")
    ap.add_argument("--skip-labels", action="store_true")
    args = ap.parse_args()

    if not TOKEN and not args.dry_run:
        sys.exit("Fehler: Umgebungsvariable GITHUB_TOKEN ist nicht gesetzt.")

    here = os.path.dirname(os.path.abspath(__file__))
    labels = json.load(open(os.path.join(here, "labels.json"), encoding="utf-8"))
    issues = json.load(open(os.path.join(here, "issues.json"), encoding="utf-8"))

    print(f"Repo: {OWNER}/{REPO}  |  Labels: {len(labels)}  |  Issues: {len(issues)}"
          + ("  [DRY-RUN]" if args.dry_run else ""))

    if not args.skip_labels:
        print("\nLabels:")
        ensure_labels(labels, args.dry_run)

    project_id = None
    if args.project and not args.dry_run:
        project_id = resolve_project_id(args.project)

    print("\nIssues:")
    for issue in issues:
        node_id = create_issue(issue, args.dry_run)
        if project_id and node_id:
            add_to_project(project_id, node_id)

    print("\nFertig.")


if __name__ == "__main__":
    main()
