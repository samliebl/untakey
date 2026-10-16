#!/usr/bin/env bash
# Tests for untakey. Run: bash tests/test.sh   (needs bash 4+, macOS for the smoke tests)

if (( BASH_VERSINFO[0] < 4 )); then echo "tests need bash 4+ (brew install bash)"; exit 2; fi
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
KF="$ROOT/bin/untakey"
# shellcheck source=../bin/untakey
source "$KF"
set +e

pass=0 fail=0
ok() { pass=$((pass + 1)); }
bad() { fail=$((fail + 1)); printf 'FAIL: %s\n' "$1"; }
eq() { [[ $2 == "$3" ]] && ok || bad "$1: expected '$3', got '$2'"; }
combo() { parse_combo "$1" && echo "$PC_COMBO" || echo "ERR"; }
menu() { parse_menu_string "$1" && echo "$PM_COMBO" || echo "ERR"; }

# ---- typed combos
eq "words"        "$(combo 'ctrl+opt+cmd+n')"       "ctrl+opt+cmd+n"
eq "symbols"      "$(combo '⌃⌥⌘N')"                  "ctrl+opt+cmd+n"
eq "dashes"       "$(combo 'Cmd-Shift-4')"          "shift+cmd+4"
eq "order"        "$(combo 'cmd+shift+ctrl+x')"     "ctrl+shift+cmd+x"
eq "aliases"      "$(combo 'control+option+command+F5')" "ctrl+opt+cmd+f5"
eq "plus key"     "$(combo 'cmd++')"                "shift+cmd+="
eq "minus key"    "$(combo 'cmd+-')"                "cmd+-"
eq "shifted char" "$(combo 'cmd+?')"                "shift+cmd+/"
eq "arrow"        "$(combo 'ctrl+Left')"            "ctrl+left"
eq "bracket"      "$(combo 'cmd+[')"                "cmd+["
eq "bad key"      "$(combo 'cmd+nope')"             "ERR"
eq "fn rejected"  "$(combo 'fn+a')"                 "ERR"
eq "empty key"    "$(combo 'cmd+')"                 "ERR"

# ---- macOS menu-string notation
eq "menu basic"   "$(menu '@$k')"                   "shift+cmd+k"
eq "menu upper"   "$(menu '@K')"                    "shift+cmd+k"
eq "menu f11"     "$(menu '^\Uf70e')"               "ctrl+f11"
eq "menu f12 dbl" "$(menu '^\\Uf70f')"              "ctrl+f12"
eq "menu all"     "$(menu '@~^n')"                  "ctrl+opt+cmd+n"
eq "menu symbol"  "$(menu '@?')"                    "shift+cmd+/"
eq "menu digit"   "$(menu '$4')"                    "shift+4"
eq "menu arrow"   "$(menu '~\Uf702')"               "opt+left"
eq "menu return"  "$(menu '@\U21a9')"               "cmd+return"
eq "menu junk"    "$(menu '@\Uffff')"               "ERR"

# ---- display
pretty_combo "ctrl+opt+cmd+n"; eq "pretty" "$KL" "⌃⌥⌘N"
pretty_combo "shift+cmd+left"; eq "pretty arrow" "$KL" "⇧⌘←"
eq "ascii table" "${#ASCII}" "94"

# ---- suggestions never include a taken combo, and respect -n
TAKEN=([ctrl+opt+cmd+a]=x [ctrl+opt+cmd+s]=x)
MODSETS=("${DEFAULT_MODSETS[@]}") KEYS=("${DEFAULT_KEYS[@]}")
suggest_collect 3
eq "skips taken" "${SUGG[*]}" "11 d 11 f 11 g"
suggest_collect 100
eq "caps at n" "${#SUGG[@]}" "100"

# ---- command line behaviour
run() { "$KF" "$@" >/dev/null 2>&1; echo $?; }
eq "version"        "$("$KF" --version)" "untakey 0.1.0"
eq "n=0"            "$(run suggest -n 0)"   "2"
eq "n=101"          "$(run suggest -n 101)" "2"
eq "n=abc"          "$(run suggest -n abc)" "2"
eq "bad combo"      "$(run check nope)"     "2"
eq "no args check"  "$(run check)"          "2"
eq "bad command"    "$(run frobnicate)"     "2"
eq "bad option"     "$(run list --nope)"    "2"
eq "bad source"     "$(run list --source x)" "2"

# ---- smoke tests against this Mac's real settings
if [[ $(uname) == Darwin ]]; then
  eq "cmd+q taken"    "$("$KF" check cmd+q --plain | cut -f2)" "taken"
  eq "check exit 1"   "$(run check cmd+q)" "1"
  eq "list columns"   "$("$KF" list --plain | head -1 | awk -F'\t' '{print NF}')" "3"
  sugg=$("$KF" suggest -n 12 --plain)
  eq "suggest count"  "$(wc -l <<<"$sugg" | tr -d ' ')" "12"
  # round trip: everything suggested must check out as free
  # shellcheck disable=SC2086
  eq "suggest is free" "$("$KF" check $sugg --plain | cut -f2 | sort -u)" "free"
fi

printf '%d passed, %d failed\n' "$pass" "$fail"
(( fail == 0 ))
