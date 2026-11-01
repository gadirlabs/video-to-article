#!/usr/bin/env python3
"""Pull the person's own recent posts, with what was said in them, from TikTok, Instagram and YouTube into an inbox
file the skill then works through. Python 3 standard library only.

    python3 pull_posts.py --config docs/video-to-article/config.json [--since 2026-11-01] [--max 10] [--no-transcripts] [--dry-run]

config.json:
    {"provider": "scrapecreators",
     "accounts": {"tiktok": "yourhandle", "instagram": "yourhandle", "youtube": "@yourhandle"},
     "since": "2026-11-01", "max_per_platform": 10, "transcripts": true}

The provider is ScrapeCreators (https://scrapecreators.com), a paid API that reads public posts: one key, no developer
app, no platform approval; about one credit per call. The key comes from the SCRAPECREATORS_API_KEY environment
variable, or from a network secret on a Claude Code cloud environment, in which case the agent proxy attaches it to
requests for api.scrapecreators.com and this script sends nothing. Only the handles in config.json are read: the
person's own accounts, never anyone else's.

Writes docs/video-to-article/inbox/<date>.json: every post newer than `since` that is not in done.json, with its
caption and transcript (native captions where the platform has them, an AI transcript otherwise; transcripts cost a
credit each). Photo and carousel posts are kept with their caption and no transcript. Stops on 401 or 402.
"""
import argparse, datetime as dt, json, os, sys, time, urllib.error, urllib.parse, urllib.request

BASE = "https://api.scrapecreators.com"
ROUTES = {
    "tiktok": {"posts": "/v3/tiktok/profile/videos", "transcript": "/v1/tiktok/video/transcript"},
    "instagram": {"posts": "/v2/instagram/user/posts", "transcript": "/v2/instagram/media/transcript"},
    "youtube": {"shorts": "/v1/youtube/channel/shorts", "videos": "/v1/youtube/channel/videos", "transcript": "/v1/youtube/video/transcript"},
}


def get(path, key, **params):
    url = BASE + path + "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    req = urllib.request.Request(url, headers={"x-api-key": key} if key else {})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read())
        except Exception:
            body = {}
        if e.code in (401, 402):
            sys.exit(f"pull_posts: {e.code} from {path}: {body.get('message') or 'check the API key or the credit balance'}; stopping")
        return e.code, body
    except (urllib.error.URLError, TimeoutError) as e:
        return 0, {"message": str(e)}


def iso(ts):
    """A unix timestamp or ISO string as an ISO date-time in UTC."""
    if ts is None:
        return None
    if isinstance(ts, (int, float)):
        return dt.datetime.fromtimestamp(ts, dt.timezone.utc).isoformat()
    try:
        return dt.datetime.fromisoformat(str(ts).replace("Z", "+00:00")).astimezone(dt.timezone.utc).isoformat()
    except ValueError:
        return str(ts)


def pull_tiktok(handle, key, max_items, errors):
    code, d = get(ROUTES["tiktok"]["posts"], key, handle=handle, trim="true")
    if code != 200 or not d.get("success"):
        errors.append(f"tiktok @{handle}: {code} {d.get('message') or d.get('error') or ''}")
        return []
    items = []
    for v in (d.get("aweme_list") or [])[:max_items]:
        url = v.get("url") or f"https://www.tiktok.com/@{handle}/video/{v.get('aweme_id')}"
        st = v.get("statistics") or {}
        items.append({
            "platform": "tiktok", "id": str(v.get("aweme_id")), "url": url,
            "kind": "photo" if (v.get("image_post_info") or "/photo/" in url) else "video",
            "posted_at": iso(v.get("create_time_utc") or v.get("create_time")),
            "title": None, "caption": v.get("desc") or "",
            "duration_s": round((v.get("video") or {}).get("duration", 0) / 1000, 1) if (v.get("video") or {}).get("duration") else None,
            "stats": {"views": st.get("play_count"), "likes": st.get("digg_count"), "comments": st.get("comment_count")},
        })
    return items


