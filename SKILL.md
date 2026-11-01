---
name: video-to-article
description: Turn the short videos and carousels you have already published on TikTok, Instagram or YouTube into articles on your own website, one page each. Starts with a short conversation about your set-up, pulls your recent videos and what you said in them, decides whether each piece is a build-log entry or a standalone article, rewrites speech as prose for a reader, draws the figures for the page instead of screenshotting the video, checks every number against a source, wires the page into your site, records where it went, and can set itself up to run on a schedule. Use when you have a run of videos or posts and want them findable on your own site.
---

# Video to article

You are turning someone's short videos, or carousels, into pages on their website. The video did its job on a feed, paced for a voice and a thumb. The page has a different reader: someone who arrived from a search or a link, wants the answer, and will read exactly as long as the page keeps giving them something. Nothing from the video is pasted; everything is adapted.

Work through the steps in order. Step 0 happens once, the first time; after that the answers live in a file in the project and you read it. Do not start writing before step 1 is settled for a piece, and do not ship before step 6 is done.

## 0. The first conversation: find out the set-up

The first time, before touching anything, ask. Keep it to one short exchange, and write the answers to `docs/video-to-article.md` in the website's repository so you never ask again.

1. **Where do you post?** TikTok, Instagram, YouTube, or more than one. For each, the handle or channel.
2. **How should I get at the videos?** The three routes, from least to most set-up, are in step 2. Offer them; take the one they choose. Never scrape a platform without being told to, and never use anyone else's account.
3. **Where do the words come from?** Captions they wrote themselves, the platform's automatic captions, or nothing yet, in which case transcription happens here.
4. **Where is the site, and which article do I copy?** The repository, where articles live, one existing article to take the pattern from, and whether the site also has a build-log series.
5. **What lists pages by hand?** A series registry, a sitemap, a feed, a navigation, an index for AI readers. Anything not scanned from a folder needs editing when a page is added.
6. **Any writing rules?** If they have them written down, read them. If not, the rules in step 3 apply.
7. **Do you want this to run by itself?** If yes, step 7 sets up a scheduled routine, and that needs a Claude plan that includes routines, plus a way to reach the platforms without a browser (an API token or an export). Say so plainly before promising it.
8. **Do you still have the files the video was made from?** Optional, and often the answer is no. The drawings' source (a design file, an overlay, a slide deck), the screen recordings, the renders, the clips of a character, the data behind a chart. They make the page's figures faster and truer: a figure is redrawn for the page either way, but from the source it keeps the real numbers, the real screens and the real character. Without them, the published video is enough; frames are read as a reference, never pasted.
9. **How do you share what you publish?** Optional. If they answer comments or direct messages with a keyword automation (ManyChat or similar), note it: a finished page can be offered as that automation's reply, and the page's own record should say which keyword sends it.

Record the answers, the date, and what was left undecided. That file is the brief for every later run.

## 1. Decide what each piece becomes

- **A build-log entry** when the piece reports the person's own project: a stage done, a decision taken, what happened, what is still open. It is a story told in order: what was attempted, what happened, what was decided, what is left. It says plainly what has not been built yet. It never claims a result the work has not produced.
- **A standalone article** when the piece answers a question on its own: how to choose something, where to look for something, why a common habit is wrong. It does not report progress and does not depend on the video.
- The entry for a stage links the article that belongs to that stage, in a short, clearly labelled optional-reading note. The article never assumes the reader saw the video.
- Some pieces should not become a page: a promo, a joke, a dance, anything with no explanation in it. Say so and move on.

## 2. Get the videos and what was said

Work from what was actually said, never from a script that was written beforehand. The routes below were checked against each platform's own documentation on 31 October 2026; platforms change these, so if a call fails, read the current page before guessing.

**The three routes, for any platform.** Offer all three in step 0.

