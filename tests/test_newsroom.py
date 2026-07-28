from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from PIL import Image

from scripts.render_poster import load_spec, render
from scripts.validate_newsroom import (
    similar,
    validate_archive,
    validate_article,
    validate_caption,
    validate_spec,
)


ARTICLE = """# FrontBrief.AI — 2026-07-29

## LINE Digest
FrontBrief.AI — 2026-07-29

TL;DR:
1. A direct signal.

Full report: https://frontbrief-ai.vercel.app/brief/2026-07-29-ai-brief

## TL;DR
- A direct signal.
- A second signal.
- A third signal.

## Top 5
### 1. New model launch changes the market
- Category: Must-Know
- Link: https://example.com/1

### 2. Second story
- Category: Product
- Link: https://example.com/2

### 3. Third story
- Category: Money
- Link: https://example.com/3

### 4. Fourth story
- Category: Research
- Link: https://example.com/4

### 5. Fifth story
- Category: People
- Link: https://example.com/5

## Money Map
Capital moved.

## Watchlist
- One
- Two
- Three

## Web Edition
A public edition.
"""


def valid_spec(image_path: str) -> dict:
    stories = [
        {
            "headline": "New model launch changes the market",
            "publication_date": "2026-07-29",
            "event_date": "2026-07-29",
            "source_url": "https://example.com/1",
        }
    ]
    for index in range(2, 6):
        stories.append(
            {
                "headline": f"Story {index}",
                "publication_date": "2026-07-28",
                "event_date": "2026-07-28",
                "source_url": f"https://example.com/{index}",
            }
        )
    return {
        "date": "2026-07-29",
        "category": "Models",
        "headline": "A NEW MODEL CHANGES THE MARKET",
        "subhead": "A concise fact that fits the locked layout",
        "poster_story": "A new model launch changes the market",
        "poster_shape": "model-launch",
        "image_kind": "photo",
        "image_path": image_path,
        "image_url": "https://images.example.com/photo.jpg",
        "visual_source_url": "https://example.com/photo",
        "source_url": "https://example.com/1",
        "publication_date": "2026-07-29",
        "brief_stories": stories,
    }


class NewsroomValidationTests(unittest.TestCase):
    def test_article_and_caption_contracts(self) -> None:
        self.assertEqual(validate_article(ARTICLE, "2026-07-29"), [])
        caption = "A strong hook.\n\nFull brief in bio.\n\n#AI #FrontBriefAI"
        self.assertEqual(validate_caption(caption), [])

    def test_similarity_catches_repeat(self) -> None:
        self.assertTrue(
            similar(
                "OpenAI launches a new agent model for developers",
                "OpenAI's new developer agent model launches",
            )
        )
        self.assertFalse(similar("New robotics benchmark", "Cloud revenue rises"))

    def test_freshness_and_shape_gates(self) -> None:
        spec = valid_spec("/tmp/example.jpg")
        self.assertEqual(validate_spec(spec, date(2026, 7, 29)), [])
        ledger = {
            "entries": [
                {
                    "date": "2026-07-28",
                    "article_lead": "Different lead",
                    "poster_story": "Different poster",
                    "poster_shape": "model-launch",
                }
            ]
        }
        errors = validate_archive(
            spec,
            ARTICLE,
            ledger,
            date(2026, 7, 29),
            Path("/nonexistent-article-archive"),
        )
        self.assertIn("poster shape repeats the previous run", errors)

    def test_renderer_produces_locked_dimensions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.jpg"
            output = root / "poster.png"
            spec_path = root / "spec.json"
            Image.new("RGB", (1600, 1000), "#16345f").save(source)
            spec_path.write_text(
                json.dumps(valid_spec(str(source))),
                encoding="utf-8",
            )
            render(load_spec(spec_path), output)
            with Image.open(output) as poster:
                self.assertEqual(poster.size, (1080, 1350))
                self.assertEqual(poster.mode, "RGB")
                self.assertEqual(poster.getpixel((0, 900)), (10, 10, 10))


if __name__ == "__main__":
    unittest.main()
