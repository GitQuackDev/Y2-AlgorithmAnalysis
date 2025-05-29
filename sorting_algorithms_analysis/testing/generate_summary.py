
import sys
import os
import json


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.config import Config
from src.utils.helpers import format_time

def load_latest_results():
    config = Config()
    results_dir = config.PERFORMANCE_DATA_DIR
    
    
    json_files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
    if not json_files:
        print("No results files found!")
        return None
    
    latest_file = max(json_files)
    filepath = os.path.join(results_dir, latest_file)
    
    with open(filepath, 'r') as f:
        return json.load(f)

def print_performance_summary(results):
    print("🔍 DETAILED PERFORMANCE ANALYSIS SUMMARY")
    print("=" * 60)
    
    algorithms = results['algorithms']
    data_types = results['data_types']
    data_sizes = results['data_sizes']
    
    print(f"📊 Analysis Overview:")
    print(f"   • Algorithms: {', '.join(algorithms)}")
    print(f"   • Data Types: {', '.join(data_types)}")
    print(f"   • Data Sizes: {', '.join([f'{s//1000}K' for s in data_sizes])}")
    print(f"   • Tests Run: {results['metadata']['total_tests_run']}")
    print(f"   • Trials per Test: {results['metadata']['num_trials_per_test']}")
    print(f"   • Analysis Date: {results['metadata']['timestamp']}")
    print()
    
    
    for data_type in data_types:
        print(f"📈 {data_type.upper().replace('_', ' ')} DATA PERFORMANCE:")
        print("-" * 50)
        
        for size in data_sizes:
            print(f"\n  📏 Size {size//1000}K elements:")
            
            
            perf_data = []
            for algo_name in algorithms:
                stats = results['results'][algo_name][data_type][str(size)]['statistics']
                perf_data.append((algo_name, stats['mean'], stats['std_dev']))
            
            
            perf_data.sort(key=lambda x: x[1])
            
            for rank, (algo_name, mean_time, std_dev) in enumerate(perf_data, 1):
                print(f"     {rank}. {algo_name:12} | {format_time(mean_time):>10} (±{format_time(std_dev)})")
        
        print()
    
    
    print("🏆 CHAMPION ALGORITHMS BY SCENARIO:")
    print("-" * 50)
    
    for data_type in data_types:
        print(f"\n  {data_type.replace('_', ' ').title()} Data:")
        
        for size in data_sizes:
            best_algo = None
            best_time = float('inf')
            
            for algo_name in algorithms:
                mean_time = results['results'][algo_name][data_type][str(size)]['statistics']['mean']
                if mean_time < best_time:
                    best_time = mean_time
                    best_algo = algo_name
            
            improvement = ""
            if best_algo:
                
                times = []
                for algo_name in algorithms:
                    if algo_name != best_algo:
                        time_val = results['results'][algo_name][data_type][str(size)]['statistics']['mean']
                        times.append(time_val)
                
                if times:
                    second_best = min(times)
                    improvement_pct = ((second_best - best_time) / best_time) * 100
                    improvement = f" (🚀 {improvement_pct:.1f}% faster)"
            
            print(f"     {size//1000}K: {best_algo} - {format_time(best_time)}{improvement}")
    
    print("\n" + "=" * 60)
    print("✅ Summary generation completed!")

def generate_csv_export(results):
    import csv
    
    config = Config()
    csv_path = os.path.join(config.PERFORMANCE_DATA_DIR, "performance_summary.csv")
    
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        
        writer.writerow(['Algorithm', 'Data_Type', 'Data_Size', 'Mean_Time_Sec', 'Std_Dev_Sec', 'Min_Time_Sec', 'Max_Time_Sec'])
        
        
        for algo_name in results['algorithms']:
            for data_type in results['data_types']:
                for size in results['data_sizes']:
                    stats = results['results'][algo_name][data_type][str(size)]['statistics']
                    writer.writerow([
                        algo_name,
                        data_type,
                        size,
                        stats['mean'],
                        stats['std_dev'],
                        stats['min'],
                        stats['max']
                    ])
    
    print(f"📁 CSV export saved to: {csv_path}")

def main():
    print("Loading latest analysis results...")
    results = load_latest_results()
    
    if results is None:
        return
    
    print_performance_summary(results)
    generate_csv_export(results)

if __name__ == "__main__":
    main()
