# coding: latin1
"""
Created on Mar 14, 2013

@author: Jaakko Leppäkangas, Atte Rautio
"""
import unittest

from statistic import Statistic

class TestStatistic(unittest.TestCase):
    """
    Unit tests for the Statistic-class.
    """
    sfreq_int = 1
    sfreq_double = 1.5
    sfreq_zero = 0
        
    arr_normal = [0,25,7,5,48,6,84,2,1]
    arr_many_maximums = [0,85,85,5,48,6,85,48]
    arr_many_minimums = [12,15,20,4,13,4]
    arr_chars = ['a','b']
    arr_negatives = [-40, -100, -10, -15]
    arr_const = [2,2,2,2]
    arr_empty = []
        
    tmin_int = 1000
    tmin_double = 1000.5
    tmin_negative = -6000
    tmin_large = 8000
        
    tmax_int = 5000
    tmax_double = 5000.5
    tmax_negative = -1000
    tmax_small = 1000
    
    ex_negative_tmin_tmax = 'Negative values for tmin and tmax not allowed.'
    ex_sfreq_zero = 'Sampling frequency cannot be zero or negative.'
    ex_arr_empty = 'No data found.'
    ex_tmin_greater_than_tmax = 'tmax must be greater than tmin.'
    
    s = Statistic()
        
    def test_all_normal(self):
        
        self.assertEqual(self.s.find_maximum(self.sfreq_int, self.arr_normal,
                                        1000, 5000), (48, 4000), 
                                        'Find_maximum normal failed')
        
        self.assertEqual(self.s.find_minimum(self.sfreq_int, self.arr_normal,
                                             self.tmin_int, self.tmax_int),
                         (5, 3000), 'Find_minimum_normal failed.')
    
    def test_freq_double(self):
        # TODO: Figure out how this should work
        self.assertEqual(self.s.find_maximum(self.sfreq_double,
                                             self.arr_normal, 1000,5000),
                                            (48, 4000),
                                        'Find_maximum frequency double failed')
        
        self.assertEqual(self.s.find_minimum(self.sfreq_double, self.arr_normal,
                                             self.tmin_int, self.tmax_int),
                         (5, 3000), 'Find_minimum frequency double failed.')
    
    def test_freq_zero(self):
        """
        Should raise an exception when sfreq <= 0.
        """
        with self.assertRaises(Exception) as e:
            self.s.find_maximum(self.sfreq_zero, self.arr_normal, 1000, 5000)
            
        self.assertEqual(e.exception.message, self.ex_sfreq_zero,
                         'Unexpected exception raised on find_maximum with\
                         sfreq zero')
        
        with self.assertRaises(Exception) as e:
            self.s.find_minimum(self.sfreq_zero, self.arr_normal, 1000, 5000)
            
        self.assertEqual(e.exception.message, self.ex_sfreq_zero,
                         'Unexpected exception raised on find_minimum with\
                         sfreq zero.')        
            
    
    def test_tmin_double(self):
        
        self.assertEqual(self.s.find_maximum(self.sfreq_int, self.arr_normal,
                                             self.tmin_double, self.tmax_int),
                         (48, 4000),
                         'Find_maximum tmin double failed')
        
        self.assertEqual(self.s.find_minimum(self.sfreq_int, self.arr_normal,
                                             self.tmin_double, self.tmax_int),
                         (5, 3000), 'Find_minimum tmin double failed.')
    
    def test_tmin_negative(self):
        """
        Statistic class shouldn't be able to receive negative values for 
        tmin and tmax.
        """
        # TODO: Is this really working as intended?
        with self.assertRaises(Exception) as e:
            self.s.find_maximum(self.sfreq_int, self.arr_normal, 
                                self.tmin_negative, self.tmax_int)
            
        self.assertEqual(e.exception.message, self.ex_negative_tmin_tmax,
                         'Unexpected exception raised.')
    
    def test_tmax_negative(self):
        
        with self.assertRaises(Exception) as e:
            self.s.find_maximum(self.sfreq_int, self.arr_normal,
                                self.tmin_int, self.tmax_negative)
            
        self.assertEqual(e.exception.message, self.ex_negative_tmin_tmax,
                         'Unexpected exception raised.')
    
    def test_tmax_smaller_than_tmin(self):
        """
        Time-window cannot end before it begins.
        """
        with self.assertRaises(Exception) as e:
            self.s.find_maximum(self.sfreq_int, self.arr_normal,
                                self.tmin_large, self.tmax_small)
            
        self.assertEqual(e.exception.message, self.ex_tmin_greater_than_tmax,
                         'Unexpected exception raised.')
    
    def test_arr_many_maximums(self):
        """
        Should return the first instance of the maximum and the time it
        occurred.
        """
        self.assertEqual(self.s.find_maximum(self.sfreq_int,
                                             self.arr_many_maximums,
                                             self.tmin_int, self.tmax_int),
                         (85, 1000), 'Find_maximum with many maximums failed.')
        
    def test_arr_many_minimums(self):
        """
        Should return the first instance of the minimum and the time it
        occurred.
        """
        self.assertEqual(self.s.find_minimum(self.sfreq_int,
                                             self.arr_many_minimums,
                                             self.tmin_int, self.tmax_int),
                         (4, 3000), 'Find_minimum with many minimums failed.')
    
    def test_arr_chars(self):
        """
        since nympy arrays should only contain numbers, a TypeError is raised.
        """
        with self.assertRaises(TypeError):
            self.s.find_maximum(self.sfreq_int, self.arr_chars,
                                self.tmin_int, self.tmax_int)                  
    
    def test_arr_negatives(self):
        
        self.assertEqual(self.s.find_maximum(self.sfreq_int,
                                             self.arr_negatives,
                                             self.tmin_int, self.tmax_int),
                         (-10, 2000), 'Find_maximum negative array failed.')
        
        self.assertEqual(self.s.find_minimum(self.sfreq_int,
                                             self.arr_negatives,
                                             self.tmin_int, self.tmax_int),
                         (-100, 1000), 'Find_minimum with negative array\
                         failed.')
        
    def test_find_max_arr_const(self):
        
        self.assertEqual(self.s.find_maximum(self.sfreq_int, self.arr_const,
                                             self.tmin_int, self.tmax_int),
                         (2, 1000), 'Find_maximum with constant array failed.')
        
        self.assertEqual(self.s.find_minimum(self.sfreq_int, self.arr_const,
                                             self.tmin_int, self.tmax_int),
                         (2, 1000), 'Find_minimum with constant array failed.')
        
    def test_arr_empty(self):
        
        with self.assertRaises(Exception) as e:
            self.s.find_maximum(self.sfreq_int, self.arr_empty,
                                self.tmin_int, self.tmax_int)
            self.assertEqual(e.exception.message, self.ex_arr_empty,
                             'Unexpected exception raised with an empty array')
        
    if __name__ == "__main__":
        #import sys;sys.argv = ['', 'TestStatistic.testMax']
        unittest.main()
    