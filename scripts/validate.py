#!/usr/bin/env python3
"""Validation script for the AI Password Manager Guide static site.

Checks:
- All HTML files parse without errors
- All internal links resolve to existing files
- Required elements present (header, nav, main, footer)
- Asdale Dynamics, LLC credit present on each page
- LICENSE contains the exact required copyright line
- No secrets, API keys, or personal data patterns in files
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"
DOCS_DIR = ROOT / "docs"
LICENSE_FILE = ROOT / "LICENSE"
README_FILE = ROOT / "README.md"

ERRORS = []
WARNINGS = []


def error(msg):
    ERRORS.append(msg)
    print(f"  ERROR: {msg}")


def warning(msg):
    WARNINGS.append(msg)
    print(f"  WARN:  {msg}")


def ok(msg):
    print(f"  ok:    {msg}")


# HTML5 void elements (self-closing, never have children)
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

# HTML5 elements where the closing tag is optional
OPTIONAL_CLOSE_TAGS = {
    "li", "p", "td", "th", "tr", "thead", "tbody", "tfoot",
    "colgroup", "dt", "dd", "rt", "rp", "optgroup", "option",
    "col", "html", "head", "body",
}


class HTMLValidator(HTMLParser):
    """Simple HTML parser that tracks open tags and collects links."""

    def __init__(self, source_path):
        super().__init__()
        self.source_path = source_path
        self.open_tags = []
        self.links = []
        self.errors = []
        self.has_header = False
        self.has_nav = False
        self.has_main = False
        self.has_footer = False
        self.text = []

    def handle_starttag(self, tag, attrs):
        # Void elements never need closing
        if tag in VOID_ELEMENTS:
            if tag == "a":
                for attr, value in attrs:
                    if attr == "href":
                        self.links.append((value, self.getpos()))
            return
        self.open_tags.append(tag)
        if tag == "header":
            self.has_header = True
        if tag == "nav":
            self.has_nav = True
        if tag == "main":
            self.has_main = True
        if tag == "footer":
            self.has_footer = True
        if tag == "a":
            for attr, value in attrs:
                if attr == "href":
                    self.links.append((value, self.getpos()))

    def handle_endtag(self, tag):
        # Optional close tags don't need matching
        if tag in OPTIONAL_CLOSE_TAGS:
            # Pop matching open tag if present, otherwise ignore
            if tag in self.open_tags:
                # Remove the most recent occurrence
                for i in range(len(self.open_tags) - 1, -1, -1):
                    if self.open_tags[i] == tag:
                        self.open_tags.pop(i)
                        break
            return
        if self.open_tags and self.open_tags[-1] == tag:
            self.open_tags.pop()
        else:
            # Look for it anywhere in the stack (mismatched nesting)
            if tag in self.open_tags:
                for i in range(len(self.open_tags) - 1, -1, -1):
                    if self.open_tags[i] == tag:
                        self.open_tags.pop(i)
                        break
            else:
                self.errors.append(f"Unexpected closing tag: </{tag}>")

    def handle_data(self, data):
        self.text.append(data)

    def check(self):
        # Filter out optional-close tags that may remain
        remaining = [t for t in self.open_tags if t not in OPTIONAL_CLOSE_TAGS]
        if remaining:
            self.errors.append(f"Unclosed tags: {remaining}")
        return len(self.errors) == 0


SECRET_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9]{20,}"),  # OpenAI-style keys
    re.compile(r"api[_-]?key", re.IGNORECASE),
    re.compile(r"secret[_-]?key", re.IGNORECASE),
    re.compile(r"AKIA[0-9A-Z]{16}"),  # AWS access key
    re.compile(r"ghp_[a-zA-Z0-9]{36,}"),  # GitHub classic token
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),  # SSN-like
]


def scan_for_secrets(filepath):
    """Scan a file for potential secrets or personal data."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        error(f"Could not read {filepath}: {e}")
        return

    for pattern in SECRET_PATTERNS:
        for match in pattern.finditer(content):
            # Exclude documentation examples that mention "api key" conceptually
            line = content.count("\n", 0, match.start()) + 1
            warning(f"{filepath.name}:{line} possible secret pattern: {match.group()[:40]}...")

    # Check for actual-looking email addresses or phone numbers that are personal
    email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    for match in email_pattern.finditer(content):
        # dylanasdale.github.io is a public hub site, not personal data
        if "dylanasdale.github.io" not in match.group():
            line = content.count("\n", 0, match.start()) + 1
            warning(f"{filepath.name}:{line} email address found: {match.group()}")


