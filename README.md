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
> never use them. See [What it can and can't see](#what-it-can-and-cant-see).

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

It sees: System Settings shortcuts, App Shortcuts you've added, Services /
Quick Actions / Shortcuts that have a key, and a short list of fixed macOS
shortcuts (⌘Tab, ⌘Q, and so on).

It can't see: shortcuts built into an app's own menus, shortcuts set inside
third-party tools (Keyboard Maestro, Alfred, BetterTouchTool, Raycast), or
sandboxed apps' private settings. "Free" means free of everything above, so a
⌘ combo can still clash with an app. `untakey` adds a note when that's likely.
See [BACKLOG.md](BACKLOG.md) for what's planned.

## Develop

```
bash tests/test.sh
```

## Credits

Written with 🤖 and ❤️ by Sam Liebl & Claude.

MIT licensed.
