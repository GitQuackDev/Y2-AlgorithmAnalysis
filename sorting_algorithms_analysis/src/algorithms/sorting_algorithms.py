
from typing import List
from abc import ABC, abstractmethod

class SortingAlgorithm(ABC):
    
    @abstractmethod
    def sort(self, arr: List[int]) -> List[int]:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def time_complexity_best(self) -> str:
        pass
    
    @property
    @abstractmethod
    def time_complexity_average(self) -> str:
        pass
    
    @property
    @abstractmethod
    def time_complexity_worst(self) -> str:
        pass
    
    @property
    @abstractmethod
    def space_complexity(self) -> str:
        pass

class QuickSort(SortingAlgorithm):
    
    def sort(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr.copy()
        
        
        arr_copy = arr.copy()
        self._quick_sort(arr_copy, 0, len(arr_copy) - 1)
        return arr_copy
    
    def _quick_sort(self, arr: List[int], low: int, high: int) -> None:
        
        stack = [(low, high)]
        
        while stack:
            low, high = stack.pop()
            
            if low < high:
                
                pivot_index = self._partition(arr, low, high)
                
                
                left_size = pivot_index - low
                right_size = high - pivot_index
                
                if left_size <= right_size:
                    stack.append((pivot_index + 1, high))
                    stack.append((low, pivot_index - 1))
                else:
                    stack.append((low, pivot_index - 1))
                    stack.append((pivot_index + 1, high))
    
    def _partition(self, arr: List[int], low: int, high: int) -> int:
        import random
        
        
        random_index = random.randint(low, high)
        arr[random_index], arr[high] = arr[high], arr[random_index]
        
        
        pivot = arr[high]
        
        
        i = low - 1
        
        for j in range(low, high):
            
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        
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
    
    def sort(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr.copy()
        
        
        arr_copy = arr.copy()
        return self._merge_sort(arr_copy)
    
    def _merge_sort(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr
        
        
        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid])
        right = self._merge_sort(arr[mid:])
        
        
        return self._merge(left, right)
    
    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        result = []
        i = j = 0
        
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        
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
    
    def sort(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr.copy()
        
        
        arr_copy = arr.copy()
        self._heap_sort(arr_copy)
        return arr_copy
    
    def _heap_sort(self, arr: List[int]) -> None:
        n = len(arr)
        
        
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i)
        
        
        for i in range(n - 1, 0, -1):
            
            arr[0], arr[i] = arr[i], arr[0]
            
            
            self._heapify(arr, i, 0)
    
    def _heapify(self, arr: List[int], n: int, i: int) -> None:
        largest = i  
        left = 2 * i + 1     
        right = 2 * i + 2    
        
        
        if left < n and arr[left] > arr[largest]:
            largest = left
        
        
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            
            
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
