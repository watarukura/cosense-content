from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import sb2md  # noqa: E402


TESTDATA_DIR = Path(__file__).resolve().parent / "testdata"


def convert(sb_path: Path) -> str:
    buf = io.StringIO()
    with redirect_stdout(buf):
        sb2md.scrapbox_to_md(str(sb_path))
    return buf.getvalue()


@pytest.mark.parametrize(
    "name",
    [
        "basic",
        "headings",
        "lists",
        "codeblock",
        "links",
        "gyazo",
        "indent_tabs_fullwidth",
    ],
)
def test_cases(name: str) -> None:
    sb_path = TESTDATA_DIR / f"{name}.sb"
    md_path = TESTDATA_DIR / f"{name}.md"
    actual = convert(sb_path)
    expected = md_path.read_text(encoding="utf-8")
    assert actual == expected
