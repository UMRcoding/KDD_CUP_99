import pandas as pd

df = pd.read_csv('D:\KDD_CUP_99\kdd_cup\AllData.csv',header=None)
df.pivot_table(index=1,values=[0,4,5],aggfunc='mean')