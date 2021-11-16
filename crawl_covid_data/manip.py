import pandas
x = pandas.read_csv('dummy.csv')
y = x.groupby(['city_code', 'kprq']).sum()
y.to_csv('res.csv')