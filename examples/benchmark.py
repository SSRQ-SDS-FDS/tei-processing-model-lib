from pathlib import Path
from tempfile import mkdtemp
from time import perf_counter

from lxml import etree

from src import TeiPM

SAMPLE_ODD = Path(__file__).parent.parent / "test/example/sample.odd"

if __name__ == "__main__":
    temp_dir = Path(mkdtemp())
    parser = etree.XMLParser()
    docs_count = 50000

    for i in range(docs_count):
        content = f"""<TEI xmlns='http://www.tei-c.org/ns/1.0'>
                <teiHeader>
                </teiHeader>
                <text>
                    <body>
                        <p>This is the paragraph of {i} <ref target="www.google.com">This is a link</ref></p>
                        <p>This is the paragraph of {i} <ref target="www.google.com">This is a link</ref></p>
                        <p>This is the paragraph of {i} <ref target="www.google.com">This is a link</ref></p>
                        <p>This is the paragraph of {i} <ref target="www.google.com">This is a link</ref></p>
                        <p>This is the paragraph of {i} <ref target="www.google.com">This is a link</ref></p>
                        <p>This is the paragraph of {i} <ref target="www.google.com">This is a link</ref></p>
                        <p>This is the paragraph of {i} <ref target="www.google.com">This is a link</ref></p>
                        <p>This is the paragraph of {i} <ref target="www.google.com">This is a link</ref></p>
                    </body>
                </text>
            </TEI>"""
        tree = etree.ElementTree(etree.fromstring(content, parser))
        tree.write(
            str(temp_dir / f"file_{i}.xml"), xml_declaration=True, encoding="utf-8"
        )

    tei_pm = TeiPM(SAMPLE_ODD)

    start = perf_counter()
    result_single = tei_pm.transform_tei(source=str(temp_dir / "*.xml"), mp=False)
    end = perf_counter()
    assert result_single is not None
    assert len(result_single) == docs_count
    print(f"Transforming {docs_count} singlethreaded took: {end - start}")

    start = perf_counter()
    result_mp = tei_pm.transform_tei(source=str(temp_dir / "*.xml"), mp=True)
    end = perf_counter()
    assert result_mp is not None
    assert len(result_mp) == docs_count
    print(f"Transforming {docs_count} using multiprocessing took: {end - start}")
