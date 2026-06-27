#!/usr/bin/env python3
"""Seed the 16-week Teen Program curriculum into the Mahir DB.

Usage:
    DATABASE_URL_SYNC=postgresql://mahir:mahir@127.0.0.1:5435/mahir python scripts/seed_curriculum.py
    python scripts/seed_curriculum.py --reseed   # clear + reseed
    python scripts/seed_curriculum.py --dry-run  # show what would be seeded

Source: curriculum-trainer/projects/teen-program/act*-week*-draft.md (16 files)
Output: 1 Curriculum + 16 Modules + N Exercises per module
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

WORKSPACE = Path(__file__).parent.parent
SOURCE_DIR = WORKSPACE / "curriculum-trainer" / "projects" / "teen-program"

DATABASE_URL = os.getenv(
    "DATABASE_URL_SYNC", "postgresql://mahir:mahir@127.0.0.1:5435/mahir"
)

CURRICULUM_TITLE = "Teen Program — Build Your AI"
CURRICULUM_VERSION = "1.0"
CURRICULUM_EDITION = "co_worker"


def parse_week_file(path: Path) -> dict:
    """Extract week number, title, and beats from a markdown file."""
    text_content = path.read_text(encoding="utf-8")
    lines = text_content.splitlines()

    # Extract week number from filename (e.g. act1-week3-draft.md → 3)
    m = re.search(r"week(\d+)", path.stem)
    week_num = int(m.group(1)) if m else 0

    # Extract title from the ## "Title" heading (second line)
    title = f"Week {week_num}"
    for line in lines[:5]:
        if line.startswith('## "') and line.endswith('"'):
            title = f"Week {week_num} — {line[4:-1]}"
            break
        elif line.startswith("## ") and '"' in line:
            raw = line[3:].strip().strip('"')
            title = f"Week {week_num} — {raw}"
            break

    # Extract Act/week type from the # heading
    act_label = ""
    week_type = ""
    for line in lines[:3]:
        if line.startswith("# Act"):
            m2 = re.search(r"Act\s+(\d+),\s+Week\s+\d+\s+[—–-]\s+(.+)", line)
            if m2:
                week_type = m2.group(2).strip()
            m3 = re.search(r"Act\s+(\d+)", line)
            if m3:
                act_label = f"Act {m3.group(1)}"

    # Extract beat structure from Section 1 metadata table
    beat_structure_raw = ""
    in_table = False
    for line in lines:
        if "| Beat structure" in line or "| Beat Structure" in line:
            beat_structure_raw = line
            break
        if line.strip().startswith("| Track"):
            in_table = True
        if in_table and "beat" in line.lower() and "|" in line:
            beat_structure_raw = line
            break

    # Parse beats from beat structure line
    beats = _parse_beats(beat_structure_raw, week_num)

    # Extract Section 3 student task content (first beat's prompt)
    section3_content = _extract_section(text_content, 3)

    # Build summary markdown from metadata
    summary_parts = [f"**{act_label} — {week_type}**" if act_label else f"**{week_type}**"]
    if beat_structure_raw:
        # Get just the value part after the last |
        parts = [p.strip() for p in beat_structure_raw.split("|") if p.strip()]
        if len(parts) >= 2:
            summary_parts.append(f"Beat structure: {parts[-1]}")
    summary_markdown = "\n\n".join(summary_parts)

    # Set exercise prompts
    for i, beat in enumerate(beats):
        if i == 0 and section3_content:
            beat["prompt_markdown"] = section3_content
        else:
            beat["prompt_markdown"] = f"**{beat['title']}**\n\n{beat.get('description', '')}"

    return {
        "week_num": week_num,
        "title": title,
        "summary_markdown": summary_markdown,
        "beats": beats,
    }


def _parse_beats(beat_structure_raw: str, week_num: int) -> list[dict]:
    """Parse beat descriptions from the Beat structure metadata row."""
    beats = []

    # Extract beat structure value from the table row
    if not beat_structure_raw:
        # Fallback: create 1 exercise if no beat structure found
        return [{"title": f"Week {week_num} — Session", "description": "", "sequence_index": 1}]

    # Get the value part (everything after last separating |)
    parts = [p.strip() for p in beat_structure_raw.split("|") if p.strip()]
    value = parts[-1] if parts else ""

    # Split on → (U+2192) separators, then parse each "Beat N: desc" segment
    segments = re.split(r"\s*→\s*", value)
    for seg in segments:
        seg = seg.strip()
        m = re.match(r"Beat\s+(\d+)\s*:\s*(.*)", seg, re.IGNORECASE)
        if m:
            beat_num = int(m.group(1))
            description = m.group(2).strip()
            beats.append({
                "title": f"Beat {beat_num}",
                "description": description,
                "sequence_index": beat_num,
            })
        elif seg:
            beats.append({
                "title": f"Beat {len(beats) + 1}",
                "description": seg,
                "sequence_index": len(beats) + 1,
            })

    return beats if beats else [{"title": "Session", "description": "", "sequence_index": 1}]


def _extract_section(text_content: str, section_num: int) -> str:
    """Extract content of a numbered section heading."""
    pattern = re.compile(
        rf"##\s+Section\s+{section_num}\s+[—–-].*?\n(.*?)(?=\n##\s+Section\s+\d+|$)",
        re.DOTALL,
    )
    m = pattern.search(text_content)
    if not m:
        return ""
    content = m.group(1).strip()
    # Return first 2000 chars (exercise prompts can be long)
    return content[:2000]


def seed(session: Session, dry_run: bool = False) -> None:
    """Insert Curriculum + Modules + Exercises. Idempotent on title+version."""
    import uuid

    def new_id() -> str:
        return str(uuid.uuid4())

    # Check if already seeded
    existing = session.execute(
        text("SELECT id FROM curricula WHERE title = :t AND version = :v AND deleted_at IS NULL"),
        {"t": CURRICULUM_TITLE, "v": CURRICULUM_VERSION},
    ).fetchone()

    if existing:
        print(f"Curriculum '{CURRICULUM_TITLE}' v{CURRICULUM_VERSION} already exists (id={existing[0]}).")
        print("Use --reseed to clear and reseed.")
        if not dry_run:
            backfill_cohorts(session, existing[0])
        return

    # Collect and sort week files
    week_files = sorted(
        [f for f in SOURCE_DIR.glob("act*-week*-draft.md")],
        key=lambda p: int(re.search(r"week(\d+)", p.stem).group(1)),
    )

    if len(week_files) != 16:
        print(f"WARNING: expected 16 week files, found {len(week_files)}")

    parsed_weeks = [parse_week_file(f) for f in week_files]
    parsed_weeks.sort(key=lambda w: w["week_num"])

    print(f"\nCurriculum: {CURRICULUM_TITLE} v{CURRICULUM_VERSION}")
    print(f"Modules: {len(parsed_weeks)}")
    total_exercises = sum(len(w["beats"]) for w in parsed_weeks)
    print(f"Exercises: {total_exercises}")
    print()

    for w in parsed_weeks:
        print(f"  Week {w['week_num']:2d}: {w['title'][:60]} — {len(w['beats'])} beat(s)")

    if dry_run:
        print("\n[dry-run] No changes written.")
        return

    # Insert Curriculum
    curriculum_id = new_id()
    session.execute(
        text("""
            INSERT INTO curricula (id, edition, title, version, status, created_at, updated_at)
            VALUES (:id, :edition, :title, :version, 'published', NOW(), NOW())
        """),
        {
            "id": curriculum_id,
            "edition": CURRICULUM_EDITION,
            "title": CURRICULUM_TITLE,
            "version": CURRICULUM_VERSION,
        },
    )
    print(f"\nCreated curriculum: {curriculum_id}")

    # Insert Modules + Exercises
    for week in parsed_weeks:
        module_id = new_id()
        session.execute(
            text("""
                INSERT INTO modules (id, curriculum_id, title, sequence_index, summary_markdown, created_at, updated_at)
                VALUES (:id, :cid, :title, :seq, :summary, NOW(), NOW())
            """),
            {
                "id": module_id,
                "cid": curriculum_id,
                "title": week["title"],
                "seq": week["week_num"],
                "summary": week["summary_markdown"],
            },
        )

        for beat in week["beats"]:
            exercise_id = new_id()
            build_spec = json.dumps({
                "schema_version": "1.0",
                "type": "curriculum_beat",
                "beat_index": beat["sequence_index"],
                "week": week["week_num"],
            })
            session.execute(
                text("""
                    INSERT INTO exercises (
                        id, module_id, title, sequence_index, prompt_markdown, build_spec,
                        min_attempts, min_distinct_approaches, min_exploration_seconds,
                        allow_fast_unlock, created_at, updated_at
                    )
                    VALUES (
                        :id, :mid, :title, :seq, :prompt, :build_spec,
                        2, 1, 180, true, NOW(), NOW()
                    )
                """),
                {
                    "id": exercise_id,
                    "mid": module_id,
                    "title": f"{week['title']} — {beat['title']}",
                    "seq": beat["sequence_index"],
                    "prompt": beat["prompt_markdown"],
                    "build_spec": build_spec,
                },
            )

        print(f"  Module week {week['week_num']:2d}: {module_id} — {len(week['beats'])} exercise(s)")

    session.commit()
    print(f"\nDone. {len(parsed_weeks)} modules, {total_exercises} exercises seeded.")

    backfill_cohorts(session, curriculum_id)


def backfill_cohorts(session: Session, curriculum_id: str) -> None:
    """Link all cohorts that have no curriculum_id to the given curriculum."""
    result = session.execute(
        text("UPDATE cohorts SET curriculum_id = :cid WHERE curriculum_id IS NULL RETURNING id"),
        {"cid": curriculum_id},
    )
    updated = result.rowcount
    session.commit()
    if updated:
        print(f"Backfilled {updated} cohort(s) → curriculum {curriculum_id}.")
    else:
        print("No cohorts needed backfill (all already linked or no cohorts exist).")


def clear(session: Session) -> None:
    """Delete existing curriculum and cascade."""
    result = session.execute(
        text("SELECT id FROM curricula WHERE title = :t AND version = :v AND deleted_at IS NULL"),
        {"t": CURRICULUM_TITLE, "v": CURRICULUM_VERSION},
    ).fetchone()
    if not result:
        print("No existing curriculum to clear.")
        return
    curriculum_id = result[0]

    # Cascade: exercises → modules → curriculum
    session.execute(
        text("""
            DELETE FROM exercises WHERE module_id IN (
                SELECT id FROM modules WHERE curriculum_id = :cid
            )
        """),
        {"cid": curriculum_id},
    )
    session.execute(text("DELETE FROM modules WHERE curriculum_id = :cid"), {"cid": curriculum_id})
    session.execute(text("DELETE FROM curricula WHERE id = :cid"), {"cid": curriculum_id})
    session.commit()
    print(f"Cleared curriculum {curriculum_id}.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed Mahir curriculum")
    parser.add_argument("--reseed", action="store_true", help="Clear existing data and reseed")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be seeded without writing")
    parser.add_argument("--backfill-only", action="store_true", help="Only backfill cohort curriculum_id links (no seed files needed)")
    args = parser.parse_args()

    engine = create_engine(DATABASE_URL, echo=False)

    if args.backfill_only:
        with Session(engine) as session:
            result = session.execute(
                text("SELECT id FROM curricula WHERE deleted_at IS NULL LIMIT 1")
            ).fetchone()
            if not result:
                print("ERROR: no curriculum found in DB — run seed first.", file=sys.stderr)
                sys.exit(1)
            backfill_cohorts(session, result[0])
        return

    if not SOURCE_DIR.exists():
        print(f"ERROR: curriculum source not found: {SOURCE_DIR}", file=sys.stderr)
        sys.exit(1)

    with Session(engine) as session:
        if args.reseed:
            clear(session)
        seed(session, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
