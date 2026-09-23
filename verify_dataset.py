"""Check a downloaded BCG dataset and report what it contains.

    python verify_dataset.py /path/to/BCG
    python verify_dataset.py /path/to/BCG --checksums

Verifies that every image has a label and the reverse, that class ids and polygon coordinates
are in range, and summarises the instance counts and the generation conditions. Needs only
Pillow; without it the image dimensions are skipped and everything else still runs.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import sys
from pathlib import Path

CLASS_NAMES = {0: "brick", 1: "broken_brick", 2: "crack"}
MOTIONS = ("stay", "translation", "settling")
VIEWS = ("close", "middle", "far")
WIDTHS = ("lt3mm", "3to5mm", "5to10mm", "10to30mm", "gt30mm")


def parse_label(path: Path) -> tuple[list[tuple[int, int]], list[str]]:
    """Return (class id, vertex count) per instance, and any problems found."""
    instances, problems = [], []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        fields = line.split()
        if not fields:
            continue
        try:
            class_id = int(fields[0])
            coordinates = [float(v) for v in fields[1:]]
        except ValueError:
            problems.append(f"{path.name}:{number} is not numeric")
            continue
        if class_id not in CLASS_NAMES:
            problems.append(f"{path.name}:{number} has class id {class_id}")
        if len(coordinates) < 6 or len(coordinates) % 2:
            problems.append(f"{path.name}:{number} has {len(coordinates)} coordinates")
            continue
        if any(not 0.0 <= v <= 1.0 for v in coordinates):
            problems.append(f"{path.name}:{number} has coordinates outside [0, 1]")
        instances.append((class_id, len(coordinates) // 2))
    return instances, problems


def condition(stem: str) -> tuple[str, str, str]:
    """Recover (motion, view range, crack width) from a filename."""
    lowered = stem.lower()
    found = []
    for group in (MOTIONS, VIEWS, WIDTHS):
        found.append(next((v for v in group if v.lower() in lowered), "unknown"))
    return tuple(found)  # type: ignore[return-value]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("root", type=Path, help="the extracted BCG directory")
    parser.add_argument("--checksums", action="store_true",
                        help="also compare against checksums.sha256 beside this script")
    args = parser.parse_args()

    images_dir, labels_dir = args.root / "images", args.root / "labels"
    for directory in (images_dir, labels_dir):
        if not directory.is_dir():
            print(f"missing directory: {directory}", file=sys.stderr)
            return 1

    images = {p.stem: p for p in sorted(images_dir.iterdir())
              if p.suffix.lower() in {".png", ".jpg", ".jpeg"}}
    labels = {p.stem: p for p in sorted(labels_dir.glob("*.txt"))}

    problems = []
    for stem in sorted(set(images) - set(labels)):
        problems.append(f"image without label: {stem}")
    for stem in sorted(set(labels) - set(images)):
        problems.append(f"label without image: {stem}")

    per_class = collections.Counter()
    vertices = collections.Counter()
    conditions = collections.Counter()
    empty = 0
    for stem in sorted(set(images) & set(labels)):
        instances, found = parse_label(labels[stem])
        problems.extend(found)
        if not instances:
            empty += 1
        for class_id, count in instances:
            per_class[class_id] += 1
            vertices[class_id] += count
        conditions[condition(stem)] += 1

    sizes = collections.Counter()
    try:
        from PIL import Image
        for stem in sorted(set(images) & set(labels)):
            with Image.open(images[stem]) as handle:
                sizes[handle.size] += 1
    except ImportError:
        print("Pillow is not installed; skipping the image-size check.\n")

    print(f"root          {args.root}")
    print(f"paired        {len(set(images) & set(labels))}")
    print(f"images only   {len(set(images) - set(labels))}")
    print(f"labels only   {len(set(labels) - set(images))}")
    print(f"empty labels  {empty}")
    if sizes:
        print("sizes         " + ", ".join(f"{w}x{h}: {n}" for (w, h), n in sizes.most_common()))

    print("\ninstances per class")
    for class_id, name in CLASS_NAMES.items():
        count = per_class[class_id]
        mean = vertices[class_id] / count if count else 0
        print(f"  {class_id} {name:14s} {count:8d}   mean vertices {mean:6.1f}")

    print("\ngeneration conditions")
    for (motion, view, width), count in sorted(conditions.items()):
        print(f"  {motion:12s} {view:7s} {width:9s} {count:6d}")

    if args.checksums:
        manifest = Path(__file__).with_name("checksums.sha256")
        if not manifest.exists():
            print(f"\nno checksum file at {manifest}", file=sys.stderr)
        else:
            mismatched = 0
            for line in manifest.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                expected, _, relative = line.partition("  ")
                target = args.root / relative.strip()
                if not target.exists():
                    problems.append(f"checksummed file missing: {relative.strip()}")
                    continue
                actual = hashlib.sha256(target.read_bytes()).hexdigest()
                if actual != expected.strip():
                    problems.append(f"checksum mismatch: {relative.strip()}")
                    mismatched += 1
            print(f"\nchecksums     {'all match' if not mismatched else f'{mismatched} mismatched'}")

    if problems:
        print(f"\n{len(problems)} problem(s):")
        for line in problems[:40]:
            print("  " + line)
        if len(problems) > 40:
            print(f"  ... and {len(problems) - 40} more")
        return 1

    print("\nno problems found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
