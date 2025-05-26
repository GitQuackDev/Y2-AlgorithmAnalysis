"""
Configuration settings for the sorting algorithms analysis
"""

import os

class Config:
    """Configuration class with project settings"""
      # Project paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    RESULTS_DIR = os.path.join(BASE_DIR, 'results')
    GRAPHS_DIR = os.path.join(RESULTS_DIR, 'graphs')
    PERFORMANCE_DATA_DIR = os.path.join(RESULTS_DIR, 'performance_data')
    REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
    
    # Test parameters
    DATA_SIZES = [1000, 10000, 100000]  # 1K, 10K, 100K
    DATA_TYPES = ['random', 'sorted', 'reversed', 'nearly_sorted']
    
    # Performance testing
    NUM_TRIALS = 5  # Number of trials to average for each test
    
    # Nearly sorted parameters
    NEARLY_SORTED_DISORDER_PERCENTAGE = 0.1  # 10% of elements out of place
    
    # Visualization settings
    FIGURE_SIZE = (12, 8)
    DPI = 300
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.DATA_DIR,
            cls.RESULTS_DIR,
            cls.GRAPHS_DIR,
            cls.PERFORMANCE_DATA_DIR,
            cls.REPORTS_DIR
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
