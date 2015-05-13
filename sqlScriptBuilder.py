import requests
import codecs
import os
import json
import uuid
import re
import csv

class sqlScriptBuilder:

	MAX_PROPERTY_NUMBER = 20

	CSV_FILE_NAME = "constraints.csv"

	CONSTRAINT_BEGIN_STRING = "{{Constraint:"

	def __init__(self):
		self.parameters = {}
		self.constraint_name = ""

	def find_next_seperator(self, constraint_parameters, equal_sign):
		next_equal_sign = constraint_parameters.find('=', equal_sign + 1)
		if next_equal_sign == -1:
			next_seperator = len(constraint_parameters)
		else:
			next_seperator = constraint_parameters.rfind('|', equal_sign, next_equal_sign)
		if next_seperator == -1:
			next_seperator = len(constraint_parameters)
		else:
			next_seperator = next_seperator + 1
		return next_seperator

	def to_comma_seperated_string(self, values):
		return values.replace("{", "").replace("}", "").replace("|", "").replace(" ", "").replace("[", "").replace("]", "").strip()

	def add_property(self, values):
		self.parameters['property'] = values.strip()

	def add_classes(self, values):
		self.parameters['class'] = self.to_comma_seperated_string(values)

	def add_exceptions(self, values):
		self.parameters['known_exception'] = self.to_comma_seperated_string(values).replace(";", ",")

	def add_group_by(self, values):
		self.parameters['group_by'] = values.strip()

	def add_items(self, values):
		itemString = ""
		snakString = ""
		for element in self.to_comma_seperated_string(values).split(","):
			if element.startswith("Q"):
				itemString = itemString + element + ","
			elif element.lower() == "somevalue" or element.lower() == "novalue":
				snakString = snakString + element + ","
		if itemString != "":
			self.parameters['item'] = itemString.rstrip(",")
		if snakString != "":
			self.parameters['snak'] = snakString.rstrip(",")

	def add_list(self, values):
		if self.constraint_name == "Qualifiers" or self.constraint_name == "Mandatory qualifiers":
			self.parameters['property'] = self.to_comma_seperated_string(values)
		else:
			self.list_parameter = self.to_comma_seperated_string(values)

	def set_constraint_name(self, values):
		if values == 'true':
			self.constraint_name = 'Mandatory qualifiers'

	def add_status(self, values):
		self.parameters['constraint_status'] = 'mandatory'

	def add_max(self, values):
		self.parameters['maximum_quantity'] = values.strip()

	def add_min(self, values):
		self.parameters['minimum_quantity'] = values.strip()

	def add_namespace(self, values):
		self.parameters['namespace'] = values.strip()

	def add_pattern(self, values):
		self.parameters['pattern'] = values.strip()

	def add_relation(self, values):
		self.parameters['relation'] = values.strip()	

	def write_one_line(self, property_number, constraint_name):
		self.write_line_to_csv(property_number, constraint_name)
		self.reset_parameter()

	def write_multiple_lines(self, property_number, constraint_name):
		for line in self.list_parameter.split(';'):
			self.split_list_parameter(line)
			self.write_line_to_csv(property_number, constraint_name)
			self.parameters.pop('item', None)
		self.reset_parameter()

	def write_line_in_sql_file(self, property_number, constraint_name):
		if self.list_parameter != 'NULL':
			self.write_multiple_lines(property_number, constraint_name)
		else:
			self.write_one_line(property_number, constraint_name)

	def write_line_to_csv(self, property_number, constraint_name):
		json_blob_string = json.dumps(self.parameters).replace("&lt;nowiki>","").replace("&lt;/nowiki>","").replace("&amp;lt;nowiki&amp;lt;","").replace("&amp;lt;/nowiki&amp;gt;","").replace("<nowiki>","").replace("</nowiki>","")
		self.csv_writer.writerow((str(uuid.uuid4()), str(property_number),  constraint_name.strip(), json_blob_string))


	def split_list_parameter(self, line):
		if ':' in line:
			self.parameters['item'] = line[line.index(':')+1:]
			self.parameters['property'] = line[:line.index(':')]
		else:
			self.parameters['property'] = line

	def reset_parameter(self):
		self.parameters = {}
		self.list_parameter = 'NULL'


	def get_constraint_part(self, property_talk_page):
		start = property_talk_page.find("{{Constraint:")
		 	
		end = property_talk_page.find("==")
		if( end != -1):
			property_talk_page = property_talk_page[start:end]
		else:
			property_talk_page = property_talk_page[start:]

		#delete <!-- --> comments from site
		open_index = property_talk_page.find("&lt;!--")
		while (open_index) != -1:
			close_index = property_talk_page.find("-->", open_index)
			if(close_index == -1):
				break
				
			property_talk_page = property_talk_page[:open_index] + property_talk_page[close_index+3:]
			
			open_index = property_talk_page.find("&lt;!--")	
		return property_talk_page


	def progress_print(self, number, maxNumber):
		if number % 10 == 0:
			print(str(number) + "/" + str(maxNumber))


	def property_exists(self, propertyTalkPage):
		# return not (propertyTalkPage.find("Creating Property talk") != -1 or 
		# 	propertyTalkPage == "")
		regex = re.compile('<title>(.*)</title>')
		match = regex.search(propertyTalkPage)
		if match:
			print str(not "Creating Property talk" in match.group(0))
			return not "Creating Property talk" in match.group(0)
		else:
			print("False")
			return False


	def get_constraint_end_index(self, constraintPart):
		#match brackets to find end of constraint
		count = 2
		for i, c in enumerate(constraintPart):
			if c == '{':
				count += 1
			elif c == '}':
				count -= 1
			if count == 0:
				return (i - 1)


	def split_constraint_block(self, constraint_part):
		start_index = constraint_part.find(self.CONSTRAINT_BEGIN_STRING)
		if start_index != -1:
			start_index += len(self.CONSTRAINT_BEGIN_STRING)
			constraint_part = constraint_part[start_index:]

			end_index = self.get_constraint_end_index(constraint_part)
			constraint_string = constraint_part[:end_index]
			remaining_constraint = constraint_part[end_index:]

			return constraint_string, remaining_constraint
		else:
			return "", ""


	call_method = {
	    'base_property' : add_property,
	    'class' : add_classes,
	    'classes' : add_classes,
	    'exceptions' : add_exceptions,
	    'group by'  : add_group_by,
	    'group property' : add_group_by,
	    'item' : add_items,
	    'items' : add_items,
	    'list' : add_list,
	    'mandatory' : add_status,
	    'max' : add_max,
	    'min' : add_min,
	    'namespace' : add_namespace,
	    'pattern' : add_pattern,
	    'property' : add_property,
	    'relation' : add_relation,
	    'required' : set_constraint_name,
	    'value' : add_items,
	    'values' : add_items
	}


	def split_parameters(self, constraint_parameters):
		equal_sign_pos = constraint_parameters.find('=')
		next_seperator = self.find_next_seperator(constraint_parameters, equal_sign_pos)
		value_end_pos = max(-1, next_seperator - 1)

		parameter_name = constraint_parameters[:equal_sign_pos].strip()
		parameter_value = constraint_parameters[equal_sign_pos + 1 : value_end_pos]
		remaining_constraint_parameters = constraint_parameters[next_seperator:]

		return parameter_name, parameter_value, remaining_constraint_parameters


	def add_all_parameters(self, constraint_parameters):
		while constraint_parameters != None and constraint_parameters.find('=') != -1:
			p_name, p_value, constraint_parameters = self.split_parameters(constraint_parameters)	
			try:
				self.call_method[p_name](self, p_value)
			except KeyError, e:  # other Exceptions will be raised
				pass

	def process_constraint_part(self, constraint_part, property_number):
		constraint_string, remaining_constraint = self.split_constraint_block(constraint_part)
		while constraint_string != "":
			self.constraint_name = None
			self.list_parameter = 'NULL'

			delimiter_index = constraint_string.find('|')

			if delimiter_index == -1:
				self.constraint_name = constraint_string
			else:			
				self.constraint_name = constraint_string[:delimiter_index]
				constraint_parameters = constraint_string[delimiter_index+1:]
				self.add_all_parameters(constraint_parameters)
					
			self.write_line_in_sql_file(property_number, self.constraint_name)

			constraint_string, remaining_constraint = self.split_constraint_block(remaining_constraint)


	def get_property_talk_page(self, property_number):
		url = "http://www.wikidata.org/w/index.php?title=Property_talk:P" + \
			  str(property_number) + "&action=edit"
		property_talk_page = requests.get(url).text
		return property_talk_page


	def process_property_talk_page(self, property_number):
		property_talk_page = self.get_property_talk_page(property_number)
		if self.property_exists(property_talk_page):
			constraintPart = self.get_constraint_part(property_talk_page)
			self.process_constraint_part(constraintPart, property_number)


	# only purpose: Build SQL-Statement to fill table with constraints
	# fetches constraints from property talk pages
	# nonetheless: use table layout that will suit the new way of storing 
	# constraints as statements on properties

	def run(self):
		csv_file = open( self.CSV_FILE_NAME, "wb")
		self.csv_writer = csv.writer(csv_file)
		for property_number in range(1, self.MAX_PROPERTY_NUMBER+1):

			self.progress_print(property_number, self.MAX_PROPERTY_NUMBER)

			self.process_property_talk_page(property_number)

		csv_file.close()

def main():
	builder = sqlScriptBuilder()
	builder.run()

if __name__ == "__main__": main()