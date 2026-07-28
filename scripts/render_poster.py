from __future__ import annotations

import argparse
import io
import json
from pathlib import Path
from typing import Any

import requests
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WIDTH = 1080
HEIGHT = 1350
IMAGE_HEIGHT = 900
PANEL_TOP = 900
BLUE = "#1261ff"
WHITE = "#f8f8fb"
MUTED = "#b8b8be"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a deterministic FrontBrief.AI 1080x1350 social poster."
    )
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def load_spec(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        spec = json.load(handle)
    required = {
        "date",
        "category",
        "headline",
        "subhead",
        "poster_shape",
        "image_kind",
    }
    missing = sorted(required - spec.keys())
    if missing:
        raise ValueError(f"Poster spec is missing: {', '.join(missing)}")
    if spec["image_kind"] not in {"photo", "branded_scene", "conceptual"}:
        raise ValueError("image_kind must be photo, branded_scene, or conceptual")
    if not spec.get("image_url") and not spec.get("image_path"):
        raise ValueError("Poster spec needs image_url or image_path")
    return spec


def load_background(spec: dict[str, Any]) -> Image.Image:
    if spec.get("image_path"):
        path = Path(spec["image_path"])
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        image = Image.open(path)
    else:
        response = requests.get(
            spec["image_url"],
            headers={"User-Agent": "FrontBriefAI-Poster/1.0"},
            timeout=60,
        )
        response.raise_for_status()
        if len(response.content) > 25_000_000:
            raise ValueError("Background image exceeds 25 MB")
        image = Image.open(io.BytesIO(response.content))
    return image.convert("RGB")


def font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont:
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default(size=size)


def headline_font(size: int) -> ImageFont.FreeTypeFont:
    return font(
        [
            "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf",
            "/System/Library/Fonts/Supplemental/Impact.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        ],
        size,
    )


def body_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return font(
        [
            (
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
                if bold
                else "/System/Library/Fonts/Supplemental/Arial.ttf"
            ),
            (
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
                if bold
                else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            ),
            (
                "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
                if bold
                else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
            ),
        ],
        size,
    )


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    chosen_font: ImageFont.ImageFont,
    max_width: int,
) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=chosen_font)[2] <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def fit_headline(
    draw: ImageDraw.ImageDraw, text: str
) -> tuple[ImageFont.ImageFont, list[str], int]:
    for size in range(76, 51, -2):
        chosen = headline_font(size)
        lines = wrap_text(draw, text.upper(), chosen, 965)
        line_height = int(size * 1.02)
        if len(lines) <= 3 and len(lines) * line_height <= 220:
            return chosen, lines, line_height
    raise ValueError("Headline is too long for the locked three-line poster layout")


def paste_branding(canvas: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    monogram = Image.open(PROJECT_ROOT / "web/public/fb-white.png").convert("RGBA")
    monogram.thumbnail((122, 122), Image.Resampling.LANCZOS)
    canvas.alpha_composite(monogram, (900, 54))

    pill = (690, 1230, 1024, 1298)
    draw.rounded_rectangle(pill, radius=34, fill="white", outline="#b8f0d0", width=2)
    brand = Image.open(PROJECT_ROOT / "assets/brand/whitebg.png").convert("RGB")
    brand = brand.crop((355, 475, 1230, 805))
    brand = ImageOps.contain(brand, (285, 54), Image.Resampling.LANCZOS)
    x = pill[0] + (pill[2] - pill[0] - brand.width) // 2
    y = pill[1] + (pill[3] - pill[1] - brand.height) // 2
    canvas.paste(brand, (x, y))


def render(spec: dict[str, Any], output: Path) -> None:
    background = ImageOps.fit(
        load_background(spec),
        (WIDTH, IMAGE_HEIGHT),
        method=Image.Resampling.LANCZOS,
        centering=(float(spec.get("focus_x", 0.5)), float(spec.get("focus_y", 0.42))),
    )
    background = ImageEnhance.Brightness(background).enhance(0.82)

    canvas = Image.new("RGBA", (WIDTH, HEIGHT), "#0a0a0a")
    canvas.paste(background, (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, PANEL_TOP, WIDTH, HEIGHT), fill="#0a0a0a")

    category = f"AI · {str(spec['category']).upper()}"
    draw.text((56, 956), category, font=body_font(30, bold=True), fill=WHITE)

    chosen_font, lines, line_height = fit_headline(draw, str(spec["headline"]))
    y = 1011
    for line in lines:
        draw.text((56, y), line, font=chosen_font, fill=WHITE)
        y += line_height

    subhead_font = body_font(27)
    subhead_lines = wrap_text(draw, str(spec["subhead"]), subhead_font, 590)
    if len(subhead_lines) > 2:
        raise ValueError("Subhead is too long for the locked two-line layout")
    subhead_y = max(1227, y + 18)
    if subhead_y + len(subhead_lines) * 32 > 1310:
        raise ValueError("Headline and subhead overflow the poster")
    for line in subhead_lines:
        draw.text((56, subhead_y), line, font=subhead_font, fill=MUTED)
        subhead_y += 32

    paste_branding(canvas, draw)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, "PNG", optimize=True)


def main() -> int:
    args = parse_args()
    spec_path = args.spec if args.spec.is_absolute() else PROJECT_ROOT / args.spec
    output_path = args.output if args.output.is_absolute() else PROJECT_ROOT / args.output
    render(load_spec(spec_path), output_path)
    print(f"Rendered {output_path} (1080x1350)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
