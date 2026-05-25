from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from common import list_story_files, load_story, dump_json


ROOT = Path(__file__).resolve().parents[2]
STORIES_DIR = ROOT / "docs" / "user-stories"
GENERATED_DIR = STORIES_DIR / "generated"
JSON_OUTPUT = GENERATED_DIR / "index.json"
MARKDOWN_OUTPUT = STORIES_DIR / "README.md"


def classify_story(story_id: str, file_name: str) -> str:
    if file_name == "HU-TEMPLATE.md" or "XXX" in story_id:
        return "template"
    return "user-story"


def build_index() -> dict:
    items = []
    for path in list_story_files(STORIES_DIR):
        story = load_story(path)
        kind = classify_story(story.story_id, path.name)
        ewm = story.front_matter.get("ewm", {})
        items.append(
            {
                "id": story.front_matter.get("id"),
                "title": story.front_matter.get("title"),
                "module": story.front_matter.get("module"),
                "status": story.front_matter.get("status"),
                "owner": story.front_matter.get("owner"),
                "repository": story.front_matter.get("repository"),
                "prototype": story.front_matter.get("prototype"),
                "version": story.front_matter.get("version"),
                "last_update": story.front_matter.get("last_update"),
                "export_targets": story.front_matter.get("export_targets", []),
                "kind": kind,
                "path": path.relative_to(ROOT).as_posix(),
                "ewm": {
                    "work_item_type": ewm.get("work_item_type"),
                    "project_area": ewm.get("project_area"),
                    "team_area": ewm.get("team_area"),
                    "category": ewm.get("category"),
                    "planned_for": ewm.get("planned_for"),
                    "iteration": ewm.get("iteration"),
                    "priority": ewm.get("priority"),
                    "severity": ewm.get("severity"),
                    "work_item_id": ewm.get("work_item_id"),
                    "parent_work_item_id": ewm.get("parent_work_item_id"),
                    "tags": ewm.get("tags", []),
                },
            }
        )

    return {
        "schema": "silic.user-stories.index.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": STORIES_DIR.relative_to(ROOT).as_posix(),
        "counts": {
            "total": len(items),
            "user_stories": sum(1 for item in items if item["kind"] == "user-story"),
            "templates": sum(1 for item in items if item["kind"] == "template"),
        },
        "items": items,
    }


def build_markdown(index_payload: dict) -> str:
    lines = [
        "# Historias de Usuario",
        "",
        "Indice gerado automaticamente a partir do front matter das historias em `docs/user-stories`.",
        "",
        f"Gerado em: {index_payload['generated_at']}",
        "",
        "| ID | Titulo | Modulo | Status | Tipo | Caminho |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for item in index_payload["items"]:
        lines.append(
            f"| {item['id']} | {item['title']} | {item['module']} | {item['status']} | {item['kind']} | {item['path']} |"
        )

    lines.extend(
        [
            "",
            "## Saidas geradas",
            "",
            "- `docs/user-stories/generated/index.json`",
            "- `docs/user-stories/README.md`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    index_payload = build_index()
    dump_json(JSON_OUTPUT, index_payload)
    MARKDOWN_OUTPUT.write_text(build_markdown(index_payload), encoding="utf-8")
    print(f"Indice gerado em {JSON_OUTPUT.relative_to(ROOT)} e {MARKDOWN_OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()