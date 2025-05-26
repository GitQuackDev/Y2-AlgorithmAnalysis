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

def format_time(seconds):
    if seconds < 0.001:
        return f"{seconds * 1000000:.1f} μs"
    elif seconds < 1:
        return f"{seconds * 1000:.1f} ms"
    else:
        return f"{seconds:.3f} s"

print("🎬 SORTING ALGORITHMS ANALYSIS - PRESENTATION NOTES")
print("=" * 60)

print("\n📊 OVERVIEW:")
print("• 3 Algorithms: Quick Sort, Merge Sort, Heap Sort")
print("• 4 Data Types: Random, Sorted, Reversed, Nearly Sorted")
print("• 3 Data Sizes: 1K, 10K, 100K elements")
print("• 36 total tests (5 trials each)")

print("\n⚡ KEY FINDINGS - 100K ELEMENTS:")
for data_type in results['data_types']:
    print(f"\n{data_type.upper()} DATA:")
    for algo in results['algorithms']:
        time_val = results['results'][algo][data_type]['100000']['statistics']['mean']
        print(f"  {algo}: {format_time(time_val)}")

# Find best performer overall
print("\n🏆 BEST PERFORMERS:")
for data_type in results['data_types']:
    best_algo = None
    best_time = float('inf')
    
    for algo in results['algorithms']:
        time_val = results['results'][algo][data_type]['100000']['statistics']['mean']
        if time_val < best_time:
            best_time = time_val
            best_algo = algo
    
    print(f"• {data_type.title()}: {best_algo} ({format_time(best_time)})")

print("\n📈 SCALABILITY (Random Data):")
for size in [1000, 10000, 100000]:
    print(f"\n{size//1000}K Elements:")
    for algo in results['algorithms']:
        time_val = results['results'][algo]['random'][str(size)]['statistics']['mean']
        print(f"  {algo}: {format_time(time_val)}")

print("\n🎯 RECOMMENDATIONS:")
print("• Merge Sort: Most consistent, best for critical applications")
print("• Quick Sort: Good general purpose, space efficient")
print("• Heap Sort: Reliable worst-case performance")

print("\n📋 PRESENTATION STRUCTURE (2-3 minutes):")
print("1. Introduction (30s): Problem statement and approach")
print("2. Methodology (30s): Show test setup and data types") 
print("3. Results (60s): Key findings with graphs")
print("4. Conclusions (30s): Recommendations and takeaways")

print(f"\n📁 Generated graphs available in: results/graphs/")
print("📊 Key graphs to show:")
print("• performance_heatmap.png - Overall comparison")
print("• scalability_analysis.png - Growth patterns") 
print("• runtime_comparison_random.png - Random data performance")
