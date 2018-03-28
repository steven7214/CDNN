#!/usr/bin/env python

xls = pd.ExcelFile('/../Data/CancerSEEK/Supplmentary Tables (Steven).xlsx')
df1 = pd.read_excel(xls, 'Table S1')
print 'hi'
