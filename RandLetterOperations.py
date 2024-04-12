import random

class RandNumberOperations():

    def get_random_letters_by_length(self, character_length_requested):
        print("inside : get_random_letters_by_length")
        alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        result = ""
        for x in range(0, character_length_requested):
            random_number = random.randint(0,25)
            result = '{}{}'.format( result, alphabet[random_number])
        print("leaving : get_random_letters_by_length")
        return result
    
    def get_random_letters_between_two_letter_indexes(self, index_one, index_two, character_length_requested):
        print("inside : get_random_letters_between_two_letter_indexes")
        alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        result = ""
        for x in range(character_length_requested):
            random_number = random.randint(index_one, index_two)
            result = '{}{}'.format(result, alphabet[random_number])
        print("leaving : get_random_letters_between_two_letter_indexes")
        return result
    
    def get_random_vowel(self, character_number_requested):
        print("inside : get_random_vowel")
        vowels = ['a','e','i','o','u','y']
        result = ""
        for x in range(0, character_number_requested):
            random_number = random.randint(0,5)
            result = '{}{}'.format( result, vowels[random_number])
        print("leaving : get_random_vowel")
        return result
    
    def get_random_consonant(self, character_number_requested):
        print("inside : get_random_consonant")
        consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
        result = ""
        for x in range(0, character_number_requested):
            random_number = random.randint(0,20)
            result = '{}{}'.format( result, consonants[random_number])
        print("leaving : get_random_consonant")
        return result
    
    def change_case_of_letters_in_string(self, request_letters, requested_case):
        print("inside : change_case_of_letters_in_string")
        result = ""
        if "uppercase" == requested_case:
            result = request_letters.upper()
        else:
            result = request_letters.lower()
        print("leaving : change_case_of_letters_in_string")
        return result
    
    def get_index_of_letter_in_alphabet(self, letter):
        print("inside : get_index_of_letter_in_alphabet")
        alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        letter = letter.lower()
        letter_index = 0
        for x in range(0, len(alphabet)):
            if letter == alphabet[x]:
                letter_index = x
                break
        print("leaving : get_index_of_letter_in_alphabet")
        return letter_index

    def process_letter_requests(self, letter_request):
        print("inside : process_letter_requests")
        result = ""
        uppercase_flag = False
        request_items = letter_request.split()
        if len(request_items) < 3: # a-z
            result = self.get_random_letters_by_length(1)
        elif len(request_items) == 3:
            if "-" in request_items[1]: # A-M
                letters = request_items[1].split("-")
                first_letter = letters[0]
                second_letter = letters[1]
                letter_index_one = self.get_index_of_letter_in_alphabet(first_letter)
                letter_index_two = self.get_index_of_letter_in_alphabet(second_letter)
                result = self.get_random_letters_between_two_letter_indexes(letter_index_one, letter_index_two, 1)
                if first_letter.isupper(): # uppercase
                    uppercase_flag = True 
            elif "VOL" in request_items[1]: # vowels
                result = self.get_random_vowel(1)
            elif "CON" in request_items[1]: # consonants
                result = self.get_random_consonant(1)
        elif len(request_items) == 4: # A-M LEN-#
            letters = request_items[1].split("-")
            length_filter = request_items[2].split("-")
            characters_requested = int(length_filter[1])
            first_letter = letters[0]
            second_letter = letters[1]
            letter_index_one = self.get_index_of_letter_in_alphabet(first_letter)
            letter_index_two = self.get_index_of_letter_in_alphabet(second_letter)
            result = self.get_random_letters_between_two_letter_indexes(letter_index_one, letter_index_two, characters_requested)
            if first_letter.isupper():
                uppercase_flag = True

        if uppercase_flag is True:
            result = self.change_case_of_letters_in_string(result, "upper")
        else:
            result = self.change_case_of_letters_in_string(result, "lower")
        print("leaving : process_letter_requests")
        return result