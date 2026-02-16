from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List, Tuple
import re


from .utils import strip_code_fences

_FILE_HEADER_RE = re.compile(r"^===\s*FILE:\s*(.+?)\s*===\s*$", re.MULTILINE)

class Tools:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path.resolve()

    def _safe(self, rel_path: str) -> Path:
        p = (self.repo_path / rel_path).resolve()
        # if not str(p).startswith(str(self.repo_path)):
        #     raise ValueError("Unsafe path traversal blocked.")
        try:
            p.relative_to(self.repo_path)
        except ValueError as e:
            raise ValueError("Unsafe path traversal blocked.") from e
        return p

    def read(self, rel_path: str, max_chars: int = 20000) -> str:
        p = self._safe(rel_path)
        if not p.exists():
            return ""
        return p.read_text(encoding="utf-8", errors="replace")[:max_chars]

    def write(self, rel_path: str, content: str) -> None:
        p = self._safe(rel_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    
    def write_from_blocks(self, text: str) -> List[str]:
        """Write multiple files from a model response containing file blocks.

        Expected format:
          === FILE: path/to/file ===
          <content>

        Returns list of written relative paths. If no blocks found, returns [].
        """
        matches = list(_FILE_HEADER_RE.finditer(text or ""))
        if not matches:
            return []

        written: List[str] = []
        for i, m in enumerate(matches):
            rel_path = m.group(1).strip()
            start = m.end()
            end = matches[i + 1].start() if (i + 1) < len(matches) else len(text)
            content = text[start:end].lstrip("\n")

            # Strip ONE outer fence if the model wrapped this file
            content = strip_code_fences(content)

            if content and not content.endswith("\n"):
                content += "\n"

            self.write(rel_path, content)
            written.append(rel_path)

        return written

    def run(self, cmd: str, timeout_s: int = 600) -> Tuple[bool, str]:
        proc = subprocess.run(
            cmd,
            cwd=self.repo_path,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        out = (out.strip() or "[NO OUTPUT]")
        return proc.returncode == 0, out[:20000]

    def git_commit(self, message: str) -> Tuple[bool, str]:
        ok1, out1 = self.run("git add -A")
        if not ok1:
            return False, out1
        safe_msg = message.replace('"', "'")
        return self.run(f'git commit -m "{safe_msg}"')

    def git_push(self) -> Tuple[bool, str]:
        return self.run("git push")
