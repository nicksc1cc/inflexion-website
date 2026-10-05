#!/usr/bin/env python3
"""Check the shared structural contract for Inflexion Perspectives articles."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
POSTS = [
    'aeo-rankings-to-citations', 'agentic-media-buying', 'ai-citations-source-map',
    'ai-impact-digital-advertising', 'ai-in-retail-media', 'ai-visibility-uncertainty',
    'amazon-ai-commerce-control', 'amazon-ai-creative-studio', 'amazon-marketing-cloud-sql',
    'amazon-rufus-sponsored-prompts', 'offsite-retail-media-measurement',
    'shoppable-ai-search', 'technical-geo-ai-crawlers'
]

class ContractParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stylesheets = []
        self.json_blocks = []
        self.in_json = False
        self.json_buffer = []
        self.tags = set()
    def handle_starttag(self, tag, attrs):
        self.tags.add(tag)
        attrs = dict(attrs)
        if tag == 'link' and attrs.get('rel') == 'stylesheet':
            self.stylesheets.append(attrs.get('href', ''))
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.in_json = True
            self.json_buffer = []
    def handle_data(self, data):
        if self.in_json:
            self.json_buffer.append(data)
    def handle_endtag(self, tag):
        if tag == 'script' and self.in_json:
            self.json_blocks.append(''.join(self.json_buffer))
            self.in_json = False

errors = []
for slug in POSTS:
    path = ROOT / slug / 'index.html'
    if not path.exists():
        errors.append(f'{slug}: missing index.html')
        continue
    parser = ContractParser()
    text = path.read_text(errors='replace')
    parser.feed(text)
    if not any(href.startswith('../assets/design-system/tokens-built.css') for href in parser.stylesheets):
        errors.append(f'{slug}: missing or incorrect token stylesheet path')
    if not any(href.startswith('../assets/common.css') for href in parser.stylesheets):
        errors.append(f'{slug}: missing or incorrect common stylesheet path')
    if not any(href.startswith('../assets/perspectives-editorial.css') for href in parser.stylesheets):
        errors.append(f'{slug}: missing shared editorial stylesheet')
    if 'article-hero' not in text or ('article-layout' not in text and 'article-grid' not in text):
        errors.append(f'{slug}: missing article hero/layout contract')
    toc_blocks = re.findall(r'<aside\b[^>]*class="[^"]*(?:article-aside|article-toc)[^"]*[\s\S]*?</aside>', text)
    if len(toc_blocks) != 1:
        errors.append(f'{slug}: expected exactly one article TOC, found {len(toc_blocks)}')
    else:
        toc_hrefs = re.findall(r'href="#([^"]+)"', toc_blocks[0])
        if not toc_hrefs:
            errors.append(f'{slug}: TOC has no in-page anchors')
        for href in toc_hrefs:
            if not re.search(r'id="' + re.escape(href) + r'"', text):
                errors.append(f'{slug}: TOC anchor #{href} has no target')
        if re.search(r'<a\s+href="(?!#)', toc_blocks[0]):
            errors.append(f'{slug}: TOC contains an external or site-navigation link')
    for index, block in enumerate(parser.json_blocks, 1):
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f'{slug}: invalid JSON-LD block {index}: {exc.msg}')
    if '<!--' in text and 'TODO' in text:
        errors.append(f'{slug}: TODO marker present')

print(f'checked {len(POSTS)} Perspectives posts')
if errors:
    print('\n'.join(f'FAIL: {error}' for error in errors))
    sys.exit(1)
print('PASS: shared stylesheet, article geometry and JSON-LD contracts present on every post')
