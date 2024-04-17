import random
import FileReadOperations as reader

class RandNameOperations():
    
    def get_a_random_first_or_middle_name(self, sex):
        print("inside : get_a_random_first_or_middle_name")
        self.r = reader.FileReadOperations()
        name_list = self.r.get_list_of_first_or_middle_names(sex)
        random_number = random.randint(0, len(name_list))
        result = str(name_list[random_number])
        result = result.title()
        print("leaving : get_a_random_first_or_middle_name")
        return result
    
    def get_first_name_as_optional(self, sex):
        print("inside : get_first_name_as_optional")
        name = ""
        random_number = random.randint(20, 100)
        result_num = (random_number % 20)
        if result_num != 0:
            name = self.get_a_random_first_or_middle_name(sex)
        print("leaving : get_first_name_as_optional")
        return name
    
    def get_first_name_initial_as_optional(self, sex):
        print("inside : get_first_name_initial_as_optional")
        name = self.get_first_name_as_optional(sex)
        name_initial = name[0].upper()
        print("leaving : get_first_name_initial_as_optional")
        return name_initial

    def get_first_name_initial(self, sex):
        print("inside : get_first_name_initial")
        first_name = self.get_a_random_first_or_middle_name(sex)
        first_name_initial = first_name[0].upper()
        print("leaving : get_first_name_initial")
        return first_name_initial

    def get_a_random_last_name(self):
        print("inside : get_a_random_last_name")
        self.r = reader.FileReadOperations()
        name_list = self.r.get_list_of_last_names()
        random_number = random.randint(0, len(name_list))
        result = str(name_list[random_number])
        result = result.title()
        print("leaving : get_a_random_last_name")
        return result
    
    def get_last_name_initial(self):
        print("inside : get_last_name_initial")
        last_name = self.get_a_random_last_name()
        last_name_initial = last_name[0].upper()
        print("leaving : get_last_name_initial")
        return last_name_initial
    
    def create_final_formatted_name(self, names_created, name_types):
        print("inside : create_final_formatted_name")
        full_name = ""
        if len(names_created) == 1:
            full_name = names_created[0]
        elif len(names_created) == 2:
            if name_types[0] == ("MALE" or "FEMALE") and name_types[1] == "LAST":
                full_name = '{} {}'.format(names_created[0], names_created[1])
            elif name_types[0] == "LAST" and name_types[1] == ("MALE" or "FEMALE"):
                full_name = '{}, {}'.format(names_created[0], names_created[1])
            elif name_types[0] == ("MI" or "FI") and name_types[1] == "LI":
                full_name = '{}. {}.'.format(names_created[0], names_created[1])
            elif name_types[0] == ("MI" or "FI") and name_types[1] == "LAST":
                full_name = '{}. {}'.format(names_created[0], names_created[1])
            elif name_types[0] == "LAST" and name_types[1] == ("MI" or "FI"):
                full_name = '{}, {}.'.format(names_created[0], names_created[1])
        elif len(names_created) == 3:
            if name_types[0] == ("MALE" or "FEMALE") and name_types[1] == ("MALE" or "FEMALE") and name_types[2] == "LAST":
                full_name = '{} {} {}'.format(names_created[0], names_created[1], names_created[2])
            elif name_types[0] == "LAST" and name_types[1] == ("MALE" or "FEMALE") and name_types[2] == ("MALE" or "FEMALE"):
                full_name = '{}, {} {}'.format(names_created[0], names_created[1], names_created[2])
            elif name_types[0] == ("MALE" or "FEMALE") and name_types[1] == ("MI" or "FI") and name_types[2] == "LAST":
                full_name = '{} {}. {}'.format(names_created[0], names_created[1], names_created[2])
            elif name_types[0] == "LAST" and name_types[1] == ("MALE" or "FEMALE") and name_types[2] == ("MI" or "FI"):
                full_name = '{}, {} {}.'.format(names_created[0], names_created[1], names_created[2])
            elif name_types[0] == ("MI" or "FI") and name_types[1] == ("MI" or "FI") and name_types[2] == "LAST":
                full_name = '{}. {}. {}'.format(names_created[0], names_created[1], names_created[2])
            elif name_types[0] == ("MI" or "FI") and name_types[1] == ("MI" or "FI") and name_types[2] == "LI":
                full_name = '{}. {}. {}.'.format(names_created[0], names_created[1], names_created[2])
        print("leaving : create_final_formatted_name")
        return full_name
    
    def refine_name_format_requested_into_names_list(self, name_format_requested):
        print("inside : refine_name_format_requested_into_names_list")
        type_names_list = []
        type_names = name_format_requested.split(" ")
        if len(type_names) == 5:
            type_names_list.append(type_names[1])
            type_names_list.append(type_names[2])
            type_names_list.append(type_names[3])
        elif len(type_names) == 4:
            type_names_list.append(type_names[1])
            type_names_list.append(type_names[2])
        elif len(type_names) == 3:
            type_names_list.append(type_names[1])
        print("leaving : refine_name_format_requested_into_names_list")
        return type_names_list

    def process_name_requests(self, name_format_requested):
        print("inside : process_name_requests")
        names_created = []
        name_types = self.refine_name_format_requested_into_names_list(name_format_requested)
        for name_type_requested in name_types:
            name_requested = ""
            match name_type_requested:
                case 'MALE':
                    name_requested = self.get_a_random_first_or_middle_name("MALE")
                case 'FEMALE':
                    name_requested = self.get_a_random_first_or_middle_name("FEMALE")
                case 'LAST':
                    name_requested = self.get_a_random_last_name("LAST")
                case 'MI':
                    name_requested = self.get_a_random_first_or_middle_name("MI")
                case 'FI':
                    name_requested = self.get_a_random_first_or_middle_name("FI")
                case 'LI':
                    name_requested = self.get_last_name_initial()
                case 'MALEOPT':
                    name = self.get_first_name_as_optional("MALE")
                    if len(name_requested) > 0:
                        name_requested = name
                case 'FEMALEOPT':
                    name = self.get_first_name_as_optional("FEMALE")
                    if len(name_requested) > 0:
                        name_requested = name
                case 'MIOPT':
                    name = self.get_first_name_initial_as_optional("MALE")
                    if len(name_requested) > 0:
                        name_requested = name
                case 'FIOPT':
                    name = self.get_first_name_initial_as_optional("FEMALE")
                    if len(name_requested) > 0:
                        name_requested = name
            if len(name_requested) > 0:
                names_created.append(name_requested)
        final_formatted_name = self.create_final_formatted_name(names_created, name_types)
        print("leaving : process_name_requests")
        return final_formatted_name