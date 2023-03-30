from asyncio import Future, gather, get_running_loop, run
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from functools import partial
from multiprocessing import cpu_count
from pathlib import Path
from typing import Optional

from saxonche import PySaxonProcessor, PyXdmNode, PyXsltExecutable  # type: ignore

from src.config import XSL_FILES
from src.utils import chunk_by_cpu_count


@dataclass
class outInfo:
    save: bool = False
    ending: str = "html"


class TeiPM:
    odd: str
    pm: str

    def __init__(self, odd: Path):
        """Initializes the Processing-Model-Class.

        Args:
            :param odd (Path): The path to the ODD file."""
        self.odd = self._read_odd(odd)
        self.pm = self.odd2xsl()

    def odd2xsl(self) -> str:
        """Transforms the ODD file to a Processing-Model-XSL-Representation.

        Returns:
            str: The Processing-Model as XSL-Representation."""

        with PySaxonProcessor(license=False) as proc:
            xsltproc = proc.new_xslt30_processor()
            xsl: PyXsltExecutable = xsltproc.compile_stylesheet(
                stylesheet_file=XSL_FILES["odd2pm"]
            )
            xml: PyXdmNode = proc.parse_xml(xml_text=self.odd)
            transformed_odd: Optional[str] = xsl.transform_to_string(xdm_node=xml)

        if transformed_odd is None:
            raise ValueError("Transformation odd2xsl failed")

        return transformed_odd

    def transform_tei(
        self,
        source: list[Path | str] | str,
        root: Optional[str] = None,
        save: Optional[outInfo] = None,
        mp: bool = False,
    ) -> list[str] | None:
        """Transforms a list of TEI files to HTML.


        Args:
            :param source (list[Path | str] | str): A list of paths to TEI files or a glob pattern.
            :param root (Optional[str], optional): The root element to be used as a starting point. Defaults to None.
            :param save (Optional[outInfo], optional): If set to True, the transformed files will be saved to disk. Defaults to None.
            :param mp (bool, optional): If set to True, the transformation will be done in parallel. Defaults to False.

        Returns:
            list[str] | None: A list of transformed files as str or None if save is set to True.
        """

        if mp:

            async def async_transform() -> list[str]:
                cpus = cpu_count()
                loop = get_running_loop()
                chunks = chunk_by_cpu_count(
                    self._find_source_files(source=source), cpus
                )

                tasks: list[Future] = []
                with ProcessPoolExecutor(max_workers=cpus) as executor:
                    for chunk in chunks:
                        tasks.append(
                            loop.run_in_executor(
                                executor,
                                partial(
                                    self._transform, source=chunk, root=root, save=save
                                ),
                            )
                        )
                process_results: list[None | list[str]] = await gather(*tasks)

                return [i for j in process_results if j is not None for i in j]

            return run(async_transform())

        return self._transform(
            source=self._find_source_files(source=source), root=root, save=save
        )

    def _find_source_files(self, source: list[Path | str] | str) -> list[str]:
        import glob

        if isinstance(source, str):
            return glob.glob(source, recursive=True)
        if isinstance(source, list):
            return [i if isinstance(i, str) else str(i) for i in source]

    def _read_odd(self, odd: Path):
        with open(odd, "r") as f:
            return f.read()

    def _transform(
        self, source: list[str], root: Optional[str], save: Optional[outInfo] = None
    ) -> list[str] | None:
        with PySaxonProcessor(license=False) as proc:
            xsltproc = proc.new_xslt30_processor()

            if root is not None:
                xsltproc.set_parameter("root", proc.make_string_value(root))

            pm_xsl: PyXsltExecutable = xsltproc.compile_stylesheet(
                stylesheet_text=self.pm
            )

            if save is not None and save.save is True:
                for i in source:
                    xml: PyXdmNode = proc.parse_xml(xml_file_name=i)
                    pm_xsl.transform_to_file(
                        xdm_node=xml, output_file=i.replace(Path(i).suffix, save.ending)
                    )
                return None

            results: list[str] = [
                pm_xsl.transform_to_string(xdm_node=proc.parse_xml(xml_file_name=i))
                for i in source
            ]

        return results
