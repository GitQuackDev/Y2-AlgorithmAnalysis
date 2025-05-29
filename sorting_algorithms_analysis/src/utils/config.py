
import os

class Config:
      
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    RESULTS_DIR = os.path.join(BASE_DIR, 'results')
    GRAPHS_DIR = os.path.join(RESULTS_DIR, 'graphs')
    PERFORMANCE_DATA_DIR = os.path.join(RESULTS_DIR, 'performance_data')
    REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
    
    
    DATA_SIZES = [1000, 10000, 100000]  
    DATA_TYPES = ['random', 'sorted', 'reversed', 'nearly_sorted']
    
    
    NUM_TRIALS = 5  
    
    
    NEARLY_SORTED_DISORDER_PERCENTAGE = 0.1  
    
    
    FIGURE_SIZE = (12, 8)
    DPI = 300
    
    @classmethod
    def ensure_directories(cls):
        directories = [
            cls.DATA_DIR,
            cls.RESULTS_DIR,
            cls.GRAPHS_DIR,
            cls.PERFORMANCE_DATA_DIR,
            cls.REPORTS_DIR
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
