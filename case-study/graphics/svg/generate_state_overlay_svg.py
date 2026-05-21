#!/usr/bin/env python3
"""Generate scenario overlays by updating data and labels inside base-graph.svg.

Input JSON schema (minimal):
{
  "mode": "overlay",  // overlay | empty | full
  "title": "Empty vs Full State Overlay",
  "x_label": "TIME",
  "y_label": "POWER / CURRENT",
  "empty_legend": "EMPTY STATE (BASELINE)",
  "full_legend": "FULL STATE (HIGH RESISTANCE)",
  "focus_text": ["PEAK LOAD SHIFTS", "EARLIER IN CYCLE", "WHEN FULL"],
  "empty_points": [[0.0, 0.32], [0.3, 0.51], [1.0, 0.45]],
  "full_points": [[0.0, 0.36], [0.3, 0.62], [1.0, 0.58]]
}

Point coordinates are normalized in [0, 1] where y=1 is the top of plot and y=0 is bottom.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence
import xml.etree.ElementTree as ET


VIEWBOX_W = 3508
VIEWBOX_H = 2481

PLOT_LEFT = 430
PLOT_RIGHT = 3160
PLOT_TOP = 760
PLOT_BOTTOM = 2210

INK = "rgb(10, 29, 87)"
ACCENT = "rgb(120, 156, 240)"

SVG_NS = "http://www.w3.org/2000/svg"
SERIF_NS = "http://www.serif.com/"

DATA_SCALE_X = 1.14199
DATA_SCALE_Y = 1.176663
DATA_OFFSET_X = -122.065504
DATA_OFFSET_Y = -811.47158

ET.register_namespace("", SVG_NS)
ET.register_namespace("serif", SERIF_NS)


@dataclass(frozen=True)
class Point:
    x: float
    y: float


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def normalize_points(points: Sequence[Sequence[float]]) -> list[Point]:
    if len(points) < 2:
        raise ValueError("Need at least 2 points per series")

    parsed = [Point(float(p[0]), float(p[1])) for p in points]
    parsed = [Point(clamp01(p.x), clamp01(p.y)) for p in parsed]
    parsed.sort(key=lambda p: p.x)
    return parsed


def to_plot_point(p: Point) -> Point:
    x = PLOT_LEFT + p.x * (PLOT_RIGHT - PLOT_LEFT)
    # Input y=1 means visually high (near top), y=0 means low (near bottom).
    y = PLOT_BOTTOM - p.y * (PLOT_BOTTOM - PLOT_TOP)
    return Point(x, y)


def to_template_point(p: Point) -> Point:
    """Convert viewBox coordinates into the transformed Data-group local coordinates."""
    x = (p.x - DATA_OFFSET_X) / DATA_SCALE_X
    y = (p.y - DATA_OFFSET_Y) / DATA_SCALE_Y
    return Point(x, y)


def line_path(points: Iterable[Point]) -> str:
    pts = list(points)
    start = pts[0]
    chunks = [f"M{start.x:.2f},{start.y:.2f}"]
    for p in pts[1:]:
        chunks.append(f"L{p.x:.2f},{p.y:.2f}")
    return " ".join(chunks)


def area_path(points: Iterable[Point], baseline_y: float) -> str:
    pts = list(points)
    if not pts:
        raise ValueError("No points provided")
    d = [f"M{pts[0].x:.2f},{baseline_y:.2f}"]
    d.append(f"L{pts[0].x:.2f},{pts[0].y:.2f}")
    for p in pts[1:]:
        d.append(f"L{p.x:.2f},{p.y:.2f}")
    d.append(f"L{pts[-1].x:.2f},{baseline_y:.2f}")
    d.append("Z")
    return " ".join(d)


def compute_focus_x(empty_plot: Sequence[Point], full_plot: Sequence[Point]) -> float:
    pairs = zip(empty_plot, full_plot)
    best = max(pairs, key=lambda pair: abs(pair[1].y - pair[0].y))
    return (best[0].x + best[1].x) / 2.0


def qname(tag: str) -> str:
    return f"{{{SVG_NS}}}{tag}"


def find_by_id(root: ET.Element, element_id: str) -> ET.Element:
    for node in root.iter():
        if node.attrib.get("id") == element_id:
            return node
    raise ValueError(f"Element with id '{element_id}' not found in template")


def first_path_in_group(root: ET.Element, group_id: str) -> ET.Element:
    group = find_by_id(root, group_id)
    node = group.find(f".//{qname('path')}")
    if node is None:
        raise ValueError(f"No path found in group '{group_id}'")
    return node


def first_text_in_group(root: ET.Element, group_id: str) -> ET.Element:
    group = find_by_id(root, group_id)
    node = group.find(f".//{qname('text')}")
    if node is None:
        raise ValueError(f"No text found in group '{group_id}'")
    return node


def set_plain_text(node: ET.Element, text: str) -> None:
    for child in list(node):
        node.remove(child)
    node.text = text


def set_or_replace_style(root: ET.Element) -> None:
    style_node = None
    for child in root.findall(qname("style")):
        if child.attrib.get("id") == "Dynamic-Mode-Style":
            style_node = child
            break

    css = f"""
    svg {{
      --ink: {INK};
      --accent: {ACCENT};
      --full-wave-fill: var(--accent);
      --empty-wave-stroke: var(--ink);
      --full-opacity: 1;
      --empty-opacity: 1;
      --full-legend-opacity: 1;
      --empty-legend-opacity: 1;
      --focus-opacity: 1;
    }}
    #High-Resistance-Full-State-Chart path {{
      fill: var(--full-wave-fill) !important;
      opacity: var(--full-opacity);
    }}
    #Baseline-Empty-State-Chart path {{
      fill: none !important;
      stroke: var(--empty-wave-stroke) !important;
      opacity: var(--empty-opacity);
    }}
    #Legend-Item-2 {{ opacity: var(--full-legend-opacity); }}
    #Legend-Item-1 {{ opacity: var(--empty-legend-opacity); }}
    #Focus {{ opacity: var(--focus-opacity); }}
    svg[data-mode="overlay"] {{
      --full-opacity: 1;
      --empty-opacity: 1;
      --full-legend-opacity: 1;
      --empty-legend-opacity: 1;
      --focus-opacity: 1;
    }}
    svg[data-mode="empty"] {{
      --full-opacity: .18;
      --empty-opacity: 1;
      --full-legend-opacity: .35;
      --empty-legend-opacity: 1;
      --focus-opacity: 0;
    }}
    svg[data-mode="full"] {{
      --full-opacity: 1;
      --empty-opacity: .25;
      --full-legend-opacity: 1;
      --empty-legend-opacity: .35;
      --focus-opacity: 1;
    }}
    """.strip()

    if style_node is None:
        style_node = ET.Element(qname("style"), {"id": "Dynamic-Mode-Style", "type": "text/css"})
        insert_at = 0
        if len(root) > 0 and root[0].tag == qname("title"):
            insert_at = 1
            if len(root) > 1 and root[1].tag == qname("desc"):
                insert_at = 2
        root.insert(insert_at, style_node)

    style_node.text = css


def ensure_title_and_desc(root: ET.Element, title: str) -> None:
    title_node = root.find(qname("title"))
    if title_node is None:
        title_node = ET.Element(qname("title"))
        root.insert(0, title_node)
    title_node.text = title

    desc_node = root.find(qname("desc"))
    if desc_node is None:
        desc_node = ET.Element(qname("desc"))
        root.insert(1, desc_node)
    desc_node.text = "Generated comparison chart from base-graph.svg template."


def upsert_focus_group(root: ET.Element, focus_x: float, focus_lines: Sequence[str]) -> None:
    focus = next((node for node in root if node.attrib.get("id") == "Focus"), None)
    if focus is None:
        focus = ET.SubElement(root, qname("g"), {"id": "Focus"})
    else:
        for child in list(focus):
            focus.remove(child)

    line_group = ET.SubElement(focus, qname("g"), {"id": "Focus-Line", f"{{{SERIF_NS}}}id": "Focus Line"})
    ET.SubElement(
        line_group,
        qname("path"),
        {
            "d": f"M{focus_x:.2f},{PLOT_BOTTOM:.2f} L{focus_x:.2f},{PLOT_TOP:.2f}",
            "style": "fill:none;stroke:rgb(120,156,240);stroke-width:4.1px;stroke-dasharray:20.5,20.5;",
        },
    )

    sign_group = ET.SubElement(focus, qname("g"), {"id": "Focus-Sign", f"{{{SERIF_NS}}}id": "Focus Sign"})
    ET.SubElement(
        sign_group,
        qname("rect"),
        {
            "x": f"{focus_x - 340:.2f}",
            "y": f"{PLOT_TOP + 120:.2f}",
            "width": "700",
            "height": "220",
            "rx": "22",
            "style": "fill:white;fill-opacity:.18;stroke:rgb(120,156,240);stroke-width:3px;",
        },
    )

    ys = [PLOT_TOP + 190, PLOT_TOP + 245, PLOT_TOP + 300]
    for i, line in enumerate(focus_lines[:3]):
        ET.SubElement(
            sign_group,
            qname("text"),
            {
                "x": f"{focus_x + 10:.2f}",
                "y": f"{ys[i]:.2f}",
                "text-anchor": "middle",
                "style": "font-family:'Inter-Bold','Inter';font-weight:700;font-size:48px;fill:rgb(10,29,87);",
            },
        ).text = line


def render_svg(data: dict, template_path: Path) -> str:
    mode = str(data.get("mode", "overlay"))
    title = str(data.get("title", "Empty vs Full State Overlay"))
    x_label = str(data.get("x_label", "TIME"))
    y_label = str(data.get("y_label", "POWER / CURRENT"))
    empty_legend = str(data.get("empty_legend", "EMPTY STATE (BASELINE)"))
    full_legend = str(data.get("full_legend", "FULL STATE (HIGH RESISTANCE)"))
    focus_lines = data.get("focus_text", ["PEAK LOAD SHIFTS", "EARLIER IN CYCLE", "WHEN FULL"])
    focus_lines = [str(line) for line in focus_lines[:3]]
    while len(focus_lines) < 3:
        focus_lines.append("")

    empty_points = normalize_points(data["empty_points"])
    full_points = normalize_points(data["full_points"])

    if len(empty_points) != len(full_points):
        raise ValueError("empty_points and full_points must have the same number of points")

    empty_plot = [to_plot_point(p) for p in empty_points]
    full_plot = [to_plot_point(p) for p in full_points]

    empty_tpl = [to_template_point(p) for p in empty_plot]
    full_tpl = [to_template_point(p) for p in full_plot]
    baseline_tpl = to_template_point(Point(PLOT_LEFT, PLOT_BOTTOM)).y

    empty_d = line_path(empty_tpl)
    full_d = area_path(full_tpl, baseline_y=baseline_tpl)
    focus_x = compute_focus_x(empty_plot, full_plot)

    root = ET.fromstring(template_path.read_text(encoding="utf-8"))
    root.set("data-mode", mode)
    root.set("viewBox", f"0 0 {VIEWBOX_W} {VIEWBOX_H}")
    root.set("width", "100%")
    root.set("height", "100%")

    ensure_title_and_desc(root, title)
    set_or_replace_style(root)

    empty_path = first_path_in_group(root, "Baseline-Empty-State-Chart")
    empty_path.set("d", empty_d)
    empty_path.set(
        "style",
        "fill:none;stroke:rgb(10,29,87);stroke-width:10.78px;stroke-linejoin:round;stroke-miterlimit:1.5;",
    )

    full_path = first_path_in_group(root, "High-Resistance-Full-State-Chart")
    full_path.set("d", full_d)
    full_path.set("style", "fill:rgb(120,156,240);")

    set_plain_text(first_text_in_group(root, "X-Axis-Label"), x_label)
    set_plain_text(first_text_in_group(root, "Y-Axis-Label"), y_label)
    set_plain_text(first_text_in_group(root, "Label1"), empty_legend)
    set_plain_text(first_text_in_group(root, "Label"), full_legend)

    upsert_focus_group(root, focus_x, focus_lines)

    xml_body = ET.tostring(root, encoding="unicode")
    return '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_body + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate empty vs full state SVG from point data")
    parser.add_argument("--input", required=True, type=Path, help="Path to input JSON")
    parser.add_argument("--output", required=True, type=Path, help="Path to output SVG")
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).with_name("base-graph.svg"),
        help="Base SVG template path (default: base-graph.svg)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    svg = render_svg(payload, args.template)
    args.output.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
