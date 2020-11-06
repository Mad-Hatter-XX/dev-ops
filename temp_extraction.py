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