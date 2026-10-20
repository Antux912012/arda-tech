#!/usr/bin/env python3
"""
Arda Tech - Automated App Version Updater from GitHub Releases
Queries GitHub API for the latest releases across all apps defined in apps.json,
updates the version numbers and .deb URLs if newer releases are found,
and optionally triggers PPA pool rebuild.
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARDA_TECH_DIR = os.path.dirname(SCRIPT_DIR)
APPS_JSON_PATH = os.path.join(ARDA_TECH_DIR, "apps.json")
PPA_DIR = "/home/antonio/arda-tech-ppa"

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def get_headers():
    headers = {"User-Agent": "Arda-Tech-Version-Updater/1.0"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers

def fetch_json(url):
    req = urllib.request.Request(url, headers=get_headers())
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"[!] GitHub API rate-limited or forbidden: {url}")
        return None
    except Exception as e:
        print(f"[!] Error fetching {url}: {e}")
        return None

def get_latest_github_release(repo_url, apt_package=None, app_id=None):
    match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
    if not match:
        return None
    owner, repo = match.group(1), match.group(2).replace(".git", "")

    # 1. Fetch releases
    releases = fetch_json(f"https://api.github.com/repos/{owner}/{repo}/releases?per_page=15")
    if releases and isinstance(releases, list) and len(releases) > 0:
        valid = [r for r in releases if not r.get("draft", False)]
        if valid:
            valid.sort(key=lambda r: r.get("published_at") or r.get("created_at") or "", reverse=True)

            # If this is a specialized sub-package (like vingilot-estel) in a shared repo,
            # find the release that actually includes this sub-package or mentions it
            if apt_package and apt_package == "vingilot-estel":
                for r in valid:
                    names = [a.get("name", "") for a in r.get("assets", [])]
                    r_title = (r.get("name") or "") + " " + (r.get("tag_name") or "")
                    if any("estel" in n.lower() for n in names) or "estel" in r_title.lower():
                        tag = r.get("tag_name", "").strip()
                        return {
                            "version": tag.lstrip("vV"),
                            "tag": tag,
                            "html_url": r.get("html_url", ""),
                            "assets": r.get("assets", [])
                        }
                return None

            top = valid[0]
            tag = top.get("tag_name", "").strip()
            return {
                "version": tag.lstrip("vV"),
                "tag": tag,
                "html_url": top.get("html_url", ""),
                "assets": top.get("assets", [])
            }

    # 2. Fallback to tags
    tags = fetch_json(f"https://api.github.com/repos/{owner}/{repo}/tags?per_page=10")
    if tags and isinstance(tags, list) and len(tags) > 0:
        if apt_package and apt_package == "vingilot-estel":
            estel_tags = [t for t in tags if "estel" in t.get("name", "").lower()]
            if estel_tags:
                tag_name = estel_tags[0].get("name", "").strip()
                return {
                    "version": tag_name.lstrip("vV"),
                    "tag": tag_name,
                    "html_url": f"https://github.com/{owner}/{repo}/releases/tag/{tag_name}",
                    "assets": []
                }
            return None

        tag_name = tags[0].get("name", "").strip()
        return {
            "version": tag_name.lstrip("vV"),
            "tag": tag_name,
            "html_url": f"https://github.com/{owner}/{repo}/releases/tag/{tag_name}",
            "assets": []
        }

    return None

def update_apps_catalog():
    if not os.path.exists(APPS_JSON_PATH):
        print(f"Error: {APPS_JSON_PATH} not found.")
        sys.exit(1)

    with open(APPS_JSON_PATH, "r", encoding="utf-8") as f:
        apps = json.load(f)

    updated_count = 0
    print("======================================================================")
    print("   Checking Arda-Tech App Versions Against GitHub Releases")
    print("======================================================================")

    for app in apps:
        name = app.get("name", "Unknown")
        current_ver = app.get("version", "").strip()
        repo_url = app.get("repoUrl", "")

        if not repo_url:
            print(f"[-] {name:<32} | {current_ver:<12} | No repoUrl defined")
            continue

        rel_info = get_latest_github_release(repo_url, apt_package=app.get("aptPackage"), app_id=app.get("id"))
        if not rel_info:
            print(f"[-] {name:<32} | {current_ver:<12} | No GitHub releases found")
            continue

        latest_ver = rel_info["version"]
        tag = rel_info["tag"]

        # Check if version should be updated
        # Preserve build/packaging extensions like -1 if base version is identical
        base_current = current_ver.split("-")[0]
        base_latest = latest_ver.split("-")[0]

        if current_ver != latest_ver and not current_ver.startswith(latest_ver + "-"):
            print(f"[+] UPDATE: {name:<24} | {current_ver:<12} -> {latest_ver:<12} (tag: {tag})")
            app["version"] = latest_ver
            updated_count += 1

            # Check if assets include deb for this app
            apt_pkg = app.get("aptPackage")
            if apt_pkg:
                for asset in rel_info.get("assets", []):
                    aname = asset.get("name", "")
                    if aname.startswith(f"{apt_pkg}_") and aname.endswith(".deb"):
                        app["debUrl"] = f"pool/main/{apt_pkg[0]}/{apt_pkg}/{aname}"
                        break
        else:
            print(f"[OK] {name:<30} | {current_ver:<12} | Up-to-date with GitHub ({tag})")

    if updated_count > 0:
        with open(APPS_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(apps, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("======================================================================")
        print(f"✅ Successfully updated {updated_count} app(s) in {APPS_JSON_PATH}")

        # Sync to arda-tech-ppa
        ppa_apps_json = os.path.join(PPA_DIR, "apps.json")
        if os.path.exists(ppa_apps_json):
            with open(ppa_apps_json, "w", encoding="utf-8") as f:
                json.dump(apps, f, indent=2, ensure_ascii=False)
                f.write("\n")
            print(f"✅ Synced to {ppa_apps_json}")
    else:
        print("======================================================================")
        print("✨ All apps are already at their latest GitHub release version!")

    return updated_count

if __name__ == "__main__":
    update_apps_catalog()
