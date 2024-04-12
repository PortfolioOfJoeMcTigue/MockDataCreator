import random

class SpecialCharOperations():

    def get_random_special_characters(self, number_of_chars_requested):
        print("inside : get_random_special_characters")
        spec_chars = ['#','$','_','-','=','+',':','?','|','.']
        result = ""
        for x in range(0, number_of_chars_requested):
            random_number = random.randint(0, 9)
            result = '{}{}'.format(result, spec_chars[random_number])
        print("leaving : get_random_special_characters")
        return result
    
    def get_special_characters(self, char_requested, number_of_chars_requested):
        print("inside : get_special_characters")
        result = ""
        for x in range(number_of_chars_requested):
            result = '{}{}'.format(result, char_requested)
        print("leaving : get_special_characters")
        return result
    
    def is_special_char_valid(self, spec_char):
        print("inside : is_special_char_valid")
        spec_chars = ['#','$','_','-','=','+',':','?','|','.']
        result = False
        if spec_char in spec_chars:
            result = True
        print("leaving : is_special_char_valid")
        return result
    
    def process_special_character_request(self, special_char_request):
        print("inside : process_special_character_request")
        result = ""
        request_items = special_char_request.split()
        if len(request_items) < 2:
            result = self.get_random_special_characters(1)
        elif len(request_items) < 3:
            is_valid = self.is_special_char_valid( request_items[1])
            if is_valid is True:
                result = str(request_items[1])
        elif len(request_items) < 4:
            spec_char = str(request_items[1])
            number_requested = int(request_items[2])
            is_valid = self.is_special_char_valid( spec_char )
            if is_valid is True:
                result = self.get_special_characters(spec_char, number_requested)
        print("leaving : process_special_character_request")
        return result
        