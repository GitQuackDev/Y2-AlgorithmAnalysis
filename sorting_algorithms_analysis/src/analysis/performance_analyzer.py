
import json
import time
import os
from typing import Dict, List, Any
from ..utils.config import Config
from ..utils.helpers import time_function, is_sorted, calculate_statistics

class PerformanceAnalyzer:
    
    def __init__(self):
        self.config = Config()
        self.config.ensure_directories()
    
    def measure_algorithm_performance(self, algorithm, data: List[int], num_trials: int = None) -> Dict[str, Any]:
        if num_trials is None:
            num_trials = self.config.NUM_TRIALS
        
        execution_times = []
        
        for trial in range(num_trials):
            
            data_copy = data.copy()
            
            
            sorted_data, exec_time = time_function(algorithm.sort, data_copy)
            
            
            if not is_sorted(sorted_data):
                raise ValueError(f"{algorithm.name} failed to sort data correctly!")
            
            execution_times.append(exec_time)
        
        
        stats = calculate_statistics(execution_times)
        
        return {
            'algorithm': algorithm.name,
            'data_size': len(data),
            'execution_times': execution_times,
            'statistics': stats,
            'time_complexities': {
                'best': algorithm.time_complexity_best,
                'average': algorithm.time_complexity_average,
                'worst': algorithm.time_complexity_worst
            },
            'space_complexity': algorithm.space_complexity
        }
    
    def analyze_algorithms(self, algorithms: Dict[str, Any], datasets: Dict[str, Dict[int, List[int]]]) -> Dict[str, Any]:
        results = {
            'algorithms': list(algorithms.keys()),
            'data_types': list(datasets.keys()),
            'data_sizes': self.config.DATA_SIZES,
            'results': {}
        }
        
        total_tests = len(algorithms) * len(datasets) * len(self.config.DATA_SIZES)
        current_test = 0
        
        for algo_name, algorithm in algorithms.items():
            print(f"\n🔍 Testing {algo_name}...")
            results['results'][algo_name] = {}
            
            for data_type, size_data in datasets.items():
                results['results'][algo_name][data_type] = {}
                
                for size, data in size_data.items():
                    current_test += 1
                    progress = (current_test / total_tests) * 100
                    
                    print(f"   [{progress:5.1f}%] {data_type} data, size {size:,}")
                    
                    
                    performance = self.measure_algorithm_performance(algorithm, data)
                    results['results'][algo_name][data_type][size] = performance
        
        
        results['metadata'] = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'num_trials_per_test': self.config.NUM_TRIALS,
            'total_tests_run': total_tests
        }
        
        return results
    
    def save_results(self, results: Dict[str, Any], filename: str = None) -> str:
        if filename is None:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"performance_results_{timestamp}.json"
        
        filepath = os.path.join(self.config.PERFORMANCE_DATA_DIR, filename)
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to: {filepath}")
        return filepath
    
    def load_results(self, filepath: str) -> Dict[str, Any]:
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def print_summary(self, results: Dict[str, Any]) -> None:
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE ANALYSIS SUMMARY")
        print("=" * 60)
        
        algorithms = results['algorithms']
        data_types = results['data_types']
        data_sizes = results['data_sizes']
        
        print(f"Algorithms tested: {', '.join(algorithms)}")
        print(f"Data types: {', '.join(data_types)}")
        print(f"Data sizes: {', '.join(map(str, data_sizes))}")
        print(f"Total tests: {results['metadata']['total_tests_run']}")
        print(f"Trials per test: {results['metadata']['num_trials_per_test']}")
        
        print(f"\nAnalysis completed: {results['metadata']['timestamp']}")
        
        
        print("\n🏆 BEST PERFORMING ALGORITHMS:")
        print("-" * 40)
        
        for data_type in data_types:
            print(f"\n{data_type.upper()} DATA:")
            
            for size in data_sizes:
                best_algo = None
                best_time = float('inf')
                
                for algo_name in algorithms:
                    mean_time = results['results'][algo_name][data_type][size]['statistics']['mean']
                    if mean_time < best_time:
                        best_time = mean_time
                        best_algo = algo_name
                
                from ..utils.helpers import format_time
                print(f"  Size {size:,}: {best_algo} ({format_time(best_time)})")
        
        print("\n" + "=" * 60)
