import unittest
from os import path, getcwd

import numpy as np

from ..data import Categorical
from ..graphs import GraphFrequency
from ..analysis.exc import MinimumSizeError, NoDataError


class MyTestCase(unittest.TestCase):

    @property
    def save_path(self):
        if getcwd().split('/')[-1] == 'test':
            return './images/'
        elif getcwd().split('/')[-1] == 'sci_analysis':
            if path.exists('./setup.py'):
                return './sci_analysis/test/images/'
            else:
                return './test/images/'
        else:
            './'

    def test_100_default_graph(self):
        input_array = ['one', 'two', 'one', 'three', 'one', 'three', 'three', 'one']
        self.assertTrue(GraphFrequency(input_array,
                                       save_to='{}test_freq_100'.format(self.save_path)))

    def test_101_show_percent(self):
        input_array = ['one', 'two', 'one', 'three', 'one', 'three', 'three', 'one']
        self.assertTrue(GraphFrequency(input_array,
                                       percent=True,
                                       save_to='{}test_freq_101'.format(self.save_path)))

    def test_102_ordered_graph(self):
        input_array = ['one', 'two', 'one', 'three', 'one', 'three', 'three', 'one']
        self.assertTrue(GraphFrequency(input_array,
                                       order=['one', 'two', 'three'],
                                       save_to='{}test_freq_102'.format(self.save_path)))

    def test_103_ordered_invalid_categories(self):
        input_array = ['one', 'two', 'one', np.nan, 'one', np.nan, np.nan, 'one']
        self.assertTrue(GraphFrequency(input_array,
                                       order=['one', 'two', 'three'],
                                       save_to='{}test_freq_103'.format(self.save_path)))

    def test_104_ordered_invalid_categories_percent(self):
        input_array = ['one', 'two', 'one', np.nan, 'one', np.nan, np.nan, 'one']
        self.assertTrue(GraphFrequency(input_array,
                                       order=['one', 'two', 'three'],
                                       percent=True,
                                       save_to='{}test_freq_104'.format(self.save_path)))

    def test_105_lots_of_categories_19(self):
        np.random.seed(987654321)
        src = 'aaaaaaaaaaaaaaaaaaa'
        input_array = [src[:np.random.randint(1, 20)] for _ in range(50)]
        self.assertTrue(GraphFrequency(input_array,
                                       save_to='{}test_freq_105'.format(self.save_path)))

    def test_106_lots_of_categories_6(self):
        np.random.seed(987654321)
        src = 'aaaaaa'
        input_array = [src[:np.random.randint(1, 7)] for _ in range(50)]
        self.assertTrue(GraphFrequency(input_array,
                                       save_to='{}test_freq_106'.format(self.save_path)))

    def test_107_lots_of_categories_9(self):
        np.random.seed(987654321)
        src = 'aaaaaaaaa'
        input_array = [src[:np.random.randint(1, 10)] for _ in range(50)]
        self.assertTrue(GraphFrequency(input_array,
                                       save_to='{}test_freq_107'.format(self.save_path)))

    def test_108_lots_of_categories_14(self):
        np.random.seed(987654321)
        src = 'aaaaaaaaaaaaaa'
        input_array = [src[:np.random.randint(1, 15)] for _ in range(50)]
        self.assertTrue(GraphFrequency(input_array,
                                       save_to='{}test_freq_108'.format(self.save_path)))

    def test_109_lots_of_categories_19_percent(self):
        np.random.seed(987654321)
        src = 'aaaaaaaaaaaaaaaaaaa'
        input_array = [src[:np.random.randint(1, 20)] for _ in range(50)]
        self.assertTrue(GraphFrequency(input_array,
                                       percent=True,
                                       save_to='{}test_freq_109'.format(self.save_path)))

    def test_110_lots_of_categories_6_vertical(self):
        np.random.seed(987654321)
        src = 'aaaaaa'
        input_array = [src[:np.random.randint(1, 7)] for _ in range(50)]
        self.assertTrue(GraphFrequency(input_array,
                                       vertical=True,
                                       save_to='{}test_freq_110'.format(self.save_path)))

    def test_111_lots_of_categories_9_vertical(self):
        np.random.seed(987654321)
        src = 'aaaaaaaaa'
        input_array = [src[:np.random.randint(1, 10)] for _ in range(50)]
        self.assertTrue(GraphFrequency(input_array,
                                       vertical=True,
                                       save_to='{}test_freq_111'.format(self.save_path)))

    def test_112_lots_of_categories_19_vertical(self):
        np.random.seed(987654321)
        src = 'aaaaaaaaaaaaaaaaaaa'
        input_array = [src[:np.random.randint(1, 20)] for _ in range(50)]
        self.assertTrue(GraphFrequency(input_array,
                                       vertical=True,
                                       save_to='{}test_freq_112'.format(self.save_path)))

    def test_113_lots_of_categories_19_vertical_percent(self):
        np.random.seed(987654321)
        src = 'aaaaaaaaaaaaaaaaaaa'
        input_array = [src[:np.random.randint(1, 20)] for _ in range(50)]
        self.assertTrue(GraphFrequency(input_array,
                                       vertical=True,
                                       percent=True,
                                       save_to='{}test_freq_113'.format(self.save_path)))

    def test_114_default_graph_title(self):
        input_array = ['one', 'two', 'one', 'three', 'one', 'three', 'three', 'one']
        self.assertTrue(GraphFrequency(input_array,
                                       title='Test',
                                       save_to='{}test_freq_114'.format(self.save_path)))

    def test_115_default_graph_order_Categorical(self):
        input_array = Categorical(['one', 'two', 'one', 'three', 'one', 'three', 'three', 'one'],
                                  order=['three', 'two', 'one'])
        self.assertTrue(GraphFrequency(input_array,
                                       save_to='{}test_freq_115'.format(self.save_path)))

    def test_none(self):
        input_array = None
        self.assertRaises(NoDataError, lambda: GraphFrequency(input_array))

    def test_empty_list(self):
        input_array = list()
        self.assertRaises(NoDataError, lambda: GraphFrequency(input_array))

    def test_empty_set(self):
        input_array = {}
        self.assertRaises(NoDataError, lambda: GraphFrequency(input_array))

    def test_single_value_list(self):
        input_array = [3]
        self.assertRaises(MinimumSizeError, lambda: GraphFrequency(input_array))

    def test_scalar(self):
        input_array = 3
        self.assertRaises(MinimumSizeError, lambda: GraphFrequency(input_array))

if __name__ == '__main__':
    unittest.main()
