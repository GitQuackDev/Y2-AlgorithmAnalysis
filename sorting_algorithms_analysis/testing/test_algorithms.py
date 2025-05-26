"""
Quick test script to verify the sorting algorithms work correctly
"""

import sys
import os

# Add project root to sys.path for correct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.algorithms.sorting_algorithms import QuickSort, MergeSort, HeapSort
from src.utils.helpers import is_sorted

def test_algorithm(algorithm, test_data):
    """Test a single algorithm"""
    print(f"Testing {algorithm.name}...")
    
    for i, data in enumerate(test_data):
        original_length = len(data)
        sorted_data = algorithm.sort(data)
        
        # Check if sorted correctly
        if not is_sorted(sorted_data):
            print(f"  ❌ Test {i+1} FAILED: Data not sorted correctly")
            return False
        
        # Check if length is preserved
        if len(sorted_data) != original_length:
            print(f"  ❌ Test {i+1} FAILED: Length changed")
            return False
        
        print(f"  ✅ Test {i+1} passed")
    
    return True

def main():
    """Run quick tests"""
    print("🧪 Running Quick Tests for Sorting Algorithms")
    print("=" * 50)
    
    # Test data
    test_data = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 4, 6, 1, 3],
        [1],
        [],
        [3, 3, 3, 3],
        list(range(100, 0, -1)),  # Reverse sorted
        list(range(100))  # Already sorted
    ]
    
    algorithms = [QuickSort(), MergeSort(), HeapSort()]
    
    all_passed = True
    for algorithm in algorithms:
        if not test_algorithm(algorithm, test_data):
            all_passed = False
        print()
    
    if all_passed:
        print("🎉 All tests passed! Algorithms are working correctly.")
    else:
        print("❌ Some tests failed. Check the implementations.")

if __name__ == "__main__":
    main()
