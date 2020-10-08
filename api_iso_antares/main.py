import sys
from pathlib import Path

from api_iso_antares.antares_io.reader import FolderReader, IniReader
from api_iso_antares.engine import UrlEngine
from api_iso_antares.web import RequestHandler
from api_iso_antares.web.server import create_server

if __name__ == "__main__":
    project_dir: Path = Path(__file__).resolve().parents[2]
    request_handler = RequestHandler(
        study_reader=FolderReader(reader_ini=IniReader(), jsonschema={}),
        url_engine=UrlEngine(jsonschema={}),
        path_to_studies=Path(sys.argv[2]),
    )
    application = create_server(request_handler)

    application.run(debug=False, host="0.0.0.0", port=8080)