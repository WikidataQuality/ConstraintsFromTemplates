# -*- coding: utf-8 -*-

from sqlScriptBuilder import sqlScriptBuilder

class TestSqlScriptBuilder():

    def setup_method(self, method):
        #  setup_method is invoked for every test method of a class
        self.builder = sqlScriptBuilder()


    def test_to_comma_seperated_string_standard(self):
        test_string = "{{Q|6581072}}, {{Q|43445}}, {{Q|1052281}}"
        expected_result = "Q6581072,Q43445,Q1052281"
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
        assert self.builder.parameters['property'] == expected_result

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


    def test_add_exceptions_standard(self, monkeypatch):
        def mockreturn(path):
            return "Q18646002;Q18646076"
        monkeypatch.setattr(self.builder, 'to_comma_seperated_string', mockreturn)
        test_value = " {{Q|18646002}}; {{Q|18646076}} "
        expected_result = "Q18646002,Q18646076"
        self.builder.add_exceptions(test_value)
        assert self.builder.parameters['known_exception'] == expected_result


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


