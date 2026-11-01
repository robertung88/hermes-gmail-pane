# hermes-gmail-pane

Gmail inside the Hermes Desktop app (Linux/macOS) — as a **dockable pane** beside
the calendar, drive and todoist panes, and as the full-page mailbox.

This is Robert's own package. It started as a fork of
[`guberm/hermes-gmail-desktop-plugin`](https://github.com/guberm/hermes-gmail-desktop-plugin)
v1.0.20 (catalog id `gmail`), which is no longer installed: the local build had
drifted well past upstream (threaded rows, batch actions, the Ask-agent handoff,
the inbox batch read, the cached first page), and every `hermes plugins update
gmail` would have silently reverted it. Upstream declares no licence in its
manifest; this fork is maintained for personal use and credits the original
author in `plugin.yaml`.

## What it does

- **Pane** (right zone, 420 px): the mailbox docked where the other work panes
  live. **Page** (`/gmail`): the same mailbox full-width, with the sidebar nav
  row and the ⌘K "Open Gmail" command.
- Inbox rows grouped per conversation, with count and unread badge; the row
  opens the newest message.
- Reading view: sanitised HTML body, per-message thread, attachments, label
  chips, reply / reply-all (drafts only — see below).
- Reviewed actions: prepare → confirm → commit → readback for archive, trash,
  star, read/unread and label changes, including conversation-scoped batches.
- **Ask agent** on any message or conversation: routes to this chat or to a
  fresh chat in a chosen Hermes profile (the app's own profile registry), and
  submits the message ids, thread id, sender/subject/snippet plus the
  `gog-robert gmail get <id> --format full` command to re-read the body.
- New-mail alert, unread-only filter, "confirm every action" switch, cached
  first page so reopening paints immediately.

## What this fork changes from upstream

- Package and plugin id are `hermes-gmail-pane`, so upstream updates cannot
  overwrite it and the two cannot load side by side.
- A `panes` contribution (id `pane`, right zone) plus a palette command for it;
  upstream registered only a route.
- The local patches that used to be re-applied by hand after each upstream
  update are now simply the code: threaded conversation grouping, batch
  archive/read/star/trash over a thread, the Ask-agent handoff with the profile
  picker, the inbox metadata batch read in `dashboard/plugin_api.py` (5.3 s →
  0.9 s on a 20-message page), and the cached-page seeding with a 10-minute read
  cache.

## Install

```bash
hermes plugins install robertung88/hermes-gmail-pane
```

Then open **Capabilities → Plugins** in the desktop app (that also re-syncs the
desktop half), enable it, and restart the app if the pane does not appear.
`hermes plugins update hermes-gmail-pane` updates it from this repo.

## Credentials

No token ships in this repo. `dashboard/plugin_api.py` reads
`$HERMES_HOME/google_token.json` for the **active profile** at request time (the
same grant the Calendar and Drive panes use) and refreshes in memory without
rewriting the file. A profile without a Gmail grant shows the pane's credential
branch, not an empty inbox.

Note that this pane's **Send really sends** — the `gmail_no_send` guard belongs
to the `gog` CLI and does not apply here. Reply/reply-all create drafts; the
Send button in the composer sends for real.

## Notes

- Desktop + Python halves; the renderer never sees the token — it reaches its
  own backend through `ctx.rest('/…')`, scoped to
  `/api/plugins/hermes-gmail-pane`.
- Plugin settings (confirm-every-action, image blocking, refresh interval) are
  stored per profile+account in plugin storage; a plugin id change means old
  settings do not carry across (re-set them once).
- `plugins.enabled` in the profile config is the gate for the Python half; the
  in-app toggle is separate.