def pull_instagram(handle, key, max_items, errors):
    code, d = get(ROUTES["instagram"]["posts"], key, handle=handle, trim="true")
    if code != 200 or not d.get("success"):
        errors.append(f"instagram @{handle}: {code} {d.get('message') or d.get('error') or ''}")
        return []
    items = []
    for p in (d.get("items") or [])[:max_items]:
        cap = p.get("caption")
        cap = cap.get("text", "") if isinstance(cap, dict) else (cap or "")
        mt, pt = p.get("media_type"), p.get("product_type")
        kind = "video" if (mt == 2 or pt == "clips") else ("carousel" if mt == 8 else "photo")
        code_ = p.get("code")
        url = p.get("url") or (f"https://www.instagram.com/{'reel' if kind == 'video' else 'p'}/{code_}/" if code_ else None)
        items.append({
            "platform": "instagram", "id": str(p.get("id")), "url": url, "kind": kind,
            "posted_at": iso(p.get("taken_at")), "title": None, "caption": cap, "duration_s": None,
            "stats": {"views": p.get("play_count"), "likes": p.get("like_count"), "comments": p.get("comment_count")},
        })
    return items


def pull_youtube(handle, key, max_items, errors):
    items, seen = [], set()
    for which in ("shorts", "videos"):
        code, d = get(ROUTES["youtube"][which], key, handle=handle)
        if code != 200 or not d.get("success"):
            errors.append(f"youtube {handle} {which}: {code} {d.get('message') or d.get('error') or 'not found'}")
            continue
        for v in (d.get("shorts") if which == "shorts" else d.get("videos")) or []:
            vid = v.get("id")
            if not vid or vid in seen:
                continue
            seen.add(vid)
            items.append({
                "platform": "youtube", "id": vid, "url": v.get("url") or f"https://www.youtube.com/watch?v={vid}", "kind": "video",
                "posted_at": iso(v.get("publishDate")), "title": v.get("title"), "caption": v.get("description") or "",
                "duration_s": round(v["durationMs"] / 1000, 1) if v.get("durationMs") else None,
                "stats": {"views": v.get("viewCountInt"), "likes": v.get("likeCountInt"), "comments": v.get("commentCountInt")},
            })
    items.sort(key=lambda x: x["posted_at"] or "", reverse=True)
    return items[:max_items]


def transcript(item, key, errors):
    r = ROUTES[item["platform"]]["transcript"]
    long_ok = "true" if (item.get("duration_s") or 0) > 120 else None
    if item["platform"] == "tiktok":
        code, d = get(r, key, url=item["url"], language="en", use_ai_as_fallback="true", allow_long_transcription=long_ok)
        text = d.get("transcript") if code == 200 else None
        segs = d.get("transcript_with_timestamp") if code == 200 else None
    elif item["platform"] == "instagram":
        code, d = get(r, key, url=item["url"], allow_long_transcription=long_ok)
        tr = (d.get("transcripts") or [{}])[0] if code == 200 else {}
        text, segs = tr.get("text"), tr.get("segments")
        if d.get("duration_seconds"):
            item["duration_s"] = round(d["duration_seconds"], 1)
    else:
        code, d = get(r, key, url=item["url"])
        text = (d.get("transcript_only_text") or (" ".join(s.get("text", "") for s in d.get("transcript") or []) if isinstance(d.get("transcript"), list) else d.get("transcript"))) if code == 200 else None
        segs = d.get("transcript") if code == 200 and isinstance(d.get("transcript"), list) else None
    if code != 200 or not text:
        errors.append(f"{item['platform']} {item['id']} transcript: {code} {d.get('message') or d.get('error') or 'no words returned'}")
    item["transcript"] = text
    item["transcript_segments"] = segs
    return item


