"""
Sorting algorithms implementations for comparative analysis
"""

from typing import List
from abc import ABC, abstractmethod

class SortingAlgorithm(ABC):
    """Abstract base class for sorting algorithms"""
    
    @abstractmethod
    def sort(self, arr: List[int]) -> List[int]:
        """Sort the given array and return the sorted result"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the sorting algorithm"""
        pass
    
    @property
    @abstractmethod
    def time_complexity_best(self) -> str:
        """Best case time complexity"""
        pass
    
    @property
    @abstractmethod
    def time_complexity_average(self) -> str:
        """Average case time complexity"""
        pass
    
    @property
    @abstractmethod
    def time_complexity_worst(self) -> str:
        """Worst case time complexity"""
        pass
    
    @property
    @abstractmethod
    def space_complexity(self) -> str:
        """Space complexity"""
        pass

class QuickSort(SortingAlgorithm):
    """Quick Sort implementation"""
    
    def sort(self, arr: List[int]) -> List[int]:
        """Sort array using Quick Sort algorithm"""
        if len(arr) <= 1:
            return arr.copy()
        
        # Make a copy to avoid modifying the original
        arr_copy = arr.copy()
        self._quick_sort(arr_copy, 0, len(arr_copy) - 1)
        return arr_copy
    
    def _quick_sort(self, arr: List[int], low: int, high: int) -> None:
        """Iterative Quick Sort helper function to avoid recursion limit"""
        # Use iterative approach to avoid stack overflow
        stack = [(low, high)]
        
        while stack:
            low, high = stack.pop()
            
            if low < high:
                # Partition the array and get pivot index
                pivot_index = self._partition(arr, low, high)
                
                # Add subarrays to stack (smaller subarray first for optimization)
                left_size = pivot_index - low
                right_size = high - pivot_index
                
                if left_size <= right_size:
                    stack.append((pivot_index + 1, high))
                    stack.append((low, pivot_index - 1))
                else:
                    stack.append((low, pivot_index - 1))
                    stack.append((pivot_index + 1, high))
    
    def _partition(self, arr: List[int], low: int, high: int) -> int:
        """Partition function for Quick Sort with random pivot selection"""
        import random
        
        # Choose a random pivot to avoid worst-case scenario
        random_index = random.randint(low, high)
        arr[random_index], arr[high] = arr[high], arr[random_index]
        
        # Choose the rightmost element as pivot (now randomized)
        pivot = arr[high]
        
        # Index of smaller element
        i = low - 1
        
        for j in range(low, high):
            # If current element is smaller than or equal to pivot
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        # Place pivot in correct position
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    @property
    def name(self) -> str:
        return "Quick Sort"
    
    @property
    def time_complexity_best(self) -> str:
        return "O(n log n)"
    
    @property
    def time_complexity_average(self) -> str:
        return "O(n log n)"
    
    @property
    def time_complexity_worst(self) -> str:
        return "O(n²)"
    
    @property
    def space_complexity(self) -> str:
        return "O(log n)"

class MergeSort(SortingAlgorithm):
    """Merge Sort implementation"""
    
    def sort(self, arr: List[int]) -> List[int]:
        """Sort array using Merge Sort algorithm"""
        if len(arr) <= 1:
            return arr.copy()
        
        # Make a copy to avoid modifying the original
        arr_copy = arr.copy()
        return self._merge_sort(arr_copy)
    
    def _merge_sort(self, arr: List[int]) -> List[int]:
        """Recursive Merge Sort function"""
        if len(arr) <= 1:
            return arr
        
        # Divide the array into two halves
        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid])
        right = self._merge_sort(arr[mid:])
        
        # Merge the sorted halves
        return self._merge(left, right)
    
    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        """Merge two sorted arrays"""
        result = []
        i = j = 0
        
        # Compare elements from both arrays and merge
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # Add remaining elements
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result
    
    @property
    def name(self) -> str:
        return "Merge Sort"
    
    @property
    def time_complexity_best(self) -> str:
        return "O(n log n)"
    
    @property
    def time_complexity_average(self) -> str:
        return "O(n log n)"
    
    @property
    def time_complexity_worst(self) -> str:
        return "O(n log n)"
    
    @property
    def space_complexity(self) -> str:
        return "O(n)"

class HeapSort(SortingAlgorithm):
    """Heap Sort implementation"""
    
    def sort(self, arr: List[int]) -> List[int]:
        """Sort array using Heap Sort algorithm"""
        if len(arr) <= 1:
            return arr.copy()
        
        # Make a copy to avoid modifying the original
        arr_copy = arr.copy()
        self._heap_sort(arr_copy)
        return arr_copy
    
    def _heap_sort(self, arr: List[int]) -> None:
        """Heap Sort main function"""
        n = len(arr)
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i)
        
        # Extract elements from heap one by one
        for i in range(n - 1, 0, -1):
            # Move current root to end
            arr[0], arr[i] = arr[i], arr[0]
            
            # Call heapify on the reduced heap
            self._heapify(arr, i, 0)
    
    def _heapify(self, arr: List[int], n: int, i: int) -> None:
        """Heapify a subtree rooted at index i"""
        largest = i  # Initialize largest as root
        left = 2 * i + 1     # Left child
        right = 2 * i + 2    # Right child
        
        # Check if left child exists and is greater than root
        if left < n and arr[left] > arr[largest]:
            largest = left
        
        # Check if right child exists and is greater than largest so far
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        # Change root if needed
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            
            # Recursively heapify the affected sub-tree
            self._heapify(arr, n, largest)
    
    @property
    def name(self) -> str:
        return "Heap Sort"
    
    @property
    def time_complexity_best(self) -> str:
        return "O(n log n)"
    
    @property
    def time_complexity_average(self) -> str:
        return "O(n log n)"
    
    @property
    def time_complexity_worst(self) -> str:
        return "O(n log n)"
    
    @property
    def space_complexity(self) -> str:
        return "O(1)"
