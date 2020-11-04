from hbpostgres import param_dic, posgres_pull, postgres_insert

class main:

    def __init__(self):
        #copy and paste your CSV values here
        self._columns = '''"Bx", "By", "Bz", "V", "n", "AE", "AL", "AU", "SYM_H"'''
        #leave this here
        self._select = """select "epochs", """
        #leave this it is the database name and number of files
        self._from = """ from omni_1hr wind LIMIT 10000"""
        #combining the statements
        self._request = self._select + self._columns + self._from

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