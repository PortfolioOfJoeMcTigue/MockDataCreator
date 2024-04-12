import random
import FileReadOperations as reader

class RandNumberOperations():
    
    def get_a_random_first_or_middle_name(self, feminine_or_masculine):
        print("inside : get_a_random_first_or_middle_name")
        self.r = reader.FileReadOperations()
        name_list = self.r.get_list_of_first_or_middle_names()
        random_number = random.randint(0, len(name_list))
        result = str(name_list[random_number])
        result = result.title()
        print("leaving : get_a_random_first_or_middle_name")

    def get_a_random_last_name(self):
        print("inside : get_a_random_last_name")
        self.r = reader.FileReadOperations()
        name_list = self.r.get_list_of_last_names()
        random_number = random.randint(0, len(name_list))
        result = str(name_list[random_number])
        result = result.title()
        print("leaving : get_a_random_last_name")
        return result

    def process_name_request(self, name_format_requested):
        print("inside : process_name_request")
        print("leaving : process_name_request")