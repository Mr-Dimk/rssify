"""
Тесты для класса RSSGenerator (app/rss_generator.py).
"""
import pytest
from app.rss_generator import RSSGenerator
from datetime import datetime, timezone


def test_rssgenerator_basic_metadata():
    gen = RSSGenerator(title="Test Feed", link="https://example.com", description="Desc")
    xml = gen.generate_feed()
    assert "Test Feed" in xml
    assert "https://example.com" in xml
    assert "Desc" in xml
    assert xml.startswith("<?xml")
    assert "<rss" in xml


def test_rssgenerator_set_metadata():
    gen = RSSGenerator(title="A", link="B", description="C")
    gen.set_metadata(title="T", link="L", description="D", language="ru")
    xml = gen.generate_feed()
    assert "T" in xml
    assert "L" in xml
    assert "D" in xml
    assert "ru" in xml


def test_rssgenerator_add_item_minimal():
    gen = RSSGenerator(title="Feed", link="/", description="D")
    gen.add_item(title="Post1", link="https://x", description="Body")
    xml = gen.generate_feed()
    assert "Post1" in xml
    assert "https://x" in xml
    assert "Body" in xml
    assert "<item>" in xml


def test_rssgenerator_add_item_guid_pubdate():
    gen = RSSGenerator(title="Feed", link="/", description="D")
    dt = datetime(2024, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    gen.add_item(title="P", link="https://l", guid="custom-guid", pubdate=dt)
    xml = gen.generate_feed()
    assert "custom-guid" in xml
    assert "P" in xml
    assert "https://l" in xml
    # pubDate in RFC822 format
    assert "Tue, 02 Jan 2024" in xml


def test_rssgenerator_multiple_items():
    gen = RSSGenerator(title="Feed", link="/", description="D")
    for i in range(3):
        gen.add_item(title=f"T{i}", link=f"https://l{i}", description=f"Desc{i}")
    xml = gen.generate_feed()
    for i in range(3):
        assert f"T{i}" in xml
        assert f"https://l{i}" in xml
        assert f"Desc{i}" in xml
    assert xml.count("<item>") == 3


def test_rssgenerator_max_items_limit():
    gen = RSSGenerator(title="Feed", link="/", description="D", max_items=2)
    gen.add_item(title="T1", link="https://l1", description="D1")
    gen.add_item(title="T2", link="https://l2", description="D2")
    gen.add_item(title="T3", link="https://l3", description="D3")
    xml = gen.generate_feed()
    assert "T1" not in xml  # только последние 2
    assert "T2" in xml
    assert "T3" in xml
    assert xml.count("<item>") == 2


def test_rssgenerator_pubdate_str_iso():
    gen = RSSGenerator(title="Feed", link="/", description="D")
    # ISO string без tzinfo
    gen.add_item(title="P", link="https://l", guid="g", pubdate="2024-01-02T03:04:05")
    xml = gen.generate_feed()
    assert "Tue, 02 Jan 2024" in xml


def test_rssgenerator_atom_feed():
    gen = RSSGenerator(title="Feed", link="/", description="D")
    gen.add_item(title="T1", link="https://l1", description="D1")
    atom = gen.generate_atom_feed()
    assert "<feed" in atom
    assert "T1" in atom
    assert "D1" in atom
    assert "application/atom+xml" not in atom  # только XML, не HTTP


def test_rssgenerator_custom_fields():
    gen = RSSGenerator(title="Feed", link="/", description="D")
    gen.add_item(title="T2", link="https://l2", description="D2", author="Ivan", category="Tech", custom1="val1")
    xml = gen.generate_feed()
    # В RSS author не поддерживается, только category и кастомные поля
    assert "Tech" in xml
    assert "custom1:val1" in xml
    # Проверим author только в Atom
    atom = gen.generate_atom_feed()
    assert "Ivan" in atom


def test_rssgenerator_html_description():
    gen = RSSGenerator(title="Feed", link="/", description="D")
    html = "<b>Bold</b> <i>Italic</i>"
    gen.add_item(title="T3", link="https://l3", description=html, html_description=True)
    xml = gen.generate_feed()
    # В RSS 2.0 и Atom HTML экранируется
    assert "&lt;b&gt;Bold&lt;/b&gt;" in xml
    assert "&lt;i&gt;Italic&lt;/i&gt;" in xml
    atom = gen.generate_atom_feed()
    assert "&lt;b&gt;Bold&lt;/b&gt;" in atom
    assert "&lt;i&gt;Italic&lt;/i&gt;" in atom
