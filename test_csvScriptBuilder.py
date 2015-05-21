# -*- coding: utf-8 -*-

import pytest
from mock import Mock
import os.path
import csv

from csvScriptBuilder import csvScriptBuilder
import uuid


class TestCsvScriptBuilder():

    def setup_method(self, method):
        #  setup_method is invoked befor every test method of a class
        self.builder = csvScriptBuilder()
        self.csv_file = open("testData/test_constraints.csv", "wb")
        self.builder.csv_writer = csv.writer(self.csv_file)

    def teardown_method(self, method):
        #  teardown_method is invoked after every test method of a class
        self.csv_file.close()

    def test_find_next_seperator_pipe_before_next_equal(self):
        test_constraint_parameters = "classes=Q1048835,Q56061|relation=instance"
        test_equal_sign = 7
        expected_result = 24
        result = self.builder.find_next_seperator(test_constraint_parameters, test_equal_sign)
        assert result == expected_result

    def test_find_next_seperator_none(self):
        test_constraint_parameters = "relation=instance"
        test_equal_sign = 8
        expected_result = 18
        result = self.builder.find_next_seperator(test_constraint_parameters, test_equal_sign)
        assert result == expected_result

    def test_find_next_seperator_no_pipe(self):
        test_constraint_parameters = "classes=Q5,Q95074 relation=instance"
        test_equal_sign = 7
        expected_result = 35
        result = self.builder.find_next_seperator(test_constraint_parameters, test_equal_sign)
        assert result == expected_result

    def test_find_next_seperator_multiple_pipes(self):
        test_constraint_parameters = "items={{Q|6581072}}, {{Q|43445}}|mandatory=true"
        test_equal_sign = 5
        expected_result = 33
        result = self.builder.find_next_seperator(test_constraint_parameters, test_equal_sign)
        assert result == expected_result

    def test_find_next_seperator_empty_parameters(self):
        test_constraint_parameters = ""
        test_equal_sign = 0
        expected_result = 1
        result = self.builder.find_next_seperator(test_constraint_parameters, test_equal_sign)
        assert result == expected_result

    def test_to_comma_seperated_string_standard(self):
        test_string = "{{Q|6581072}}, {{Q|43445}}, {{Q|1052281}}"
        expected_result = "Q6581072,Q43445,Q1052281"
        result = self.builder.to_comma_seperated_string(test_string)
        assert result == expected_result


    def test_to_comma_seperated_string_another_standard(self):
        test_string = "{{Q|1035954}}, {{Q|6636}}, {{Q|43200}}, {{Q|592}}, {{Q|6649}}, {{Q|339014}}"
        expected_result = "Q1035954,Q6636,Q43200,Q592,Q6649,Q339014"
        result = self.builder.to_comma_seperated_string(test_string)
        assert result == expected_result


    def test_to_comma_seperated_string_third_standard(self):
        test_string = "novalue, somevalue, [[Q889]], [[Q222]], [[Q262]], [[Q228]], [[Q916]], [[Q781]]"
        expected_result = "novalue,somevalue,Q889,Q222,Q262,Q228,Q916,Q781"
        result = self.builder.to_comma_seperated_string(test_string)
        assert result == expected_result


    def test_to_comma_seperated_string_empty(self):
        test_string = ""
        expected_result = ""
        result = self.builder.to_comma_seperated_string(test_string)
        assert result == expected_result       


    def test_to_comma_seperated_string_unicode(self):
        test_string = "¡“¶¢[]|{}≠¿'≤¥ç √~∫µ…–∞≈å  æœ∂‚ƒ@© πª•ºπ«∑€ ®†Ω¨⁄øπ•   ±‘æœ@∆‚å≈~–"
        expected_result = "¡“¶¢≠¿'≤¥ç√~∫µ…–∞≈åæœ∂‚ƒ@©πª•ºπ«∑€®†Ω¨⁄øπ•±‘æœ@∆‚å≈~–"
        result = self.builder.to_comma_seperated_string(test_string)
        assert result == expected_result


    def test_add_property_standard(self):
        test_value = "P1337"
        expected_result = "P1337"
        self.builder.add_property(test_value)
        assert self.builder.parameters['property'] == expected_result


    def test_add_property_whitepace(self):
        test_value = " P7331 "
        expected_result = "P7331"
        self.builder.add_property(test_value)
        assert self.builder.parameters['property'] == expected_result


    def test_add_property_empty(self):
        test_value = ""
        expected_result = ""
        self.builder.add_property(test_value)
        assert self.builder.parameters['property'] == expected_result


    def test_add_property_multiple(self):
        expected_result = ""
        with pytest.raises(KeyError):
            parameter_property = self.builder.parameters['property']

        test_value = "P2992"
        expected_result = "P2992"
        self.builder.add_property(test_value)
        assert self.builder.parameters['property'] == expected_result

        test_value = "P1234567890"
        expected_result = "P1234567890"
        self.builder.add_property(test_value)
        assert self.builder.parameters['property'] == expected_result


    def test_add_classes_standard(self, monkeypatch):
        def mockreturn(path):
            return "Q5,Q95074"
        monkeypatch.setattr(self.builder, 'to_comma_seperated_string', mockreturn)
        test_value = "Q5,Q95074"
        expected_result = "Q5,Q95074"
        self.builder.add_classes(test_value)
        assert self.builder.parameters['class'] == expected_result


    def test_add_classes_empty(self, monkeypatch):
        def mockreturn(path):
            return ""
        monkeypatch.setattr(self.builder, 'to_comma_seperated_string', mockreturn)
        test_value = ""
        expected_result = ""
        self.builder.add_classes(test_value)
        assert self.builder.parameters['class'] == expected_result


    def test_add_classes_multiple(self, monkeypatch):
        def first(path):
            return "first"
        def second(path):
            return "second"
        monkeypatch.setattr(self.builder, 'to_comma_seperated_string', first)
        test_value = "first"
        expected_result = "first"
        self.builder.add_classes(test_value)
        assert self.builder.parameters['class'] == expected_result

        monkeypatch.setattr(self.builder, 'to_comma_seperated_string', second)
        test_value = "second"
        expected_result = "second"
        self.builder.add_classes(test_value)
        assert self.builder.parameters['class'] == expected_result


    def test_add_exceptions_semicolon(self, monkeypatch):
        def mockreturn(path):
            return "Q18646002;Q18646076"
        monkeypatch.setattr(self.builder, 'to_comma_seperated_string', mockreturn)
        test_value = " {{Q|18646002}}; {{Q|18646076}} "
        expected_result = "Q18646002,Q18646076"
        self.builder.add_exceptions(test_value)
        assert self.builder.parameters['known_exception'] == expected_result


    def test_add_exceptions_comma(self, monkeypatch):
        def mockreturn(path):
            return "Q41054,Q83160,Q79015"
        monkeypatch.setattr(self.builder, 'to_comma_seperated_string', mockreturn)
        test_value = "{{Q|41054}}, {{Q|83160}}, {{Q|79015}}"
        expected_result = "Q41054,Q83160,Q79015"
        self.builder.add_exceptions(test_value)
        assert self.builder.parameters['known_exception'] == expected_result


    def test_add_exceptions_no_mock(self):
        test_value = "{{Q|28860}}, {{Q|49957}}, {{Q|50032}}, {{Q|271818}}, {{Q|3497268}}, {{Q|1543006}} "
        expected_result = "Q28860,Q49957,Q50032,Q271818,Q3497268,Q1543006"
        self.builder.add_exceptions(test_value)
        assert self.builder.parameters['known_exception'] == expected_result


    def test_add_goup_by_standard(self):
        test_value = "P17"
        expected_result = "P17"
        self.builder.add_group_by(test_value)
        assert self.builder.parameters['group_by'] == expected_result


    def test_add_goup_by_whitespace(self):
        test_value = "  P31   "
        expected_result = "P31"
        self.builder.add_group_by(test_value)
        assert self.builder.parameters['group_by'] == expected_result


    def test_add_goup_by_empty(self):
        test_value = ""
        expected_result = ""
        self.builder.add_group_by(test_value)
        assert self.builder.parameters['group_by'] == expected_result


    def test_add_items_standard(self, monkeypatch):
        def mockreturn(path):
            return "Q1035954,Q6636,Q43200,Q592,Q6649,Q339014"
        monkeypatch.setattr(self.builder, 'to_comma_seperated_string', mockreturn)
        test_value = "{{Q|1035954}}, {{Q|6636}}, {{Q|43200}}, {{Q|592}}, {{Q|6649}}, {{Q|339014}}"
        expected_parameters_item = "Q1035954,Q6636,Q43200,Q592,Q6649,Q339014"
        self.builder.add_items(test_value)
        assert self.builder.parameters['item'] == expected_parameters_item
        with pytest.raises(KeyError):
            snak = self.builder.parameters['snak']


    def test_add_items_with_snak(self, monkeypatch):
        def mockreturn(path):
            return "novalue,somevalue,Q889,Q222,Q262,Q228,Q916,Q781"
        monkeypatch.setattr(self.builder, 'to_comma_seperated_string', mockreturn)
        test_value = "novalue, somevalue, [[Q889]], [[Q222]], [[Q262]], [[Q228]], [[Q916]], [[Q781]]"
        expected_parameters_item = "Q889,Q222,Q262,Q228,Q916,Q781"
        expected_parameters_snak = "novalue,somevalue"
        self.builder.add_items(test_value)
        assert self.builder.parameters['item'] == expected_parameters_item
        assert self.builder.parameters['snak'] == expected_parameters_snak


    def test_add_items_empty(self, monkeypatch):
        def mockreturn(path):
            return ""
        monkeypatch.setattr(self.builder, 'to_comma_seperated_string', mockreturn)
        test_value = ""
        self.builder.add_items(test_value)
        with pytest.raises(KeyError):
            item = self.builder.parameters['item']
        with pytest.raises(KeyError):
            snak = self.builder.parameters['snak']


    def test_add_items_with_snak_no_mock(self):
        test_value = "somevalue, [[Q121]], [[Q212]], [[Q44998]], [[Q19765]]"
        expected_parameters_item = "Q121,Q212,Q44998,Q19765"
        expected_parameters_snak = "somevalue"
        self.builder.add_items(test_value)
        assert self.builder.parameters['item'] == expected_parameters_item
        assert self.builder.parameters['snak'] == expected_parameters_snak


    def test_add_list_qualifiers(self, monkeypatch):
        def mockreturn(path):
            return "P580,P582,P805"
        monkeypatch.setattr(self.builder, 'to_comma_seperated_string', mockreturn)
        test_value = "{{P|580}}, {{P|582}}, {{P|805}}"
        expected_parameter_property = "P580,P582,P805"
        self.builder.constraint_name = "Qualifiers"
        self.builder.add_list(test_value)
        assert self.builder.parameters['property'] == expected_parameter_property
        with pytest.raises(AttributeError):
            list_parameter = self.builder.list_parameter


    def test_add_list_conflicts_with(self, monkeypatch):
        def mockreturn(path):
            return "P31:Q4167410,Q101352,Q12308941,Q11879590,Q3409032,Q202444,Q577"
        monkeypatch.setattr(self.builder, 'to_comma_seperated_string', mockreturn)
        test_value = "{{P|31}}: {{Q|4167410}}, {{Q|101352}}, {{Q|12308941}}, {{Q|11879590}}, {{Q|3409032}}, {{Q|202444}}, {{Q|577}}"
        expected_list_parameter = "P31:Q4167410,Q101352,Q12308941,Q11879590,Q3409032,Q202444,Q577"
        self.builder.constraint_name = "Conflicts with"
        self.builder.add_list(test_value)
        with pytest.raises(KeyError):
            parameter_property = self.builder.parameters['property']
        assert self.builder.list_parameter == expected_list_parameter


    def test_set_constraint_name_true(self):
        test_value = 'true'
        expected_result = 'Mandatory qualifiers'
        self.builder.set_constraint_name(test_value)
        assert self.builder.constraint_name == expected_result


    def test_set_constraint_name_not_true(self):
        test_value = 'asdfdsa'
        expected_result = ''
        self.builder.set_constraint_name(test_value)
        assert self.builder.constraint_name == expected_result


    def test_set_constraint_name_true_typo(self):
        test_value = 'ture'
        expected_result = ''
        self.builder.set_constraint_name(test_value)
        assert self.builder.constraint_name == expected_result


    def test_add_status(self):
        test_value = 'over 9000'
        expected_result = 'mandatory'
        self.builder.add_status(test_value)
        assert self.builder.parameters['constraint_status'] == expected_result


    def test_add_status_another(self):
        test_value = 'foo'
        expected_result = 'mandatory'
        self.builder.add_status(test_value)
        assert self.builder.parameters['constraint_status'] == expected_result


    def test_add_max_year(self):
        test_value = '1753'
        expected_result = '1753'
        self.builder.add_max(test_value)
        assert self.builder.parameters['maximum_quantity'] == expected_result


    def test_add_max_now(self):
        test_value = 'now'
        expected_result = 'now'
        self.builder.add_max(test_value)
        assert self.builder.parameters['maximum_quantity'] == expected_result


    def test_add_max_empty(self):
        test_value = ''
        expected_result = ''
        self.builder.add_max(test_value)
        assert self.builder.parameters['maximum_quantity'] == expected_result


    def test_add_max_whitespace(self):
        test_value = '  1 '
        expected_result = '1'
        self.builder.add_max(test_value)
        assert self.builder.parameters['maximum_quantity'] == expected_result


    def test_add_min_date(self):
        test_value = '1957-10-04'
        expected_result = '1957-10-04'
        self.builder.add_min(test_value)
        assert self.builder.parameters['minimum_quantity'] == expected_result


    def test_add_min_negative(self):
        test_value = '-10'
        expected_result = '-10'
        self.builder.add_min(test_value)
        assert self.builder.parameters['minimum_quantity'] == expected_result


    def test_add_min_zero_decimal(self):
        test_value = '0.00'
        expected_result = '0.00'
        self.builder.add_min(test_value)
        assert self.builder.parameters['minimum_quantity'] == expected_result


    def test_add_min_empty(self):
        test_value = ''
        expected_result = ''
        self.builder.add_min(test_value)
        assert self.builder.parameters['minimum_quantity'] == expected_result


    def test_add_min_whitespace(self):
        test_value = '  5 '
        expected_result = '5'
        self.builder.add_min(test_value)
        assert self.builder.parameters['minimum_quantity'] == expected_result


    def test_add_namespace_standard(self):
        test_value = 'File'
        expected_result = 'File'
        self.builder.add_namespace(test_value)
        assert self.builder.parameters['namespace'] == expected_result


    def test_add_namespace_empty(self):
        test_value = ''
        expected_result = ''
        self.builder.add_namespace(test_value)
        assert self.builder.parameters['namespace'] == expected_result


    def test_add_namespace_whitespace(self):
        test_value = ' namespaceValue '
        expected_result = 'namespaceValue'
        self.builder.add_namespace(test_value)
        assert self.builder.parameters['namespace'] == expected_result


    def test_add_pattern_img_formats(self):
        test_value = '&lt;nowiki>(?i).+\.(svg|png|jpg|jpeg|gif)|&lt;/nowiki>'
        expected_result = r'&lt;nowiki>(?i).+\.(svg|png|jpg|jpeg|gif)|&lt;/nowiki>'
        self.builder.add_pattern(test_value)
        assert self.builder.parameters['pattern'] == expected_result


    def test_add_pattern_many_d(self):
        test_value = '\d\d\d\d \d\d\d\d \d\d\d\d \d\d\d[\dX]'
        expected_result = r'\d\d\d\d \d\d\d\d \d\d\d\d \d\d\d[\dX]'
        self.builder.add_pattern(test_value)
        assert self.builder.parameters['pattern'] == expected_result


    def test_add_pattern_empty(self):
        test_value = ''
        expected_result = ''
        self.builder.add_pattern(test_value)
        assert self.builder.parameters['pattern'] == expected_result


    def test_add_pattern_whitespace(self):
        test_value = ' patternValue '
        expected_result = 'patternValue'
        self.builder.add_pattern(test_value)
        assert self.builder.parameters['pattern'] == expected_result


    def test_add_relation_standard(self):
        test_value = 'instance'
        expected_result = 'instance'
        self.builder.add_relation(test_value)
        assert self.builder.parameters['relation'] == expected_result


    def test_add_relation_empty(self):
        test_value = ''
        expected_result = ''
        self.builder.add_relation(test_value)
        assert self.builder.parameters['relation'] == expected_result


    def test_add_relation_whitespace(self):
        test_value = ' relationValue '
        expected_result = 'relationValue'
        self.builder.add_relation(test_value)
        assert self.builder.parameters['relation'] == expected_result


    def test_write_one_line(self):
        self.builder.write_element_into_csv = Mock()
        self.builder.reset_parameter = Mock()
        self.builder.write_one_line(1235, "fo shizzle")
        self.builder.write_element_into_csv.assert_called_once_with(1235, "fo shizzle")
        self.builder.reset_parameter.assert_called_once_with()


    def test_write_one_line_other_values(self):
        self.builder.write_element_into_csv = Mock()
        self.builder.reset_parameter = Mock()
        self.builder.write_one_line(5910, "trololo")
        self.builder.write_element_into_csv.assert_called_once_with(5910, "trololo")
        self.builder.reset_parameter.assert_called_once_with()


    def test_write_multiple_lines_indivisible(self):
        self.builder.list_parameter = "P31:Q11879590,Q202444,Q12308941"
        self.builder.split_list_parameter = Mock()
        self.builder.write_element_into_csv = Mock()
        self.builder.reset_parameter = Mock()
        self.builder.write_multiple_lines(190523, "best contraintname ever")
        self.builder.split_list_parameter.assert_called_once_with("P31:Q11879590,Q202444,Q12308941")
        self.builder.write_element_into_csv.assert_called_once_with(190523, "best contraintname ever")
        self.builder.reset_parameter.assert_called_once_with()


    def test_write_multiple_lines_divisible(self):
        self.builder.list_parameter = "P625;P17;P131"
        self.builder.split_list_parameter = Mock()
        self.builder.write_element_into_csv = Mock()
        self.builder.reset_parameter = Mock()
        self.builder.write_multiple_lines(10000, "another constraint")
        assert self.builder.split_list_parameter.call_count == 3
        assert self.builder.write_element_into_csv.call_count == 3
        self.builder.reset_parameter.assert_called_once_with()


    def test_write_into_csv_file_null(self):
        self.builder.write_multiple_lines = Mock()
        self.builder.write_one_line = Mock()
        self.builder.list_parameter = 'NULL'
        test_property_number = 1234
        test_constraint_name = 'Constraint Name'
        self.builder.write_into_csv_file(test_property_number, test_constraint_name)
        assert self.builder.write_multiple_lines.call_count == 0
        self.builder.write_one_line.assert_called_once_with(1234, 'Constraint Name')


    def test_write_into_csv_file_not_null(self):
        self.builder.write_multiple_lines = Mock()
        self.builder.write_one_line = Mock()
        self.builder.list_parameter = 'not Null'
        test_property_number = 4321
        test_constraint_name = 'Another Constraint Name'
        self.builder.write_into_csv_file(test_property_number, test_constraint_name)
        self.builder.write_multiple_lines.assert_called_once_with(4321, 'Another Constraint Name')
        assert self.builder.write_one_line.call_count == 0


    def test_split_list_parameter_splitable(self):
        test_line = "asdf:xyz"
        assert self.builder.parameters == {}
        self.builder.split_list_parameter(test_line)
        assert self.builder.parameters['property'] == "asdf"
        assert self.builder.parameters['item'] == "xyz"


    def test_split_list_parameter_no_item(self):
        test_line = "top kek"
        assert self.builder.parameters == {}
        self.builder.split_list_parameter(test_line)
        assert self.builder.parameters['property'] == "top kek"
        with pytest.raises(KeyError):
            item = self.builder.parameters['item']


    def test_split_list_parameter_empty(self):
        test_line = ""
        assert self.builder.parameters == {}
        self.builder.split_list_parameter(test_line)
        assert self.builder.parameters['property'] == ""
        with pytest.raises(KeyError):
            item = self.builder.parameters['item']


    def test_progress_print_standard(self, capsys):
        self.builder.progress_print(0, 2000)
        out, err = capsys.readouterr()
        expectedOut = '0/2000\n'
        assert out == expectedOut

        self.builder.progress_print(1, 2000)
        self.builder.progress_print(2, 2000)
        self.builder.progress_print(3, 2000)
        self.builder.progress_print(4, 2000)
        self.builder.progress_print(5, 2000)
        self.builder.progress_print(6, 2000)
        self.builder.progress_print(7, 2000)
        self.builder.progress_print(8, 2000)
        self.builder.progress_print(9, 2000)
        out, err = capsys.readouterr()
        expectedOut = ''
        assert out == expectedOut

        self.builder.progress_print(10, 2000)
        out, err = capsys.readouterr()
        expectedOut = '10/2000\n'
        assert out == expectedOut

        self.builder.progress_print(11, 2000)
        self.builder.progress_print(12, 2000)
        self.builder.progress_print(13, 2000)
        self.builder.progress_print(14, 2000)
        self.builder.progress_print(15, 2000)
        self.builder.progress_print(16, 2000)
        self.builder.progress_print(17, 2000)
        self.builder.progress_print(18, 2000)
        self.builder.progress_print(19, 2000)
        out, err = capsys.readouterr()
        expectedOut = ''
        assert out == expectedOut

        self.builder.progress_print(20, 2000)
        out, err = capsys.readouterr()
        expectedOut = '20/2000\n'
        assert out == expectedOut


    def test_progress_print_negative(self, capsys):
        self.builder.progress_print(-1, 1234)
        out, err = capsys.readouterr()
        expectedOut = ''
        assert out == expectedOut

        self.builder.progress_print(-10, 1234)
        out, err = capsys.readouterr()
        expectedOut = '-10/1234\n'
        assert out == expectedOut


    def test_property_exists_false(self):
        test_html = '<!DOCTYPE html><html lang="en" dir="ltr" class="client-nojs"><head><meta charset="UTF-8" /><title>Creating Property talk:P2 - Wikidata</title><meta name="generator" content="MediaWiki 1.26wmf1" /><meta name="robots" content="noindex,nofollow" /><link rel="alternate" type="application/x-wiki" title="Edit" href="/w/index.php?title=Property_talk:P2&amp;action=edit" /><link rel="edit" title="Edit" href="/w/index.php?title=Property_talk:P2&amp;action=edit" /></head><body><p>Dis is ma fancy html page</p></body></html>'
        expected_result = False
        result = self.builder.property_exists(test_html)
        assert result == expected_result


    def test_property_exists_true(self):
        test_html = '<!DOCTYPE html><html lang="en" dir="ltr" class="client-nojs"><head><meta charset="UTF-8" /><title>Editing Property talk:P9 - Wikidata</title><meta name="generator" content="MediaWiki 1.26wmf1" /><meta name="robots" content="noindex,nofollow" /><link rel="alternate" type="application/x-wiki" title="Edit" href="/w/index.php?title=Property_talk:P9&amp;action=edit" /><link rel="edit" title="Edit" href="/w/index.php?title=Property_talk:P9&amp;action=edit" /></head><body>Much content<br>such website<br>wow</body></html>'
        expected_result = True
        result = self.builder.property_exists(test_html)
        assert result == expected_result


    def test_property_exists_empty(self):
        test_html = ''
        expected_result = False
        result = self.builder.property_exists(test_html)
        assert result == expected_result


    def test_get_constraint_end_index_standard(self):
        test_constraintPart = 'Type|classes=Q1048835,Q56061|relation=instance}}\n{{Constraint:Value type|classes=Q5,Q95074|relation=instance|mandatory=true}}\n{{Constraint:Target required claim|property=P21}}\n{{Constraint:Target required claim|property=P39}}\n{{Constraint:Qualifiers|list={{P|580}}, {{P|582}} }}\n\n{{ExternalUse|\n* [[:cs:Šablona:Infobox - kraj]]\n* [[:la:Formula:Capsa civitatis Vicidata]]\n* [[:ru:Шаблон:НП]]\n* [[:ru:Шаблон:НП+]]\n* [[:ru:Шаблон:Данные о субъекте Российской Федерации]]\n* [[:ru:Шаблон:Регион Киргизии]]\n* [[:ru:Шаблон:НП/temp]]\n* [[:ru:Шаблон:Административная единица]], [[:ru:Шаблон:Субъект РФ]]\n* [[:ru:Шаблон:Аильный округ Киргизии]]\n}}\n\n'
        expected_result = 46
        result = self.builder.get_constraint_end_index(test_constraintPart)
        assert result == expected_result


    def test_get_constraint_end_index_second_standard(self):
        test_constraintPart = 'Target required claim|property=P21|items={{Q|6581072}}, {{Q|43445}}, {{Q|1052281}}|mandatory=true}}\n{{Constraint:Type|classes=Q5,Q95074|relation=instance}}\n{{Constraint:Item|property=P21|mandatory=true}}\n{{Constraint:Item|property=P19}}\n{{Constraint:Item|property=P569}}\n{{Constraint:Qualifiers|list={{P|1039}}|mandatory=true}}\n\n{{Person properties}}\n[[Category: Reciprocal properties]]\n\n'
        expected_result = 97
        result = self.builder.get_constraint_end_index(test_constraintPart)
        assert result == expected_result


    def test_get_constraint_end_index_empty(self):
        test_constraintPart = ''
        expected_result = None
        result = self.builder.get_constraint_end_index(test_constraintPart)
        assert result == expected_result


    def test_get_constraint_end_index_many_brackets(self):
        test_constraintPart = '{{{}{{}{}}{}{}}}{}{{{{{}{{{}}{{}}}}}}}}}{}{{{}}{{}{}}}{{}}'
        expected_result = 38
        result = self.builder.get_constraint_end_index(test_constraintPart)
        assert result == expected_result


    def test_split_constraint_block_standard(self):
        test_constraint_part = '{{Constraint:Type|classes=Q1048835,Q56061|relation=instance}}\n{{Constraint:Value type|classes=Q5,Q95074|relation=instance|mandatory=true}}\n{{Constraint:Target required claim|property=P21}}\n{{Constraint:Target required claim|property=P39}}\n{{Constraint:Qualifiers|list={{P|580}}, {{P|582}} }}\n\n{{ExternalUse|\n* [[:cs:Šablona:Infobox - kraj]]\n* [[:la:Formula:Capsa civitatis Vicidata]]\n* [[:ru:Шаблон:НП]]\n* [[:ru:Шаблон:НП+]]\n* [[:ru:Шаблон:Данные о субъекте Российской Федерации]]\n* [[:ru:Шаблон:Регион Киргизии]]\n* [[:ru:Шаблон:НП/temp]]\n* [[:ru:Шаблон:Административная единица]], [[:ru:Шаблон:Субъект РФ]]\n* [[:ru:Шаблон:Аильный округ Киргизии]]\n}}'
        expected_result_string = "Type|classes=Q1048835,Q56061|relation=instance"
        expected_result_remaining = "}}\n{{Constraint:Value type|classes=Q5,Q95074|relation=instance|mandatory=true}}\n{{Constraint:Target required claim|property=P21}}\n{{Constraint:Target required claim|property=P39}}\n{{Constraint:Qualifiers|list={{P|580}}, {{P|582}} }}\n\n{{ExternalUse|\n* [[:cs:Šablona:Infobox - kraj]]\n* [[:la:Formula:Capsa civitatis Vicidata]]\n* [[:ru:Шаблон:НП]]\n* [[:ru:Шаблон:НП+]]\n* [[:ru:Шаблон:Данные о субъекте Российской Федерации]]\n* [[:ru:Шаблон:Регион Киргизии]]\n* [[:ru:Шаблон:НП/temp]]\n* [[:ru:Шаблон:Административная единица]], [[:ru:Шаблон:Субъект РФ]]\n* [[:ru:Шаблон:Аильный округ Киргизии]]\n}}"
        result_string, result_remaining = self.builder.split_constraint_block(test_constraint_part)
        assert result_string == expected_result_string
        assert result_remaining == expected_result_remaining


    def test_split_constraint_block_another_standard(self):
        test_constraint_part = '}}\n{{Constraint:Item|property=P19}}\n{{Constraint:Item|property=P569}}\n{{Constraint:Qualifiers|list={{P|1039}}|mandatory=true}}\n\n{{Person properties}}\n[[Category: Reciprocal properties]]\n\n\n'
        expected_result_string = 'Item|property=P19'
        expected_result_remaining = '}}\n{{Constraint:Item|property=P569}}\n{{Constraint:Qualifiers|list={{P|1039}}|mandatory=true}}\n\n{{Person properties}}\n[[Category: Reciprocal properties]]\n\n\n'
        result_string, result_remaining = self.builder.split_constraint_block(test_constraint_part)
        assert result_string == expected_result_string
        assert result_remaining == expected_result_remaining


    def test_split_constraint_block_empty_result_standard(self):
        test_constraint_part = '}}\n\n{{Person properties}}\n[[Category: Reciprocal properties]]\n\n'
        expected_result_string = ''
        expected_result_remaining = ''
        result_string, result_remaining = self.builder.split_constraint_block(test_constraint_part)
        assert result_string == expected_result_string
        assert result_remaining == expected_result_remaining


    def test_split_constraint_block_valid_with_authority_string(self):
        test_constraint_part = '}}\n{{Constraint:Qualifiers|list=}}\n\n{{ExternalUse|\n* [[:cs:Šablona:Autoritní kontrola]]\n* [[:oc:Modèl:Infobox identificacions autoritats]]\n* [[:fr:Module:Autorité]]\n* [[:wikisource:fr:Modèle:Autorité]]\n* [[:cs:Šablona:Autoritní data]]\n}}\n\n{{Authority control properties}}\n\n__TOC__\n\n'
        expected_result_string = 'Qualifiers|list='
        expected_result_remaining = '}}\n\n{{ExternalUse|\n* [[:cs:Šablona:Autoritní kontrola]]\n* [[:oc:Modèl:Infobox identificacions autoritats]]\n* [[:fr:Module:Autorité]]\n* [[:wikisource:fr:Modèle:Autorité]]\n* [[:cs:Šablona:Autoritní data]]\n}}\n\n{{Authority control properties}}\n\n__TOC__\n\n'
        result_string, result_remaining = self.builder.split_constraint_block(test_constraint_part)
        assert result_string == expected_result_string
        assert result_remaining == expected_result_remaining


    def test_run_complete(self, capsys):
        csv_path = "testData/test.csv"
        self.builder.CSV_FILE_NAME = csv_path
        self.builder.MAX_PROPERTY_NUMBER = 3
        try:
            os.remove(csv_path)
        except OSError:
            pass
        with open("testData/first_test_property_talk_page.html", 'r') as first:
            first_test_property_talk_page = first.read()
        with open("testData/second_test_property_talk_page.html", 'r') as second:
            second_test_property_talk_page = second.read()
        with open("testData/third_test_property_talk_page.html", 'r') as third:
            third_test_property_talk_page = third.read()
        self.builder.get_property_talk_page = Mock(side_effect=[first_test_property_talk_page, second_test_property_talk_page, third_test_property_talk_page])
        assert os.path.isfile(csv_path) == False
        self.builder.run()
        assert os.path.isfile(csv_path) == True
        with open("testData/test.csv", 'r') as result:
            with open("testData/expectedResult.csv", 'r') as expected_result:
                for result_line in result.readlines():
                    expected_line = expected_result.readline()
                    assert result_line[result_line.find(","):] == expected_line[expected_line.find(","):]
                assert '' == expected_result.readline()


