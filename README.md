# untakey

Find a free keyboard shortcut on your Mac, or check whether one is taken.

macOS has no single place that lists every shortcut in use. `untakey` reads the
places shortcuts live (System Settings, per-app shortcuts, Services, Quick
Actions and Shortcuts) and answers three questions:

```
untakey list                  # what's taken?
untakey check ctrl+opt+cmd+n  # is this one free?
untakey suggest -n 10         # give me ten free ones
```

**100% bash.** One readable script, no Python, no Node, no compiled code. It
uses only tools every Mac already has (`defaults`, `plutil`, `awk`), plus bash 5,
which Homebrew installs for you. It only reads your preferences and never
changes anything.

> **Read this first: "free" means free of the shortcuts untakey can read, not
> free of every shortcut on your Mac.** It cannot see the shortcuts built into
> apps' own menus (⌘S, ⌘N, ⌘B and so on), hotkeys set inside tools like
> Keyboard Maestro, Alfred, BetterTouchTool or Raycast, or a few shortcuts macOS
> handles internally. Combos that use ⌃⌥⌘ are the safest bet, because apps almost
> never use them. macOS also only records a system shortcut once you change it,
> so untakey fills the gaps with a built-in list of factory defaults (details
> below). See [What it can and can't see](#what-it-can-and-cant-see).

## Install

```
brew tap samliebl/untakey https://github.com/samliebl/untakey
brew install untakey
```

Homebrew installs bash 5 for you. To run from a checkout instead, you need
bash 4 or newer (`brew install bash`; macOS itself ships 3.2).

## Use

```
$ untakey suggest -n 4
#  SHORTCUT  NOTES
1  ⌃⌥⌘A      -
2  ⌃⌥⌘S      -
3  ⌃⌥⌘D      -
4  ⌃⌥⌘F      -

$ untakey check cmd+q ctrl+opt+cmd+z
SHORTCUT  STATUS   DETAILS
⌘Q        ✗ Taken  macOS: Quit app
⌃⌥⌘Z      ✓ Free   -
```

Write shortcuts as `ctrl+opt+cmd+n` or `⌃⌥⌘N`. Modifiers: `ctrl`, `opt` (or
`alt`), `shift`, `cmd`.

### suggest

| Option | Meaning |
| --- | --- |
| `-n 1..100` | How many to show (default 10; anything outside 1–100 is an error) |
| `--mods SETS` | Comma-separated modifier sets to use, e.g. `ctrl+opt,ctrl+opt+cmd` |
| `--keys KEYS` | Comma-separated keys to try, e.g. `n,t,f5` |

Suggestions come safest first: ⌃⌥⌘, then ⌃⌥, ⌃⌘, ⌥⌘, then the same with ⇧
added. Plain ⌘, ⌥ or ⇧ combos are left out on purpose: apps use ⌘ in their
menus, and ⌥ and ⇧ combos make text characters.

### Scripting

When output is piped (or with `--plain`) you get plain text with no colors:
tab-separated for `list` and `check`, one combo per line for `suggest`.

`untakey check` exits `0` if every combo is free, `1` if any is taken, and `2`
for bad input. Set `NO_COLOR=1` to turn colors off.

```
untakey check ctrl+opt+cmd+n && echo "go ahead"
untakey suggest -n 3 --plain | pbcopy
untakey list --plain > shortcuts.txt
```

## What it can and can't see

**It sees:**
- Your System Settings shortcuts, plus macOS's factory defaults for any you
  haven't touched (see below)
- App Shortcuts you've added yourself
- Services, Quick Actions and Shortcuts that have a key
- A short built-in list of fixed macOS shortcuts (⌘Tab, ⌘Q, and so on)

**It can't see:**
- Shortcuts built into an app's own menus
- Hotkeys set inside third-party tools (Keyboard Maestro, Alfred,
  BetterTouchTool, Raycast)
- App Shortcuts for sandboxed apps, which store their settings elsewhere

"Free" means free of everything in the first list, so a ⌘ combo can still clash
with an app. `untakey` adds a note when that's likely.

### The factory-defaults baseline

macOS only writes a System Settings shortcut into your preferences once you
change it. On a fresh account the preferences hold almost nothing, so reading
them alone would call ⌘Space (Spotlight) "free". To avoid that, `untakey` has a
built-in list of 16 common macOS defaults (Spotlight, screenshots, Mission
Control, switching spaces, and so on). A default is used only when your
preferences don't mention that shortcut at all, so anything you've changed or
turned off is respected.

The list covers the common defaults, not every one, and it was written from
what macOS does today, so a future macOS could differ. If your preferences
can't be read, `untakey` says so and falls back to the defaults.

### Other things to know

- **Tested on one Mac so far** (Apple silicon). It relies on the text layout of
  `plutil -p` and `defaults`, which Apple could change in a future macOS.
- **US keyboard layout only.** Keys are matched by character, not by physical
  position. Other layouts (Dvorak, ISO, JIS) aren't handled yet.
- **The `fn` key is ignored.** Shortcuts that need it are skipped.
- **Cautious about Services.** A Service or Shortcut with a key assigned counts
  as taken even if you've switched it off.
- **Some system shortcuts have no name yet** and show as "System shortcut (ID
  n)".
- **It takes a second or two to run**, because it reads your preferences each
  time.

See [BACKLOG.md](BACKLOG.md) for what's planned.

## Develop

```
bash tests/test.sh
```

## Credits

Written with 🤖 and ❤️ by Sam Liebl & Claude (Anthropic).

MIT licensed.
