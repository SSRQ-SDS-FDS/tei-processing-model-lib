from pathlib import Path

XSL_PATH = Path(__file__).parent.absolute() / "core"
XSL_FILES = {
    "odd2pm": str(XSL_PATH / "compile.xsl"),
}
