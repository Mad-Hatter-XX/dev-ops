from hbpostgres import param_dic, posgres_pull, postgres_insert
import json
import os

#configuration file
dirname = os.path.dirname(__file__)
configuration_path = dirname + "\configuration.json"
with open(configuration_path) as f:
    configure = json.load(f)
#https://docs.google.com/spreadsheets/d/1z8j3iDtHbODajGcrLqgEFGJD3gARnnfHCsqmFkc0HLM/edit#gid=0
class main:

    def __init__(self):
        #select columns
        self.select_columns = "select" +" "+ str(configure['gloabal_forcast']['input_variables']).strip('[]')
        if self.select_columns == """select '*'""":
            self.select_columns = """select *"""
        #select data from which table
        self._from = "from" + " " + str(configure['gloabal_forcast']['sql_table']).strip('[]')
        #select how much data
        self._limit = "limit" +" "+ str(configure['gloabal_forcast']['data_needed'])
        #join tables with wheres optional
        self._optional_join = str(configure['gloabal_forcast']['OPTIONAL_join']) + " on " + str(configure['gloabal_forcast']['sql_table'])
        if self._optional_join == "null on " + str(configure['gloabal_forcast']['sql_table']):
           self. _optional_join = ""
        else: 
            self._optional_join = self._optional_join + "where" + str(configure['gloabal_forcast']['OPTIONAL_join_where'])
        #combining the statements
        self._request = self.select_columns + self._from + self._optional_join + self._limit

        #send data to database the same way
        self._to_columns = '''"AE", "AL", "AU", "SYM_H"'''
        self._to_select = """select "epochs", """
        self._to_from = """ from omni_1hr_prediction"""
        self._to_request = self._to_select + self._to_columns + self._to_from

    #select = """select "epochs", """ + columns + """ from omni_1hr wind LIMIT 10000"""
    def get_data_from_database(self, param_dic):
        data = posgres_pull(self._request, param_dic)
        return data


    def your_function_here(self, data):
        print('''.
        .
        .
        .
        .
        .
        .
        ...all of you code goes 
        here that df is data
        , also return data....
        .
        .
        .
        .
        .''')
        return data


    def send_data_to_database(self, data):
        postgres_insert(self._to_request, data, param_dic)