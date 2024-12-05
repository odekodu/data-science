"""
Defines an enumeration for representing different data types for a column.

The ColumnType enumeration provides a set of named values for common data types,
including integer, number, datetime, date, time, `and category.

Author: [Ojuju]
Date: [01-11-2024]
"""


import pandas as pd
import numpy as np
import random
from enum import Enum


class ColumnType(Enum):
    # The different data types a column can have.
    integer = 'int64' # Whole numbers
    number = 'float64' # Decimal numbers
    datetime = 'datetime64[ns]' # Date and time
    category = 'category' # Categorical
    text = 'object' # Text
    boolean = 'bool' # Boolean


class ColumnSpan:
    def __init__(self, start, end):
        """
        Constructor for ColumnSpan.
        
        Parameters
        ----------
        start : object
            The start of the span
        end : object
            The end of the span
        
        Returns
        -------
        None
        """
        self.start = start
        self.end = end


class Column:
    def __init__(self, name, dtype:ColumnType, span:ColumnSpan= None, choices:list= ['aaa', 'bbb', 'ccc']):
        """
        Constructor for Column.
        
        Parameters
        ----------
        name : str
            The name of the column
        dtype : ColumnType
            The data type of the column
        span : ColumnSpan
            The span of the data. If None, a default span will be created
        choices : list
            The possible values for the column when dtype is category. If None, a default list of ['a', 'b', 'c'] will be used
        
        Returns
        -------
        None
        """
        self.name = name
        self.dtype = dtype
        self.choices = choices

        # Check if the column is a type of time like (datetime, date or time)
        is_date = ColumnType.datetime == dtype
        
        # set the defualt span when no value is provided
        start = 0 if not is_date else '2022-01-01'
        end = 100 if not is_date else '2023-01-01'
        self.span = span if span else ColumnSpan(start= start, end= end)


def randomSeries(column:Column, rows= 10, missing= 0):
    """
    Generate a random pandas Series with the given column specs.

    Parameters
    ----------
    column : Column
        The column specs
    rows : int
        The number of rows of the series (default is 10)
    missing : float
        The proportion of missing values in the series (default is 0.1)

    Returns
    -------
    pd.Series
        The random pandas Series
    """
    dtype = column.dtype
    choices = column.choices
    span = column.span

    # set the number of missing values using the missing percentage parameter
    missing_count = int(missing * rows)
    
    # set the number of non-missing values by subtracting the missing from the number of rows
    not_missing_count = rows - missing_count
    
    # generate a random list of floats
    if dtype == ColumnType.number:
        dataset = np.random.uniform(span.start, span.end, not_missing_count)
        
    # generate a random list of whole numbers
    elif dtype == ColumnType.integer:
        dataset = np.random.randint(span.start, span.end, not_missing_count)
        
    # generate a random list of datetimes
    elif dtype == ColumnType.datetime:
        dataset = pd.date_range(span.start, span.end, periods=not_missing_count)
    
    # generate a random list of categorical data using the choices provided
    elif (dtype == ColumnType.category):
        dataset = [random.choice(choices) for _ in range(not_missing_count)]

    # generate a random list of object data using the choices provided
    elif (dtype == ColumnType.text):
        dataset = [random.choice(choices) for _ in range(not_missing_count)]

    # generate a random list of object data using the choices provided
    elif (dtype == ColumnType.boolean):
        dataset = [random.choice([True, False]) for _ in range(not_missing_count)]
        
    # Throw an error when an unsupported data type is provided
    else:
        raise ValueError(f"Unsupported dtype: {ColumnType[dtype]}")

    # generate a list of missing data
    missing_dataset = [None] * missing_count
    
    # merge the non-missing and missing datasets and shuffle the entire list then convert to a pandas series
    series = pd.Series([*dataset, *missing_dataset], name= column.name).sample(rows).reset_index(drop=True)

    return series


def randomDataframe(columns: list, rows= 10, missing= 0):
    """
    Generate a random pandas DataFrame with the given column specs.

    Parameters
    ----------
    columns : list
        A list of Column objects
    rows : int
        The number of rows of the DataFrame (default is 10)
    missing : float
        The proportion of missing values in the DataFrame (default is 0.1)

    Returns
    -------
    pd.DataFrame
        The random pandas DataFrame
    """

    # Generate a random Series for each of the provided columns
    series_list = [randomSeries(column, rows, missing).to_frame() for column in columns]
    
    # Concat the generated Series into a DataFrame
    df = pd.concat(series_list, axis=1)
    return df


def populateSeries(series: pd.Series, rows= 10, missing= 0):
    """
    Populate the given Series with random data.

    Parameters
    ----------
    series : pd.Series
        The Series to populate
    missing : float
        The proportion of missing values in the Series (default is 0.1)

    Returns
    -------
    pd.Series
        The populated Series
    """

    # Filter the Series for non-null values
    mask = series.notna()

    # Get the span of the Series
    span = ColumnSpan(start= min(series[mask]), end= max(series[mask]))

    # Get the data type of the Series
    dtype = ColumnType(series.dtype.name)

    # Create a Column object from the existing Series
    column = Column(name= series.name, dtype= dtype, span=span, choices= series[mask].unique().tolist())

    missing = missing if missing else (series.isna().sum() / series.size)
    # Generate a random Series

    # Generate a random Series
    generated = randomSeries(column, rows, missing)

    # merge the generated and existing datasets and shuffle the entire list then convert to a pandas series
    populated_series = pd.Series([*series, *generated], name= column.name).sample(series.size + generated.size).reset_index(drop=True)

    return populated_series


def populateDataframe(df: pd.DataFrame, rows= 10, missing= 0):
    """
    Populate the given DataFrame with random data.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to populate
    columns : list
        A list of Column objects
    rows : int
        The number of rows of the DataFrame (default is 10)
    missing : float
        The proportion of missing values in the DataFrame (default is 0.1)

    Returns
    -------
    pd.DataFrame
        The populated DataFrame
    """

    # Generate a random Series for each of the provided columns
    series_list = [populateSeries(series=df[column], rows=rows, missing=missing).to_frame() for column in df.columns]

    # Concat the generated Series into a DataFrame
    populated_df = pd.concat(series_list, axis=1)

    return populated_df
