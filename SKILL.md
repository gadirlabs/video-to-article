---
name: video-to-article
description: Turn a short video or a carousel you have already published into an article on your website. Starts from what you actually said, decides whether the piece is a build-log entry or a standalone article, rewrites speech as prose for a reader, replaces the video's on-screen cards with figures drawn for the page, checks every number against a source, wires the page into your site, and records where the piece went. Use when you have a run of videos or posts and want them findable on your own site, one page each.
---

# Video to article

You are turning a short video, or a carousel, into a page on the person's website. The video did its job on a feed, paced for a voice and a thumb. The page has a different reader: someone who arrived from a search or a link, wants the answer, and will read exactly as long as the page keeps giving them something. Nothing from the video is pasted; everything is adapted.

Work through the six steps in order. Do not start writing before step 1 is settled, and do not ship before step 6 is done.

## What you need from the person

- The video's transcript, corrected: what was actually said, not the script that was written. If only a script exists, say so in the page's record and use it, but the spoken version is the source when there is one. For a carousel, the approved slide copy.
- Where their site keeps articles, and one existing article to copy the pattern from (the file layout, the metadata export, the components for figures and callouts, how images are imported). If the site has a build-log series as well as standalone articles, one of each.
- Their writing rules, if they have any written down. If not, the rules in step 2 apply.
- Any fact-check or review notes made when the video was produced. Apply them.

## 1. Decide what the piece becomes

- **A build-log entry** when the piece reports the person's own project: a stage done, a decision taken, what happened, what is still open. It is a story told in order: what was attempted, what happened, what was decided, what is left. It says plainly what has not been built yet. It never claims a result the work has not produced.
- **A standalone article** when the piece answers a question on its own: how to choose something, where to look for something, why a common habit is wrong. It does not report progress and does not depend on the video.
- The entry for a stage links the article that belongs to that stage, in a short, clearly labelled optional-reading note. The article never assumes the reader saw the video.
- Some pieces should not become a page: a promo, a joke, anything with no explanation in it. Say so and stop.

## 2. Adapt, do not transcribe

Speech becomes prose for a reader who was not there.

- **Open with what the reader came for.** The video's hook was written to stop a thumb; the page's first sentence is short and plain, and the first paragraph gives the answer or the result the title promises. Nothing opens with the process, a definition nobody asked for, or an account of what the series does.
- **Cut the feed furniture.** "Follow for more", "subscribe", "okay bye", the part number, the greeting. The site's layout supplies the author box, the navigation and the next link.
- **Keep the voice, lose the pacing.** The jokes stay where they land on the page and go where they needed the voice. A spoken list becomes a real list. A spoken "he" for a tool becomes "it".
- **Apply the fact-check.** If the video's review found something wrong, the page gets the corrected version, never the spoken error.
- **Never turn notes into content.** A sentence that describes what the piece does, how good the method is, or what the series covers is a note to the writer and goes. Do the thing; never announce it. The forms that slip through: "so you can", "which is why", "there is no", "we always", "we never", "our approach", "that is how", "rather than just". Search for them before shipping.
- **Every number has a source you inspected**, cited beside the claim, with the sources listed at the end. A number without a source is cut or softened to what can be stood behind. A link to a file in a repository is only added if that file is on the public branch.
- **Nothing invented.** No quotation, approval, result, client reaction or decision that is not in the transcript or the project's own records.

## 3. The page

Copy the pattern of the existing article the person gave you, exactly: the same metadata export, the same layout component, the same way of declaring the contents list, the same heading markup, the same image imports. A page that follows the site's conventions needs no explanation; one that invents its own breaks the build or the listing.

- Title and description for listings and search; a short summary that gives the takeaway, who it helps and a qualification where one is needed.
- A contents list for a page with several sections; none for a short piece.
- Headings that say what the section is on their own.
- An optional-reading note where an entry links its stage's article, never an inline aside among the steps.
- A sources list at the end when anything was cited. No compulsory FAQ, no repeated conclusion, no sales pitch.
- Publication date set to the day the page goes live, and never changed afterwards to make old material look new.

## 4. Pictures: each one has to earn its place

These rules came from a real review, and each one was broken before it was written down.

- **Never lift the video's on-screen cards as screenshots.** A card that repeats the heading it sits under, the same idea shown twice because the video spread it over two cards, a frame caught before an animation finished: all of these read as lifted, and they are. A video card is paced for a voice; on a page it duplicates the prose around it.
- **Never ship a picture of something the page could render.** A row of three options, a link in a pill, a before-and-after strip, a tree of folders: draw it as an inline SVG in the site's own style, with the site's colours and fonts, dark mode included, and a title and description for people who cannot see it. A list, a tree or a table is text. A docs folder is a code block; a stack is a bullet list.
- **One figure per idea, and none for anything the prose already carries.** Merge what the video showed in steps into one figure. A page can have no pictures at all: a list of places to look is text with the names in bold, because pictures of them add nothing.
- **A photograph only when it shows the subject of the text.** A photo of the person being quoted belongs beside the quote, with its credit in the caption and its licence in the sources. A render of the thing being discussed belongs where it is discussed, cropped to the subject with no card chrome or on-screen heading. Generated photographs of nobody, illustrating a mood, come out. Where a generated image does stay, the caption says it is generated.
- **Name example products clearly.** A quiet row of their icons with the names beside them, or the names in bold in the sentence. Not a logo wall. Icons are trademarks used to name what is discussed, never to imply endorsement.
- **Reaction clips stay where they live.** Embed a GIF through its host's own embed with a link back; never copy another creator's clip into the site.
- **Look at every drawn figure at both widths before it ships**, as an image, not as a type check. A shallow graph box turns a curve into a wave; a label can cross a ring; a bottom bar can poke past a phone's rounded corners; a two-word label can clip on a phone. Light comes first on a lightness axis when the strips beside it run light to dark. Check a figure's own numbers against the text, and drop a figure whose numbers disagree.
- Convert images yourself, to the format and size the site uses, and keep the conversion to the files you added. A site-wide optimiser run can rewrite images you never touched.

## 5. Wire it in

Whatever the site lists by hand needs the new page added: a series registry, a sitemap, a feed, a plain-text index for AI readers, a navigation. Whatever it lists by scanning a folder needs nothing. Check which is which by reading the site's code, not by assuming.

## 6. Check, record, hand over

1. Read the page once as its one reader, the person who arrived from the title and cannot read code. Mark where they would stall, what they were told that they did not need, and what they needed that is missing. Fix those first.
2. Run the sweep from step 2 for notes-as-content, and for any targeting language, persona names or internal decisions that drifted in.
3. Build the site the way its own instructions say, request the new pages, and crawl their links and anchors. Screenshot every figure at desktop and phone width and look at them.
4. Record where the piece went: in the video's own record, the page's path and the date; in the site's plan, the new pages. Set the publication date to the real day.
5. Commit only when asked. Deploy only when the person authorises it, and tell them everything the deploy would publish, not only your part.

## What this skill will not do

It will not paste a transcript onto a page and call it an article. It will not keep a number it cannot source. It will not invent a quotation or a result. It will not screenshot a video to illustrate a page. It will not deploy on its own.
