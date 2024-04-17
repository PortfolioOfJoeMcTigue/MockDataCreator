from functools import reduce
import DictionaryOperations as dicts
import FileReadOperations as read
import FileWriteOperations as write
import RandLetterOperations as letters
import RandNumberOperations as numbers
import RandNameOperations as names
import SpecialCharOperations as specs


class FormatService():
    
    unique_values = []
    start_date_values = []
    start_date_titles = []
    end_date_values = []
    end_date_titles = []

    def process_config_file_data(self, file_name):
        print("inside : process_config_file_data")

        self.d = dicts.DictionaryOperations()
        self.r = read.FileReadOperations()
        self.w = write.FileWriteOperations()

        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)

        records_needed = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 0, "records_needed")
        file_format = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 1, "file_format")
        file_name = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 2, "file_name")
        number_of_records = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 3, "config_records")
        columns_per_record = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 4, "columns_per_record")

        records_to_affect = 0

        for record_index in range(0, number_of_records):
            
            records_to_affect = self.d.retrieve_records_to_affect_from_dictionary(file_dict, record_index)
            sql_table = self.d.retrieve_sql_table_from_dictionary(file_dict, record_index)
            sql_action = self.d.retrieve_sql_action_from_dictionary(file_dict, record_index)
            sql_anchor = self.d.retrieve_sql_anchor_from_dictionary(file_dict, record_index)
            sql_info = '{}-{}-{}'.format(sql_table, sql_action, sql_anchor)

            title_list = [] 
            value_list = [] 
            type_list = [] 
            format_list = [] 
            new_value_list = []
                        
            for column_index in range(0, columns_per_record):
                
                title = str(self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 0, "TITLE"))
                title_list.append(title)
                value = str(self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 1, "VALUE"))
                value_list.append(value)
                type = str(self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 2, "TYPE"))
                type_list.append(type)
                format = str(self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 3, "FORMAT"))
                format_list.append(format)

            for x in range(0, records_to_affect):
                
                for col_index in range(0, len(title_list)):
                    
                    format = format_list[col_index]
                    unique_flag = False
                    if "UNIQUE" in format:
                        unique_flag = True
                        format = format.replace("UNIQUE@", "")
                        
                    value = value_list[col_index]
                    if value == "auto-gen" and unique_flag is True:
                        while True:
                            value = self.get_autogen_value_from_format(format)
                            if value not in new_value_list:
                                value_list.append( value )
                                break
                    elif value == "auto-gen" and unique_flag is False:
                        value = self.get_autogen_value_from_format(format)
                        value_list.append( value )
                    else:
                        value_list.append( value )

                    title_list.append( title )
                    type_list.append( type )

                line_list = []
                is_first_line = False
                if record_index == 0:
                    is_first_line = True
                
                line_list = self.format_lines_for_printing(title_list, value_list, type_list, file_format, sql_info, is_first_line)
                self.w.create_and_append_to_output_data_file(line_list, file_name, file_format)
        print("leaving : process_config_file_data")

    def format_lines_for_printing(self, title_list, value_list, type_list, file_format, sql_info, rec_of_records):
        print("inside : format_lines_for_printing")
        match str(file_format):
                    case "csv":
                        segment_list = self.process_csv_request(title_list, value_list, rec_of_records)
                    case "json":
                        segment_list = self.process_json_requests(title_list, value_list, type_list, rec_of_records)
                    case "parquet":
                        segment_list = self.process_parquet_request(title_list, value_list, type_list, rec_of_records)
                    case "sql":
                        segment_list = self.process_sql_request(title_list, value_list, type_list, sql_info)
        print("leaving : format_lines_for_printing")
        return segment_list

    def process_csv_request(self, title_list, value_list, rec_of_records):
        print("inside : process_csv_request")
        file_list = []
        delim = ","
        rec_info = rec_of_records.split("-")
        current_rec = int(rec_info[0])
        total_recs = int(rec_info[1])
        if current_rec == 1:
            line = reduce(lambda x, y: str(x) +delim + str(y), title_list)
            file_list.append(line)
        if current_rec > 1:
            line = reduce(lambda x, y: str(x) +delim + str(y), value_list)
        file_list.append(line)
        print("leaving : process_csv_request")
        return file_list
    
    def process_json_requests(self, title_list, value_list, type_list, rec_of_records):
        print("inside : process_json_requests")
        file_list = []
        rec_info = rec_of_records.split("-")
        current_rec = int(rec_info[0])
        total_recs = int(rec_info[1])
        records_pre_line = '{'
        records_line = '    "RECORDS": ['
        record_pre_line = '        {'
        record_line = '            "RECORD":['
        columns_pre_line = '                {'
        columns_line = '                    "COLUMNS": ['
        column_pre_line = '                        {'
        column_line = '                            "COLUMN": ['
        if current_rec == 1:
            file_list.append(records_pre_line)
            file_list.append(records_line)
        file_list.append(record_pre_line)
        file_list.append(record_line)
        file_list.append(columns_pre_line)
        file_list.append(columns_line)
        file_list.append(column_pre_line)
        file_list.append(column_line)
        for column_index in range(0, len(title_list)):
            record = '                        {"TITLE": "{}", "VALUE": "{}", "TYPE" : "{}"}'.format(title_list[column_index], value_list[column_index], type_list[column_index])
            if (column_index + 1) != len(title_list):
                record = '{},'.format(record)
                file_list.append(record)
            else:
                file_list.append(record)
                file_list.append('                    ]') # close column array
        if current_rec == total_recs:
            file_list.append('                }') # close column
            file_list.append('            ]') # close record array
            file_list.append('        }') # close record
            file_list.append('    ]') # close records array
            file_list.append('}')
        else:
            file_list.append('                },') # close column with trailing comma, leaving open for next column of elements
        print("leaving : process_json_requests")
        return file_list

    def process_parquet_request(self, title_list, value_list, type_list, rec_of_records):
        print("inside : process_parquet_request")
        file_list = []
        rec_info = rec_of_records.split("-")
        current_rec = int(rec_info[0])
        total_recs = int(rec_info[1])
        print("leaving : process_parquet_request")

    def process_sql_request(self, title_list, value_list, type_list, sql_info):
        print("inside : process_sql_request")
        file_list = []
        record = ""
        segments = sql_info.split("-")
        table_name = segments[0]
        action_value = segments[1]
        anchor_value = segments[2]
        
        if action_value == "INSERT":
            for title_rec in range(0, len(title_list)):
                if title_rec == 0:
                    record = 'INSERT INTO {} ({}'.format(table_name, title_list[title_rec])
                else:
                    record = '{}, {}'.format(record, title_list[title_rec])
            for value_rec in range(0, len(value_list)):
                if value_rec == 0:
                    record = '{}) VALUES (\'{}\''.format(record, value_list[value_rec])
                else:
                    record = '\'{}\', \'{}\''.format(record, value_list[value_rec])
            record = '{});'.format(record)

        if action_value == "UPDATE":
            match_index = self.get_anchor_value_match_from_record(title_list, value_list, anchor_value)
            for title_rec in range(0, len(title_list)):
                if title_rec == 0:
                    record = 'UPDATE {} SET {} = \'{}\''.format(table_name, title_list[title_rec], value_list[title_rec])
                else:
                    record = '{}, {} = \'{}\''.format(record, title_list[title_rec], value_list[title_rec])
            if type_list[match_index] == "integer":
                record = '{} WHERE {} = {};'.format(record, anchor_value, value_list[match_index])
            elif type_list[match_index] == "string":
                record = '{} WHERE {} = \'{}\';'.format(record, anchor_value, value_list[match_index])

        file_list.append(record)
        print("leaving : process_sql_request")
        return file_list

    def get_anchor_value_match_from_record(self, title_list, value_list, anchor_value):
        print("inside : get_anchor_value_match_from_record")
        found_index = 0
        for title_index in range(0, len(title_list)):
            if anchor_value == title_list[title_index]:
                found_index = title_index
                break
        print("inside : get_anchor_value_match_from_record")
        return found_index

    def get_autogen_value_from_format(self, format_request):
        print("inside : get_autogen_value_from_format")

        self.lett = letters.RandNumberOperations()
        self.numb = numbers.RandNumberOperations()
        self.name = names.RandNameOperations()
        self.spec = specs.SpecialCharOperations()

        result = ""
        if "@" in format_request:
            format_list = format_request.split("@")
            result = ""
            for num in reversed(range(len(format_list) + 1)):
                filter_list = format_list[num].split("[")
                match_string = filter_list[0]
                match str(match_string):
                    case "RANDNUM":
                        segment = self.numb.process_number_request(format_list[num])
                    case "RANDLET":
                        segment = self.lett.process_letter_requests(format_list[num])
                    case "RANDNAME":
                        segment = self.name.process_name_requests(format_list[num])
                    case "SPEC":
                        segment = self.spec.process_special_character_request(format_list[num])
                result = '{}{}'.format(result, segment)
        print("leaving : get_autogen_value_from_format")
        return result
