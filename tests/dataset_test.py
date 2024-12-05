from utils.dataset import randomDataframe, randomSeries, Column, ColumnType, ColumnSpan
import unittest
import pandas as pd

class TestRandomSeries(unittest.TestCase):
        def test_random_series_should_return_a_pandas_series(self):
            column = Column(name= 'A', dtype= ColumnType.number, span= ColumnSpan(start= 0, end= 100))
            series = randomSeries(column= column)
            self.assertIsInstance(series, pd.Series)