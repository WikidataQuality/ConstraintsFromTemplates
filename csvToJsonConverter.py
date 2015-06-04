import csv
import json

class csvToJsonConverter:

	PROPERTY_INDEX = 1
	CONSTRAINT_INDEX = 2
	JSON_BLOB_INDEX = 3


	def write_dump_list_to_file(self, dump_list, jsonPath):
		with open(jsonPath, 'w') as f:
				complete_dump = json.dump(dump_list, f)


	def create_dump_list(self, csvPath):
		with open(csvPath, 'r') as csv_file:
			csv_reader = csv.reader(csv_file)
			dump_list = []
			for line in csv_reader:
				csv_json_blob = json.loads(line[self.JSON_BLOB_INDEX])
				dump_element = {
					'Property': line[self.PROPERTY_INDEX], 
					'Constraint': line[self.CONSTRAINT_INDEX],
					'Constraint_Parameters': csv_json_blob
					}
				dump_list.append(dump_element)
		return dump_list


	def run(self, csvPath, jsonPath):
		dump_list = self.create_dump_list(csvPath)
		self.write_dump_list_to_file(dump_list, jsonPath)

			
def main():
	converter = csvToJsonConverter()
	converter.run("constraints.csv", "dump.json")

if __name__ == "__main__": main()