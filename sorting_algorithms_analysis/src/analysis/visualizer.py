"""
Visualization module for sorting algorithm performance analysis
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
from typing import Dict, List, Any
from ..utils.config import Config
from ..utils.helpers import format_time

class Visualizer:
    """Class for creating performance visualizations"""
    
    def __init__(self):
        self.config = Config()
        self.config.ensure_directories()
          # Set style for better-looking plots
        try:
            plt.style.use('seaborn-v0_8')
        except OSError:
            try:
                plt.style.use('seaborn')
            except OSError:
                plt.style.use('default')
        sns.set_palette("husl")
    
    def create_runtime_comparison_plot(self, results: Dict[str, Any], data_type: str) -> str:
        """
        Create a line plot comparing algorithm runtimes for a specific data type
        
        Args:
            results: Analysis results
            data_type: Type of data to plot ('random', 'sorted', etc.)
        
        Returns:
            str: Path to saved plot
        """
        fig, ax = plt.subplots(figsize=self.config.FIGURE_SIZE)
        
        algorithms = results['algorithms']
        data_sizes = results['data_sizes']
        
        for algo_name in algorithms:
            mean_times = []
            std_times = []
            
            for size in data_sizes:
                stats = results['results'][algo_name][data_type][size]['statistics']
                mean_times.append(stats['mean'])
                std_times.append(stats['std_dev'])
            
            # Plot line with error bars
            ax.errorbar(data_sizes, mean_times, yerr=std_times, 
                       marker='o', linewidth=2, markersize=8, 
                       label=algo_name, capsize=5)
        
        ax.set_xlabel('Data Size', fontsize=12)
        ax.set_ylabel('Execution Time (seconds)', fontsize=12)
        ax.set_title(f'Sorting Algorithm Performance Comparison\\n{data_type.replace("_", " ").title()} Data', 
                    fontsize=14, fontweight='bold')
        
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        
        # Format x-axis labels
        ax.set_xticks(data_sizes)
        ax.set_xticklabels([f'{size//1000}K' for size in data_sizes])
        
        plt.tight_layout()
        
        # Save plot
        filename = f'runtime_comparison_{data_type}.png'
        filepath = os.path.join(self.config.GRAPHS_DIR, filename)
        plt.savefig(filepath, dpi=self.config.DPI, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_algorithm_comparison_heatmap(self, results: Dict[str, Any]) -> str:
        """
        Create a heatmap showing performance across all algorithms and data types
        
        Args:
            results: Analysis results
        
        Returns:
            str: Path to saved plot
        """
        algorithms = results['algorithms']
        data_types = results['data_types']
        data_sizes = results['data_sizes']
        
        # Create subplot for each data size
        fig, axes = plt.subplots(1, len(data_sizes), figsize=(16, 5))
        if len(data_sizes) == 1:
            axes = [axes]
        
        for i, size in enumerate(data_sizes):
            # Create matrix for heatmap
            matrix = []
            for algo_name in algorithms:
                row = []
                for data_type in data_types:
                    mean_time = results['results'][algo_name][data_type][size]['statistics']['mean']
                    row.append(mean_time)
                matrix.append(row)
            
            # Create heatmap
            im = axes[i].imshow(matrix, cmap='YlOrRd', aspect='auto')
            
            # Set labels
            axes[i].set_title(f'Size {size//1000}K', fontsize=12, fontweight='bold')
            axes[i].set_xticks(range(len(data_types)))
            axes[i].set_xticklabels([dt.replace('_', '\\n') for dt in data_types], fontsize=10)
            
            if i == 0:
                axes[i].set_yticks(range(len(algorithms)))
                axes[i].set_yticklabels(algorithms, fontsize=10)
            else:
                axes[i].set_yticks([])
            
            # Add text annotations
            for j in range(len(algorithms)):
                for k in range(len(data_types)):
                    text = f'{matrix[j][k]:.4f}s'
                    axes[i].text(k, j, text, ha='center', va='center', 
                               fontsize=8, color='black' if matrix[j][k] < np.max(matrix)/2 else 'white')
        
        plt.suptitle('Algorithm Performance Heatmap (Execution Time in Seconds)', 
                    fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        # Save plot
        filename = 'performance_heatmap.png'
        filepath = os.path.join(self.config.GRAPHS_DIR, filename)
        plt.savefig(filepath, dpi=self.config.DPI, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_scalability_plot(self, results: Dict[str, Any]) -> str:
        """
        Create a plot showing how each algorithm scales with data size
        
        Args:
            results: Analysis results
        
        Returns:
            str: Path to saved plot
        """
        algorithms = results['algorithms']
        data_types = results['data_types']
        data_sizes = results['data_sizes']
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()
        
        for i, data_type in enumerate(data_types):
            ax = axes[i]
            
            for algo_name in algorithms:
                times = []
                for size in data_sizes:
                    mean_time = results['results'][algo_name][data_type][size]['statistics']['mean']
                    times.append(mean_time)
                
                ax.plot(data_sizes, times, marker='o', linewidth=2, markersize=6, label=algo_name)
            
            ax.set_xlabel('Data Size', fontsize=11)
            ax.set_ylabel('Execution Time (seconds)', fontsize=11)
            ax.set_title(f'{data_type.replace("_", " ").title()} Data', fontsize=12, fontweight='bold')
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=9)
            
            # Format x-axis labels
            ax.set_xticks(data_sizes)
            ax.set_xticklabels([f'{size//1000}K' for size in data_sizes])
        
        plt.suptitle('Algorithm Scalability Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Save plot
        filename = 'scalability_analysis.png'
        filepath = os.path.join(self.config.GRAPHS_DIR, filename)
        plt.savefig(filepath, dpi=self.config.DPI, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_complexity_comparison_plot(self, results: Dict[str, Any]) -> str:
        """
        Create a bar plot comparing time complexities
        
        Args:
            results: Analysis results
        
        Returns:
            str: Path to saved plot
        """
        algorithms = results['algorithms']
        
        # Extract complexity information
        complexities = {}
        for algo_name in algorithms:
            # Get complexity from first result (same for all)
            first_result = list(results['results'][algo_name].values())[0]
            first_size_result = list(first_result.values())[0]
            complexities[algo_name] = first_size_result['time_complexities']
        
        # Create comparison table
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Prepare data for table
        table_data = []
        for algo_name in algorithms:
            row = [
                algo_name,
                complexities[algo_name]['best'],
                complexities[algo_name]['average'],
                complexities[algo_name]['worst'],
                first_size_result['space_complexity']  # Same for all algorithms in this context
            ]
            table_data.append(row)
        
        # Create table
        columns = ['Algorithm', 'Best Case', 'Average Case', 'Worst Case', 'Space Complexity']
        
        # Hide axes
        ax.axis('tight')
        ax.axis('off')
        
        # Create table
        table = ax.table(cellText=table_data, colLabels=columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.5)
        
        # Style the table
        for i in range(len(columns)):
            table[(0, i)].set_facecolor('#4CAF50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        for i in range(1, len(algorithms) + 1):
            for j in range(len(columns)):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#f0f0f0')
        
        plt.title('Time and Space Complexity Comparison', fontsize=16, fontweight='bold', pad=20)
        
        # Save plot
        filename = 'complexity_comparison.png'
        filepath = os.path.join(self.config.GRAPHS_DIR, filename)
        plt.savefig(filepath, dpi=self.config.DPI, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_all_plots(self, results: Dict[str, Any]) -> List[str]:
        """
        Create all visualization plots
        
        Args:
            results: Analysis results
        
        Returns:
            List[str]: Paths to all created plots
        """
        created_plots = []
        
        print("  Creating runtime comparison plots...")
        for data_type in results['data_types']:
            plot_path = self.create_runtime_comparison_plot(results, data_type)
            created_plots.append(plot_path)
            print(f"    ✅ {os.path.basename(plot_path)}")
        
        print("  Creating performance heatmap...")
        plot_path = self.create_algorithm_comparison_heatmap(results)
        created_plots.append(plot_path)
        print(f"    ✅ {os.path.basename(plot_path)}")
        
        print("  Creating scalability analysis...")
        plot_path = self.create_scalability_plot(results)
        created_plots.append(plot_path)
        print(f"    ✅ {os.path.basename(plot_path)}")
        
        print("  Creating complexity comparison...")
        plot_path = self.create_complexity_comparison_plot(results)
        created_plots.append(plot_path)
        print(f"    ✅ {os.path.basename(plot_path)}")
        
        return created_plots
