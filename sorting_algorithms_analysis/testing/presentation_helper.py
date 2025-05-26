"""
Presentation Helper Script
Generates talking points and key statistics for video presentation
"""

import json
import os

def load_results():
    """Load the analysis results"""
    # Find the most recent results file
    results_dir = os.path.join(os.path.dirname(__file__), '../results/performance_data')
    files = [f for f in os.listdir(results_dir) if f.startswith("performance_results_") and f.endswith(".json")]
    if not files:
        raise FileNotFoundError("No results files found")
    
    latest_file = max(files)
    results_file = os.path.join(results_dir, latest_file)
    
    with open(results_file, 'r') as f:
        return json.load(f)

def format_time(seconds):
    """Format time for presentation"""
    if seconds < 0.001:
        return f"{seconds * 1000000:.1f} microseconds"
    elif seconds < 1:
        return f"{seconds * 1000:.1f} milliseconds"
    else:
        return f"{seconds:.3f} seconds"

def generate_presentation_notes():
    """Generate talking points for presentation"""
    results = load_results()
    
    print("🎬 PRESENTATION TALKING POINTS")
    print("=" * 50)
    
    print("\n📖 SLIDE 1: Introduction")
    print("• Today I'll present our analysis of 3 sorting algorithms")
    print("• Quick Sort, Merge Sort, and Heap Sort")
    print("• Tested on 4 data types with 3 different sizes")
    print("• Total of 36 performance tests")
    
    print("\n📖 SLIDE 2: Methodology")
    print("• Data sizes: 1K, 10K, and 100K elements")
    print("• Data types: Random, Sorted, Reversed, Nearly Sorted")
    print("• Each test run 5 times for accuracy")
    print("• Measured execution time in seconds")
    
    print("\n📖 SLIDE 3: Algorithm Implementations")
    print("• Quick Sort: Iterative with randomized pivot (avoids worst case)")
    print("• Merge Sort: Recursive divide-and-conquer (stable performance)")
    print("• Heap Sort: Binary heap with in-place sorting (space efficient)")
    
    print("\n📖 SLIDE 4: Key Results")
    
    # Find overall best performer
    total_times = {}
    for algo in results['algorithms']:
        total_times[algo] = 0
        count = 0
        for data_type in results['data_types']:
            for size in results['data_sizes']:
                total_times[algo] += results['results'][algo][data_type][str(size)]['statistics']['mean']
                count += 1
        total_times[algo] /= count
    
    best_overall = min(total_times.keys(), key=lambda k: total_times[k])
    print(f"• Overall best performer: {best_overall}")
    
    # Performance by data type
    for data_type in results['data_types']:
        best_for_type = None
        best_time = float('inf')
        
        for algo in results['algorithms']:
            avg_time = sum(results['results'][algo][data_type][str(size)]['statistics']['mean'] 
                          for size in results['data_sizes']) / len(results['data_sizes'])
            if avg_time < best_time:
                best_time = avg_time
                best_for_type = algo
        
        print(f"• Best for {data_type} data: {best_for_type}")
    
    print("\n📖 SLIDE 5: Specific Examples")
    
    # Get some specific numbers
    size_100k = 100000
    random_data = 'random'
    
    print(f"• For {size_100k//1000}K random elements:")
    for algo in results['algorithms']:
        time_val = results['results'][algo][random_data][str(size_100k)]['statistics']['mean']
        print(f"  - {algo}: {format_time(time_val)}")
    
    print("\n📖 SLIDE 6: Scalability")
    print("• All algorithms show expected O(n log n) growth")
    print("• Merge Sort most consistent across data sizes")
    print("• Quick Sort benefits significantly from randomization")
    print("• Heap Sort maintains steady performance")
    
    print("\n📖 SLIDE 7: Conclusions")
    print("• Merge Sort: Most reliable, best for general use")
    print("• Quick Sort: Good average performance, space efficient")
    print("• Heap Sort: Consistent with minimal memory usage")
    print("• Choice depends on specific requirements")
    
    print("\n📖 SLIDE 8: Questions")
    print("• What questions do you have about the analysis?")
    print("• Would you like to see any specific comparisons?")
    print("• Are there other algorithms you'd like me to test?")

def generate_quick_stats():
    """Generate quick statistics for reference"""
    results = load_results()
    
    print("\n🔢 QUICK REFERENCE STATISTICS")
    print("=" * 40)
    
    # Fastest and slowest overall
    all_times = []
    for algo in results['algorithms']:
        for data_type in results['data_types']:
            for size in results['data_sizes']:
                time_val = results['results'][algo][data_type][str(size)]['statistics']['mean']
                all_times.append((algo, data_type, size, time_val))
    
    fastest = min(all_times, key=lambda x: x[3])
    slowest = max(all_times, key=lambda x: x[3])
    
    print(f"⚡ Fastest: {fastest[0]} on {fastest[1]} data ({fastest[2]//1000}K) - {format_time(fastest[3])}")
    print(f"🐌 Slowest: {slowest[0]} on {slowest[1]} data ({slowest[2]//1000}K) - {format_time(slowest[3])}")
    
    # Speed improvement
    improvement_ratio = slowest[3] / fastest[3]
    print(f"📈 Speed difference: {improvement_ratio:.1f}x faster")

def main():
    """Main function"""
    print("🎥 PRESENTATION PREPARATION TOOL")
    print("For 2-3 minute video presentation")
    print()
    
    try:
        generate_presentation_notes()
        generate_quick_stats()
        
        print("\n📋 PRESENTATION CHECKLIST:")
        print("□ Show algorithm comparison graphs")
        print("□ Explain methodology briefly") 
        print("□ Highlight key findings")
        print("□ Demonstrate one algorithm working")
        print("□ Conclude with recommendations")
        print("□ Time: 2-3 minutes")
        
        print("\n📁 Graphs available in: results/graphs/")
        print("📊 Use the performance heatmap and scalability analysis!")
        
    except FileNotFoundError:
        print("❌ Results file not found. Run main.py first!")

if __name__ == "__main__":
    main()
