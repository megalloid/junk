#!/usr/bin/env python3

import json
import requests
import unittest

class api_test:

    def __init__(self):
        self.api_url = ('https://regions-test.2gis.com/1.0/regions')
        self.country_codes = ['ru', 'kg', 'kz', 'cz']


    # Return field total
    def get_total(self):
        resp = requests.get(self.api_url)
        res = resp.json()['total']
        return res


    # Return field total
    def get_total_default_page(self):
        resp = requests.get(self.api_url)
        res = resp.json()['items']
        return res


    def check_default_page_size(self):
        count = len(self.get_total_default_page())
        if(count != 15): 
            message = f'Count of records with default page_size is not equal 15. Given {count}'
            print(message)
            exit(message)


    # Get count returned records from request
    def get_count_items_from_page(self, page, page_size):
        assert (page > 0), f'Get count from page: Error page number! Should be > 0, given: {page}'
        assert (page_size == 5) or (page_size == 10) or (page_size == 15), f'Get count from page: Error page size! Should be 5, 10 or 15, given: {page_size}'

        count_items_on_page = len(self.get_all_from_page(page, page_size))

        print(f'Get count from page: {page} page with page size = {page_size} have {count_items_on_page} records') 
        return count_items_on_page


    # Return data from page with size
    def check_incorrect_page(self):
        check_nums = [0, -1, '', 'a', 1.5, '2,1']
        
        for i in check_nums:
            params = {'page': i}
            resp = requests.get(self.api_url, params)
        
            if('500' in str(resp)): 
                print(resp)
                continue

            elif('200' in str(resp)):
                res = resp.json()['error']
                print(res)

            if(res['message'] == ''):
                print(f'Error, incorrect value {i} in page not handled!')
                exit()


    # Return data from page with size
    def check_incorrect_page_size(self):
        check_nums = [0, -1, '', 'a', 1, 1.2, 1.5, '2,01', 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17]
        
        for i in check_nums:
            params = {'page_size': i}
            resp = requests.get(self.api_url, params)
        
            if('500' in str(resp)): 
                print(resp)
                continue

            elif('200' in str(resp)):
                res = resp.json()['error']
                print(res)

            if(res['message'] == ''):
                print(f'Error, incorrect value {i} in page size not handled!')
                exit()


    # Return data from page with size
    def check_incorrect_name(self):
        check_names = [0, -1, '', 'ор']
        
        for i in check_names:
            params = {'q': i}
            resp = requests.get(self.api_url, params)
        
            if('500' in str(resp)): 
                print(resp)
                continue

            elif('200' in str(resp)):
                res = resp.json()['error']
                print(res)

            if(res['message'] == ''):
                print(f'Error, incorrect value {i} in page size not handled!')
                exit()


    def check_page_size_params(self):
        page_sizes = [5, 10, 15]

        for i in page_sizes:
            params = {'page_size' : i}
            resp = requests.get(self.api_url, params)
            res = resp.json()['items']

            if(len(res) == i):
                given_records = len(res)
                print(f'Given records: {given_records} equal that expected {i}')
            else:
                exit(f'Given records: {given_records} NOT equal that expected {i}')


    def check_ignoring_params_till_q_used(self):
        
        clear_params = {'q' : 'рск'}
        resp = requests.get(self.api_url, clear_params)
        clear_res = resp.json()['items']

        params = [{'q' : 'рск', 'page' : '1'}, {'q' : 'рск', 'page' : '2', 'page_size': '5'}, {'q' : 'рск', 'page' : '2', 'page_size': '5', 'country_code' : 'kz'}, {'q' : 'рск', 'page' : '2', 'page_size': '4', 'country_code' : 'ua'}]

        for i in params:
            resp = requests.get(self.api_url, i)
            res = resp.json()['items']

            if(res == clear_res): 
                print(f'\n\r Current results: \n\r {res} \n\r \n\r is equal with clear query: \n\r {clear_res} \r\n \n\r Arguments is not work. Fine! \n\r')
            else:
                exit('Arguments is work! Error! ')


    # Return data from page with size
    def get_all_from_page(self, page, page_size):
        assert (page > 0), f'Get all from page: Error page number! Should be > 0, given: {page}'
        assert (page_size == 5) or (page_size == 10) or (page_size == 15), f'Get all from page: Error page size! Should be 5, 10 or 15, given: {page_size}'

        params = {'page': page, 'page_size': page_size}
        resp = requests.get(self.api_url, params)
        res = resp.json()['items']

        if(len(res) == 0):
            print(f'Get all from page = {page} and page_size = {page_size}: Empty answer!')
        
        return res


    def get_record_by_name(self, name):
        assert (len(name) >= 3), 'Get record by name: Error in name! Shoud be bigger or equal 3 symbols!'

        params = {'q': name}
        resp = requests.get(self.api_url, params)
        res = resp.json()['items']

        if(len(res) == 0):
            print(f'Get record by name = {name} - Empty answer!')
            
        return res

    
    # Return data from page with size
    def get_all_from_page_country(self, page, page_size, country_code):
        assert (page > 0), 'Get all from page, page_size, country: Error page number! Should be > 0'
        assert (page_size == 5) or (page_size == 10) or (page_size == 15), 'Get all from page, page_size, country: Error page size! Should be 5, 10 or 15 '
        assert (country_code == 'ru') or (country_code == 'kz') or (country_code == 'kg') or (country_code == 'cz'), 'Get all from page, page_size, country: Error country code! Should be ru, kz, kg or cz'

        params = {'page': page, 'page_size': page_size, 'country_code': country_code}
        resp = requests.get(self.api_url, params)
        res = resp.json()['items']

        if(len(res) == 0):
            print(f'Get all from page = {page}, page_size = {page_size}, country_code = {country_code}: Empty answer!')
        
        return res


    # Get count records in all db
    def get_total_count_records(self, page_size):
        assert (page_size == 5) or (page_size == 10) or (page_size == 15), 'Error page size! Should be 5, 10 or 15 '

        i = 1
        while self.get_count_items_from_page(i, page_size) == page_size:
            i = i + 1

        count_last_page = len(self.get_all_from_page(i, page_size))
        total = (i * page_size) - (page_size - count_last_page)

        print(f' ')
        print(f'{i} pages with page size = {page_size}') 
        print(f'Count records on last page: {count_last_page}')
        print(f'Total count records: {total}')

        return total


    # Get count recods in all db
    def get_total_records(self, page_size):
        assert (page_size == 5) or (page_size == 10) or (page_size == 15), 'Error page size! Should be 5, 10 or 15 '

        i = 1
        while self.get_count_items_from_page(i, page_size) == page_size:
            i = i + 1

        j = 1
        sum_dict = []
        while j <= i:
            page_content = self.get_all_from_page(j, page_size)
            j = j + 1

            sum_dict = sum_dict + page_content

        return sum_dict


    def check_doubles_with_page_size(self, page_size):
        assert (page_size == 5) or (page_size == 10) or (page_size == 15), 'Error page size! Should be 5, 10 or 15 '

        total_list = self.get_total_records(page_size)

        #no_dupes = [x for n, x in enumerate(total_list) if x not in total_list[:n]]
        #print("No dupes: "+str(no_dupes)+"\n\r")

        dupes = [x for n, x in enumerate(total_list) if x in total_list[:n]]

        if(len(dupes) > 0):
            print("\n\rDupes: "+str(dupes))
            exit('Duplicates found!')
        else:
            print("No dupes")


    def check_total_records_on_pages(self, page_size):
        assert (page_size == 5) or (page_size == 10) or (page_size == 15), 'Error page size! Should be 5, 10 or 15 '

        if(self.get_total_count_records(page_size) == self.get_total()):
            print(f"Total records in DB equal with realy given with {page_size} page size  \n\r")
        else:
            message = f"Total records in DB not equal with realy given with {page_size} page size \n\r"
            print(message)
            exit(message)

    
    def check_valid_country(self, page_size, country_code):
        assert (page_size == 5) or (page_size == 10) or (page_size == 15), 'Error page size! Should be 5, 10 or 15 '
        assert (country_code == 'ru') or (country_code == 'kz') or (country_code == 'kg') or (country_code == 'cz'), 'Error country code! Should be ru, kz, kg or cz'

        i = 1
        while self.get_all_from_page_country(i, page_size, country_code) == page_size:
            i = i + 1

        j = 1
        sum_dict = []
        while j <= i:
            page_content = self.get_all_from_page_country(j, page_size, country_code)
            j = j + 1

            sum_dict = sum_dict + page_content

        for item in sum_dict:
            current_item = item['name']
            current_country_code = item['country']['code']

            if(current_country_code != country_code):
                exit(f'Current record {current_item} is incorrect: Country code mismatch, shoud be \'{country_code}\' but \'{current_country_code}\' given') 
            

    def check_valid_country_in_all_records(self, page_size):
        assert (page_size == 5) or (page_size == 10) or (page_size == 15), 'Error page size! Should be 5, 10 or 15 '

        i = 1
        while self.get_count_items_from_page(i, page_size) == page_size:
            i = i + 1
        
        print(f'Total pages {i}')

        j = 1
        sum_dict = []
        while j <= i:
            page_content = self.get_all_from_page(j, page_size)
            j = j + 1

            sum_dict = sum_dict + page_content

        for item in sum_dict:
            current_item = item['name']
            current_country_code = item['country']['code']
            
            if(current_country_code != 'ru') and (current_country_code != 'kz') and (current_country_code != 'kg') and (current_country_code != 'cz'):
                exit(f'Current record {current_item} is incorrect: Country code should be exist in DB, but this country code not exist: \'{current_country_code}\'') 


    def check_valid_struct_all_records(self, page_size):
        assert (page_size == 5) or (page_size == 10) or (page_size == 15), 'Error page size! Should be 5, 10 or 15 '

        i = 1
        while self.get_count_items_from_page(i, page_size) == page_size:
            i = i + 1
        
        print(f'Total pages {i}')

        j = 1
        sum_dict = []
        while j <= i:
            page_content = self.get_all_from_page(j, page_size)
            j = j + 1

            sum_dict = sum_dict + page_content

        for item in sum_dict:
            assert ('id' in item) and (str(item['id']) != ''), 'Check struct: Field ID not exist or empty'
            assert ('name' in item) and (str(item['name']) != ''), 'Check struct: Field \'name\' not exist or empty'
            assert ('code' in item) and (str(item['code']) != ''), 'Check struct: Field \'code\' not exist or empty'
            assert ('country' in item) and (str(item['country']) != ''), 'Check struct: Field \'country\' not exist or empty'
            #assert 'foo' in items, 'Check struct: Field \'foo\' not existт'

            for country in item['country']:
                assert ('name' in country) or ('code' in country), 'Check struct: Fields \'country\':\'name\' not \'country\':\'code\' not exist'


    def check_is_name_valid_all(self, page_size):
        assert (page_size == 5) or (page_size == 10) or (page_size == 15), 'Error page size! Should be 5, 10 or 15 '

        i = 1
        while self.get_count_items_from_page(i, page_size) == page_size:
            i = i + 1
        
        print(f'Total pages {i}')

        j = 1
        sum_dict = []
        while j <= i:
            page_content = self.get_all_from_page(j, page_size)
            j = j + 1

            sum_dict = sum_dict + page_content

        for item in sum_dict:
            current_item = item['name']

            if(len(current_item) < 3):
                message = f'Current record {current_item} is incorrect: size of name is not correct. Should be >= 3 symbols '
                print(message)
                exit(message)


    def check_is_query_valid_with_specsymbols_all(self, page_size):
        assert (page_size == 5) or (page_size == 10) or (page_size == 15), 'Error page size! Should be 5, 10 or 15 '

        i = 1
        while self.get_count_items_from_page(i, page_size) == page_size:
            i = i + 1
        
        print(f'Total pages {i}')

        j = 1
        sum_dict = []
        while j <= i:
            page_content = self.get_all_from_page(j, page_size)
            j = j + 1

            sum_dict = sum_dict + page_content

        for item in sum_dict:
            current_item = item['name']

            if 'ё' in current_item:
                returned_record = self.get_record_by_name(current_item)

                if(len(returned_record) == 0):
                    exit(f'Error handle \'ё\' symbol in {current_item}. Empty result!')


    def check_valid_all_countries(self, page_size):
        assert (page_size == 5) or (page_size == 10) or (page_size == 15), 'Error page size! Should be 5, 10 or 15 '

        for cc in self.country_codes:
            print(f"Check country code \'{cc}\'")
            self.check_valid_country(5, cc)



