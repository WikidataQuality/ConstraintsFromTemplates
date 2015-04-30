# -*- coding: utf-8 -*-

import pytest

from sqlScriptBuilder import sqlScriptBuilder


class TestSqlScriptBuilder():

    def setup_method(self, method):
        #  setup_method is invoked for every test method of a class
        self.builder = sqlScriptBuilder()

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


