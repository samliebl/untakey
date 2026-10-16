# Backlog

Ideas for after v0.1. Nothing here is promised; add new ideas here instead of
growing the current build.

## Next up (small)
- `--format json` and `--format csv` for `list`, `check`, `suggest`
- Read combos to check from stdin (`echo "ctrl+opt+cmd+n" | untakey check -`)
- A `conflicts` command: the same combo claimed by more than one thing
- Install shell completions (zsh, bash) with the formula
- Name the remaining system shortcut IDs (currently shown as "System shortcut (ID n)")

## Smarter suggestions
- Rank by physical reach and the fewest keys, not just a fixed tier order
- Mnemonic mode: `untakey suggest --for "sound settings"` prefers S, O, U
- Full-size vs compact keyboards (numpad, Page Up, etc.), via `--keyboard full|compact`
- Option to include punctuation, arrows and numpad keys by default
- Non-US layouts (ISO, JIS, Dvorak): match keys by position, not by character

## More sources
- Keyboard Maestro macros (read the macro plist)
- Alfred workflow and app hotkeys
- BetterTouchTool, via an exported preset
- Shortcuts.app shortcuts with a keyboard shortcut set
- Menu-bar shortcuts inside running apps (needs Accessibility permission; ask first)
- Sandboxed apps (`~/Library/Containers/*/Data/Library/Preferences`)
- Raycast: not possible today (settings export is encrypted)

## Packaging
- Tag v0.1.0, fill in the formula's sha256, publish the tap
- Homebrew `brew audit --strict` pass
- Man page
