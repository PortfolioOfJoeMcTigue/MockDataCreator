from DictionaryOperations import DictionaryOperations
import FileReadOperations as reader
import DictionaryOperations as dict
import FileWriteOperations as write

class ListOperations():

    d = dict.DictionaryOperations()
    w = write.FileWriteOperations()
    r = reader.FileReadOperations()
    tab_01 = "    "
    tab_02 = '{}{}'.format(tab_01, tab_01)
    tab_03 = '{}{}'.format(tab_02, tab_01)
    tab_04 = '{}{}'.format(tab_03, tab_01)
    tab_05 = '{}{}'.format(tab_04, tab_01)
    tab_06 = '{}{}'.format(tab_05, tab_01)
    tab_07 = '{}{}'.format(tab_06, tab_01)
    tab_08 = '{}{}'.format(tab_07, tab_01)
    tab_09 = '{}{}'.format(tab_08, tab_01)
    tab_10 = '{}{}'.format(tab_09, tab_01)
    tab_11 = '{}{}'.format(tab_10, tab_01)
    open_curly = "{"
    closed_curly = "}"
    closed_curly_comma = "},"
    open_block = "["
    closed_block = "]"
    config_open_block = "\"config\": ["
    records_open_block = "\"records\": ["
    record_open_block = "\"record\": ["
    columns_open_block = "\"columns\": ["
    column_open_block = "\"column\": ["

    def add_additional_column_to_all_records_in_file_list(self, new_column_list, general_list):
        print("     inside: add_additional_column_to_all_records_in_file_list")
        my = ListOperations()
        records_needed = str(general_list[1])
        file_format = str(general_list[2])
        file_name = str(general_list[3])
        config_records = int(general_list[4])
        columns_per_record= int(general_list[5])
        new_file_list = []

        new_file_list.append(my.open_curly)
        new_file_list.append('{}{}'.format(my.tab_01, my.config_open_block))
        new_file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        new_file_list.append('{}"{}": "{}"'.format(my.tab_03, 'records_needed', records_needed))
        new_file_list.append('{}{}'.format(my.tab_02, my.closed_curly_comma))
        new_file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        new_file_list.append('{}"{}": "{}"'.format(my.tab_03, 'file_format', file_format))
        new_file_list.append('{}{}'.format(my.tab_02, my.closed_curly_comma))
        new_file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        new_file_list.append('{}"{}": "{}"'.format(my.tab_03, 'file_name', file_name))
        new_file_list.append('{}{}'.format(my.tab_02, my.closed_curly_comma))
        new_file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        new_file_list.append('{}"{}": "{}"'.format(my.tab_03, 'config_records', config_records))
        new_file_list.append('{}{}'.format(my.tab_02, my.closed_curly_comma))
        new_file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        new_file_list.append('{}"{}": "{}"'.format(my.tab_03, 'columns_per_record', columns_per_record))
        new_file_list.append('{}{}'.format(my.tab_02, my.closed_curly_comma))
        new_file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        new_file_list.append('{}{}'.format(my.tab_03, my.records_open_block))
        
        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)

        for rec in range(0, config_records):

            records_to_affect = self.d.retrieve_records_to_affect_from_dictionary(file_dict, rec) 
            sql_table = self.d.retrieve_sql_table_from_dictionary(file_dict, rec)
            sql_action = self.d.retrieve_sql_action_from_dictionary(file_dict, rec)
            sql_anchor = self.d.retrieve_sql_anchor_from_dictionary(file_dict, rec)

            new_file_list.append('{}{}'.format(my.tab_04, my.open_curly))
            new_file_list.append('{}{}'.format(my.tab_05, my.record_open_block))
            new_file_list.append('{}{}'.format(my.tab_06, my.open_curly))
            new_file_list.append('{}"{}": "{}"'.format(my.tab_07, 'records_to_affect', records_to_affect))
            new_file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
            new_file_list.append('{}{}'.format(my.tab_06, my.open_curly))
            new_file_list.append('{}"{}": "{}"'.format(my.tab_07, 'sql_table', sql_table))
            new_file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
            new_file_list.append('{}{}'.format(my.tab_06, my.open_curly))
            new_file_list.append('{}"{}": "{}"'.format(my.tab_07, 'sql_action', sql_action))
            new_file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
            new_file_list.append('{}{}'.format(my.tab_06, my.open_curly))
            new_file_list.append('{}"{}": "{}"'.format(my.tab_07, 'sql_anchor', sql_anchor))
            new_file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
            new_file_list.append('{}{}'.format(my.tab_06, my.open_curly))
            new_file_list.append('{}{}'.format(my.tab_07, my.columns_open_block))

            titles_list = self.d.retrieve_all_column_titles_from_record(file_dict, rec)
            values_list = self.d.retrieve_all_column_values_from_record(file_dict, rec)
            types_list  = self.d.retrieve_all_column_types_from_record(file_dict, rec)
            formats_list= self.d.retrieve_all_column_formats_from_record(file_dict, rec)

            for col in range(0, len(titles_list)):
                
                new_file_list.append('{}{}'.format(my.tab_08, my.open_curly))
                new_file_list.append('{}{}'.format(my.tab_09, my.column_open_block))
                new_file_list.append('{}{}'.format(my.tab_10, my.open_curly))
                new_file_list.append('{}"{}": "{}"'.format(my.tab_11, 'TITLE', titles_list[col]))
                new_file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
                new_file_list.append('{}{}'.format(my.tab_10, my.open_curly))
                new_file_list.append('{}"{}": "{}"'.format(my.tab_11, 'VALUE', values_list[col]))
                new_file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
                new_file_list.append('{}{}'.format(my.tab_10, my.open_curly))
                new_file_list.append('{}"{}": "{}"'.format(my.tab_11, 'TYPE', types_list[col]))
                new_file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
                new_file_list.append('{}{}'.format(my.tab_10, my.open_curly))
                new_file_list.append('{}"{}": "{}"'.format(my.tab_11, 'FORMAT', formats_list[col]))
                new_file_list.append('{}{}'.format(my.tab_10, my.closed_curly))
                new_file_list.append('{}{}'.format(my.tab_09, my.closed_block))
                new_file_list.append('{}{}'.format(my.tab_08, my.closed_curly_comma))

            new_file_list.append('{}{}'.format(my.tab_08, my.open_curly))
            new_file_list.append('{}{}'.format(my.tab_09, my.column_open_block))
            new_file_list.append('{}{}'.format(my.tab_10, my.open_curly))
            new_file_list.append('{}"{}": "{}"'.format(my.tab_11, 'TITLE', new_column_list[0]))
            new_file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
            new_file_list.append('{}{}'.format(my.tab_10, my.open_curly))
            new_file_list.append('{}"{}": "{}"'.format(my.tab_11, 'VALUE', new_column_list[1]))
            new_file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
            new_file_list.append('{}{}'.format(my.tab_10, my.open_curly))
            new_file_list.append('{}"{}": "{}"'.format(my.tab_11, 'TYPE', new_column_list[2]))
            new_file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
            new_file_list.append('{}{}'.format(my.tab_10, my.open_curly))
            new_file_list.append('{}"{}": "{}"'.format(my.tab_11, 'FORMAT', new_column_list[3]))
            new_file_list.append('{}{}'.format(my.tab_10, my.closed_curly))
            new_file_list.append('{}{}'.format(my.tab_09, my.closed_block))
            new_file_list.append('{}{}'.format(my.tab_08, my.closed_curly))
            new_file_list.append('{}{}'.format(my.tab_07, my.closed_block))
            new_file_list.append('{}{}'.format(my.tab_06, my.closed_curly))
            new_file_list.append('{}{}'.format(my.tab_05, my.closed_block))
            new_file_list.append('{}{}'.format(my.tab_04, my.closed_curly_comma))
        
        new_file_list.pop()
        new_file_list.append('{}{}'.format(my.tab_04, my.closed_curly))
        new_file_list.append('{}{}'.format(my.tab_03, my.closed_block))
        new_file_list.append('{}{}'.format(my.tab_02, my.closed_curly))
        new_file_list.append('{}{}'.format(my.tab_01, my.closed_block))
        new_file_list.append(my.closed_curly)      
        print("     leaving: add_additional_column_to_all_records_in_file_list")
        return new_file_list

    def add_additional_record_to_file_list(self, current_file_list, record_list, title_list, value_list, type_list, format_list, record_count):
        print("     inside: add_additional_record_to_file_list")
        my = ListOperations()
        tab4 = '            '
        current_record = '{}"{}": "{}"'.format(tab4, 'config_records', record_count)
        current_file_list[12] = current_record
        records_to_affect = record_list[0]
        sql_table = record_list[1]
        sql_action = record_list[2]
        sql_anchor = record_list[3]
        # remove all closing blocks and curly braces after last record.
        for i in range(5):
            current_file_list.pop()
        
        current_file_list.append('{}{}'.format(my.tab_04, my.closed_curly_comma))
        # adding new record here
        current_file_list.append('{}{}'.format(my.tab_04, my.open_curly))
        current_file_list.append('{}{}'.format(my.tab_05, my.record_open_block))
        current_file_list.append('{}{}'.format(my.tab_06, my.open_curly))
        current_file_list.append('{}"{}": "{}"'.format(my.tab_07, 'records_to_affect', records_to_affect))
        current_file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
        current_file_list.append('{}{}'.format(my.tab_06, my.open_curly))
        current_file_list.append('{}"{}": "{}"'.format(my.tab_07, 'sql_table', sql_table))
        current_file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
        current_file_list.append('{}{}'.format(my.tab_06, my.open_curly))
        current_file_list.append('{}"{}": "{}"'.format(my.tab_07, 'sql_action', sql_action))
        current_file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
        current_file_list.append('{}{}'.format(my.tab_06, my.open_curly))
        current_file_list.append('{}"{}": "{}"'.format(my.tab_07, 'sql_anchor', sql_anchor))
        current_file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
        current_file_list.append('{}{}'.format(my.tab_06, my.open_curly))
        current_file_list.append('{}{}'.format(my.tab_07, my.columns_open_block))

        compareLen = (len(title_list) - 1)
        for num in range(0, len(title_list)):

            title_string   = '{}{}"{}"'.format(my.tab_11, "\"TITLE\": ", title_list[num]) 
            value_string   = '{}{}"{}"'.format(my.tab_11, "\"VALUE\": ", value_list[num])
            type_string    = '{}{}"{}"'.format(my.tab_11, "\"TYPE\": ", type_list[num])
            format_string  = '{}{}"{}"'.format(my.tab_11, "\"FORMAT\": ", format_list[num])

            current_file_list.append('{}{}'.format(my.tab_08, my.open_curly))
            current_file_list.append('{}{}'.format(my.tab_09, my.column_open_block))
            current_file_list.append('{}{}'.format(my.tab_10, my.open_curly))
            current_file_list.append(title_string)
            current_file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
            current_file_list.append('{}{}'.format(my.tab_10, my.open_curly))
            current_file_list.append(value_string)
            current_file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
            current_file_list.append('{}{}'.format(my.tab_10, my.open_curly))
            current_file_list.append(type_string)
            current_file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
            current_file_list.append('{}{}'.format(my.tab_10, my.open_curly))
            current_file_list.append(format_string)
            current_file_list.append('{}{}'.format(my.tab_10, my.closed_curly))
            current_file_list.append('{}{}'.format(my.tab_09, my.closed_block))

            if num == compareLen or len(title_list) == 1:
                current_file_list.append('{}{}'.format(my.tab_08, my.closed_curly))
            else:
                current_file_list.append('{}{}'.format(my.tab_08, my.closed_curly_comma))
            num += 1

        current_file_list.append('{}{}'.format(my.tab_07, my.closed_block))
        current_file_list.append('{}{}'.format(my.tab_06, my.closed_curly))
        current_file_list.append('{}{}'.format(my.tab_05, my.closed_block))
        current_file_list.append('{}{}'.format(my.tab_04, my.closed_curly)) 
        # end of record   
        current_file_list.append('{}{}'.format(my.tab_03, my.closed_block))
        current_file_list.append('{}{}'.format(my.tab_02, my.closed_curly))
        current_file_list.append('{}{}'.format(my.tab_01, my.closed_block))
        current_file_list.append(my.closed_curly)
        # end of file
        print("     leaving: add_additional_record_to_file_list")
        return current_file_list

    def create_a_list_from_dictionary(self, file_dict):
        print("     inside: create_a_list_from_dictionary")
        my = ListOperations()
        file_list = []
        file_list.append(my.open_curly)
        file_list.append('{}{}'.format(my.tab_01, my.config_open_block))
        file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        recs_needed_string = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 0, 'records_needed')
        file_list.append('{}"{}": "{}"'.format(my.tab_03, 'records_needed', recs_needed_string))
        file_list.append('{}{}'.format(my.tab_02, my.closed_curly_comma))
        file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        file_format_string = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 1, 'file_format')
        file_list.append('{}"{}": "{}"'.format(my.tab_03, 'file_format', file_format_string))
        file_list.append('{}{}'.format(my.tab_02, my.closed_curly_comma))
        file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        file_name_string = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 2, 'file_name')
        file_list.append('{}"{}": "{}"'.format(my.tab_03, 'file_name', file_name_string))
        file_list.append('{}{}'.format(my.tab_02, my.closed_curly_comma))
        file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        number_of_records = int(self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 3, 'config_records'))
        file_list.append('{}"{}": "{}"'.format(my.tab_03, 'config_records', str(number_of_records)))
        file_list.append('{}{}'.format(my.tab_02, my.closed_curly_comma))
        file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        columns_per_record = int(self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 4, 'columns_per_record'))
        file_list.append('{}"{}": "{}"'.format(my.tab_03, 'columns_per_record', str(columns_per_record)))
        file_list.append('{}{}'.format(my.tab_02, my.closed_curly_comma))
        file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        file_list.append('{}{}'.format(my.tab_03, my.records_open_block))

        if number_of_records == 1:
            record_index = 0
            file_list.append('{}{}'.format(my.tab_04, my.open_curly))
            file_list.append('{}{}'.format(my.tab_05, my.record_open_block))
            file_list.append('{}{}'.format(my.tab_06, my.open_curly))
            records_to_affect = self.d.retrieve_records_to_affect_from_dictionary(file_dict, record_index)
            file_list.append('{}"{}": "{}"'.format(my.tab_07, 'records_to_affect', records_to_affect))
            file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
            file_list.append('{}{}'.format(my.tab_06, my.open_curly))
            sql_table = self.d.retrieve_sql_table_from_dictionary(file_dict, record_index)
            file_list.append('{}"{}": "{}"'.format(my.tab_07, 'sql_table', sql_table))
            file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
            file_list.append('{}{}'.format(my.tab_06, my.open_curly))
            sql_action = self.d.retrieve_sql_action_from_dictionary(file_dict, record_index)
            file_list.append('{}"{}": "{}"'.format(my.tab_07, 'sql_action', sql_action))
            file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
            file_list.append('{}{}'.format(my.tab_06, my.open_curly))
            sql_anchor = self.d.retrieve_sql_anchor_from_dictionary(file_dict, record_index)
            file_list.append('{}"{}": "{}"'.format(my.tab_07, 'sql_anchor', sql_anchor))
            file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
            file_list.append('{}{}'.format(my.tab_06, my.open_curly))
            file_list.append('{}{}'.format(my.tab_07, my.columns_open_block))

            for column_index in range( 0, columns_per_record):
                file_list.append('{}{}'.format(my.tab_08, my.open_curly))
                file_list.append('{}{}'.format(my.tab_09, my.column_open_block))
                file_list.append('{}{}'.format(my.tab_10, my.open_curly))
                title_string = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 0, 'TITLE')
                file_list.append('{}"{}": "{}"'.format(my.tab_11, "TITLE", title_string))
                file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
                file_list.append('{}{}'.format(my.tab_10, my.open_curly))
                value_string = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 1, 'VALUE')
                file_list.append('{}"{}": "{}"'.format(my.tab_11, "VALUE", value_string))
                file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
                file_list.append('{}{}'.format(my.tab_10, my.open_curly))
                type_string = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 2, 'TYPE')
                file_list.append('{}"{}": "{}"'.format(my.tab_11, "TYPE", type_string))
                file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
                file_list.append('{}{}'.format(my.tab_10, my.open_curly))
                format_string = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 3, 'FORMAT')
                file_list.append('{}"{}": "{}"'.format(my.tab_11, "FORMAT", format_string))
                file_list.append('{}{}'.format(my.tab_10, my.closed_curly))
                file_list.append('{}{}'.format(my.tab_09, my.closed_block))
                file_list.append('{}{}'.format(my.tab_08, my.closed_curly_comma))
            
            file_list.pop()
            file_list.append('{}{}'.format(my.tab_08, my.closed_curly))
            file_list.append('{}{}'.format(my.tab_07, my.closed_block))
            file_list.append('{}{}'.format(my.tab_06, my.closed_curly))
            file_list.append('{}{}'.format(my.tab_05, my.closed_block))
            file_list.append('{}{}'.format(my.tab_04, my.closed_curly_comma))
        
        elif number_of_records > 1:
            for record_index in range(0, number_of_records):
                file_list.append('{}{}'.format(my.tab_04, my.open_curly))
                file_list.append('{}{}'.format(my.tab_05, my.record_open_block))
                file_list.append('{}{}'.format(my.tab_06, my.open_curly))
                records_to_affect = self.d.retrieve_records_to_affect_from_dictionary(file_dict, record_index)
                file_list.append('{}"{}": "{}"'.format(my.tab_07, 'records_to_affect', records_to_affect))
                file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
                file_list.append('{}{}'.format(my.tab_06, my.open_curly))
                sql_table = self.d.retrieve_sql_table_from_dictionary(file_dict, record_index)
                file_list.append('{}"{}": "{}"'.format(my.tab_07, 'sql_table', sql_table))
                file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
                file_list.append('{}{}'.format(my.tab_06, my.open_curly))
                sql_action = self.d.retrieve_sql_action_from_dictionary(file_dict, record_index)
                file_list.append('{}"{}": "{}"'.format(my.tab_07, 'sql_action', sql_action))
                file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
                file_list.append('{}{}'.format(my.tab_06, my.open_curly))
                sql_anchor = self.d.retrieve_sql_anchor_from_dictionary(file_dict, record_index)
                file_list.append('{}"{}": "{}"'.format(my.tab_07, 'sql_anchor', sql_anchor))
                file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
                file_list.append('{}{}'.format(my.tab_06, my.open_curly))
                file_list.append('{}{}'.format(my.tab_07, my.columns_open_block))

                for column_index in range( 0, columns_per_record):
                    file_list.append('{}{}'.format(my.tab_08, my.open_curly))
                    file_list.append('{}{}'.format(my.tab_09, my.column_open_block))
                    file_list.append('{}{}'.format(my.tab_10, my.open_curly))
                    title_string = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 0, 'TITLE')
                    file_list.append('{}"{}": "{}"'.format(my.tab_11, "TITLE", title_string))
                    file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
                    file_list.append('{}{}'.format(my.tab_10, my.open_curly))
                    value_string = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 1, 'VALUE')
                    file_list.append('{}"{}": "{}"'.format(my.tab_11, "VALUE", value_string))
                    file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
                    file_list.append('{}{}'.format(my.tab_10, my.open_curly))
                    type_string = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 2, 'TYPE')
                    file_list.append('{}"{}": "{}"'.format(my.tab_11, "TYPE", type_string))
                    file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
                    file_list.append('{}{}'.format(my.tab_10, my.open_curly))
                    format_string = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 3, 'FORMAT')
                    file_list.append('{}"{}": "{}"'.format(my.tab_11, "FORMAT", format_string))
                    file_list.append('{}{}'.format(my.tab_10, my.closed_curly))
                    file_list.append('{}{}'.format(my.tab_09, my.closed_block))
                    file_list.append('{}{}'.format(my.tab_08, my.closed_curly_comma))
            
                file_list.pop()
                file_list.append('{}{}'.format(my.tab_08, my.closed_curly))
                file_list.append('{}{}'.format(my.tab_07, my.closed_block))
                file_list.append('{}{}'.format(my.tab_06, my.closed_curly))
                file_list.append('{}{}'.format(my.tab_05, my.closed_block))
                file_list.append('{}{}'.format(my.tab_04, my.closed_curly_comma))

        file_list.pop()
        file_list.append('{}{}'.format(my.tab_04, my.closed_curly))
        file_list.append('{}{}'.format(my.tab_03, my.closed_block))
        file_list.append('{}{}'.format(my.tab_02, my.closed_curly))
        file_list.append('{}{}'.format(my.tab_01, my.closed_block))
        file_list.append(my.closed_curly)
        print("     leaving: create_a_list_from_dictionary")
        return file_list
    
    def create_and_return_new_file_list_from_data_lists(self, general_list, record_list, titles_list, values_list, types_list, formats_list):
        print("     inside: create_and_return_new_file_dictionary_from_lists")
        my = ListOperations()
        records_needed = '"records_needed": "{}"'.format( general_list[0] )
        file_format = '"file_format": "{}"'.format(general_list[1])
        file_name = '"file_name": "{}"'.format(general_list[2])
        config_records = '"config_records": "{}"'.format(general_list[3])
        columns_per_record = '"columns_per_record": "{}"'.format(general_list[4])
        records_to_affect = '"records_to_affect": "{}"'.format(record_list[0])
        sql_table = '"sql_table": "{}"'.format(record_list[1])
        sql_action = '"sql_action": "{}"'.format(record_list[2])
        sql_anchor = '"sql_anchor": "{}"'.format(record_list[3])
        # create structure of json format in list.
        file_list = []
        file_list.append(my.open_curly) 
        file_list.append('{}{}'.format(my.tab_01, my.config_open_block))
        file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        file_list.append('{}{}'.format(my.tab_03, records_needed))
        file_list.append('{}{}'.format(my.tab_02, my.closed_curly_comma))
        file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        file_list.append('{}{}'.format(my.tab_03, file_format))
        file_list.append('{}{}'.format(my.tab_02, my.closed_curly_comma))
        file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        file_list.append('{}{}'.format(my.tab_03, file_name))
        file_list.append('{}{}'.format(my.tab_02, my.closed_curly_comma))
        file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        file_list.append('{}{}'.format(my.tab_03, config_records))
        file_list.append('{}{}'.format(my.tab_02, my.closed_curly_comma))
        file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        file_list.append('{}{}'.format(my.tab_03, columns_per_record))
        file_list.append('{}{}'.format(my.tab_02, my.closed_curly_comma))
        file_list.append('{}{}'.format(my.tab_02, my.open_curly))
        file_list.append('{}{}'.format(my.tab_03, my.records_open_block))
        # begining of record.
        file_list.append('{}{}'.format(my.tab_04, my.open_curly))
        file_list.append('{}{}'.format(my.tab_05, my.record_open_block))
        file_list.append('{}{}'.format(my.tab_06, my.open_curly))
        file_list.append('{}{}'.format(my.tab_07, records_to_affect))
        file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
        file_list.append('{}{}'.format(my.tab_06, my.open_curly))
        file_list.append('{}{}'.format(my.tab_07, sql_table))
        file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
        file_list.append('{}{}'.format(my.tab_06, my.open_curly))
        file_list.append('{}{}'.format(my.tab_07, sql_action))
        file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
        file_list.append('{}{}'.format(my.tab_06, my.open_curly))
        file_list.append('{}{}'.format(my.tab_07, sql_anchor))
        file_list.append('{}{}'.format(my.tab_06, my.closed_curly_comma))
        file_list.append('{}{}'.format(my.tab_06, my.open_curly))
        file_list.append('{}{}'.format(my.tab_07, my.columns_open_block))
        
        # build columns for record.
        compareLen = (len(titles_list) - 1)
        for num in range(0, len(titles_list)):

            title_string   = '{}"{}": "{}"'.format(my.tab_11, 'TITLE', titles_list[num]) 
            value_string   = '{}"{}": "{}"'.format(my.tab_11, 'VALUE', values_list[num])
            type_string    = '{}"{}": "{}"'.format(my.tab_11, 'TYPE', types_list[num])
            format_string  = '{}"{}": "{}"'.format(my.tab_11, 'FORMAT', formats_list[num])

            file_list.append('{}{}'.format(my.tab_08, my.open_curly))
            file_list.append('{}{}'.format(my.tab_09, my.column_open_block))
            file_list.append('{}{}'.format(my.tab_10, my.open_curly))
            file_list.append(title_string)
            file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
            file_list.append('{}{}'.format(my.tab_10, my.open_curly))
            file_list.append(value_string)
            file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
            file_list.append('{}{}'.format(my.tab_10, my.open_curly))
            file_list.append(type_string)
            file_list.append('{}{}'.format(my.tab_10, my.closed_curly_comma))
            file_list.append('{}{}'.format(my.tab_10, my.open_curly))
            file_list.append(format_string)
            file_list.append('{}{}'.format(my.tab_10, my.closed_curly))
            file_list.append('{}{}'.format(my.tab_09, my.closed_block))

            if num == compareLen or len(titles_list) == 1:
                file_list.append('{}{}'.format(my.tab_08, my.closed_curly))
            else:
                file_list.append('{}{}'.format(my.tab_08, my.closed_curly_comma))
            num += 1

        file_list.append('{}{}'.format(my.tab_07, my.closed_block))
        file_list.append('{}{}'.format(my.tab_06, my.closed_curly))
        file_list.append('{}{}'.format(my.tab_05, my.closed_block))
        file_list.append('{}{}'.format(my.tab_04, my.closed_curly)) 
        # end of record   
           
        file_list.append('{}{}'.format(my.tab_03, my.closed_block))
        file_list.append('{}{}'.format(my.tab_02, my.closed_curly))
        file_list.append('{}{}'.format(my.tab_01, my.closed_block))
        file_list.append(my.closed_curly)
        # end of file
        print("     leaving: create_and_return_new_file_dictionary_from_lists")
        return file_list

    def add_new_column_to_all_records_in_list(self, file_dict, file_list, column_insert_number, column_values_list):
        print("     inside: add_new_column_to_all_records_in_list")
        number_of_records = int(file_dict["config"][3]["config_records"])
        columns_per_record = int(file_dict["config"][4]["columns_per_record"])

        index_point = 19 #first column starts at this index in list.
        column_indexes = []
        column_indexes.append(index_point)
        for x in range(columns_per_record):
            index_point = (index_point + 16)
            column_indexes.append((index_point + 1))

        if number_of_records == 1 and int(column_insert_number) <= columns_per_record:
            index_number = column_indexes[int(column_insert_number)]
            file_list = self.add_column_to_list(file_list, index_number, column_values_list, False)
            print("     leaving: add_new_column_to_all_records_in_list")
            return file_list
        elif number_of_records == 1 and int(column_insert_number) > columns_per_record:
            index_number = column_indexes[int(column_insert_number)]
            file_list = self.add_column_to_list(file_list, index_number, column_values_list, True)
            print("     leaving: add_new_column_to_all_records_in_list")
            return file_list
        elif number_of_records > 1:
            base_lines = 13
            pre_rec_lines = 5
            cols_lines = 16
            post_rec_lines = 5
            total_rec_lines = (pre_rec_lines + (cols_lines * 16) + post_rec_lines)
            for x in range(number_of_records, -1, -1):
                if x == number_of_records and int(column_insert_number) <= columns_per_record:
                    index_number = (base_lines + pre_rec_lines + (total_rec_lines * (x - 1)) + (cols_lines * (int(column_insert_number) - 1)))
                    file_list = self.add_column_to_list(file_list, index_number, column_values_list, False)
                    print("     leaving: add_new_column_to_all_records_in_list")
                    return file_list
                elif x == number_of_records and int(column_insert_number) > columns_per_record:
                    index_number = (base_lines + pre_rec_lines + (total_rec_lines * (x - 1)) + (cols_lines * (int(column_insert_number) - 1)))
                    file_list = self.add_column_to_list(file_list, index_number, column_values_list, True)
                    print("     leaving: add_new_column_to_all_records_in_list")
                    return file_list

    def add_column_to_list(self, file_list, index_number, column_values_list, last_flag):
        print("     inside: add_column_to_list")
        my = ListOperations()
        if last_flag is False:
            file_list.insert(index_number, '{}{}'.format(my.tab_08, my.closed_curly_comma))
        else:
            file_list.insert(index_number, '{}{}'.format(my.tab_08, my.closed_curly))
        file_list.insert(index_number, '{}{}'.format(my.tab_09, my.closed_block))
        file_list.insert(index_number, '{}{}'.format(my.tab_10, my.closed_curly))
        file_list.insert(index_number, '{}"{}": "{}"'.format(my.tab_11, 'FORMAT', column_values_list[3]))
        file_list.insert(index_number, '{}{}'.format(my.tab_10, my.open_curly))
        file_list.insert(index_number, '{}{}'.format(my.tab_10, my.closed_curly_comma))
        file_list.insert(index_number, '{}"{}": "{}"'.format(my.tab_11, 'TYPE', column_values_list[2]))
        file_list.insert(index_number, '{}{}'.format(my.tab_10, my.open_curly))
        file_list.insert(index_number, '{}{}'.format(my.tab_10, my.closed_curly_comma))
        file_list.insert(index_number, '{}"{}": "{}"'.format(my.tab_11, 'VALUE', column_values_list[1]))
        file_list.insert(index_number, '{}{}'.format(my.tab_10, my.open_curly))
        file_list.insert(index_number, '{}{}'.format(my.tab_10, my.closed_curly_comma))
        file_list.insert(index_number, '{}"{}": "{}"'.format(my.tab_11, 'TITLE', column_values_list[0]))
        file_list.insert(index_number, '{}{}'.format(my.tab_10, my.open_curly))
        file_list.insert(index_number, '{}{}'.format(my.tab_09, my.column_open_block))  
        print("     leaving: add_column_to_list")
        return file_list
    
    def correctly_order_of_columns_and_return_list(self, file_name, config_dict):
        print("     inside: correctly_order_of_columns_and_return_list")
        my = ListOperations()
        self.r = reader.FileReadOperations()
        ordered_list = []
        ordered_list.append(my.open_curly)
        ordered_list.append('{}"{}": {}'.format( my.tab_01, 'config', '['))
        ordered_list.append('{}{}'.format( my.tab_02, my.open_curly))
        records_needed = self.d.retrieve_a_file_statistic_in_dictionary(config_dict, 0, 'records_needed')
        ordered_list.append('{}"{}": "{}"'.format( my.tab_03, 'records_needed', records_needed))
        ordered_list.append('{}{}'.format( my.tab_02, my.closed_curly_comma))
        ordered_list.append('{}{}'.format( my.tab_02, my.open_curly))
        file_format = self.d.retrieve_a_file_statistic_in_dictionary(config_dict, 1, 'file_format')
        ordered_list.append('{}"{}": "{}"'.format(my.tab_03, 'file_format', file_format))
        ordered_list.append('{}{}'.format( my.tab_02, my.closed_curly_comma))
        ordered_list.append('{}{}'.format( my.tab_02, my.open_curly))
        file_name = self.d.retrieve_a_file_statistic_in_dictionary(config_dict, 2, 'file_name')
        ordered_list.append('{}"{}": "{}"'.format( my.tab_03, 'file_name', file_name))
        ordered_list.append('{}{}'.format( my.tab_02, my.closed_curly_comma))
        ordered_list.append('{}{}'.format( my.tab_02, my.open_curly))
        number_of_records = int(config_dict["config"][3]["config_records"])
        ordered_list.append('{}"{}": "{}"'.format( my.tab_03, 'config_records', str(number_of_records)))
        ordered_list.append('{}{}'.format( my.tab_02, my.closed_curly_comma))
        ordered_list.append('{}{}'.format( my.tab_02, my.open_curly))
        columns_per_record = int(config_dict["config"][4]["columns_per_record"])
        ordered_list.append('{}"{}": "{}"'.format(my.tab_03, 'columns_per_record', str(columns_per_record)))
        ordered_list.append('{}{}'.format( my.tab_02, my.closed_curly_comma))
        ordered_list.append('{}{}'.format( my.tab_02, my.open_curly))
        ordered_list.append('{}"{}": {}'.format( my.tab_03, 'records', '['))
                
        for rec in range(0, (number_of_records - 1)):
            
            ordered_list.append('{}{}'.format( my.tab_04, my.open_curly))
            ordered_list.append('{}"{}": {}'.format( my.tab_05, 'record', '['))
            ordered_list.append('{}{}'.format( my.tab_06, my.open_curly))
            recs_to_affect = self.d.retrieve_records_to_affect_from_dictionary(config_dict, rec)
            ordered_list.append('{}"{}": "{}"'.format( my.tab_07, 'records_to_affect', recs_to_affect))
            ordered_list.append('{}{}'.format( my.tab_06, my.closed_curly_comma))
            ordered_list.append('{}{}'.format( my.tab_06, my.open_curly))
            sql_table = self.d.retrieve_sql_table_from_dictionary(config_dict, rec)
            ordered_list.append('{}"{}": "{}"'.format( my.tab_07, 'sql_table', sql_table))
            ordered_list.append('{}{}'.format( my.tab_06, my.closed_curly_comma))
            ordered_list.append('{}{}'.format( my.tab_06, my.open_curly))
            sql_action = self.d.retrieve_sql_action_from_dictionary(config_dict, rec)
            ordered_list.append('{}"{}": "{}"'.format( my.tab_07, 'sql_action', sql_action))
            ordered_list.append('{}{}'.format( my.tab_06, my.closed_curly_comma))
            ordered_list.append('{}{}'.format( my.tab_06, my.open_curly))
            sql_anchor = self.d.retrieve_sql_anchor_from_dictionary(config_dict, rec)
            ordered_list.append('{}"{}": "{}"'.format( my.tab_07, 'sql_anchor', sql_anchor))
            ordered_list.append('{}{}'.format( my.tab_06, my.closed_curly_comma))
            ordered_list.append('{}{}'.format( my.tab_06, my.open_curly))
            ordered_list.append('{}"{}": {}'.format( my.tab_07, 'columns', '['))
                
            for col in range(int(columns_per_record)):
                    
                ordered_list.append('{}{}'.format( my.tab_08, my.open_curly))
                ordered_list.append('{}"{}": {}'.format( my.tab_09, 'column', '['))
                ordered_list.append('{}{}'.format( my.tab_10, my.open_curly))
                title_string = self.d.retrieve_a_column_value_of_a_record_in_dictionary(config_dict, rec, col, 0, 'TITLE')
                ordered_list.append('{}"{}": "{}"'.format(my.tab_11, 'TITLE', title_string))
                ordered_list.append('{}{}'.format( my.tab_10, my.closed_curly_comma))
                ordered_list.append('{}{}'.format( my.tab_10, my.open_curly))
                value_string = self.d.retrieve_a_column_value_of_a_record_in_dictionary(config_dict, rec, col, 1, 'VALUE')
                ordered_list.append('{}"{}": "{}"'.format(my.tab_11, 'VALUE', value_string))
                ordered_list.append('{}{}'.format( my.tab_10, my.closed_curly_comma))
                ordered_list.append('{}{}'.format( my.tab_10, my.open_curly))
                type_string = self.d.retrieve_a_column_value_of_a_record_in_dictionary(config_dict, rec, col, 2, 'TYPE')
                ordered_list.append('{}"{}": "{}"'.format(my.tab_11, 'TYPE', type_string))
                ordered_list.append('{}{}'.format( my.tab_10, my.closed_curly_comma))
                ordered_list.append('{}{}'.format( my.tab_10, my.open_curly))
                format_string = self.d.retrieve_a_column_value_of_a_record_in_dictionary(config_dict, rec, col, 3, 'FORMAT')
                ordered_list.append('{}"{}": "{}"'.format(my.tab_11, 'FORMAT', format_string))
                ordered_list.append('{}{}'.format( my.tab_10, my.closed_curly))
                ordered_list.append('{}{}'.format( my.tab_09, my.closed_block))
                ordered_list.append('{}{}'.format( my.tab_08, my.closed_curly_comma))
                break
            
            ordered_list.pop()
            ordered_list.append('{}{}'.format( my.tab_08, my.closed_curly))
            ordered_list.append('{}{}'.format( my.tab_07, my.closed_block))
            ordered_list.append('{}{}'.format( my.tab_06, my.closed_curly))
            ordered_list.append('{}{}'.format( my.tab_05, my.closed_block))
            ordered_list.append('{}{}'.format( my.tab_04, my.closed_curly_comma))
        
        ordered_list.pop()
        ordered_list.append('{}{}'.format( my.tab_04, my.closed_curly))
        ordered_list.append('{}{}'.format( my.tab_03, my.closed_block))
        ordered_list.append('{}{}'.format( my.tab_02, my.closed_curly))
        ordered_list.append('{}{}'.format( my.tab_01, my.closed_block))
        ordered_list.append(my.closed_curly)
        print("     leaving: correctly_order_of_columns_and_return_list")
        return ordered_list
    