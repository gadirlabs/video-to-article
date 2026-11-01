# Video to article

A free Claude Code skill that turns the short videos and carousels you have already published on TikTok, Instagram or YouTube into articles on your own website, one page each.

It starts with a short conversation about your set-up, pulls your recent videos and what you said in them, decides which of your site's kinds of page each piece becomes, rewrites the speech as prose for someone who arrived from a search, draws the figures for the page instead of screenshotting the video, checks every number against a source, wires the page into your site, and records where the piece went. It can also set itself up to run on a schedule, with the pages arriving as a pull request for you to read.

Made by [GadirLabs](https://gadirlabs.io). It came out of turning nine videos into nine pages in one evening, and the review that followed.

## Who it is for

Anyone who makes short videos or carousels about their work and wants them findable on their own site, where a search or a link can reach them and a reader can take their time. You need a site that already has at least one article to copy the pattern from. You do not need to be a writer.

## What it asks first

The first time, it asks a few questions and writes the answers into your repository so it never asks again: where you post and your handles; how it should get at the videos (paste the links, use the platform's data export, or connect an API); where the words come from (your captions, the platform's automatic captions, or transcription); where the site lives and which article to copy; what the site lists by hand; any writing rules you keep; whether you want it to run by itself; and, if you answer comments with a keyword automation, which keyword should offer a finished page.

## What it does

1. **Decides what each piece becomes**, from the kinds of page your site already has. A how-to becomes a guide or a recipe page; an explanation becomes an article; an answer to one question becomes an FAQ entry; a video of your own work becomes a case study, a portfolio page or a journal entry; a list stays a list; a promo, a trend or a joke becomes nothing. When the video is the work, a reveal or a dish or a performance, the page is written around the embedded video rather than instead of it. It never invents a kind of page your site does not have.
2. **Gets the videos and what you said.** Three routes per platform, from pasting links to the official APIs: YouTube's Data API and its caption tracks, TikTok's Display API, the Instagram API with Instagram Login, with transcription where a platform exposes no captions. Your own account only, and never a scrape you did not ask for.
3. **Adapts the speech.** Opens with what the reader came for, cuts the feed furniture, keeps your voice, applies any corrections made when the video was reviewed, and sources every number.
4. **Follows your site's pattern exactly**, from the metadata to the way images are imported.
5. **Draws the pictures for the page.** Diagrams as inline SVG in your site's style. Photographs only when they show the subject, credited. Product names as a quiet row of icons or in bold. Never a screenshot of the video's own cards, and never a picture of something the page could render.
6. **Wires the page in, checks and records.** A read as the one reader, a sweep for sentences that are notes rather than content, a build and a link crawl, a look at every figure at desktop and phone width, and a record of where the piece went.
7. **Runs on a schedule, if you want.** As a Claude Code scheduled task (Pro, Max, Ultra, Team or Enterprise): it clones your site, pulls the posts since the last run with their transcripts through a creator-data API key (the included `scripts/pull_posts.py`, reading only your own handles), drafts the pages on a branch and opens a pull request. You read, you merge, you deploy. `routine.md` is the prompt to paste in.

## What it is not

It is not a transcript formatter. It will not paste what you said onto a page. It will not keep a number it cannot source, invent a quotation, scrape a platform you did not point it at, or deploy anything by itself.

## Install

Copy this folder into your skills directory, for example `~/.claude/skills/video-to-article/`, and start a conversation in your website's repository. Say which videos you want turned into pages. It will ask the set-up questions the first time.

## Licence

MIT.
