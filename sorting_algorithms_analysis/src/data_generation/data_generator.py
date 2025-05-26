"""
Data generation utilities for testing sorting algorithms
"""

import random
import math
from typing import List, Dict
from ..utils.config import Config

class DataGenerator:
    """Class for generating different types of test data"""
    
    def __init__(self):
        self.config = Config()
    
    def generate_random_data(self, size: int) -> List[int]:
        """Generate completely random data"""
        return [random.randint(0, size * 10) for _ in range(size)]
    
    def generate_sorted_data(self, size: int) -> List[int]:
        """Generate already sorted data"""
        return list(range(size))
    
    def generate_reversed_data(self, size: int) -> List[int]:
        """Generate reverse-sorted data"""
        return list(range(size, 0, -1))
    
    def generate_nearly_sorted_data(self, size: int) -> List[int]:
        """
        Generate nearly sorted data with some elements out of place
        """
        # Start with sorted data
        data = list(range(size))
        
        # Calculate number of swaps based on disorder percentage
        num_swaps = int(size * self.config.NEARLY_SORTED_DISORDER_PERCENTAGE)
        
        # Perform random swaps
        for _ in range(num_swaps):
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            data[i], data[j] = data[j], data[i]
        
        return data
    
    def generate_dataset(self, data_type: str, size: int) -> List[int]:
        """
        Generate a dataset of specified type and size
        
        Args:
            data_type: Type of data ('random', 'sorted', 'reversed', 'nearly_sorted')
            size: Size of the dataset
        
        Returns:
            List[int]: Generated dataset
        """
        generators = {
            'random': self.generate_random_data,
            'sorted': self.generate_sorted_data,
            'reversed': self.generate_reversed_data,
            'nearly_sorted': self.generate_nearly_sorted_data
        }
        
        if data_type not in generators:
            raise ValueError(f"Unknown data type: {data_type}")
        
        return generators[data_type](size)
    
    def generate_all_datasets(self) -> Dict[str, Dict[int, List[int]]]:
        """
        Generate all combinations of data types and sizes
        
        Returns:
            Dict: Nested dictionary with structure {data_type: {size: data}}
        """
        datasets = {}
        
        for data_type in self.config.DATA_TYPES:
            datasets[data_type] = {}
            for size in self.config.DATA_SIZES:
                print(f"  Generating {data_type} data of size {size:,}")
                datasets[data_type][size] = self.generate_dataset(data_type, size)
        
        return datasets
    
    def save_datasets(self, datasets: Dict[str, Dict[int, List[int]]]) -> None:
        """
        Save generated datasets to files for later use
        
        Args:
            datasets: Dictionary of datasets to save
        """
        import json
        import os
        
        # Ensure data directory exists
        self.config.ensure_directories()
        
        for data_type, size_data in datasets.items():
            for size, data in size_data.items():
                filename = f"{data_type}_{size}.json"
                filepath = os.path.join(self.config.DATA_DIR, filename)
                
                with open(filepath, 'w') as f:
                    json.dump(data, f)
                
                print(f"Saved {data_type} data (size {size}) to {filename}")
    
    def load_datasets(self) -> Dict[str, Dict[int, List[int]]]:
        """
        Load previously saved datasets from files
        
        Returns:
            Dict: Loaded datasets
        """
        import json
        import os
        
        datasets = {}
        
        for data_type in self.config.DATA_TYPES:
            datasets[data_type] = {}
            for size in self.config.DATA_SIZES:
                filename = f"{data_type}_{size}.json"
                filepath = os.path.join(self.config.DATA_DIR, filename)
                
                if os.path.exists(filepath):
                    with open(filepath, 'r') as f:
                        datasets[data_type][size] = json.load(f)
                else:
                    print(f"Warning: {filename} not found, generating new data")
                    datasets[data_type][size] = self.generate_dataset(data_type, size)
        
        return datasets
