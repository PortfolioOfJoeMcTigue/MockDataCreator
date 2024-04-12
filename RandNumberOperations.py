import random


class RandNumberOperations():

    def get_random_number_by_digit_length(self, digit_length_requested):
        print("inside : get_random_number_by_length")
        rand_number = ""
        for x in range(0, digit_length_requested):
            rand_num = random.randint(0,9)
            rand_number = '{}{}'.format(rand_number, str(rand_num))
        print("leaving : get_random_number_by_length")
        return rand_number
    
    def get_precision_number(self, left_digit_length, right_digit_length):
        print("inside : get_precision_number")
        left_number = self.get_random_number_by_digit_length(left_digit_length)
        right_number= self.get_random_number_by_digit_length(right_digit_length)
        rand_precision = '{}.{}'.format(left_number, right_number)
        print("leaving : get_precision_number")
        return rand_precision
    
    def process_number_request(self, request_string):
        print("inside : process_number_request")
        result = ""
        has_spaces = " " in request_string
        if has_spaces is False:
            result = self.get_random_number_by_digit_length(1)
        else:
            request_item = request_string.split()
            action_item = request_item[1]
            action = "LEN" in action_item
            if action is True:
                segments = action_item.split('-')
                digits_needed = int(segments[1])
                result = self.get_random_number_by_digit_length(digits_needed) 
            else:
                segments = action_item.split('-')
                left_digits = int(segments[1])
                right_digits= int(segments[2])
                result = self.get_precision_number(left_digits, right_digits)
        print("leaving : process_number_request")
        return result
      