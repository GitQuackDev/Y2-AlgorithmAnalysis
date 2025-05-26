"""
Main execution script for Sorting Algorithms Comparative Analysis
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_generation.data_generator import DataGenerator
from src.algorithms.sorting_algorithms import QuickSort, MergeSort, HeapSort
from src.analysis.performance_analyzer import PerformanceAnalyzer
from src.analysis.visualizer import Visualizer
from src.utils.config import Config

def main():
    """Main function to run the sorting algorithms analysis"""
    print("🔍 Starting Sorting Algorithms Comparative Analysis")
    print("=" * 60)
    
    # Initialize components
    config = Config()
    data_generator = DataGenerator()
    performance_analyzer = PerformanceAnalyzer()
    visualizer = Visualizer()
    
    # Define algorithms to test
    algorithms = {
        'Quick Sort': QuickSort(),
        'Merge Sort': MergeSort(),
        'Heap Sort': HeapSort()
    }
    
    print(f"📊 Testing {len(algorithms)} algorithms:")
    for name in algorithms.keys():
        print(f"   • {name}")
    
    print(f"📈 Data sizes: {config.DATA_SIZES}")
    print(f"📋 Data types: {config.DATA_TYPES}")
    print()
    
    # Generate test data
    print("🔧 Generating test data...")
    test_data = data_generator.generate_all_datasets()
    print(f"✅ Generated {len(test_data)} datasets")
    
    # Run performance analysis
    print("\n⚡ Running performance analysis...")
    results = performance_analyzer.analyze_algorithms(algorithms, test_data)
    print("✅ Performance analysis completed")
    
    # Generate visualizations
    print("\n📊 Generating visualizations...")
    visualizer.create_all_plots(results)
    print("✅ Visualizations saved to results/graphs/")
    
    # Save results
    print("\n💾 Saving results...")
    performance_analyzer.save_results(results)
    print("✅ Results saved to results/performance_data/")
    
    print("\n🎉 Analysis completed successfully!")
    print("📁 Check the 'results' directory for outputs")

if __name__ == "__main__":
    main()
