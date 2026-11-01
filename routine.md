# The scheduled task's prompt

Paste this as the prompt of a Claude Code scheduled task (claude.ai/code/routines, or `/schedule` in the CLI) whose
repository is your website and whose cloud environment has the network secret or variable `SCRAPECREATORS_API_KEY`
and `api.scrapecreators.com` on its allowed domains. Weekly is a good cadence. Change the folder paths if yours differ.

---

You are in my website's repository. Use the `video-to-article` skill in `.claude/skills/video-to-article/` and its
brief in `docs/video-to-article/brief.md`.

1. Run `python3 .claude/skills/video-to-article/scripts/pull_posts.py --config docs/video-to-article/config.json`.
   It writes today's new posts, with their words, to `docs/video-to-article/inbox/`. If it reports nothing new, stop
   here and push nothing.
2. For each new item (a video posted on more than one platform arrives as one item with the others under `also_on`), decide which kind of page it becomes, following the skill's step 1, and say which and why in
   your summary. Skip what should not become a page.
3. Write each page the way the skill says (steps 3 to 6): adapted for a reader, the site's own pattern, figures drawn
   for the page, every number sourced, the site's listings updated, the site's build run and passing.
4. Add each page to `docs/video-to-article/done.json` with the post's platform, id and the page's path, so the next run
   skips it.
5. Commit on a branch named `claude/video-to-article-<today>` and push it. Open a pull request titled
   "Pages from this week's videos" whose description lists each video, the page it became and anything left out, with
   the reason. Do not deploy, and do not push to the default branch.
