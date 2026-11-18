import secrets
import shutil
import string
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def synthetic_token():
    alphabet = string.ascii_letters + string.digits
    return "ghp" + "_" + "".join(secrets.choice(alphabet) for _ in range(36))


class GitHooksTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = self.root / "checkout"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        shutil.copytree(ROOT / ".githooks", self.repo / ".githooks")
        (self.repo / "scripts").mkdir()
        shutil.copy2(ROOT / "scripts/verify.py", self.repo / "scripts/verify.py")
        tool = subprocess.check_output(
            ["git", "rev-parse", "--git-path", "ai-hygiene-tools/gitleaks"], cwd=ROOT, text=True
        ).strip()
        tool_dir = self.repo / ".git/ai-hygiene-tools"
        tool_dir.mkdir()
        (tool_dir / "gitleaks").symlink_to((ROOT / tool).resolve())
        self.git("config", "core.hooksPath", ".githooks")
        self.file = self.repo / "guide.md"
        self.file.write_text("Starting guide\n")
        self.git("add", "guide.md")
        self.git("commit", "-qm", "docs: start the guide")

    def git(self, *args, succeeds=True):
        result = subprocess.run(["git", *args], cwd=self.repo, capture_output=True, text=True)
        if succeeds:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result

    def test_only_the_staged_snapshot_is_committed(self):
        token = synthetic_token()
        self.file.write_text(token + "\n")
        self.git("add", "guide.md")
        self.file.write_text("Public update\n")
        blocked = self.git("commit", "-qm", "docs: revise guide", succeeds=False)
        self.assertNotIn(token, blocked.stdout + blocked.stderr)

        self.git("add", "guide.md")
        self.file.write_text(token + "\n")
        self.git("commit", "-qm", "docs: revise guide")
        self.assertEqual(self.git("show", "HEAD:guide.md").stdout, "Public update\n")

    def test_private_files_and_nonconventional_subjects_are_rejected(self):
        for filename in (".env.local", "semantics.md"):
            private = self.repo / "nested" / filename
            private.parent.mkdir(exist_ok=True)
            private.write_text("Local only\n")
            self.git("add", "-f", str(private))
            self.git("commit", "-qm", "docs: add a file", succeeds=False)
            self.git("rm", "--cached", "-q", str(private))
        (self.repo / ".env.example").write_text("ENVIRONMENT=example\n")
        self.git("add", "-f", ".env.example")
        self.git("commit", "-qm", "miscellaneous changes", succeeds=False)
        self.git("commit", "-qm", "docs: include example settings")

    def test_push_rejects_a_secret_deleted_before_the_tip(self):
        remote = str(self.root / "remote.git")
        self.git("init", "-q", "--bare", remote)
        self.git("push", remote, "main")
        baseline = self.git("rev-parse", "HEAD").stdout.strip()

        # Model a contributor who made local commits before installing the hooks.
        self.git("config", "core.hooksPath", ".git/empty-hooks")
        token = synthetic_token()
        self.file.write_text(token + "\n")
        self.git("commit", "-qam", "docs: add fixture")
        self.file.write_text("Public final version\n")
        self.git("commit", "-qam", "docs: remove fixture")
        self.git("config", "core.hooksPath", ".githooks")

        for target in ("main", "new-branch"):
            result = self.git("push", remote, f"HEAD:refs/heads/{target}", succeeds=False)
            self.assertNotIn(token, result.stdout + result.stderr)
        self.assertEqual(self.git("ls-remote", remote, "refs/heads/main").stdout.split()[0], baseline)


if __name__ == "__main__":
    unittest.main()
