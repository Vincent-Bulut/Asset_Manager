import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm


def linearRegression_xl_file(path,
                             explanatoryVariable,
                             dependantVariable,
                             x_lbound=0,
                             x_ubound=2500,
                             y_lbound=0,
                             y_ubound=1500000):
    data = pd.read_excel(path)
    x = data[explanatoryVariable]
    y = data[dependantVariable]
    plt.scatter(x, y)
    plt.axis([x_lbound, x_ubound, y_lbound, y_ubound])
    plt.xlabel(explanatoryVariable)
    plt.ylabel(dependantVariable)
    plt.show()
    x1 = sm.add_constant(x)
    reg = sm.OLS(y, x1).fit()
    print(reg.summary())
    print('\n')
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    print('slope: ' + str(slope))
    print('intercept: ' + str(intercept))
    print('r_value: ' + str(r_value))
    print('r_squared_value: ' + str(r_value ** 2))
    print('p_value :' + str(p_value))
    print('std_err :' + str(std_err))

# example:
# myPath = 'Housing.xlsx'
# explanatoryVariable = 'House Size (sq.ft.)'
# dependantVariable = 'House Price'
# linearRegression_xl_file(myPath, explanatoryVariable, dependantVariable)

