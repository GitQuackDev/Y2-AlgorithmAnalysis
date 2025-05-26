"""
Simple script to view and summarize analysis results
"""

import json
import os
import glob

# Dynamically find the latest results JSON file
results_dir = os.path.join(os.path.dirname(__file__), '../results/performance_data')
json_files = glob.glob(os.path.join(results_dir, 'performance_results_*.json'))
if not json_files:
    raise FileNotFoundError('No performance results JSON files found in results/performance_data/')
results_file = max(json_files, key=os.path.getmtime)

with open(results_file, 'r') as f:
    results = json.load(f)

print("🔍 ANALYSIS RESULTS SUMMARY")
print("=" * 50)

print(f"Algorithms tested: {', '.join(results['algorithms'])}")
print(f"Data types: {', '.join(results['data_types'])}")
print(f"Data sizes: {results['data_sizes']}")
print(f"Analysis date: {results['metadata']['timestamp']}")
print()

# Find best performers for each scenario
print("🏆 BEST PERFORMERS:")
print("-" * 30)

for data_type in results['data_types']:
    print(f"\n{data_type.replace('_', ' ').title()} Data:")
    
    for size in results['data_sizes']:
        best_algo = None
        best_time = float('inf')
        
        for algo_name in results['algorithms']:
            mean_time = results['results'][algo_name][data_type][str(size)]['statistics']['mean']
            if mean_time < best_time:
                best_time = mean_time
                best_algo = algo_name
        
        print(f"  {size//1000}K: {best_algo} ({best_time:.6f}s)")

print(f"\n✅ Analysis completed successfully!")
print(f"📊 View graphs in: src/results/graphs/")
print(f"📁 Full data in: {results_file}")
