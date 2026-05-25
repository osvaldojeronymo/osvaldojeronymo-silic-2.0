from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Any

from common import dump_json, extract_section, load_story, markdown_to_html, parse_markdown_table


ROOT = Path(__file__).resolve().parents[2]


def normalize_status(value: str) -> str:
    mapping = {
        "rascunho": "Draft",
        "em elaboracao": "In Progress",
        "em validacao": "In Review",
        "homologado": "Resolved",
        "aprovado": "Closed",
    }
    return mapping.get(value.strip().lower(), value)


def story_to_ewm_payload(story_path: Path) -> dict[str, Any]:
    story = load_story(story_path)
    ewm = story.front_matter.get("ewm", {})
    acceptance = parse_markdown_table(extract_section(story.body, "Criterios de aceitacao"))
    business_rules = parse_markdown_table(extract_section(story.body, "Regras de negocio"))
    traceability = parse_markdown_table(extract_section(story.body, "Rastreabilidade"))
    description_html = markdown_to_html(story.body)

    payload = {
        "schema": "silic.hu.ewm.payload.v1",
        "source": {
            "path": story_path.relative_to(ROOT).as_posix(),
            "id": story.front_matter.get("id"),
            "version": story.front_matter.get("version"),
            "last_update": story.front_matter.get("last_update"),
        },
        "fields": {
            "externalId": story.front_matter.get("id"),
            "summary": story.summary,
            "workItemType": ewm.get("work_item_type", "Story"),
            "status": story.front_matter.get("status"),
            "statusNormalized": normalize_status(str(story.front_matter.get("status", ""))),
            "ownedBy": story.front_matter.get("owner"),
            "projectArea": ewm.get("project_area"),
            "teamArea": ewm.get("team_area"),
            "filedAgainst": story.front_matter.get("module"),
            "category": ewm.get("category", story.front_matter.get("module")),
            "plannedFor": ewm.get("planned_for"),
            "iteration": ewm.get("iteration"),
            "priority": ewm.get("priority"),
            "severity": ewm.get("severity"),
            "workItemId": ewm.get("work_item_id"),
            "parentWorkItemId": ewm.get("parent_work_item_id"),
            "repository": story.front_matter.get("repository"),
            "prototype": story.front_matter.get("prototype"),
            "documentVersion": story.front_matter.get("version"),
            "lastUpdate": story.front_matter.get("last_update"),
            "exportTargets": story.front_matter.get("export_targets", []),
            "tags": ewm.get("tags", []),
            "descriptionMarkdown": story.body,
            "descriptionHtml": description_html,
            "acceptanceCriteria": acceptance,
            "businessRules": business_rules,
            "traceability": traceability,
        },
        "oslc_cm": {
            "dcterms:title": story.summary,
            "dcterms:description": description_html,
            "dcterms:modified": story.front_matter.get("last_update"),
            "oslc_cm:status": story.front_matter.get("status"),
            "rtc_cm:workItemType": ewm.get("work_item_type", "Story"),
            "rtc_cm:ownedBy": story.front_matter.get("owner"),
            "rtc_cm:projectArea": ewm.get("project_area"),
            "rtc_cm:teamArea": ewm.get("team_area"),
            "rtc_cm:filedAgainst": story.front_matter.get("module"),
            "rtc_cm:category": ewm.get("category", story.front_matter.get("module")),
            "rtc_cm:plannedFor": ewm.get("planned_for"),
            "rtc_cm:iteration": ewm.get("iteration"),
            "rtc_cm:priority": ewm.get("priority"),
            "rtc_cm:severity": ewm.get("severity"),
            "rtc_cm:identifier": ewm.get("work_item_id"),
            "rtc_cm:parent": ewm.get("parent_work_item_id"),
            "rtc_cm:tags": ewm.get("tags", []),
            "rtc_ext:repository": story.front_matter.get("repository"),
            "rtc_ext:prototype": story.front_matter.get("prototype"),
            "rtc_ext:documentVersion": story.front_matter.get("version"),
            "rtc_ext:externalId": story.front_matter.get("id"),
            "rtc_ext:exportTargets": story.front_matter.get("export_targets", []),
            "rtc_ext:acceptanceCriteria": acceptance,
            "rtc_ext:businessRules": business_rules,
            "rtc_ext:traceability": traceability,
        },
    }
    return payload


def run_pandoc(story_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = ["pandoc", str(story_path), "--standalone", "-o", str(output_path)]
    if output_path.suffix.lower() == ".pdf":
        command.extend(["--pdf-engine=pdflatex"])
    subprocess.run(command, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exporta HU para PDF, DOCX, HTML e payload EWM.")
    parser.add_argument("input", help="Arquivo Markdown da HU")
    parser.add_argument(
        "--targets",
        nargs="+",
        default=["pdf", "docx", "html", "ewm-json"],
        choices=["pdf", "docx", "html", "ewm-json"],
        help="Alvos de exportacao",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Diretorio de saida. Por padrao usa docs/user-stories/generated/<ID>/",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    story_path = (ROOT / args.input).resolve() if not Path(args.input).is_absolute() else Path(args.input)
    story = load_story(story_path)
    output_dir = Path(args.output_dir).resolve() if args.output_dir else ROOT / "docs" / "user-stories" / "generated" / story.story_id
    output_dir.mkdir(parents=True, exist_ok=True)

    if "pdf" in args.targets:
        run_pandoc(story_path, output_dir / f"{story.story_id}.pdf")
    if "docx" in args.targets:
        run_pandoc(story_path, output_dir / f"{story.story_id}.docx")
    if "html" in args.targets:
        run_pandoc(story_path, output_dir / f"{story.story_id}.html")
    if "ewm-json" in args.targets:
        dump_json(output_dir / f"{story.story_id}.ewm.json", story_to_ewm_payload(story_path))

    print(f"Exportacao concluida em {output_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    main()