def merge_crossposts(items):
    """The same video posted on two platforms is one piece: items whose caption opens the same way within four days
    are merged into the earliest, which lists the others under also_on, so the run writes one page, not two."""
    def key(i):
        text = (i.get("title") or i.get("caption") or "").strip().lower()
        return " ".join(text.split())[:40]
    items = sorted(items, key=lambda i: i.get("posted_at") or "")
    kept = []
    for i in items:
        k = key(i)
        match = None
        if k:
            for j in kept:
                same = key(j) == k and j["platform"] != i["platform"]
                close = abs(dt.datetime.fromisoformat(i["posted_at"]) - dt.datetime.fromisoformat(j["posted_at"])).days <= 4 if (i.get("posted_at") and j.get("posted_at")) else False
                if same and close:
                    match = j
                    break
        if match:
            match.setdefault("also_on", []).append({"platform": i["platform"], "id": i["id"], "url": i["url"]})
        else:
            kept.append(i)
    return sorted(kept, key=lambda i: i.get("posted_at") or "", reverse=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--config", default="docs/video-to-article/config.json")
    ap.add_argument("--since", help="ISO date; overrides config")
    ap.add_argument("--max", type=int, help="posts per platform; overrides config")
    ap.add_argument("--no-transcripts", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="list what would be pulled, fetch no transcripts, write nothing")
    a = ap.parse_args()
    cfg = json.load(open(a.config))
    folder = os.path.dirname(os.path.abspath(a.config))
    done_path = os.path.join(folder, "done.json")
    done = {(d["platform"], str(d["id"])) for d in (json.load(open(done_path)).get("done", []) if os.path.exists(done_path) else [])}
    since = a.since or cfg.get("since") or "1970-01-01"
    max_items = a.max or cfg.get("max_per_platform", 10)
    key = os.environ.get("SCRAPECREATORS_API_KEY", "")
    if cfg.get("provider", "scrapecreators") != "scrapecreators":
        sys.exit(f"pull_posts: provider {cfg.get('provider')!r} is not supported by this script")
    errors, pulled = [], []
    for platform, handle in (cfg.get("accounts") or {}).items():
        if not handle:
            continue
        fn = {"tiktok": pull_tiktok, "instagram": pull_instagram, "youtube": pull_youtube}.get(platform)
        if not fn:
            errors.append(f"{platform}: not a platform this script knows")
            continue
        items = fn(handle.lstrip("@") if platform != "youtube" else handle, key, max_items, errors)
        pulled.extend(items)
        time.sleep(0.5)
    older = [i for i in pulled if (i["posted_at"] or "") < since]
    already = [i for i in pulled if (i["platform"], i["id"]) in done]
    new = merge_crossposts([i for i in pulled if i not in older and i not in already])
    crossposted = sum(len(i.get("also_on", [])) for i in new)
    print(f"pulled {len(pulled)}: {len(new)} new" + (f" ({crossposted} cross-posted copies folded in)" if crossposted else "") + f", {len(older)} older than {since}, {len(already)} already pages")
    for i in new:
        first = (i["title"] or i["caption"] or "").strip().splitlines()
        also = ("  also on " + ", ".join(x["platform"] for x in i["also_on"])) if i.get("also_on") else ""
        print(f"  {i['platform']:9} {i['kind']:8} {(i['posted_at'] or '')[:10]}  {first[0][:70] if first else '(no caption)'}  {i['url']}{also}")
    if a.dry_run:
        for e in errors:
            print("  !", e)
        return
    if cfg.get("transcripts", True) and not a.no_transcripts:
        for i in new:
            if i["kind"] == "video":
                transcript(i, key, errors)
                time.sleep(0.5)
    out_dir = os.path.join(folder, "inbox")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, dt.date.today().isoformat() + ".json")
    json.dump({"pulled_at": dt.datetime.now(dt.timezone.utc).isoformat(), "since": since, "items": new,
               "skipped": {"older": len(older), "already_pages": len(already)}, "errors": errors}, open(out, "w"), indent=1, ensure_ascii=False)
    with_words = sum(1 for i in new if i.get("transcript") or (i["kind"] != "video" and i["caption"]))
    print(f"wrote {os.path.relpath(out)}: {len(new)} items, {with_words} with words" + (f", {len(errors)} notes" if errors else ""))
    for e in errors:
        print("  !", e)


if __name__ == "__main__":
    main()
