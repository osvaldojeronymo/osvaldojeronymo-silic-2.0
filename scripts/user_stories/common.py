from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


@dataclass
class StoryDocument:
    path: Path
    front_matter: dict[str, Any]
    body: str

    @property
    def story_id(self) -> str:
        return str(self.front_matter.get("id", ""))

    @property
    def title(self) -> str:
        return str(self.front_matter.get("title", ""))

    @property
    def summary(self) -> str:
        story_id = self.story_id.strip()
        title = self.title.strip()
        if story_id and title:
            return f"{story_id} - {title}"
        return title or story_id


def load_story(path: Path) -> StoryDocument:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise ValueError(f"Arquivo sem front matter YAML: {path}")
    front_matter_text = match.group(1)
    body = text[match.end():].lstrip("\n")
    return StoryDocument(path=path, front_matter=parse_simple_yaml(front_matter_text), body=body)


def parse_simple_yaml(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()

        parent = stack[-1][1]

        if line.startswith("- "):
            if not isinstance(parent, list):
                raise ValueError(f"Lista YAML invalida: {raw_line}")
            parent.append(_parse_scalar(line[2:].strip()))
            continue

        if ":" not in line:
            raise ValueError(f"Linha YAML invalida: {raw_line}")

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value:
            if not isinstance(parent, dict):
                raise ValueError(f"Mapa YAML invalido: {raw_line}")
            parent[key] = _parse_scalar(value)
            continue

        next_container = _guess_next_container(text, raw_line)
        if not isinstance(parent, dict):
            raise ValueError(f"Estrutura YAML invalida: {raw_line}")
        parent[key] = next_container
        stack.append((indent, next_container))

    return root


def _guess_next_container(full_text: str, current_line: str) -> Any:
    lines = full_text.splitlines()
    index = lines.index(current_line)
    current_indent = len(current_line) - len(current_line.lstrip(" "))
    for next_line in lines[index + 1:]:
        if not next_line.strip() or next_line.lstrip().startswith("#"):
            continue
        next_indent = len(next_line) - len(next_line.lstrip(" "))
        if next_indent <= current_indent:
            break
        return [] if next_line.strip().startswith("- ") else {}
    return {}


def _parse_scalar(value: str) -> Any:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def extract_section(body: str, section_name: str) -> str:
    headings = list(HEADING_RE.finditer(body))
    for index, match in enumerate(headings):
        if match.group(1).strip().lower() == section_name.strip().lower():
            start = match.end()
            end = headings[index + 1].start() if index + 1 < len(headings) else len(body)
            return body[start:end].strip()
    return ""


def parse_markdown_table(section_text: str) -> list[dict[str, str]]:
    lines = [line.strip() for line in section_text.splitlines() if line.strip()]
    table_lines = [line for line in lines if line.startswith("|") and line.endswith("|")]
    if len(table_lines) < 2:
        return []

    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def markdown_to_html(markdown_text: str) -> str:
    completed = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html5"],
        input=markdown_text,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def list_story_files(root: Path) -> list[Path]:
    return sorted(path for path in root.glob("*.md") if path.name not in {"README.md", "EWM-FIELD-MAPPING.md"})