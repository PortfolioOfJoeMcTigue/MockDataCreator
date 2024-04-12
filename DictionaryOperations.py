
from csv import reader
import FileWriteOperations as writer
import FileReadOperations as read
import ListOperations as listOps

class DictionaryOperations():

    def delete_all_column_elements_matching_given_column_index_from_dictionary(self, file_dict, remove_column_index):
        print("     inside: delete_column_data_in_dict") 
        remove_column_index = int(remove_column_index)
        number_of_records = int(file_dict["config"][3]["config_records"])
        columns_per_record = int(file_dict["config"][4]["columns_per_record"])
        for record_index in range(0, (number_of_records - 1)):
            for column in range(0, (columns_per_record - 1)):
                if column == remove_column_index:
                    print(f"remove_column_index", remove_column_index)
                    del file_dict["config"][5]["records"][record_index]["record"][4]["columns"][remove_column_index]
        columns_per_record -= 1
        file_dict["config"][4]["columns_per_record"] = str(columns_per_record)
        print("     leaving: delete_column_data_in_dict")
        return file_dict
  
    def delete_a_record_from_dictionary(self, file_dict, remove_record_index):
        print("     inside: delete_a_record_from_dictionary")
        file_name = str(file_dict["config"][2]["file_name"])
        self.w = writer.FileWriteOperations()
        number_of_records = int(file_dict["config"][3]["config_records"])
        if number_of_records == 1:
            self.w.delete_unwanted_file(file_name, "user-config-path")
            return {}
        else:
            del file_dict["config"][5]["records"][remove_record_index]
            number_of_records -= 1
            file_dict["config"][3]["config_records"] = str(number_of_records)
        print("     leaving: delete_a_record_from_dictionary")
        return file_dict
  
    def update_a_column_value_of_a_record_in_dictionary(self, file_dict, record_index, column_index, element_index, key, value):
        print("     inside: update_a_column_value_of_a_record_in_dictionary")
        record_index = int(record_index)
        column_index = int(column_index)
        element_index = int(element_index)
        file_dict["config"][5]["records"][record_index]["record"][4]["columns"][column_index]["column"][element_index][key] = "\""+value+"\""
        print("     leaving: update_a_column_value_of_a_record_in_dictionary")
        return file_dict
  
    def update_a_file_statistic_in_dictionary(self, file_dict, config_index, config_key, config_value):
        print("     inside: update_a_file_statistic_in_dictionary, config_value:"+ config_value)
        config_index = int(config_index)
        file_dict["config"][config_index][config_key] = "\""+config_value+"\""
        print("     leaving: update_a_file_statistic_in_dictionary")
        return file_dict
  
    def retrieve_a_file_statistic_in_dictionary(self, file_dict, config_index, config_key):
        print("     inside: retrieve_a_file_statistic_in_dictionary")
        config_index = int(config_index)
        result = file_dict["config"][config_index][config_key]
        print("     leaving: retrieve_a_file_statistic_in_dictionary")
        return result
  
    def update_records_to_affect_in_dictionary(self, file_dict, record_index, value):
        print("     inside: update_records_to_affect_in_dictionary")
        record_index = int(record_index)
        file_dict["config"][5]["records"][record_index]["record"][0]["records_to_affect"] = "\""+value+"\""
        print("     leaving: update_records_to_affect_in_dictionary")
        return file_dict
        
  
    def retrieve_records_to_affect_from_dictionary(self, file_dict, record_index):
        print("     inside: retrieve_records_to_affect_from_dictionary")
        record_index = int(record_index)
        result = file_dict["config"][5]["records"][record_index]["record"][0]["records_to_affect"]
        print("     leaving: retrieve_records_to_affect_from_dictionary")
        return result
  
    def update_sql_table_in_dictionary(self, file_dict, record_index, value):
        print("     inside: update_sql_table_in_dictionary")
        record_index = int(record_index)
        file_dict["config"][5]["records"][record_index]["record"][1]["sql_table"] = "\""+value+"\""
        print("     leaving: update_sql_table_in_dictionary")
        return file_dict
  
    def retrieve_sql_table_from_dictionary(self, file_dict, record_index):
        print("     inside: retrieve_sql_table_from_dictionary")
        record_index = int(record_index)
        result = file_dict["config"][5]["records"][int(record_index)]["record"][1]["sql_table"]
        print("     leaving: retrieve_sql_table_from_dictionary")
        return result
  
    def update_sql_action_in_dictionary(self, file_dict, record_index, value):
        print("     inside: update_sql_action_in_dictionary")
        record_index = int(record_index)
        file_dict["config"][5]["records"][record_index]["record"][2]["sql_action"] = "\""+value+"\""
        print("     leaving: update_sql_action_in_dictionary")
        return file_dict
  
    def retrieve_sql_action_from_dictionary(self, file_dict, record_index):
        print("     inside: retrieve_sql_action_from_dictionary")
        record_index = int(record_index)
        result = file_dict["config"][5]["records"][record_index]["record"][2]["sql_action"]
        print("     leaving: retrieve_sql_action_from_dictionary")
        return result
  
    def update_sql_anchor_in_dictionary(self, file_dict, record_index, value):
        print("     inside: update_sql_anchor_in_dictionary")
        record_index = int(record_index)
        file_dict["config"][5]["records"][record_index]["record"][3]["sql_anchor"] = "\""+value+"\""
        print("     leaving: update_sql_anchor_in_dictionary")
        return file_dict
  
    def retrieve_sql_anchor_from_dictionary(self, file_dict, record_index):
        print("     inside: retrieve_sql_anchor_from_dictionary")
        record_index = int(record_index)
        result = file_dict["config"][5]["records"][record_index]["record"][3]["sql_anchor"]
        print("     leaving: retrieve_sql_anchor_from_dictionary")
        return result
    
    def update_all_sql_table_action_and_anchor_in_dictionary_to_default(self, file_dict):
        print("     inside: update_all_sql_table_action_and_anchor_in_dictionary_to_default")
        record_count = int(self.retrieve_a_file_statistic_in_dictionary(file_dict, 3, "config_records"))
        for record_number in range(0, record_count):
            file_dict = self.update_sql_table_in_dictionary(file_dict, record_number, "Enter SQL Table Name")
            file_dict = self.update_sql_action_in_dictionary(file_dict, record_number, "Select SQL Action")
            file_dict = self.update_sql_anchor_in_dictionary(file_dict, record_number, "Select SQL Anchor")
        print("     leaving: update_all_sql_table_action_and_anchor_in_dictionary_to_default")
        return file_dict
  
    def retrieve_a_column_value_of_a_record_in_dictionary(self, file_dict, record_index, column_index, element_index, key):
        print("     inside: retrieve_a_column_value_of_a_record_in_dictionary:")
        record_index = int(record_index)
        column_index = int(column_index)
        element_index = int(element_index)
        result = file_dict["config"][5]["records"][record_index]["record"][4]["columns"][column_index]["column"][element_index][key]
        print("     leaving: retrieve_a_column_value_of_a_record_in_dictionary:")
        return result
  
    def retrieve_all_column_titles_from_record(self, file_dict, record_number):
        print("     inside: retrieve_all_column_titles_from_record")
        titles = []
        columns_per_record = int(self.retrieve_a_file_statistic_in_dictionary(file_dict, 4, "columns_per_record"))
        for x in range(0, columns_per_record):
            titles.append(str(self.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_number, x, 0, "TITLE")))
        print("     leaving: retrieve_all_column_titles_from_record")
        return titles
  
    def retrieve_all_column_values_from_record(self, file_dict, record_number):
        print("     inside: retrieve_all_column_values_from_record")
        values = []
        columns_per_record = int(self.retrieve_a_file_statistic_in_dictionary(file_dict, 4, "columns_per_record"))
        for x in range(columns_per_record):
            values.append(str(self.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_number, x, 1, "VALUE")))
        print("     leaving: retrieve_all_column_values_from_record")
        return values
  
    def retrieve_all_column_types_from_record(self, file_dict, record_number):
        print("     inside: retrieve_all_column_types_from_record")
        types = []
        columns_per_record = int(self.retrieve_a_file_statistic_in_dictionary(file_dict, 4, "columns_per_record"))
        for x in range(columns_per_record):
            types.append(str(self.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_number, x, 2, "TYPE")))
        print("     leaving: retrieve_all_column_types_from_record")
        return types
  
    def retrieve_all_column_formats_from_record(self, file_dict, record_number):
        print("     inside: retrieve_all_column_formats_from_record")
        formats = []
        columns_per_record = int(self.retrieve_a_file_statistic_in_dictionary(file_dict, 4, "columns_per_record"))
        for x in range(columns_per_record):
            formats.append(str(self.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_number, x, 3, "FORMAT")))
        print("     leaving: retrieve_all_column_formats_from_record")
        return formats
    
    def retrieve_all_column_data_from_record(self, file_dict, record_number):
        print("     inside: retrieve_all_column_data_from_record")
        titles = []
        values = []
        types = []
        formats = []
        columns_per_record = int(self.retrieve_a_file_statistic_in_dictionary(file_dict, 4, "columns_per_record"))
        for x in range(columns_per_record):
            titles.append(str(self.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_number, x, 0, "TITLE")))
            values.append(str(self.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_number, x, 1, "VALUE")))
            types.append(str(self.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_number, x, 2, "TYPE")))
            formats.append(str(self.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_number, x, 3, "FORMAT")))
        print("     leaving: retrieve_all_column_data_from_record")
        return (titles, values, types, formats)
  
