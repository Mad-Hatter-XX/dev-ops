import json
import os

#configuration file
dirname = os.path.dirname(__file__)
configuration_path = dirname + "\configuration.json"
with open(configuration_path) as f:
    configure = json.load(f)


select_columns = "select" +" "+ str(configure['gloabal_forcast']['input_variables']).strip('[]') 
if select_columns == """select '*'""":
    select_columns = """select *"""


print(select_columns)


_from = "from" + " " + str(configure['gloabal_forcast']['sql_table']).strip('[]')

print(_from)

_join = str(configure['gloabal_forcast']['sql_table']).strip('[]') + " on " + str(configure['gloabal_forcast']['sql_table']).strip('[]')
print(_join)


_limit = "limit" +" "+ str(configure['gloabal_forcast']['data_needed']).strip('[]')
print(_limit)


_optional_join = str(configure['gloabal_forcast']['OPTIONAL_join']).strip('[]') + " on " + str(configure['gloabal_forcast']['sql_table']).strip('[]')
if _optional_join == "null on " + str(configure['gloabal_forcast']['sql_table']).strip('[]'):
    _optional_join = ""
else: 
    _optional_join + "where" + str(configure['gloabal_forcast']['OPTIONAL_join_where']).strip('[]')

print(_optional_join)



""" we want to fee a min of 60 days to the model
once it runs we check to see if the other model can run and keep refernce of the dates ran
adding 60 to the end date so we know the next take off point

in reality once enough data is collected the model should see the indicator by the count then start the next model. """
import datetime

start_date = str(configure['gloabal_forcast']['last_pull_date_time'])
date_1 = datetime.datetime.strptime(start_date,'%m/%d/%Y %H:%M:%S.%f')
end_date = datetime.timedelta(days=60) + date_1
end_date2 = str(end_date)
date_2 = datetime.datetime.strptime(end_date2,'%Y-%m-%d %H:%M:%S').strftime("%m/%d/%Y %H:%M:%S.%f")
print(end_date)
print(date_2)

print(start_date)

x = datetime.datetime.strptime(start_date,'%m/%d/%Y %H:%M:%S.%f')
y = datetime.datetime.strptime(date_2,'%m/%d/%Y %H:%M:%S.%f')
diff = x - y


print(diff.days)


#last date ran:


#tracking last date ran
last_date = '05/21/2020 13:00:00.0000'

#configuration file
dirname = os.path.dirname(__file__)
configuration_path = dirname + "\configuration.json"
with open(configuration_path, "r") as jsonFile:
    data = json.load(jsonFile)

data['gloabal_forcast']['last_pull_date_plus_one'] = last_date

with open(configuration_path, "w") as jsonFile:
    json.dump(data, jsonFile)


#get the last date within the prediction database
check_date = "SELECT MAX(epochs) FROM omni_1hr"
check_date = '05/21/2020 13:00:00.0000'

###check date and push forward the time clock
if last_date == check_date:
    date = datetime.datetime.strptime(last_date,'%m/%d/%Y %H:%M:%S.%f')
    date = datetime.timedelta(days=60) + date
    date = str(date)
    new_date = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S').strftime("%m/%d/%Y %H:%M:%S.%f")
    #new_date = datetime.timedelta(days=60) + date
    print(new_date)


#model chech date on last data then run

dirname = os.path.dirname(__file__)
configuration_path = dirname + "\configuration.json"

def check_date():
    with open(configuration_path, "r") as jsonFile:
        configure = json.load(jsonFile)
    last_date_pulled = configure['gloabal_forcast']['last_pull_date_plus_one']
    return last_date_pulled

def sql_check_date_in_datebase(check=str):
    check_date = "SELECT MAX(epochs) FROM omni_1hr"
    check_date = '05/21/2020 13:00:00.0000'
    return check_date


model = 'gloabal_forcast'
variable = 'last_pull_date_plus_one'
def check_updateed_and_update_config_file(model=str, variable=str):
    dirname = os.path.dirname(__file__)
    configuration_path = dirname + "\configuration.json"
    with open(configuration_path, "r") as jsonFile:
        data = json.load(jsonFile)

    data[model][variable] = last_date

    with open(configuration_path, "w") as jsonFile:
        json.dump(data, jsonFile)
    return 0 

#check_updateed_and_update_config_file(model, variable)

from ./postgres import hbpostgres
from ./postgres/hbpostgres import postgres_pull, param_dic

def initalizer():
    #run system if date range and data is avaliable. Continue to run for each range of time is avaliable.
    #Once the range is no longer avalaible stop model and save the last time used

    #first check the date configuration file
    last_date_pulled = check_date()
    #Second find the most current date in omni table or source table
    check_currnent_date_in_sql_though_config_based_on_model = configure['generic']['last_date_in_table'] #"SELECT MAX(epochs) FROM omni_1hr"
    sql_check_date_in_datebase = sql_check_date_in_datebase(check_currnent_date_in_sql_though_config_based_on_model)
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

    pull_data = 'SELECT * FROM omni_1hr where' +' '+ time_variable + ' BETWEEN ' +  last_date_pulled + ' AND ' + new_date

    # pull data and run to system
    results = posgres_pull(pull_data, param_dic)

    #pass data to the model for running
    return False, results

#add a four loop to repeat this task
#if the task trys 2-3 times break the for loop and move on to the next task

    

def runner():
    '''running loop 2-3 times to check if data is avaliable if not exit the model and move on to the next'''
    initalizer, results = initalizer()
    while initalizer == True:
        #done all data is uptodate
        break
    while initalizer == False:
        #call models funtion here
        model_function(results)
        #run this section if initializer is false #run until True
        initalizer, results = initalizer()
        if initalizer == True:
            break

# def upon_start():
#     '''start 

runner()