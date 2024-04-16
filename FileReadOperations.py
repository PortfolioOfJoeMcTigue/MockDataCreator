import re
import os
#from collections import OrderedDict
import pandas as pd
#import json
from os.path import exists
from pathlib import Path
import FileWriteOperations as writer

class FileReadOperations():
    
    def get_list_from_from_user_config_file(self, file_name):
        print("     inside: get_list_from_from_user_config_file")
        home_path = self.get_configs_home_path("user-config-path")
        file_path = '{}\\{}'.format(home_path, str(file_name))
        file_list = []
        file = open(file_path, 'r')
        lines = file.readlines()
        for line in lines:
            line = line.strip('\n')
            if len(line) > 0:
                file_list.append(line)
        print("     leaving: get_list_from_from_user_config_file")
        return file_list
    
    def get_list_of_first_or_middle_names(self, name_preference):
        print("     inside: get_list_of_first_or_middle_names")
        if name_preference == "MALE":
            file_name = "male_first_or_middle_names.cfg"
        else:
            file_name = "female_first_or_middle_names.cfg"
        home_path = self.get_configs_home_path("name-path")
        file_path = '{}\\{}'.format(home_path, file_name)
        file_list = []
        file = open(file_path, 'r')
        lines = file.readlines()
        for line in lines:
            line = line.strip('\n')
            if len(line) > 0:
                file_list.append(line)
        print("     leaving: get_list_of_first_or_middle_names")
        return file_list

    def get_list_of_last_names(self):
        print("     inside: get_list_of_last_names")
        file_name = "last_names.cfg"
        home_path = self.get_configs_home_path("name-path")
        file_path = '{}\\{}'.format(home_path, file_name)
        file_list = []
        file = open(file_path, 'r')
        lines = file.readlines()
        for line in lines:
            line = line.strip('\n')
            if len(line) > 0:
                file_list.append(line)
        print("     leaving: get_list_of_last_names")
        return file_list
        
    def retrieve_dictionary_from_json_file(self, file_name):
        print("     inside: retrieve_dictionary_from_json_file")
        file_dict = {}
        home_path = self.get_configs_home_path("user-config-path")
        file_path = '{}\\{}'.format(home_path, file_name)
        file_dict = pd.read_json(file_path)
        print("     leaving: retrieve_dictionary_from_json_file")
        return file_dict
  
    def get_configs_home_path(self, config):
        print("     inside: get_configs_home_path")
        property_path = "C://Projects/Python/Mock-Data-Creator/app-configs/application.properties"
        config_path = ""
        file = open(property_path, 'r')
        lines = file.readlines()
        for line in lines:
            title_path_list = line.split("@")
            if config == title_path_list[0]:
                config_path = title_path_list[1]
                break
        config_path = config_path.strip()
        print("     leaving: get_configs_home_path")
        return config_path

    def get_list_of_config_files_in_home_dir(self):
        print("     inside: get_list_of_config_files_in_home_dir")
        config_path = self.get_configs_home_path("user-config-path") 
        pattern = re.compile(r'^[a-z|A-Z]{1}\d{6}_\w_\d{2}-\d{2}-\d{4}_\d{2}.cfg$')
        results = ["Create New Configuration File"]
        for file_name in os.listdir(config_path):
            check_path = os.path.join(config_path, file_name)
            if os.path.isdir(check_path):
                continue
            finding = pattern.search(file_name)
            if str(finding) == "None":
                results.append(file_name)
        print("     leaving: get_list_of_config_files_in_home_dir")
        return results
    
    def get_list_of_data_output_files_in_output_dir(self):
        print("     inside: get_list_of_data_output_files_in_output_dir")
        config_path = self.get_configs_home_path("output-file-path") 
        results = ["Create New Configuration File"]
        for file_name in os.listdir(config_path):
            check_path = os.path.join(config_path, file_name)
            if os.path.isdir(check_path):
                continue
            results.append(file_name)
        print("     leaving: get_list_of_data_output_files_in_output_dir")
        return results

    # def remove_column_from_ordered_properties_file(self, file_name, remove_column_index):
    #     print("inside: remove_column_from_ordered_properties_file")
    #     self.w = writer.FileWriteOperations()
    #     property_file_name = "ordered.properties" 
    #     home_path = self.get_configs_home_path("column-order-path")
    #     order_path = '{}\\{}'.format(home_path, property_file_name)
    #     result_list = []
    #     temp_list = []
    #     file = open(order_path, 'r')
    #     lines = file.readlines()
    #     for line in lines:
    #         string_list = line.split("@")
    #         if str(file_name) == str(string_list[0]):
    #             tmp_string = str(string_list[1])
    #             tmp_string = tmp_string.strip()
    #             temp_list = tmp_string.split(",")
    #             temp_list.pop(remove_column_index)
    #             new_line = '{}@{}'.format(file_name, temp_list.join(","))
    #             result_list.append(new_line)
    #         else:
    #             result_list.append(line)
    #     self.w.write_list_to_file(self, "column-order-path", property_file_name, result_list)
    #     print("leaving: remove_column_from_ordered_properties_file")

    def add_new_column_to_ordered_properties_file(self, file_name, column_value, add_column_index):
        print("     inside: add_new_column_to_ordered_properties_file")
        self.w = writer.FileWriteOperations()
        property_file_name = "ordered.properties" 
        home_path = self.get_configs_home_path("column-order-path")
        order_path = '{}\\{}'.format(home_path, property_file_name)
        result_list = []
        temp_list = []
        file = open(order_path, 'r')
        lines = file.readlines()
        for line in lines:
            string_list = line.split("@")
            if str(file_name) == str(string_list[0]):
                tmp_string = str(string_list[1])
                tmp_string = tmp_string.strip()
                temp_list = tmp_string.split(",")
                temp_list.insert(add_column_index, column_value)
                new_line = '{}@{}'.format(file_name, temp_list.join(","))
                result_list.append(new_line)
            else:
                result_list.append(line)
        self.w.write_list_to_file(self, "column-order-path", property_file_name, result_list)
        print("     leaving: add_new_column_to_ordered_properties_file")

    # def read_in_ordered_list_properties(self):
    #     print("inside : read_in_ordered_list_properties")
    #     order_path = "C:\\Users\\josep\\Projects\\Python\\Mock-Data-Creator\\app-configs\\order.property"
    #     ordered_list = []
    #     file = open(order_path, 'r')
    #     lines = file.readlines()
    #     for line in lines:
    #         ordered_list.append(line)
    #     print("leaving: read_in_ordered_list_properties")
    #     return ordered_list

    def get_size_of_file(self, file_name):
        print("     inside: get_size_of_file")
        home_path = self.get_configs_home_path("user-config-path")
        absolute_file_path = '{}\\{}'.format(home_path, str(file_name))
        file_size = os.stat(absolute_file_path).st_size
        print("     leaving: get_size_of_file")
        return file_size
    
    def read_in_types_and_formats_from_config_file(self):
        print("     inside: read_in_types_and_formats_from_config_file")
        home_path = self.get_configs_home_path("app-config-path")
        type_file_name = "type.config"
        format_file_name = "format.config"
        type_path = '{}\\{}'.format(home_path, type_file_name)
        format_path = '{}\\{}'.format(home_path, format_file_name)
        typesList = self.read_column_list_in(type_path)
        formatsList = self.read_column_list_in(format_path)
        print("     leaving: read_in_types_and_formats_from_config_file")
        return (typesList, formatsList)
    
    def read_column_list_in(self, config_path):
        print("     inside: read_column_list_in")
        results_list = []
        file = open(config_path, 'r')
        lines = file.readlines()
        for line in lines:
            results_list.append(line)
        print("     leaving: read_column_list_in")
        return results_list

