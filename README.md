# Video to article

A free Claude Code skill that turns the short videos and carousels you have already published into articles on your own website, one page each.

You give it what you actually said and one existing article from your site to copy. It decides whether the piece is a build-log entry or a standalone article, rewrites the speech as prose for someone who arrived from a search, draws the figures for the page instead of screenshotting the video, checks every number against a source, wires the page into your site, and records where the piece went.

Made by [GadirLabs](https://gadirlabs.io). It came out of turning nine videos into nine pages in one evening, and the review that followed.

## Who it is for

Anyone who makes short videos or carousels about their work and wants them findable on their own site, where a search or a link can reach them and a reader can take their time. You need a site that already has at least one article to copy the pattern from. You do not need to be a writer.

## What it does

1. **Decides what each piece becomes.** A build-log entry when the video reports your own project; a standalone article when it answers a question on its own; nothing at all when it is a promo or a joke.
2. **Adapts the speech.** Opens with what the reader came for, cuts the feed furniture, keeps your voice, applies any corrections made when the video was reviewed, and sources every number.
3. **Follows your site's pattern exactly**, from the metadata to the way images are imported.
4. **Draws the pictures for the page.** Diagrams as inline SVG in your site's style. Photographs only when they show the subject, credited. Product names as a quiet row of icons or in bold. Never a screenshot of the video's own cards, and never a picture of something the page could render.
5. **Wires the page in** wherever your site lists pages by hand.
6. **Checks and records.** A read as the one reader, a sweep for sentences that are notes rather than content, a build and a link crawl, a look at every figure at desktop and phone width, and a record of where the piece went.

## What it is not

It is not a transcript formatter. It will not paste what you said onto a page. It will not keep a number it cannot source, invent a quotation, or deploy anything by itself.

## Install

Copy this folder into your skills directory, for example `~/.claude/skills/video-to-article/`, and start a conversation in your website's repository. Give it the transcript, point it at one existing article, and tell it which pages list articles by hand.

## Licence

MIT.
