import os
import sys
import xlrd
#import xlutils
from xlutils.copy import copy as xlutils_copy

def read(file):
    data = xlrd.open_workbook(file)
    table = data.sheet_by_index(0)

    nRows = table.nrows
    nCols = table.ncols

    for i in range(nRows):
        for j in range(nCols):
            print(table.cell(i, j).value)

    input('input anything to next test.')

    dst = xlutils_copy(data)
    writable_table = dst.get_sheet(0)
    writable_table.write(0, 0, "23232323232323~!!")
    dst.save('abc.xls')

if __name__ == '__main__':
    current = sys.path[0]
    file = current + '/ELSA6P_5090Y_TS27-2.xlsx'

    read(file)    
