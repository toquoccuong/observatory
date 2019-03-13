from benchmarks.benchmark_tracking import start_run

from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
from sklearn.metrics import accuracy_score
import xlsxwriter
import xlrd
import pandas as pd
from os.path import expanduser

NUMBER_OF_RUNS = 1000

def test_function(_state):
    # generate regression dataset
    X, y = make_regression(n_samples=10000, n_features=10, noise=0.1)
    model = LinearRegression()

    with start_run('testmodel', 1, _state, 'testexperiment') as run:
        # fit final model
        model.fit(X, y)
        # record the R-squared
        run.record_metric('r-squared', float(model.score(X, y)))

def test_function_null(_state):
    # generate regression dataset
    X, y = make_regression(n_samples=10000, n_features=10, noise=0.1)
    model = LinearRegression()

    with start_run('testmodel', 1, _state, 'testexperiment') as run:
        # fit final model
        model.fit(X, y)

def test_null():
    import timeit
    setup = "from __main__ import test_function_null; from benchmarks.benchmark_tracking import LocalState_null"
    results = []
    for i in range(10):
        #runs the benchmark x times
        time = timeit.timeit("test_function_null(LocalState_null)", setup= setup, number= NUMBER_OF_RUNS)
        #capture the time it took a certain run to complete
        results.append([i+1 , time])

    return results

def test_method(_state):
    import timeit
    setup = "from __main__ import test_function; from benchmarks.benchmark_tracking import LocalState_cpickle, LocalState_json, LocalState_pickle, LocalState_pytables, LocalState_sqlite, LocalState_text"
    results = []
    for i in range(10):
        #runs the benchmark x times
        time = timeit.timeit("test_function(" + _state + ")", setup= setup, number= NUMBER_OF_RUNS)
        #capture the time it took a certain run to complete
        results.append([i+1 , time])

    return results

def write_to_excel(worksheet, results):
    #worksheet.write(0, col, title + ' (s)')
    row = 1
    col = 0
    
    for result in results:
        sumR = 0
        for run, time in (result):
            worksheet.write(row, col, time)
            sumR += time
            row += 1
        avg = sumR / results.__len__()
        worksheet.write(row, col, avg)
    col += 1
    row = 1

def create_excel_chart(workbook):
    writer = pd.ExcelWriter('C:\\Users\\MichielL\\Documents\\obervatory_output\\Results01.xlsx', engine='xlsxwriter')
    df = pd.DataFrame()
    df.to_excel(writer, sheet_name='Sheet1')

    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({'values': '=Sheet1!$A$12:$G$12'})

    worksheet.insert_chart('K2', chart)


if __name__ == "__main__":
    
    results = [[]]

    results.append(test_null())
    results.append(test_method('LocalState_text'))
    results.append(test_method('LocalState_json'))
    results.append(test_method('LocalState_pickle'))
    results.append(test_method('LocalState_cpickle'))
    results.append(test_method('LocalState_sqlite'))
    results.append(test_method('LocalState_pytables'))

    #create excel file
    home = expanduser("~")
    wbRD = xlrd.open_workbook('C:\\Users\\MichielL\\Documents\\observatory_output\\Results01.xlsx'.format(home))
    sheets = wbRD.sheets()
    workbook = xlsxwriter.Workbook('C:\\Users\\MichielL\\Documents\\observatory_output\\Results01.xlsx'.format(home))
    worksheet = workbook.add_worksheet()
    format1 = workbook.add_format({'num_format': '0.000'})
    worksheet.set_column('A:H', 15, format1)

    #insert date to excel file
    write_to_excel(worksheet, results)


    #make chart
    create_excel_chart(workbook)

    #save file
    workbook.close()
