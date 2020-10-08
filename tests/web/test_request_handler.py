from pathlib import Path
from unittest.mock import Mock

import pytest

from api_iso_antares.web import RequestHandler
from api_iso_antares.web.request_handler import StudyNotFoundError


@pytest.mark.unit_test
def test_get(tmp_path: str) -> None:
    # Create folders
    tmp = Path(tmp_path)
    (tmp / "study1").mkdir()
    (tmp / "myfile").touch()
    path_study2 = tmp / "study2.py"
    path_study2.mkdir()
    (path_study2 / "settings").mkdir()

    data = {"toto": 42}
    expected_data = {"titi": 43}
    path_to_studies = tmp
    sub_route = "settings/blabla"

    study_reader_mock = Mock()
    study_reader_mock.read.return_value = data

    url_engine_mock = Mock()
    url_engine_mock.apply.return_value = expected_data

    request_handler = RequestHandler(
        study_reader=study_reader_mock,
        url_engine=url_engine_mock,
        path_to_studies=path_to_studies,
    )

    output = request_handler.get(route=f"study2.py/{sub_route}")

    assert output == expected_data

    study_reader_mock.read.assert_called_once_with(path_to_studies / "study2.py")
    study_reader_mock.validate.assert_called_once_with(data)
    url_engine_mock.apply.assert_called_once_with(sub_route, data)


@pytest.mark.unit_test
def test_assert_study_exist(tmp_path: str) -> None:
    # Create folders
    tmp = Path(tmp_path)
    (tmp / "study1").mkdir()
    (tmp / "myfile").touch()
    path_study2 = tmp / "study2.py"
    path_study2.mkdir()
    (path_study2 / "settings").mkdir()

    # Input
    study_name = 'study2.py'
    path_to_studies = Path(tmp_path)

    # Test & Verify
    request_handler = RequestHandler(study_reader=Mock(), url_engine=Mock(), path_to_studies=path_to_studies)
    request_handler._assert_study_exist(study_name)


@pytest.mark.unit_test
def test_assert_study_not_exist(tmp_path: str) -> None:
    # Create folders
    tmp = Path(tmp_path)
    (tmp / "study1").mkdir()
    (tmp / "myfile").touch()
    path_study2 = tmp / "study2.py"
    path_study2.mkdir()
    (path_study2 / "settings").mkdir()

    # Input
    study_name = 'study3'
    path_to_studies = Path(tmp_path)

    # Test & Verify
    request_handler = RequestHandler(study_reader=Mock(), url_engine=Mock(), path_to_studies=path_to_studies)
    with pytest.raises(StudyNotFoundError):
        request_handler._assert_study_exist(study_name)
