# -*- coding: utf-8 -*-

import pytest
from mock import Mock
from mock import patch

import os

from csvToJsonConverter import csvToJsonConverter

class TestCsvToJsonConverter():

    # def teardown_method(self, method):
    #     #  teardown_method is invoked after every test method of a class
    #     self.csv_file.close()

    def setup_method(self, method):
        #  setup_method is invoked befor every test method of a class
        self.converter = csvToJsonConverter()

    def test_complete_run(self):
        result_path = "testData/test_result.json"
        try:
            os.remove(result_path)
        except OSError:
            pass
        assert os.path.isfile(result_path) == False
        self.converter.run("testData/test_for_jsonConverter.csv", result_path)
        assert os.path.isfile(result_path) == True
        with open("testData/expected_result.json", 'r') as expected_result_file:
            expected_result = expected_result_file.read()
        with open(result_path, 'r') as result_file:
            result = result_file.read()
        assert expected_result == result

    def test_run(self):
        self.converter.create_dump_list = Mock(return_value=[{"dumpListElement1"}, {"dumpListElement2"}])
        self.converter.write_dump_list_to_file = Mock()
        self.converter.run("csvPath", "jsonPath")
        self.converter.create_dump_list.assert_called_once_with("csvPath")
        self.converter.write_dump_list_to_file.assert_called_once_with([{"dumpListElement1"}, {"dumpListElement2"}], "jsonPath")