- *Paste.* The person gives you the link to each video and its transcript or caption, by hand. No set-up, works today, fine for a handful.
- *Export.* Each platform lets an account download its own data as a file. TikTok: Settings → Account → Download your data (a JSON or text file listing each post with its link, description and date). Instagram: Accounts Centre → Your information and permissions → Download your information. YouTube: Google Takeout, which includes the channel's videos and their metadata. Exports arrive after a wait and contain the person's own posts only.
- *API.* The official route for a routine. It needs a developer app, a token, and for some platforms an approval step. Details per platform below.

**YouTube.** The YouTube Data API v3 lists a channel's own uploads (`channels.list` for the uploads playlist, then `playlistItems.list`) and `captions.list` shows the caption tracks on a video; `captions.download` needs an OAuth token from the video's owner and returns the track. Several guides report that it returns only captions the owner uploaded, not YouTube's automatic ones; for automatic captions, `yt-dlp --write-auto-subs --sub-langs "en.*" --skip-download "URL"` fetches the subtitle file without the video, and `--cookies-from-browser` lets it reach the person's own unlisted videos. yt-dlp reads public pages, not an API, so it can break when YouTube changes and it should only ever be pointed at the person's own videos.

**TikTok.** The Display API's `POST /v2/video/list/` (scope `video.list`, through Login Kit) returns the account's own public videos, newest first, up to 20 per page with a cursor, and each video's `id`, `create_time`, `title`, `video_description`, `duration`, `share_url`, `embed_link`, `cover_image_url` and the counts. No field is a link to the video file, and TikTok's automatic captions are not exposed, so for the words either take the caption the person wrote, or get the file (the app's own Save video, the data export, or yt-dlp on `share_url`) and transcribe it in step 2b. The app needs TikTok's approval for Login Kit and the Display API before the token works.

**Instagram.** The Instagram API with Instagram Login: a professional account (Business or Creator), a Business-type Meta app, the `instagram_business_basic` permission (it reads the account's own profile and media; an app reading only the owner's account does not need App Review, which Meta requires for data you do not own), and a token from the App Dashboard (long-lived, 60 days). `GET https://graph.instagram.com/<version>/<IG_ID>/media` lists the account's media; ask for the fields `id, caption, media_type, media_product_type, media_url, permalink, thumbnail_url, timestamp`, and keep `media_product_type = REELS` for the videos. `media_url` is left out for any video that contains licensed audio, including the person's own, so a Reel with music may have no file to fetch; the caption is still there, and the data export has the file. Instagram's automatic captions are not exposed either; transcribe.

**2b. Transcription.** When there is a file and no written words, transcribe locally: whisper.cpp or faster-whisper with a large model, English or whichever language they speak. Correct the names and the product terms by hand before writing; a transcript with the wrong name in it ends up as a page with the wrong name in it. Keep the transcript beside the page's record.

Keep a list of what has been turned into a page already, with each video's id and the page's path, in the same `docs/video-to-article.md`, so a run only looks at what is new.

## 3. Adapt, do not transcribe

Speech becomes prose for a reader who was not there.

- **Open with what the reader came for.** The video's hook was written to stop a thumb; the page's first sentence is short and plain, and the first paragraph gives the answer or the result the title promises. Nothing opens with the process, a definition nobody asked for, or an account of what the series does.
- **Cut the feed furniture.** "Follow for more", "subscribe", "okay bye", the part number, the greeting. The site's layout supplies the author box, the navigation and the next link.
- **Keep the voice, lose the pacing.** The jokes stay where they land on the page and go where they needed the voice. A spoken list becomes a real list. A spoken "he" for a tool becomes "it".
- **Apply any review notes** made when the video was produced. The page gets the corrected version, never the spoken error.
- **Never turn notes into content.** A sentence that describes what the piece does, how good the method is, or what the series covers is a note to the writer and goes. Do the thing; never announce it. The forms that slip through: "so you can", "which is why", "there is no", "we always", "we never", "our approach", "that is how", "rather than just". Search for them before shipping.
- **Every number has a source you inspected**, cited beside the claim, with the sources listed at the end. A number without a source is cut or softened to what can be stood behind. A link to a file in a repository is only added if that file is on the public branch.
- **Nothing invented.** No quotation, approval, result, client reaction or decision that is not in the transcript or the project's own records.

## 4. The page

Copy the pattern of the existing article the person gave you, exactly: the same metadata export, the same layout component, the same way of declaring the contents list, the same heading markup, the same image imports. A page that follows the site's conventions needs no explanation; one that invents its own breaks the build or the listing.

- Title and description for listings and search; a short summary that gives the takeaway, who it helps and a qualification where one is needed.
- A contents list for a page with several sections; none for a short piece.
- Headings that say what the section is on their own.
- An optional-reading note where an entry links its stage's article, never an inline aside among the steps.
- A sources list at the end when anything was cited. No compulsory FAQ, no repeated conclusion, no sales pitch.
- Publication date set to the day the page goes live, and never changed afterwards to make old material look new.

## 5. Pictures: each one has to earn its place

These rules came from real reviews, and each one was broken before it was written down.

- **The page carries the video's visual weight.** Every idea the video spent a drawing on becomes a figure on the page, one per idea, redrawn for the page. A video that was half drawings once became a page with one table under a thousand words, and read as a wall of text; its sibling kept all six of its drawings and read like the video. Before shipping, list the video's graphics beside the page's figures: a page with far fewer has lost something. Architecture and system drawings are the ones a build-log reader comes for.
- **A GIF or a graphic where the video had a GIF, by tone.** The reaction clip does not have to return as the same GIF, or as a GIF at all; it can be a GIF, a drawn graphic or nothing. The test is whether the page keeps the tone of the line it sat on: a joke that survives as a joke can carry a GIF; a hook that is gone from the page takes its GIF with it. Feel the tone of the paragraph before deciding, and never decorate a paragraph that has become plain prose.

- **Never lift the video's on-screen cards as screenshots.** A card that repeats the heading it sits under, the same idea shown twice because the video spread it over two cards, a frame caught before an animation finished: all of these read as lifted, and they are. A video card is paced for a voice; on a page it duplicates the prose around it.
- **Never ship a picture of something the page could render.** A row of three options, a link in a pill, a before-and-after strip, a tree of folders: draw it as an inline SVG in the site's own style, with the site's colours and fonts, dark mode included, and a title and description for people who cannot see it. A list, a tree or a table is text. A docs folder is a code block; a stack is a bullet list.
- **One figure per idea, and none for anything the prose already carries.** Merge what the video showed in steps into one figure. A page can have no pictures at all: a list of places to look is text with the names in bold, because pictures of them add nothing.
- **A photograph only when it shows the subject of the text.** A photo of the person being quoted belongs beside the quote, with its credit in the caption and its licence in the sources. A render of the thing being discussed belongs where it is discussed, cropped to the subject with no card chrome or on-screen heading. Generated photographs of nobody, illustrating a mood, come out. Where a generated image does stay, the caption says it is generated.
- **Name example products clearly.** A quiet row of their icons with the names beside them, or the names in bold in the sentence. Not a logo wall. Icons are trademarks used to name what is discussed, never to imply endorsement.
- **Reaction clips stay where they live.** Embed a GIF through its host's own embed with a link back; never copy another creator's clip into the site.
- **The person's own clip can come to the page as a short loop.** A character, a render in motion, a few seconds of their own screen: convert it to a small muted video (H.264, a few seconds, under a megabyte, with a poster image) and play it inline, looping, with no controls, the way a GIF would play. A GIF file is larger and looks worse. Credit nothing; it is theirs.
- **Look at every drawn figure at both widths before it ships**, as an image, not as a type check. A shallow graph box turns a curve into a wave; a label can cross a ring; a bottom bar can poke past a phone's rounded corners; a two-word label can clip on a phone. Light comes first on a lightness axis when the strips beside it run light to dark. Check a figure's own numbers against the text, and drop a figure whose numbers disagree.
- Convert images yourself, to the format and size the site uses, and keep the conversion to the files you added. A site-wide optimiser run can rewrite images you never touched.

## 6. Wire it in, check, record

1. Whatever the site lists by hand needs the new page added: a series registry, a sitemap, a feed, a plain-text index for AI readers, a navigation. Check which is which by reading the site's code, not by assuming.
2. Read the page once as its one reader, the person who arrived from the title and cannot read code. Mark where they would stall, what they were told that they did not need, and what they needed that is missing. Fix those first.
3. Run the sweep from step 3 for notes-as-content, and for any internal decisions that drifted in.
4. Build the site the way its own instructions say, request the new pages, and crawl their links and anchors. Screenshot every figure at desktop and phone width and look at them.
5. Record where the piece went in `docs/video-to-article.md`: the video's id and link, the page's path, the date, and which keyword automation offers it, if any.
6. Commit only when asked. Deploy only when the person authorises it, and tell them everything the deploy would publish, not only your part.

## 7. Run it on a schedule

If the person said yes in step 0, set the work up as a Claude Code **scheduled task** (the docs' current name for a routine). The facts below are from the Claude Code documentation as read on 31 October 2026; the feature is in research preview, so check `code.claude.com/docs/en/routines` before promising a detail.

- **Who can.** Scheduled tasks are on the Pro, Max, Ultra, Team and Enterprise plans, and each run draws on the plan's usage like an ordinary session. Someone on the free plan runs this skill by hand instead, which works just as well, one conversation a week.
- **How.** `/schedule` in the terminal, or claude.ai/code/routines, with the website repository attached. Weekly is the right cadence for most people; the smallest interval allowed is hourly. Each run is a fresh cloud session that clones the repository, so everything the run needs has to be in the repository or reachable over the network: the set-up file from step 0, the list of pages already made, the transcripts.
- **What a run does.** Read `docs/video-to-article.md`; fetch the account's videos since the last run through the route chosen in step 0; for each one with words available, write the page exactly as in steps 1 to 6; commit to a `claude/` branch; open a draft pull request that lists the videos found, the pages written, and the ones skipped for having no transcript. The person reads, merges and deploys. A run never deploys and never pushes to the default branch.
- **Reaching the platforms.** The cloud environment's network access is a list of allowed hosts. Google's API hosts are on the default list, so the YouTube route works as is; TikTok's and Meta's hosts have to be added under Custom access. API keys go in as **network secrets**, which the proxy attaches to requests for the hosts you name and which never enter the session; never put a key in an environment variable, where anyone using the environment can read it.
- **Words without captions.** The cloud session has no transcription tool. Where a platform gives captions (YouTube's own tracks, or captions the person wrote), the run has what it needs. Where it does not (a TikTok or a Reel with no caption), the run lists the video in the pull request as waiting for a transcript, and the person adds the transcript by hand or through a hosted transcription service reached with a network secret. Do not promise automatic transcription of TikToks and Reels in the cloud; say what the routine will and will not do.
- **Limits worth knowing.** Runs can start a few minutes after the scheduled time; a task can be fired at most thirty times an hour; a command inside a run times out after two minutes unless the prompt raises it. Keep each run small: a handful of videos, not a back catalogue. The back catalogue is a conversation.

Write the routine's prompt as a short brief that points at the set-up file and this skill, names the branch and the pull-request format, and says plainly that it must not deploy.


## What this skill will not do

It will not paste a transcript onto a page and call it an article. It will not keep a number it cannot source. It will not invent a quotation or a result. It will not screenshot a video to illustrate a page. It will not scrape a platform it was not told to, or use an account that is not the person's own. It will not deploy on its own.
