#!/usr/bin/env python3
"""Tests for loop_check.py. Run after any change to it: python3 test_loop_check.py"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("loop_check.py")
SKILL = Path(__file__).parent.parent / "SKILL.md"


def python():
    """A real Python interpreter: inside an AppImage, sys.executable can point at the app."""
    if Path(sys.executable).name.startswith("python"):
        return sys.executable
    return shutil.which("python3") or sys.executable


def run(*args):
    result = subprocess.run([python(), str(SCRIPT), *map(str, args)], capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


def numbered_brief(work="the pricing page"):
    """Render the brief template from SKILL.md with its list numbers, as an agent would write it."""
    literal = {}
    for line in SKILL.read_text().splitlines():
        for item in ("1", "8", "9"):
            if line.startswith(f"{item}. ") and line.endswith('"'):
                literal[item] = line[line.index('"') + 1:-1].replace("<the work>", work)
    assert set(literal) == {"1", "8", "9"}, "the brief template lines in SKILL.md moved"
    return "\n".join([
        f"1. {literal['1']}",
        "2. The request: make the pricing page clearer for new customers, judged by our style guide.",
        "3. The work: /srv/app/pricing.html, built by `make site`.",
        "4. The evidence folder: /tmp/share/review-evidence/",
        "5. The platform docs: /srv/app/docs/",
        "6. The price table: /srv/app/data/prices.csv",
        "7. Verified facts: the page must load without JavaScript.",
        f"8. {literal['8']}",
        f"9. {literal['9']}",
    ]) + "\n"


class Fixture(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.root = Path(self.dir.name)

    def tearDown(self):
        self.dir.cleanup()

    def fresh(self):
        self.dir.cleanup()
        self.setUp()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path


class Scores(Fixture):
    def check(self, lines, target=9):
        log = self.write("scores.tsv", "".join(line + "\n" for line in lines))
        return run("scores", "--target", target, log)

    def decision(self, lines, target=9):
        code, out = self.check(lines, target)
        self.assertEqual(code, 0, out)
        return out.split("Decision: ")[1].strip()

    def test_target_reached_when_every_reviewer_meets_it(self):
        lines = ["roster\ta,b", "1\ta\t8", "1\tb\t8", "2\ta\t9", "2\tb\t9.5"]
        self.assertEqual(self.decision(lines), "target reached")

    def test_one_reviewer_below_target_continues(self):
        lines = ["roster\ta,b", "1\ta\t8", "1\tb\t8", "2\ta\t9", "2\tb\t8.5"]
        self.assertEqual(self.decision(lines), "continue")

    def test_a_rising_mean_alone_counts_as_progress(self):
        lines = ["roster\ta,b", "1\ta\t8", "1\tb\t8", "2\ta\t8", "2\tb\t8", "3\ta\t8", "3\tb\t8.5"]
        self.assertEqual(self.decision(lines), "continue")

    def test_a_rising_lowest_alone_counts_as_progress(self):
        lines = ["roster\ta,b", "1\ta\t7", "1\tb\t10", "2\ta\t7", "2\tb\t10", "3\ta\t8", "3\tb\t9"]
        self.assertEqual(self.decision(lines), "continue")

    def test_swinging_scores_change_approach_then_ask(self):
        swing = ["roster\ta,b", "1\ta\t8", "1\tb\t9", "2\ta\t9", "2\tb\t8", "3\ta\t8", "3\tb\t9"]
        self.assertEqual(self.decision(swing), "change the approach: no progress for 2 rounds")
        self.assertEqual(self.decision(swing + ["4\ta\t9", "4\tb\t8"]), "ask the user: no progress for 3 rounds")

    def test_progress_must_beat_every_earlier_round_not_just_the_previous_one(self):
        lines = ["roster\ta", "1\ta\t9", "2\ta\t7", "3\ta\t8", "4\ta\t8.5"]
        self.assertEqual(self.decision(lines), "ask the user: no progress for 3 rounds")

    def test_a_roster_change_starts_a_fresh_progress_count(self):
        lines = ["roster\ta,b", "1\ta\t8", "1\tb\t9", "2\ta\t8.5", "2\tb\t9",
                 "roster\ta,c", "3\ta\t8.5", "3\tc\t7", "4\ta\t8.5", "4\tc\t7.5"]
        self.assertEqual(self.decision(lines), "continue")

    def test_returning_to_an_earlier_roster_still_starts_a_fresh_count(self):
        lines = ["roster\ta,b", "1\ta\t8", "1\tb\t8", "2\ta\t8", "2\tb\t8",
                 "roster\ta,c", "3\ta\t8", "3\tc\t8", "4\ta\t8", "4\tc\t8",
                 "roster\ta,b", "5\ta\t8", "5\tb\t8"]
        self.assertEqual(self.decision(lines), "continue")

    def test_a_reviewer_added_after_the_last_round_blocks_the_target(self):
        code, out = self.check(["roster\ta", "1\ta\t9", "roster\ta,b"])
        self.assertIn("Decision: continue: the roster changed after round 1", out)
        self.assertIn("Next round: a, b", out)

    def test_an_equal_score_is_not_a_drop(self):
        code, out = self.check(["roster\ta", "1\ta\t8", "2\ta\t8"])
        self.assertNotIn("Dropped", out)

    def test_progress_after_a_stall_resets_the_count(self):
        lines = ["roster\ta", "1\ta\t8", "2\ta\t8", "3\ta\t8", "4\ta\t8.5"]
        self.assertEqual(self.decision(lines), "continue")

    def test_missing_reviewer_in_latest_round_is_incomplete(self):
        lines = ["roster\ta,b", "1\ta\t8", "1\tb\t8", "2\ta\t9"]
        self.assertEqual(self.decision(lines), "incomplete: round 2 has no score from b")

    def test_single_score_cannot_reach_the_target(self):
        lines = ["roster\tsol,opus,flash", "1\tsol\t9"]
        self.assertEqual(self.decision(lines), "incomplete: round 1 has no score from flash, opus")

    def test_incomplete_middle_round_is_marked_and_not_counted(self):
        code, out = self.check(["roster\ta,b", "1\ta\t8", "1\tb\t8", "2\ta\t9", "3\ta\t8.5", "3\tb\t8.5"])
        self.assertIn("| 2 (incomplete) |", out)
        self.assertIn("Not counted, incomplete: round 2", out)
        self.assertIn("Decision: continue", out)

    def test_void_round_is_not_counted(self):
        voided = ["roster\ta,b", "1\ta\t8", "1\tb\t8", "2\ta\t9", "2\tb\t9", "void\t2"]
        self.assertEqual(self.decision(voided), "continue")
        self.assertEqual(self.decision(voided + ["3\ta\t8.5", "3\tb\t8.5"]), "continue")

    def test_scoring_a_void_round_again_is_rejected(self):
        code, out = self.check(["roster\ta", "1\ta\t8", "void\t1", "1\ta\t9"])
        self.assertEqual(code, 2, out)
        self.assertIn("give a fresh round the next number", out)

    def test_names_ignore_letter_case_and_scores_accept_out_of_10(self):
        lines = ["roster\tOpus,Sol", "1\topus\t8/10", "1\tSOL\t8", "2\tOpus\t9/10", "2\tsol\t9"]
        self.assertEqual(self.decision(lines), "target reached")

    def test_drops_compare_with_the_previous_counted_round(self):
        code, out = self.check(["roster\ta,b", "1\ta\t9", "1\tb\t7", "2\ta\t8", "2\tb\t9"])
        self.assertIn("Dropped since the previous counted round: a 9 -> 8", out)
        code, out = self.check(["roster\ta", "1\ta\t9", "2\ta\t7", "3\ta\t8"])
        self.assertNotIn("Dropped", out)

    def test_output_states_the_target(self):
        code, out = self.check(["roster\ta", "1\ta\t8"], target=8.5)
        self.assertTrue(out.startswith("Target: 8.5\n"), out)

    def test_bad_input_exits_2_with_line_number(self):
        for lines, message in [
            (["1\ta\t8"], "add a roster line"),
            (["roster\ta", "1\tz\t8"], "not in the roster"),
            (["roster\ta", "1\ta 8"], ":2:"),
            (["roster\ta", "1\ta\tnine"], "must be a number"),
            (["roster\ta", "1\ta\t85"], "from 0 to 10"),
            (["roster\ta", "1\ta\t8", "roster\ta,b", "1\tb\t8"], "not in the roster for round 1"),
            (["roster\ta", "1\ta\t8", "1\ta\t9"], "a second score"),
        ]:
            code, out = self.check(lines)
            self.assertEqual(code, 2, out)
            self.assertIn(message, out)

    def test_target_outside_0_to_10_exits_2(self):
        log = self.write("scores.tsv", "roster\ta\n1\ta\t0\n")
        for target in ("-1", "11", "nan", "inf"):
            self.assertEqual(run("scores", "--target", target, log)[0], 2, target)
            self.assertEqual(run("leaks", "--target", target, log)[0], 2, target)

    def test_missing_log_exits_2(self):
        code, out = run("scores", "--target", 9, self.root / "nope.tsv")
        self.assertEqual(code, 2)
        self.assertIn("error:", out)


class Pause(Fixture):
    """A reviewer that repeats a score above another reviewer pauses until the others catch up."""

    def check(self, lines, target=9):
        log = self.write("scores.tsv", "".join(line + "\n" for line in lines))
        code, out = run("scores", "--target", target, log)
        self.assertEqual(code, 0, out)
        return out

    def test_steady_reviewer_pauses_until_the_others_reach_its_score(self):
        lines = ["roster\tclaude,sol,flash", "1\tclaude\t8", "1\tsol\t6", "1\tflash\t7",
                 "2\tclaude\t8", "2\tsol\t6", "2\tflash\t7"]
        out = self.check(lines)
        self.assertIn("Paused: claude at 8, until every other reviewer reaches 8 or every score reaches the target", out)
        self.assertIn("Paused: flash at 7, until every other reviewer reaches 7", out)
        self.assertIn("Next round: sol\n", out)
        lines += ["3\tsol\t7"]
        out = self.check(lines)
        self.assertIn("| 3 | (8) | (7) | 7 | 7 | 7.33 |", out)
        self.assertIn("Paused: claude at 8", out)
        self.assertNotIn("Paused: flash", out)
        self.assertIn("Next round: flash, sol\n", out)
        self.assertIn("Decision: continue\n", out)
        lines += ["4\tsol\t8", "4\tflash\t8"]
        out = self.check(lines)
        self.assertNotIn("Paused:", out)
        self.assertIn("Next round: claude, flash, sol\n", out)
        lines += ["5\tclaude\t9", "5\tsol\t9", "5\tflash\t9"]
        self.assertIn("Decision: target reached", self.check(lines))

    def test_a_paused_reviewer_left_out_is_not_missing_but_an_active_one_is(self):
        lines = ["roster\tclaude,sol,flash", "1\tclaude\t8", "1\tsol\t6", "1\tflash\t7",
                 "2\tclaude\t8", "2\tsol\t6", "2\tflash\t6.5"]
        out = self.check(lines)
        self.assertIn("Paused: claude at 8", out)
        self.assertIn("Next round: flash, sol\n", out)
        self.assertIn("Decision: incomplete: round 3 has no score from flash", self.check(lines + ["3\tsol\t7"]))

    def test_a_paused_reviewer_that_scores_anyway_counts_as_scored(self):
        lines = ["roster\ta,b", "1\ta\t9", "1\tb\t7", "2\ta\t9", "2\tb\t7.5", "3\ta\t9", "3\tb\t9"]
        self.assertIn("Decision: target reached", self.check(lines))

    def test_a_paused_reviewer_dropped_from_the_roster_is_not_listed(self):
        lines = ["roster\ta,b,c", "1\ta\t9", "1\tb\t7", "1\tc\t7", "2\ta\t9", "2\tb\t7", "2\tc\t7.5",
                 "roster\tb,c"]
        out = self.check(lines)
        self.assertNotIn("Paused: a", out)
        self.assertIn("Next round: b, c", out)

    def test_reviewers_level_with_everyone_do_not_pause(self):
        out = self.check(["roster\ta,b", "1\ta\t8", "1\tb\t8", "2\ta\t8", "2\tb\t8"])
        self.assertNotIn("Paused:", out)
        self.assertIn("Next round: a, b", out)

    def test_target_with_a_carried_score_needs_a_round_with_everyone(self):
        lines = ["roster\ta,b", "1\ta\t9", "1\tb\t7", "2\ta\t9", "2\tb\t7.5"]
        self.assertIn("Paused: a at 9", self.check(lines))
        lines += ["3\tb\t9"]
        out = self.check(lines)
        self.assertIn("Decision: continue: every reviewer reviews the next round to confirm the target", out)
        self.assertIn("Next round: a, b", out)
        lines += ["4\ta\t9", "4\tb\t9"]
        self.assertIn("Decision: target reached", self.check(lines))

    def test_a_reviewer_paused_above_the_target_rejoins_once_everyone_is_at_target(self):
        lines = ["roster\ta,b", "1\ta\t9.5", "1\tb\t8", "2\ta\t9.5", "2\tb\t8.5", "3\tb\t9"]
        out = self.check(lines)
        self.assertNotIn("Paused:", out)
        self.assertIn("Next round: a, b", out)


class Leaks(Fixture):
    def leaks(self, brief, files=None, title=None, target=7):
        path = self.write("notes/brief.md", brief)
        evidence = self.root / "share" / "review-evidence"
        evidence.mkdir(parents=True, exist_ok=True)
        for name, content in (files or {}).items():
            (evidence / name).write_bytes(content if isinstance(content, bytes) else content.encode())
        return run("leaks", "--target", target, "--title", title or "Review the work", path, evidence.parent)

    def assert_flagged(self, brief, kind, **kwargs):
        code, out = self.leaks(brief, **kwargs)
        self.assertEqual(code, 1, f"{brief!r}: {out}")
        self.assertIn(f"[{kind}]", out, brief)
        return out

    def test_target_in_quoted_request_is_flagged(self):
        self.assert_flagged('The request: "/bar-raiser 7 the pricing page, judged by our style guide".\n',
                            "target number")

    def test_target_next_to_hyphens_paths_and_decimals_is_flagged(self):
        for line in ["See /tmp/target-7/work.md.", "The goal is 7.0 overall."]:
            self.assert_flagged(line + "\n", "target number")
        self.assert_flagged("Review the work.\n", "target number", title="Reach-7")
        self.assert_flagged("The goal is 8.50.\n", "target number", target=8.5)

    def test_scores_out_of_10_are_flagged(self):
        for line in ["It got 6.5/10.", "6 out of 10", "Opus gave 6/10 and Sol 5 / 10."]:
            self.assert_flagged(line + "\n", "score")

    def test_rounds_and_earlier_reviews_are_flagged(self):
        for line in ["Fixed in round 2.", "See round-3 notes.", "Round #4 is next."]:
            self.assert_flagged(line + "\n", "round")
        self.assert_flagged("Review the work.\n", "round", title="Round 2 review")
        for line in ["The earlier reviewer said so.", "Fix what the previous review found.",
                     "The last scores were low."]:
            self.assert_flagged(line + "\n", "earlier round or review")

    def test_evidence_names_and_contents_are_scanned(self):
        for name in ("round-2-home.png", "round2.png"):
            with self.subTest(name=name):
                self.fresh()
                out = self.assert_flagged("Review the work and score it.\n", "round", files={name: b"\x89PNG\0data"})
                self.assertIn(f"(file names):2: [round] review-evidence/{name}", out)
                self.assertIn(f"not scanned (binary or over 1 MB), check by eye: review-evidence/{name}\n", out)
        out = self.assert_flagged("Review the work and score it.\n", "score",
                                  files={"notes.txt": "Decision: continue\nscored 6/10, about 6 out of 10\n"})
        self.assertEqual(out.count("notes.txt:2:"), 1, "one hit per kind per line")

    def test_list_numbers_are_exempt_in_the_brief_only(self):
        self.assert_flagged("Review the work and score it.\n", "target number",
                            files={"notes.txt": "7. The pricing page is slow.\n"})
        self.fresh()
        out = self.assert_flagged("Review the work.\n", "target number", title="7. Review the work")
        self.assertIn("title:1: [target number]", out)

    def test_only_the_scale_wording_is_exempt_not_every_slash_10(self):
        self.assert_flagged("The work is /srv/releases/10/pricing.html.\n", "target number", target=10)
        self.assert_flagged("Review the work.\n", "target number", target=10,
                            files={"links.txt": "https://example.test/releases/10/index.html\n"})

    def test_binary_files_are_not_scanned(self):
        code, out = self.leaks("Review the work and score it.\n", files={"x.bin": b"round 2\0"})
        self.assertEqual(code, 0, out)
        self.assertIn("check by eye: review-evidence/x.bin", out)

    def test_the_share_folder_is_required(self):
        path = self.write("notes/brief.md", "Review the work.\n")
        self.assertEqual(run("leaks", "--target", 7, "--title", "Review the work", path)[0], 2)

    def test_the_work_copy_in_the_share_folder_is_scanned(self):
        path = self.write("notes/brief.md", "Review the work and score it.\n")
        self.write("share/review-evidence/home.txt", "home page\n")
        self.write("share/work/doc.md", "The target is 7.\n")
        code, out = run("leaks", "--target", 7, "--title", "Review the work", path, self.root / "share")
        self.assertEqual(code, 1, out)
        self.assertIn("work/doc.md:1: [target number]", out)

    def test_oversized_evidence_text_is_listed_not_scanned(self):
        code, out = self.leaks("Review the work and score it.\n",
                               files={"big.log": "x" * 1_000_001 + "\nscored 6/10\n"})
        self.assertEqual(code, 0, out)
        self.assertIn("check by eye: review-evidence/big.log", out)

    def test_numbered_brief_template_has_no_hits_for_any_target(self):
        brief = numbered_brief()
        for target in range(0, 11):
            code, out = self.leaks(brief, target=target, title="Review the work")
            self.assertEqual(code, 0, f"target {target}: {out}")

    def test_neutral_brief_passes(self):
        brief = ("Review the skill and score it.\n"
                 "Uses gpt-6.1-sol, Opus 5.5, skills-ref 0.1.1, v0.7, 1.7 and /tmp/5c1e2dd7-41be-4c0a.\n")
        code, out = self.leaks(brief, files={"home-screen.png": b"\0", "test-output.txt": "11 tests OK\n"},
                               title="Review the work")
        self.assertEqual(code, 0, out)

    def test_missing_brief_exits_2(self):
        code, out = run("leaks", "--target", 7, "--title", "Review the work", self.root / "nope.md")
        self.assertEqual(code, 2)
        self.assertIn("error:", out)


class Loop(Fixture):
    """A loop with target 9 in which one reviewer fails twice and the user drops or replaces it."""

    def test_failed_reviewer_dropped_then_target_reached(self):
        brief = self.write("notes/brief.md", numbered_brief())
        evidence = self.root / "share" / "review-evidence"
        evidence.mkdir(parents=True)
        (evidence / "pricing-page-desktop.png").write_bytes(b"\x89PNG\0")
        (evidence / "make-site-output.txt").write_text("built pricing.html\n")
        code, out = run("leaks", "--target", 9, "--title", "Review the work", brief, evidence.parent)
        self.assertEqual(code, 0, out)

        log = self.root / "notes" / "scores.tsv"
        steps = [
            (["roster\tsol,opus,flash", "1\tsol\t8", "1\topus\t7.5", "1\tflash\t8"], "continue"),
            (["2\tsol\t9", "2\topus\t9"], "incomplete: round 2 has no score from flash"),
            (["void\t2", "roster\tsol,opus"], "continue: the roster changed after round 1; run a round with the new roster"),
            (["3\tsol\t9", "3\topus\t9.5"], "target reached"),
        ]
        lines = []
        for added, expected in steps:
            lines += added
            log.write_text("".join(line + "\n" for line in lines))
            code, out = run("scores", "--target", 9, log)
            self.assertEqual(code, 0, out)
            self.assertEqual(out.split("Decision: ")[1].strip(), expected, out)
        self.assertIn("Not counted, void: round 2", out)

    def test_failed_reviewer_replaced_takes_a_fresh_round(self):
        log = self.write("scores.tsv", "".join(line + "\n" for line in [
            "roster\tsol,opus,flash", "1\tsol\t8", "1\topus\t8", "1\tflash\t8",
            "2\tsol\t8.5", "2\topus\t8.5", "void\t2", "roster\tsol,opus,luna",
            "3\tsol\t8.5", "3\topus\t8.5", "3\tluna\t8"]))
        code, out = run("scores", "--target", 9, log)
        self.assertEqual(code, 0, out)
        self.assertIn("Decision: continue", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
