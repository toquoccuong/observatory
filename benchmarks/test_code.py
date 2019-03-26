from benchmarks.benchmark_tracking import start_run, LocalState_null, LocalState_text, LocalState_json, LocalState_pickle, LocalState_cpickle, LocalState_sqlite, LocalState_pytables

from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
from sklearn.metrics import accuracy_score
import xlsxwriter
import xlrd
import pandas as pd
from os.path import expanduser
import numpy as np

NUMBER_OF_RUNS = 1000
TIMES_TO_RUN = 10

def test_function(_state):
    # generate regression dataset
    X, y = make_regression(n_samples=10000, n_features=10, noise=0.1)
    model = LinearRegression()

    if _state == 1:
        with start_run('testmodel', 1, LocalState_text, 'testexperiment') as run:
            # fit final model
            model.fit(X, y)
            # record the R-squared
            run.record_metric('r-squared', float(model.score(X, y)))
    elif _state == 2:
        with start_run('testmodel', 1, LocalState_json, 'testexperiment') as run:
            # fit final model
            model.fit(X, y)
            # record the R-squared
            run.record_metric('r-squared', float(model.score(X, y)))
    elif _state == 3:
        with start_run('testmodel', 1, LocalState_pickle, 'testexperiment') as run:
            # fit final model
            model.fit(X, y)
            # record the R-squared
            run.record_metric('r-squared', float(model.score(X, y)))
    elif _state == 4:
        with start_run('testmodel', 1, LocalState_cpickle, 'testexperiment') as run:
            # fit final model
            model.fit(X, y)
            # record the R-squared
            run.record_metric('r-squared', float(model.score(X, y)))
    elif _state == 5:
        with start_run('testmodel', 1, LocalState_sqlite, 'testexperiment') as run:
            # fit final model
            model.fit(X, y)
            # record the R-squared
            run.record_metric('r-squared', float(model.score(X, y)))
    elif _state == 6:
        with start_run('testmodel', 1, LocalState_pytables, 'testexperiment') as run:
            # fit final model
            model.fit(X, y)
            # record the R-squared
            run.record_metric('r-squared', float(model.score(X, y)))
    

def test_function_null():
    # generate regression dataset
    X, y = make_regression(n_samples=10000, n_features=10, noise=0.1)
    model = LinearRegression()

    with start_run('testmodel', 1, LocalState_null, 'testexperiment') as run:
        # fit final model
        model.fit(X, y)

def test_null():
    import timeit
    setup = "from __main__ import test_function_null; from benchmarks.benchmark_tracking import LocalState_null"
    results = []
    for i in range(TIMES_TO_RUN):
        #runs the benchmark x times
        time = timeit.timeit("test_function_null()", setup= setup, number= NUMBER_OF_RUNS)
        #capture the time it took a certain run to complete
        results.append([i+1 , time])

    return results

def test_method(_state):
    import timeit
    setup = "from __main__ import test_function"
    results = []
    for i in range(TIMES_TO_RUN):
        #runs the benchmark x times
        time = timeit.timeit("test_function(" + str(_state) + ")", setup= setup, number= NUMBER_OF_RUNS)
        #capture the time it took a certain run to complete
        results.append([i+1 , time])

    return results

def write_to_excel(worksheet, results):
    col = 0
    avgAll = []
    for i in range(len(results)):
        sumR = 0
        row = 1
        for j in range(len(results[i])):
            worksheet.write(row, col, results[i][j][1])
            sumR += results[i][j][1]
            row += 1
        avg = sumR / TIMES_TO_RUN
        avgAll.append(avg)
        worksheet.write(row, col, avg)
        col += 1
    
    return avgAll

def create_headers_excel(worksheet):
    row = 0
    worksheet.write(row, 0, 'Nul meting (s)')
    worksheet.write(row, 1, 'File Saving (s)')
    worksheet.write(row, 2, 'JSON  (s)')
    worksheet.write(row, 3, 'Pickle (s)')
    worksheet.write(row, 4, 'cPickle (s)')
    worksheet.write(row, 5, 'SQLite (s)')
    worksheet.write(row, 6, 'PyTables (s)')


def create_excel_chart(workbook, worksheet, avg):
    writer = pd.ExcelWriter('C:\\Users\\USER\\Documents\\observatory_output\\Results01.xlsx', engine='xlsxwriter')
    df = pd.DataFrame()
    df.to_excel(writer, sheet_name='Sheet1')
    
    T = ['Nul meting', 'File Saving', 'JSON', 'Pickle', 'cPickle', 'SQLite', 'PyTables']
    list1 = np.column_stack((T, avg))

    #this sorting function needs some work, it sorts on the first number, so 60 is smaller than 9 -_-
    list2 = sorted(list1, key=lambda l:l[1], reverse= True)
    print(list2)

    worksheet.write(20, 0, list2[0][0])
    worksheet.write(21, 0, list2[1][0])
    worksheet.write(22, 0, list2[2][0])
    worksheet.write(23, 0, list2[3][0])
    worksheet.write(24, 0, list2[4][0])
    worksheet.write(25, 0, list2[5][0])
    worksheet.write(26, 0, list2[6][0])

    worksheet.write(20, 1, float(list2[0][1]))
    worksheet.write(21, 1, float(list2[1][1]))
    worksheet.write(22, 1, float(list2[2][1]))
    worksheet.write(23, 1, float(list2[3][1]))
    worksheet.write(24, 1, float(list2[4][1]))
    worksheet.write(25, 1, float(list2[5][1]))
    worksheet.write(26, 1, float(list2[6][1]))

    chart = workbook.add_chart({'type': 'bar'})
    chart.add_series({
        'name'          : 'Benchmark results',
        'categories'    : '=Sheet1!$A$21:$A$27',
        'values'        : '=Sheet1!$B$21:$B$27'
        })

    worksheet.insert_chart('K2', chart)


if __name__ == "__main__":
    
    results_null = test_null()
    results_text = test_method(1)
    results_json = test_method(2)
    results_pickle = test_method(3)
    results_cpickle = test_method(4)
    results_sqlite = test_method(5)
    results_pytables = test_method(6)

    results_All = [results_null, results_text, results_json, results_pickle, results_cpickle, results_sqlite, results_pytables]

    #create excel file
    home = expanduser("~")
    workbook = xlsxwriter.Workbook('C:\\Users\\USER\\Documents\\observatory_output\\Results01.xlsx'.format(home))
    worksheet = workbook.add_worksheet()
    format1 = workbook.add_format({'num_format': '0.000'})
    

    #insert date to excel file
    create_headers_excel(worksheet)
    avgAll = write_to_excel(worksheet, results_All)

    #make chart
    create_excel_chart(workbook, worksheet, avgAll)

    #save file
    worksheet.set_column('A:H', 15, format1)
    workbook.close()
