"""Disposable local Git fixtures for ship-it's documented commands; no GitHub calls.

Run: python docs/testing/test_ship_it_git.py
Each test owns its temporary home, config, bare remote and worktrees.
"""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class ShipItGit(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="ship-it-fixture-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.env = {k: v for k, v in os.environ.items() if not k.upper().startswith("GIT_")}
        self.env.update(HOME=str(self.root), USERPROFILE=str(self.root),
                        XDG_CONFIG_HOME=str(self.root), GIT_CONFIG_NOSYSTEM="1",
                        GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
        self.remote = self.root / "remote.git"
        self.main = self.root / "default checkout"
        self.task = self.root / "task worktree"
        self.git(self.root, "init", "--bare", str(self.remote))
        self.git(self.root, "init", "-b", "main", str(self.main))
        self.git(self.main, "config", "user.name", "Fixture")
        self.git(self.main, "config", "user.email", "fixture@example.invalid")
        self.git(self.main, "config", "core.autocrlf", "false")
        self.git(self.main, "config", "core.hooksPath", str(self.root / "hooks"))
        for name in ("selected.txt", "delete.txt", "unrelated.txt", "rename.txt"):
            (self.main / name).write_text("base\n")
        (self.main / ".gitignore").write_text("ignored/\n")
        self.git(self.main, "add", ".")
        self.git(self.main, "commit", "-m", "Base")
        self.git(self.main, "remote", "add", "origin", str(self.remote))
        self.git(self.main, "push", "-u", "origin", "main")
        self.git(self.main, "worktree", "add", "-b", "feature-x", str(self.task))

    def git(self, cwd, *args, ok=True):
        proc = subprocess.run(["git", *args], cwd=cwd, env=self.env,
                              text=True, capture_output=True, timeout=20)
        if ok and proc.returncode:
            self.fail(f"git {args}: {proc.stdout}\n{proc.stderr}")
        return proc

    def out(self, cwd, *args):
        return self.git(cwd, *args).stdout.strip()

    def selected_commit(self):
        (self.task / "selected.txt").write_text("selected change\n")
        self.git(self.task, "add", "selected.txt")
        self.git(self.task, "commit", "--only", "-m", "Task", "--", "selected.txt")
        return self.out(self.task, "rev-parse", "HEAD")

    def clean(self, path):
        return not (self.out(path, "status", "--porcelain", "--untracked-files=all")
                    or self.out(path, "ls-files", "--others", "--ignored", "--exclude-standard"))

    def test_literal_paths_preserve_foreign_index_and_tree(self):
        (self.task / "unrelated.txt").write_text("foreign staged\n")
        self.git(self.task, "add", "unrelated.txt")
        before = self.out(self.task, "ls-files", "--stage", "--", "unrelated.txt")
        (self.task / "unrelated.txt").write_text("foreign unstaged\n")
        (self.task / "scratch.txt").write_text("keep\n")
        (self.task / "selected.txt").write_text("selected change\n")
        (self.task / "delete.txt").unlink()
        (self.task / "new [literal].txt").write_text("new\n")
        paths = ["selected.txt", "delete.txt", "new [literal].txt"]
        self.git(self.task, "--literal-pathspecs", "add", "--", *paths)
        self.git(self.task, "--literal-pathspecs", "commit", "--only", "-m", "Selected", "--", *paths)
        actual = self.out(self.task, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines()
        self.assertEqual(set(actual), set(paths))
        self.assertEqual(before, self.out(self.task, "ls-files", "--stage", "--", "unrelated.txt"))
        self.assertEqual((self.task / "unrelated.txt").read_text(), "foreign unstaged\n")
        self.assertEqual((self.task / "scratch.txt").read_text(), "keep\n")

    def test_rename_both_sides(self):
        (self.task / "rename.txt").rename(self.task / "renamed.txt")
        self.git(self.task, "--literal-pathspecs", "add", "--", "rename.txt", "renamed.txt")
        self.git(self.task, "--literal-pathspecs", "commit", "--only", "-m", "Rename", "--", "rename.txt", "renamed.txt")
        self.assertTrue(self.clean(self.task))

    def test_failed_commit_preserves_changes_and_foreign_index(self):
        (self.task / "unrelated.txt").write_text("foreign\n")
        self.git(self.task, "add", "unrelated.txt")
        before = self.out(self.task, "ls-files", "--stage", "--", "unrelated.txt")
        (self.task / "selected.txt").write_text("selected\n")
        self.git(self.task, "add", "selected.txt")
        head = self.out(self.task, "rev-parse", "HEAD")
        # An empty message fails reliably without depending on shell hook support.
        result = self.git(self.task, "commit", "--only", "-m", "", "--", "selected.txt", ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(head, self.out(self.task, "rev-parse", "HEAD"))
        self.assertEqual(before, self.out(self.task, "ls-files", "--stage", "--", "unrelated.txt"))
        self.assertEqual((self.task / "selected.txt").read_text(), "selected\n")

    def test_worktree_git_paths_detect_operation(self):
        self.assertTrue((self.task / ".git").is_file())
        path = Path(self.out(self.task, "rev-parse", "--git-path", "MERGE_HEAD"))
        if not path.is_absolute():
            path = self.task / path
        path.write_text(self.out(self.task, "rev-parse", "HEAD") + "\n")
        self.assertTrue(path.exists())
        self.assertNotEqual(self.git(self.task, "commit", "--only", "-m", "No", "--", "selected.txt", ok=False).returncode, 0)

    def test_lease_rejects_remote_advance(self):
        old = self.selected_commit()
        self.git(self.task, "push", "origin", "feature-x")
        self.git(self.task, "commit", "--allow-empty", "-m", "Concurrent work")
        new = self.out(self.task, "rev-parse", "HEAD")
        self.git(self.task, "push", "origin", "feature-x")
        result = self.git(self.main, "push", f"--force-with-lease=refs/heads/feature-x:{old}", "origin", ":refs/heads/feature-x", ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(new, self.out(self.main, "ls-remote", "origin", "refs/heads/feature-x"))

    def test_clean_worktree_squash_sync_cleanup(self):
        head = self.selected_commit()
        self.git(self.task, "push", "origin", "feature-x")
        # Emulate the server's squash merge in a third checkout.
        integrator = self.root / "integrator"
        self.git(self.main, "worktree", "add", "--detach", str(integrator), "main")
        self.git(integrator, "merge", "--squash", "feature-x")
        self.git(integrator, "commit", "-m", "Squash task")
        merge = self.out(integrator, "rev-parse", "HEAD")
        self.git(integrator, "push", "origin", "HEAD:main")
        self.assertNotEqual(self.git(self.task, "switch", "main", ok=False).returncode, 0)
        self.git(self.main, "pull", "--ff-only")
        self.assertEqual(merge, self.out(self.main, "rev-parse", "HEAD"))
        self.git(self.main, "merge-base", "--is-ancestor", merge, "HEAD")
        self.git(self.main, "push", f"--force-with-lease=refs/heads/feature-x:{head}", "origin", ":refs/heads/feature-x")
        self.assertTrue(self.clean(self.task))
        self.assertEqual(head, self.out(self.task, "rev-parse", "HEAD"))
        self.git(self.main, "worktree", "remove", str(self.task))
        # Simulated interruption after worktree removal: rediscover and finish.
        self.assertNotIn(str(self.task).replace("\\", "/"), self.out(self.main, "worktree", "list", "--porcelain"))
        self.assertEqual(head, self.out(self.main, "rev-parse", "feature-x"))
        self.git(self.main, "update-ref", "-d", "refs/heads/feature-x", head)
        self.assertFalse(self.task.exists())
        self.assertFalse(self.out(self.main, "ls-remote", "origin", "refs/heads/feature-x"))

    def test_local_delete_rejects_advance_after_worktree_removal(self):
        old = self.selected_commit()
        self.git(self.main, "worktree", "remove", str(self.task))
        # A concurrent writer advances the ref after our pre-deletion read.
        tree = self.out(self.main, "rev-parse", "feature-x^{tree}")
        new = self.out(self.main, "commit-tree", tree, "-p", old, "-m", "Concurrent work")
        self.git(self.main, "update-ref", "refs/heads/feature-x", new, old)
        result = self.git(self.main, "update-ref", "-d", "refs/heads/feature-x", old, ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(new, self.out(self.main, "rev-parse", "feature-x"))

    def test_dirty_default_and_ignored_task_are_preserved(self):
        (self.main / "unrelated.txt").write_text("default work\n")
        (self.task / "ignored").mkdir()
        (self.task / "ignored" / "sentinel").write_text("keep\n")
        self.assertFalse(self.clean(self.main))
        self.assertFalse(self.clean(self.task))
        # Guards defer sync/removal; ignored files require the second inventory.
        self.assertFalse(self.out(self.task, "status", "--porcelain", "--untracked-files=all"))
        self.assertEqual((self.task / "ignored" / "sentinel").read_text(), "keep\n")
        self.assertEqual((self.main / "unrelated.txt").read_text(), "default work\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