class TestAPI(unittest.TestCase):

    def setUp(self):
        self.regions = api_test()
        self.page_sizes = [5,10,15]
        self.country_codes = ['ru', 'kg', 'kz', 'cz']


    def test_check_handlers_on_incorrect_values(self):
        print('\n\r ######## Check is work handlers on incorrect values ######## ')
        self.regions.check_incorrect_page()
        self.regions.check_incorrect_page_size()
        self.regions.check_incorrect_name()
        

    def test_page_size_params_give_correct_count(self):
        print('\n\r ######## Check is page_size params give correct results ######## ')
        self.regions.check_page_size_params()


    def test_check_ignore_params_till_q_used(self):
        print('\n\r ######## Check is ignored another arguments till used q-parameter for search elements ######## ')
        self.regions.check_ignoring_params_till_q_used()


    def test_check_struct_and_empty_fields(self):
        print('\n\r ######## Test check struct and empty fields started ######## ')
        for i in self.page_sizes:
            print(f'\n\rCheck with page_size = {i}')
            self.regions.check_valid_struct_all_records(i)


    def test_default_page_size(self):
        print('\n\r ######## Test default page size started ######## ')
        self.regions.check_default_page_size()


    def test_check_doubles(self):
        print('\n\r ######## Test check doubles started ######## ')
        for i in self.page_sizes:
            print(f'\n\rCheck with page_size = {i}')
            self.regions.check_doubles_with_page_size(i)
    
    
    def test_check_valid_country_in_all_records(self):
        print('\n\r ######## Test test_check_valid_country_in_all_records  ######## ')
        for i in self.page_sizes:
            print(f'\n\rCheck with page_size = {i}')
            self.regions.check_valid_country_in_all_records(i)


    def test_check_countries(self):
        print('\n\r ######## Test that all records has valid country values ######## ')
        for i in self.page_sizes:
            print(f'\n\rCheck with page_size = {i}')
            self.regions.check_valid_all_countries(i)


    def test_check_count_of_records_in_all_pages(self):
        print('\n\r ######## Test check count of records in all pages (with doubles) started ######## ')
        for i in self.page_sizes:
            print(f'\n\rCheck with page_size = {i}')
            self.regions.check_total_records_on_pages(i)


    def test_check_length_name(self):
        print('\n\r ######## Test that all records has valid length names ######## ')
        for i in self.page_sizes:
            print(f'\n\rCheck with page_size = {i}')
            self.regions.check_is_name_valid_all(i)


    def test_check_special_russian_symbols(self):
        print('\n\r ######## Test that symbol \'ё\' correctly used in query ######## ')
        for i in self.page_sizes:
            print(f'\n\rCheck with page_size = {i}')
            self.regions.check_is_query_valid_with_specsymbols_all(i)


if __name__ == '__main__':

    unittest.main()
    

    
    

    

    
        
    
    


    
    

