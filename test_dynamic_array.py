import unittest
from time import time
from dynamic_array import DynamicArray


class DynamicArrayTestCase(unittest.TestCase):
    """Tests for all public methods and operations of the DynamicArray class using
    _INITIAL_SIZE as the size of the test array which is filled with the values
    range(self._INITIAL_SIZE) and _GROWTH_FACTOR as the multiplier for shrinking
    and expanding the dynamic array.
    """
    _INITIAL_SIZE = 5  # Do not set below 5
    _GROWTH_FACTOR = 2

    def setUp(self):
        """Create a new DynamicArray instance"""
        self.arr = DynamicArray(self._GROWTH_FACTOR)
        for i in range(self._INITIAL_SIZE):
            self.arr.append(i)

    def test_append(self):
        """Test correct placement in array when appending 1,000 numbers"""
        arr = DynamicArray(self._GROWTH_FACTOR)
        num_elements = 1000
        self.assertEqual(0, len(arr))  # Make sure the array begins empty

        # Insert num_elements elements
        for i in range(num_elements):
            arr.append(i)
            self.assertEqual(i, arr[i])  # Check element inserted correctly
        self.assertEqual(num_elements, len(arr))  # Check all elements inserted

    def test_extend(self):
        """Test extending array maintains original values and adds new values"""
        # Add 20 new elements to the array and make sure the starting value matches
        # the pattern of the original array to easily test for equality
        self.arr.extend([i for i in range(self._INITIAL_SIZE, self._INITIAL_SIZE + 20)])
        for i in range(self._INITIAL_SIZE + 20):
            self.assertEqual(i, self.arr[i])

    def test_insert(self):
        """Test array insertion correctly inserts value at desired index"""
        # [0, 1, 2, 3, 4] --> ['apple', 0, 1, (5, -1), 2, 3, 4, self.arr]
        # Create the array [0, 1, 2, 3, 4]
        arr = DynamicArray(self._GROWTH_FACTOR)
        for i in range(5):
            arr.append(i)

        # Insert new values
        arr.insert(0, 'apple')
        arr.insert(3, (5, -1))
        arr.insert(len(arr), self.arr)

        self.assertEqual(['apple', 0, 1, (5, -1), 2, 3, 4,
                          [i for i in range(self._INITIAL_SIZE)]], arr)

    def test_insert_out_of_bounds(self):
        """Test inserting with indices that are out of bounds"""
        # [0, 1, 2, 3, 4] --> [-1, 0, 1, 2, 3, 5, 4, 6]
        # Create the array [0, 1, 2, 3, 4]
        arr = DynamicArray(self._GROWTH_FACTOR)
        for i in range(5):
            arr.append(i)

        arr.insert(-1, 5)  # Insert 5 at the front
        arr.insert(100, 6)  # Insert 6 at the end
        arr.insert(-10, -1)  # Insert -1 at the front

        self.assertEqual([-1, 0, 1, 2, 3, 5, 4, 6], arr)

    def test_remove_valid_item(self):
        """Test that element in array is removed"""
        self.arr.remove(2)  # Remove 2 from the array
        self.assertNotIn(2, self.arr)  # Check that removed element is gone
        self.assertEqual(3, self.arr[2])  # Make sure elements moved up

    def test_remove_invalid_item(self):
        """Test that ValueError is raised when element not found"""
        # _INITIAL_SIZE should not be present in the array since it is populated
        # using range(self._INITIAL_SIZE)
        self.assertRaises(ValueError, self.arr.remove, self._INITIAL_SIZE)

    def test_pop_from_end(self):
        """Test that value popped from end is removed and returned"""
        self.assertEqual(self._INITIAL_SIZE - 1, self.arr.pop())
        self.assertNotIn(self._INITIAL_SIZE - 1, self.arr)  # Make sure value removed
        self.assertEqual(self._INITIAL_SIZE - 1, len(self.arr))

    def test_pop_from_middle(self):
        """Test that value popped from middle is removed and returned"""
        self.assertEqual(2, self.arr.pop(2))
        self.assertNotIn(2, self.arr)
        self.assertEqual(self._INITIAL_SIZE - 1, len(self.arr))

    def test_pop_from_beginning(self):
        """Test that value popped from beginning is removed and returned"""
        self.assertEqual(0, self.arr.pop(0))
        self.assertNotIn(0, self.arr)
        self.assertEqual(self._INITIAL_SIZE - 1, len(self.arr))

    def test_clear(self):
        """Test that all values are removed from the array"""
        self.arr.clear()
        self.assertEqual(0, len(self.arr))
        self.assertEqual([], self.arr)  # Array should be empty

    def test_index_single(self):
        """Test that index of item is returned when item is in array"""
        # Since the range function is used for setting up the initial values in the
        # dynamic array, the value at any index is equal to that index value. This makes
        # it ambiguous whether or not index() is returning the index or the value, so
        # that is why a new value without this property is appended and tested against.
        unique_value = self._INITIAL_SIZE + 2
        self.arr.append(unique_value)
        self.assertEqual(self._INITIAL_SIZE, self.arr.index(unique_value))

    def test_index_slice(self):
        """Test that index of item is returned from slice of array"""
        # See test_index_single method for explanation of unique_value
        unique_value = self._INITIAL_SIZE + 2
        self.arr.append(unique_value)
        s = self._INITIAL_SIZE  # Alias for less verbose statement
        # Make sure that value unique_value is found as the last element in the array
        # (meaning index self._INITIAL_SIZE) when array is indexed such that only the
        # last half of the array is included
        self.assertEqual(s, self.arr.index(unique_value, s - (s // 2)))

    def test_index_invalid(self):
        """Test that ValueError is raised when item is not present in array"""
        self.assertRaises(ValueError, self.arr.index, self._INITIAL_SIZE + 2)

    def test_count(self):
        """Test correct number of occurrences is returned"""
        self.arr.append(self._INITIAL_SIZE - 1)  # Add another copy of the last element
        self.assertEqual(2, self.arr.count(self._INITIAL_SIZE - 1))
        self.assertEqual(1, self.arr.count(0))
        self.assertEqual(0, self.arr.count(self._INITIAL_SIZE))

    def test_sort(self):
        """Test that elements are correctly sorted in ascending order"""
        sorted_list = sorted([i for i in range(self._INITIAL_SIZE)])
        self.arr.sort()
        self.assertEqual(sorted_list, self.arr)

    def test_reverse(self):
        """Test that elements are reversed in array"""
        reversed_list = list(reversed([i for i in range(self._INITIAL_SIZE)]))
        self.arr.reverse()
        self.assertEqual(reversed_list, self.arr)

    def test_copy(self):
        """Test that a shallow copy of the list is returned"""
        copied_list = self.arr.copy()
        for i in range(len(self.arr)):
            # Check for alias equality since this should be a shallow copy
            self.assertIs(copied_list[i], self.arr[i])

    def test_print(self):
        """Test that array prints values similar to print(list)"""
        # Compare how python prints a list with the print of the array
        self.assertEqual(str([i for i in range(self._INITIAL_SIZE)]), str(self.arr),)

    def test_comparison_operators(self):
        """Test array support for comparison operators (==, !=, <, <=, >, >=)"""
        arr = DynamicArray(self._GROWTH_FACTOR)
        for i in range(5):
            arr.append(i)

        self.assertEqual([i for i in range(5)], arr)  # [0,1,2,3,4] == [0,1,2,3,4]
        self.assertNotEqual([i for i in range(1, 6)], arr)  # [1,2,3,4,5] != [0,1,2,3,4]
        self.assertNotEqual([i for i in range(0, 4)], arr)  # [0,1,2,3] != [0,1,2,3,4]
        self.assertLess([i for i in range(-1, 4)], arr)  # [-1,0,1,2,3] < [0,1,2,3,4]
        self.assertLessEqual([i for i in range(-1, 4)], arr)  # [-1,0,1,2,3] <= [0,1,2,3,4]
        self.assertLessEqual([i for i in range(5)], arr)  # [0,1,2,3,4] <= [0,1,2,3,4]
        self.assertGreater([i for i in range(1, 6)], arr)  # [1,2,3,4,5] > [0,1,2,3,4]
        self.assertGreaterEqual([i for i in range(1, 6)], arr)  # [1,2,3,4,5] >= [0,1,2,3,4]
        self.assertGreaterEqual([i for i in range(5)], arr)  # [0,1,2,3,4] >= [0,1,2,3,4]

    def test_item_assignment(self):
        """Test that array supports item assignment such as arr[1] = 2"""
        # Reassign values in array
        self.arr[0] = 'apple'
        self.arr[3] = -5

        # Test the result of the reassignment
        self.assertEqual('apple', self.arr[0])
        self.assertEqual(-5, self.arr[3])

    def test_array_in_operator(self):
        """Test functionality of the in operator for the array"""
        # Add values to end of array
        self.arr.append('apple')
        self.arr.append(20)

        # Test that values were added to the array
        self.assertIn('apple', self.arr)
        self.assertIn(20, self.arr)

    def test_array_concatenation(self):
        """Test that array supports concatenation"""
        # Create a new array with 20 new values following the pattern of self._arr
        arr = DynamicArray(self._GROWTH_FACTOR)
        for i in range(self._INITIAL_SIZE, self._INITIAL_SIZE + 20):
            arr.append(i)

        # Add the new array to the end of self.arr and test the concatenation
        concat_arr = self.arr + arr
        self.assertEqual([i for i in range(self._INITIAL_SIZE + 20)], concat_arr)

    def test_array_multiplication(self):
        """Test that array supports multiplication"""
        # Compare self.arr multiplication to python list multiplication
        self.arr *= 5
        self.assertEqual([i for i in range(self._INITIAL_SIZE)] * 5, self.arr)

    def test_array_deletion(self):
        """Test that array deletes item with syntax del arr[idx]"""
        # Delete element at end and two elements at the beginning
        del self.arr[self._INITIAL_SIZE - 1]
        del self.arr[0]
        del self.arr[0]

        # Make sure the new array is missing all three elements
        self.assertEqual([i for i in range(2, self._INITIAL_SIZE - 1)], self.arr)

    def test_array_slicing(self):
        """Test slicing notation support for the array"""
        # Create a python list matching the values in self.arr
        py_list = [i for i in range(self._INITIAL_SIZE)]

        self.assertEqual(py_list[0:2], self.arr[0:2])  # Slice with start and stop
        self.assertEqual(py_list[:2], self.arr[:2])  # Slice with only stop
        self.assertEqual(py_list[2:], self.arr[2:])  # Slice with only start
        self.assertEqual(py_list[:], self.arr[:])  # Slice without start or stop
        self.assertEqual(py_list[-3:-1], self.arr[-3:-1])  # Slice with negative start and stop
        self.assertEqual(py_list[::-1], self.arr[::-1])  # Slice with negative step
        self.assertEqual(py_list[::-3], self.arr[::-3])  # Slice with negative step >1

    def test_array_default_bool(self):
        """Test if array's default boolean value is False if no items or True otherwise"""
        self.assertTrue(self.arr)  # Array should be True if there are elements in it
        self.assertFalse(DynamicArray())  # An empty array should be False

    def time_array_appends(self, num_elements):
        """Returns average time in seconds of num_elements appends"""
        arr = DynamicArray(self._GROWTH_FACTOR)  # Create new array

        start_time = time()  # Begin timing the operations
        for i in range(num_elements):
            arr.append(i)
        end_time = time()  # Stop timing the operations

        # Return arr so it can be used for other testing the time of deletion
        # without needing to recreate each array (since this takes time).
        # Also return the average time per operation
        return arr, (end_time - start_time) / num_elements

    @staticmethod
    def time_array_deletions(arr):
        """Returns average time in seconds of deleting all elements in arr"""
        start_time = time()  # Begin timing the operations
        length = len(arr)  # Save starting length
        for i in range(length):  # Remove all elements from array one at a time
            arr.pop()
        end_time = time()  # Stop timing the operations
        return (end_time - start_time) / length  # Average time per operation

    def test_insert_and_delete_performance(self):
        """Test amortized runtime by comparing 10, 1000, and 1000000 operations"""
        # Test insertion runtime
        small_arr, avg_small_ins = self.time_array_appends(10)  # 10 appends
        medium_arr, avg_medium_ins = self.time_array_appends(1000)  # 1,000 appends
        large_arr, avg_large_ins = self.time_array_appends(1000000)  # 1,000,000 appends

        # Test that all average append times are within 0.05 (meaning the amortized
        # runtime for append is constant)
        self.assertAlmostEqual(avg_small_ins, avg_medium_ins, delta=0.05)
        self.assertAlmostEqual(avg_small_ins, avg_large_ins, delta=0.05)
        self.assertAlmostEqual(avg_medium_ins, avg_large_ins, delta=0.05)

        # Test deletion runtime
        avg_small_del = self.time_array_deletions(small_arr)  # 10 deletions
        avg_medium_del = self.time_array_deletions(medium_arr)  # 1,000 deletions
        avg_large_del = self.time_array_deletions(large_arr)  # 1,000,000 deletions

        # Test that all average deletion times are within 0.05 (meaning the amortized
        # runtime for deleting an element is constant)
        self.assertAlmostEqual(avg_small_del, avg_medium_del, delta=0.05)
        self.assertAlmostEqual(avg_small_del, avg_large_del, delta=0.05)
        self.assertAlmostEqual(avg_medium_del, avg_large_del, delta=0.05)

        # Test that the size of the array actually changes
        # It seems to be bad practice to rely on protected data for testing, but
        # it needs to be specifically tested whether or not the true size of the
        # underlying array is actually shrinking when these deletion operations
        # are executed.
        self.assertEqual(self._GROWTH_FACTOR, len(small_arr._arr))
        self.assertEqual(self._GROWTH_FACTOR, len(medium_arr._arr))
        self.assertEqual(self._GROWTH_FACTOR, len(large_arr._arr))


# Run tests when executed directly
if __name__ == '__main__':
    unittest.main()
