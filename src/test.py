import xlrd

rb = xlrd.open_workbook('../inputs/Savedtranslations.xlsx')
sheet = rb.sheet_by_index(0)
print (sheet)
mysheet = []
for i in range(sheet.nrows):
    mysheet.append([sheet.cell_value(i, 0), sheet.cell_value(i, 1), sheet.cell_value(i, 2), sheet.cell_value(i, 3)])
n = len(mysheet)
print(mysheet)