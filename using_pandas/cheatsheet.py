__author__ = 'sunary'


import pandas as pd


df = pd.DataFrame()

def reading_and_writing():
    df = pd.read_csv('src.csv')
    df.to_csv('dist.csv')

    df = pd.read_excel('src.xlsx', 'sheet1')
    df.to_excel('dist.xlsx', 'sheet2')


def preview():
    df.head(10)
    df.tail(10)
    df.dtypes
    df.columns


def rename():
    global df2

    df.rename(columns={'old_column': 'new_column'})
    df2 = df.rename(columns={'old_column': 'new_column'}, inplace=True)


def select():
    df[['column1', 'column2']]
    df[df['column1'] > 5 & df['column2'] < 10]
    df[df['column1'] < 5 | df['column2'] == 30]


def handing_na():
    df.dropna()
    df.findna(value=1)

    mean = df['column1'].mean()
    df.findna(value=mean)


def new_column():
    df['new_column'] = df['column']

    df['new_column2'] = df['column'] + 10

    df['new_column3'] = df['column1'] + df['column2']


def aggregate():
    df.groupby('column').sum()

    df.groupby(['column1', 'column2']).count()

    pd.pivot_table(df, values='column_value', index=['column_x', 'column_y'], columns=['column_sss'])


def merge():
    global df1, df2

    pd.merge(df1, df2, on='columns', how='left')


def lambda_func():
    df['column1'].map(lambda x: 10 + x)


def unique():
    df['column'].unique()


def statistic():
    df.describe()
    df.cov()
    df.corr()