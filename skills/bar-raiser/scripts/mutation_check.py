#!/usr/bin/env python3
"""Check that test_loop_check.py catches known bugs in loop_check.py.

Each mutant puts one deliberate bug into a temporary copy of loop_check.py and
runs the unchanged tests against it. Every mutant must make the tests fail.
Run after changing loop_check.py or its tests: python3 mutation_check.py
First it runs the unchanged tests, which must pass. Exit 0 when every mutant is
caught, 1 when one survives, 2 when the unchanged tests fail or a mutant no
longer applies because loop_check.py changed; then update MUTANTS.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent


def python():
    """A real Python interpreter: inside an AppImage, sys.executable can point at the app."""
    if Path(sys.executable).name.startswith("python"):
        return sys.executable
    return shutil.which("python3") or sys.executable

MUTANTS = [
    ("void rounds counted",
     "live = [r for r in sorted(rounds) if r not in void]", "live = sorted(rounds)"),
    ("missing reviewers ignored",
     "missing = sorted(roster - set(actual) - set(held))", "missing = []"),
    ("paused reviewers counted as missing",
     "missing = sorted(roster - set(actual) - set(held))", "missing = sorted(roster - set(actual))"),
    ("pausing disabled",
     "                held[name] = score", "                pass"),
    ("paused reviewers never rejoin",
     "held = {n: s for n, s in held.items() if not all(eff[o] >= s for o in eff if o != n)}", "held = dict(held)"),
    ("target claimed on a carried score",
     "        if result.carried[latest]:", "        if False:"),
    ("progress needs both lowest and mean",
     "                    or mean(current)", "                    and mean(current)"),
    ("rising mean ignored",
     "or mean(current) > max(mean(s) for s in earlier))", "or False)"),
    ("drops compared with the first counted round",
     "before, now = result.effective[counted[-2]], rounds[latest]",
     "before, now = result.effective[counted[0]], rounds[latest]"),
    ("0-to-10 scale not exempt",
     "without_scale = SCALE.sub(\" \", body)", "without_scale = body"),
    ("list numbers not exempt",
     "body = LIST_MARKER.sub(\"\", line)", "body = line"),
    ("evidence contents not scanned",
     "                hits += find_leaks(str(path), text, patterns)", "                pass"),
    ("size limit removed",
     "    if path.stat().st_size > MAX_TEXT_BYTES:\n        return None\n", ""),
    ("score range unchecked",
     "    if not math.isfinite(score) or not 0 <= score <= 10:", "    if False:"),
    ("progress compared with the previous round only",
     "        earlier = [result.effective[r] for r in same_roster]", "        earlier = [result.effective[same_roster[-1]]]"),
    ("progress compared across rosters",
     "        same_roster = [r for r, seg in zip(counted[:index], segments) if seg == segments[index]]",
     "        same_roster = counted[:index]"),
    ("a roster line rewrites a round already scored",
     "        rosters.setdefault(round_number, roster)", "        rosters[round_number] = roster"),
    ("fractional target with trailing zeros missed",
     '''(r"(?:\\.0+)?" if float(target).is_integer() else "0*")''', '''(r"(?:\\.0+)?" if float(target).is_integer() else "")'''),
    ('equal score reported as a drop',
     'if name in before and now[name] < before[name]]',
     'if name in before and now[name] <= before[name]]'),
    ('binary files scanned as text',
     '    if b"\\0" in data:\n        return None\n',
     ''),
    ('a paused reviewer that scored stays carried',
     'held = {n: s for n, s in held.items() if n in roster and n not in actual}',
     'held = {n: s for n, s in held.items() if n in roster}'),
    ('paused reviewer kept after leaving the roster',
     'result.held = {n: s for n, s in held.items() if n in final_roster}',
     'result.held = dict(held)'),
    ('target claimed after a roster change',
     '    if rosters[latest] != final_roster:',
     '    if False:'),
    ('returning roster continues an old count',
     'same_roster = [r for r, seg in zip(counted[:index], segments) if seg == segments[index]]',
     'same_roster = [r for r in counted[:index] if rosters[r] == rosters[counted[index]]]'),
    ('scale exemption covers every slash 10',
     'SCALE = re.compile(r"\\b0\\s+to\\s+10\\b|\\bN\\s*/\\s*10\\b")',
     'SCALE = re.compile(r"\\b0\\s+to\\s+10\\b|/\\s*10\\b")'),
    ('title treated as a numbered list',
     '    hits += find_leaks("title", args.title, patterns)',
     '    hits += find_leaks("title", args.title, patterns, numbered=True)'),
    ("target range unchecked",
     "    if not math.isfinite(value) or not 0 <= value <= 10:", "    if False:"),
]


def run_tests(folder):
    return subprocess.run([python(), str(folder / "scripts" / "test_loop_check.py")],
                          capture_output=True, text=True).returncode


def copy_with(source):
    folder = Path(tempfile.mkdtemp())
    (folder / "scripts").mkdir()
    shutil.copy(HERE.parent / "SKILL.md", folder / "SKILL.md")
    shutil.copy(HERE / "test_loop_check.py", folder / "scripts")
    (folder / "scripts" / "loop_check.py").write_text(source)
    return folder


def main():
    source = (HERE / "loop_check.py").read_text()
    baseline = copy_with(source)
    try:
        if run_tests(baseline) != 0:
            print("baseline failed: the unchanged tests do not pass, so no mutant result means anything")
            return 2
    finally:
        shutil.rmtree(baseline)
    survived = stale = 0
    for name, old, new in MUTANTS:
        if source.count(old) != 1:
            print(f"stale: {name} (its text is not in loop_check.py exactly once)")
            stale += 1
            continue
        copy = copy_with(source.replace(old, new))
        try:
            code = run_tests(copy)
        finally:
            shutil.rmtree(copy)
        if code == 0:
            print(f"SURVIVED: {name}")
            survived += 1
        else:
            print(f"caught: {name}")
    print(f"{len(MUTANTS) - survived - stale} of {len(MUTANTS)} mutants caught")
    return 2 if stale else 1 if survived else 0


if __name__ == "__main__":
    sys.exit(main())
