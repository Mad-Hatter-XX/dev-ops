#from hbpostgres import param_dic, posgres_pull, postgres_insert
import json
import os

from postgres.hbpostgres import param_dic, posgres_pull, postgres_insert


#configuration file
dirname = os.path.dirname(__file__)
configuration_path = dirname + r"\configuration.json"
with open(configuration_path) as f:
    configure = json.load(f)
#https://docs.google.com/spreadsheets/d/1z8j3iDtHbODajGcrLqgEFGJD3gARnnfHCsqmFkc0HLM/edit#gid=0
class main(model_name=str):


    def __init__(self, model_name=str):
        '''This section is for downloading data
        ---Note---
        You have the option to fill in all of the sections in the config file or just type the custom_sql_output
        You must fill in null for the sql_table if that is the case.
        '''
        self.model_name = model_name
        if str(configure[self.model_name]['sql_table']) == "null":
            self._request = str(configure[self.model_name]['custom_sql_out_db'])
        else:
            '''This section is for downloading data'''
            self.select_columns = "select" +" "+ str(configure[self.model_name]['input_variables']).strip('[]')
            if self.select_columns == """select '*'""":
                self.select_columns = """select *"""
            #select data from which table
            self._from = "from" + " " + str(configure[self.model_name]['sql_table']).strip('[]')
            #select how much data
            self._limit = "limit" +" "+ str(configure[self.model_name]['data_needed'])
            #join tables with wheres optional
            self._optional_join = str(configure[self.model_name]['OPTIONAL_join']) + " on " + str(configure[self.model_name]['sql_table'])
            if self._optional_join == "null on " + str(configure[self.model_name]['sql_table']):
                self._optional_join = ""
            else: 
                self._optional_join = self._optional_join + "where" + str(configure[self.model_name]['OPTIONAL_join_where'])
            #combining the statements
            self._request = self.select_columns + self._from + self._optional_join + self._limit
        '''This section is for uploading data'''
        if str(configure[self.model_name]['send_to_sql_table']) == "null":
            self._to_request = str(configure[self.model_name]['custom_sql_into_db']) 
        else:
            #send data to database the same way
            self.select_to_columns = "select" +" "+ str(configure[self.model_name]['output_variables']).strip('[]')
            #select data from which table
            self._to_from =  "from" + " " + str(configure[self.model_name]['send_to_sql_table']).strip('[]')     #""" from omni_1hr_prediction"""
            self._to_request = self.select_to_columns + self._to_from

    #select = """select "epochs", """ + columns + """ from omni_1hr wind LIMIT 10000""

    def check_date(self):
        #getting last pulled date from configfile
        with open(configuration_path, "r") as jsonFile:
            configure = json.load(jsonFile)
        last_date_pulled = str(configure[self.model_name]['last_pull_date_plus_one'])
        return last_date_pulled

    def sql_check_date_in_datebase(self):
        check_date = str(configure[self.model_name]['check_date_in_sql_for_main_table'])
        check_date = posgres_pull(check_date, param_dic)
        return check_date


    def check_date_and_update_config_file(self, model_name=str, last_date_pulled=str):
        dirname = os.path.dirname(__file__)
        configuration_path = dirname + r"\configuration.json"
        with open(configuration_path, "r") as jsonFile:
            configure = json.load(jsonFile)

        configure[self.model_name]['last_pull_date_plus_one'] = last_date_pulled

        with open(configuration_path, "w") as jsonFile:
            json.dump(configure, jsonFile)
        return 0 

    def initalizer(self):
        '''run system if date range and data is avaliable. Continue to run for each range of time is avaliable.
        Once the range is no longer avalaible stop self.model_name and save the last time used
        '''
        time_variable = "epochs"
        #first check the date configuration file
        last_date_pulled = self.check_date()
        #Second find the most current date in omni table or source table
        check_currnent_date_in_sql_though_config_based_on_model = str(configure['generic']['last_date_in_table']) #"SELECT MAX(epochs) FROM omni_1hr"
        #postgres check highest date
        sql_check_date_in_datebase = posgres_pull(check_currnent_date_in_sql_though_config_based_on_model, param_dic)
        #third compare the two dates
        if last_date_pulled == sql_check_date_in_datebase:
            results = 0
            return True, results
        else:
            #create the range of data that needs to be pulled
            date = datetime.datetime.strptime(last_date_pulled,'%m/%d/%Y %H:%M:%S.%f')
            date = datetime.timedelta(days=60) + date
            date = str(date)
            new_date = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S').strftime("%m/%d/%Y %H:%M:%S.%f")
        #Finally
        #get the data from the database in the given range 
        pull_data = "select" +" "+ str(configure[self.model_name]['input_variables']).strip('[]') +" "+"from" + " " + str(configure[self.model_name]['sql_table']).strip('[]') +" "+ "where" +" "+ time_variable +" "+"BETWEEN" + " "+ last_date_pulled +" "+ "AND" +" "+ new_date
        # pull data and run to system
        results = posgres_pull(pull_data, param_dic)

        #update for last date/time pulled
        last_date_pulled = new_date
        #this will update the config file
        self.check_date_and_update_config_file(self.model_name, last_date_pulled)
        #pass data to the self.model_name for running
        return False, results

    def model_function(self, data):
        'pass data in and pass data out'
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



    def runner(self):
        '''running loop 2-3 times to check if data is avaliable if not exit the self.model_name and move on to the next'''
        initalizer, results = self.initalizer()
        while initalizer == True:
            #done all data is uptodate
            break
        while initalizer == False:
            #call models funtion here
            data_output_from_model = self.model_function(results)
            #insert data into postgres
            postgres_insert(self._to_request, data_output_from_model, param_dic)
            #run this section if initializer is false #run until True
            initalizer, results = self.initalizer()
            if initalizer == True:
                break



   #runner()