#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Counter for University Semester Data

This program reads the data.json file and reports how many classes 
are in each department (outer layer dictionary).
"""

import json
import sys
from typing import Dict, Any


def load_json_data(file_path: str) -> Dict[str, Any]:
    """
    Load JSON data from file with error handling.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        Dict[str, Any]: Loaded JSON data
        
    Raises:
        SystemExit: If file cannot be read or parsed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{file_path}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        sys.exit(1)


def count_classes_per_department(data: Dict[str, Any]) -> Dict[str, int]:
    """
    Count the number of classes in each department.
    
    Args:
        data (Dict[str, Any]): University data with departments as outer keys
        
    Returns:
        Dict[str, int]: Department names mapped to class counts
    """
    class_counts = {}
    
    for department_name, department_data in data.items():
        if isinstance(department_data, dict):
            class_counts[department_name] = len(department_data)
        else:
            print(f"Warning: Department '{department_name}' does not contain dictionary data")
            class_counts[department_name] = 0
    
    return class_counts


def display_results(class_counts: Dict[str, int]) -> None:
    """
    Display the class count results in a formatted way.
    
    Args:
        class_counts (Dict[str, int]): Department names mapped to class counts
    """
    total_classes = sum(class_counts.values())
    total_departments = len(class_counts)
    
    print("=" * 80)
    print("CLASS COUNT REPORT BY DEPARTMENT")
    print("=" * 80)
    print()
    
    # Sort departments by class count (descending) for better readability
    sorted_departments = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (department, count) in enumerate(sorted_departments, 1):
        print(f"{i:2d}. {department:<50} | {count:4d} classes")
    
    print()
    print("=" * 80)
    print(f"SUMMARY:")
    print(f"Total Departments: {total_departments}")
    print(f"Total Classes: {total_classes}")
    print(f"Average Classes per Department: {total_classes/total_departments:.1f}")
    print("=" * 80)


def save_results_to_file(class_counts: Dict[str, int], output_file: str) -> None:
    """
    Save the results to a JSON file.
    
    Args:
        class_counts (Dict[str, int]): Department names mapped to class counts
        output_file (str): Path to output file
    """
    try:
        # Create a more detailed output structure
        output_data = {
            "summary": {
                "total_departments": len(class_counts),
                "total_classes": sum(class_counts.values()),
                "average_classes_per_department": sum(class_counts.values()) / len(class_counts)
            },
            "departments": class_counts,
            "departments_sorted_by_count": dict(
                sorted(class_counts.items(), key=lambda x: x[1], reverse=True)
            )
        }
        
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(output_data, file, ensure_ascii=False, indent=2)
        
        print(f"\nResults saved to: {output_file}")
        
    except Exception as e:
        print(f"Warning: Could not save results to file: {e}")


def main():
    """Main function to run the class counting program."""
    
    # Configuration
    input_file = "data.json"
    output_file = "class_count_report.json"
    
    # Check if custom file path is provided via command line
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    print(f"Reading data from: {input_file}")
    print(f"Output will be saved to: {output_file}")
    print()
    
    # Load and process data
    data = load_json_data(input_file)
    class_counts = count_classes_per_department(data)
    
    # Display results
    display_results(class_counts)
    
    # Save results to file
    save_results_to_file(class_counts, output_file)


if __name__ == "__main__":
    main()