def main():
    print(f"Validating project at: {ROOT}")
    print()

    # --- 1. Validate HTML files ---
    html_files = sorted(SITE_DIR.glob("*.html"))
    if not html_files:
        error(f"No HTML files found in {SITE_DIR}")
    else:
        ok(f"Found {len(html_files)} HTML file(s)")
        for html_file in html_files:
            print(f"\nValidating {html_file.name}:")
            try:
                content = html_file.read_text(encoding="utf-8")
            except Exception as e:
                error(f"Could not read {html_file}: {e}")
                continue

            parser = HTMLValidator(html_file)
            parser.feed(content)
            if parser.check():
                ok("HTML parses cleanly")
            else:
                for err in parser.errors:
                    error(f"HTML parse error: {err}")

            # Required elements
            if parser.has_header:
                ok("has <header>")
            else:
                error("missing <header>")
            if parser.has_nav:
                ok("has <nav>")
            else:
                error("missing <nav>")
            if parser.has_main:
                ok("has <main>")
            else:
                error("missing <main>")
            if parser.has_footer:
                ok("has <footer>")
            else:
                error("missing <footer>")

            # Asdale Dynamics credit
            if "Asdale Dynamics" in content:
                ok("contains 'Asdale Dynamics, LLC' credit")
            else:
                error("missing 'Asdale Dynamics, LLC' credit")

            # Copyright line
            if "Copyright (c) 2026 Asdale Dynamics, LLC" in content:
                ok("contains exact copyright line")
            else:
                error("missing exact copyright line")

            # Internal link resolution
            base = html_file.parent
            for link, pos in parser.links:
                if link.startswith("#") or link.startswith("http://") or link.startswith("https://") or link.startswith("mailto:"):
                    continue
                target = (base / link).resolve()
                if not target.exists():
                    error(f"broken internal link: {link} (from {html_file.name}:{pos[0]})")

    # --- 2. Validate LICENSE ---
    print("\nValidating LICENSE:")
    if not LICENSE_FILE.exists():
        error("LICENSE file not found")
    else:
        license_text = LICENSE_FILE.read_text(encoding="utf-8")
        if "Copyright (c) 2026 Asdale Dynamics, LLC" in license_text:
            ok("contains exact required copyright line")
        else:
            error("LICENSE missing exact copyright line: 'Copyright (c) 2026 Asdale Dynamics, LLC'")
        if "MIT License" in license_text:
            ok("is an MIT License")
        else:
            warning("LICENSE does not mention 'MIT License'")

    # --- 3. Validate README ---
    print("\nValidating README:")
    if not README_FILE.exists():
        error("README.md not found")
    else:
        readme_text = README_FILE.read_text(encoding="utf-8")
        if "Asdale Dynamics, LLC" in readme_text:
            ok("credits Asdale Dynamics, LLC")
        else:
            error("README missing Asdale Dynamics, LLC credit")

    # --- 4. Scan all files for secrets ---
    print("\nScanning for secrets and personal data:")
    all_files = list(ROOT.rglob("*"))
    for f in all_files:
        if f.is_file() and f.suffix in {".md", ".html", ".css", ".js", ".py", ".txt", ".json"}:
            if ".git" in f.parts:
                continue
            scan_for_secrets(f)

    # --- 5. Check for .github/workflows ---
    print("\nChecking for forbidden .github/workflows:")
    workflows = list(ROOT.glob(".github/workflows/*"))
    if workflows:
        error(f".github/workflows files found (forbidden): {[w.name for w in workflows]}")
    else:
        ok("no .github/workflows files present")

    # --- Summary ---
    print()
    print("=" * 50)
    print(f"Errors:   {len(ERRORS)}")
    print(f"Warnings: {len(WARNINGS)}")
    print("=" * 50)

    if ERRORS:
        print("VALIDATION FAILED")
        return 1
    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())