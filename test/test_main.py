from pathlib import Path
from tempfile import mkdtemp

import pytest
from lxml import etree
from saxonche import PySaxonProcessor

from src import TeiPM

SAMPLE_ODD = Path(__file__).parent / "example/sample.odd"


class SimpleTEIWriter:
    path: Path

    def __init__(self, dir: Path):
        self.path = dir

    def write(self, name: str, content: str) -> None:
        parser = etree.XMLParser()
        tree = etree.ElementTree(etree.fromstring(content, parser))

        tree.write(
            str(self.path / f"{name}.xml"), xml_declaration=True, encoding="utf-8"
        )

    def list(self) -> list[str]:
        return [str(file.absolute()) for file in self.path.glob("*.xml")]

    def construct_file_pattern(self) -> str:
        return str(self.path.absolute() / "*.xml")


def query(xml_input: str, xpath: str):
    with PySaxonProcessor(license=False) as proc:
        xp = proc.new_xpath_processor()
        node = proc.parse_xml(xml_text=xml_input)
        xp.set_context(xdm_item=node)
        return xp.evaluate_single(xpath)


@pytest.fixture(scope="function")
def writer(tmp_path: Path) -> SimpleTEIWriter:
    """A fixture, which returns a SimpleTEIWriter object, which can be used to write TEI files to a temporary directory."""
    return SimpleTEIWriter(tmp_path)


@pytest.fixture(scope="function")
def tei_files(writer: SimpleTEIWriter) -> str:
    """A fixture, which returns a list of paths to TEI files, which are written to a temporary directory."""
    template = """<TEI xmlns='http://www.tei-c.org/ns/1.0'>
            <teiHeader>
            </teiHeader>
            <text>
                <body>
                    <p>This is a paragraph <ref target="www.google.com">This is a link</ref></p>
                </body>
            </text>
        </TEI>"""
    writer.write("sample_one.xml", template)
    return writer.construct_file_pattern()


@pytest.fixture(scope="session")
def tei_pm() -> TeiPM:
    return TeiPM(SAMPLE_ODD)


def test_odd2xsl(tei_pm: TeiPM):
    """The generated xsl:templates should be equal to the models in the odd + 2."""
    assert tei_pm.pm is not None
    assert isinstance(tei_pm.pm, str)
    models = query(xml_input=tei_pm.odd, xpath="count(//*:model)")
    templates = query(xml_input=tei_pm.pm, xpath="count(//*:template)")
    assert int(models) + 2 == int(templates)


def test_mp_transformation(tei_pm: TeiPM):
    len_files = 80
    mp_writer = SimpleTEIWriter(Path(mkdtemp()))
    for i in range(len_files):
        template = f"""<TEI xmlns='http://www.tei-c.org/ns/1.0'>
                <teiHeader>
                </teiHeader>
                <text>
                    <body>
                        <p>This is a paragraph of number {i}  <ref target="www.google.com">This is a link</ref></p>
                    </body>
                </text>
            </TEI>"""
        mp_writer.write(f"sample_mp_{i}.xml", template)

    t = tei_pm.transform_tei(source=mp_writer.construct_file_pattern(), mp=True)
    assert t is not None
    assert len(t) == len_files


def test_behaviour_document(tei_pm: TeiPM, tei_files: str):
    t = tei_pm.transform_tei(source=tei_files, mp=False)
    assert t is not None
    for i in t:
        assert int(query(xml_input=i, xpath="count(/*:html)")) == 1
        assert str(query(xml_input=i, xpath="local-name(./*:html)")) == "html"
        assert bool(query(xml_input=i, xpath="./*:html/@class => contains('tei-html')"))


def test_behaviour_paragraph(tei_pm: TeiPM, tei_files: str):
    t = tei_pm.transform_tei(source=tei_files, root="//p", mp=False)

    assert t is not None
    for i in t:
        assert int(query(xml_input=i, xpath="count(//*:p)")) == 1
        assert str(query(xml_input=i, xpath="local-name(./*:p)")) == "p"
        assert bool(query(xml_input=i, xpath="./*:p/@class => contains('tei-p')"))


def test_behaviour_link(tei_pm: TeiPM, tei_files: str):
    t = tei_pm.transform_tei(source=tei_files, root="//p", mp=False)

    assert t is not None
    for i in t:
        assert int(query(xml_input=i, xpath="count(//*:a)")) == 1
        assert str(query(xml_input=i, xpath="local-name(./*:p[1]/*:a)")) == "a"
        assert bool(query(xml_input=i, xpath="./*:p/@href => contains('google')"))
