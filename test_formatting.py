#!/usr/bin/env python3
"""
Test script for empirical findings formatting
Tests edge cases and complex nested data structures
"""

import json
import sys
sys.path.insert(0, 'backend/api')

from app import format_findings_section, safe_str, format_table, format_nested_dict

# Test data from user's example
test_findings = {
    'Sample counts': '117 transcripts (from 113 patients); PiB+ n = 47; PiB- n = 70.',
    'Classification (LOOCV, feature selection nested per fold)': [
        {
            'Classifier': 'Support Vector Machine (linear kernel)',
            'Class weighting': 'PiB+ class weighted to 150% to balance sensitivity/specificity',
            'Accuracy': 0.77,
            'Sensitivity': 0.74,
            'Specificity': 0.79
        },
        {
            'Classifier': 'Logistic Regression (liblinear)',
            'Accuracy': 0.74,
            'Sensitivity': 0.72,
            'Specificity': 0.74
        }
    ],
    'Feature-selection & statistical testing procedure (for group-level differences)': "Welch's t-tests across PiB groups, Benjamini-Hochberg FDR correction (q=0.05), stepwise removal of multicollinearity (>0.75 correlation) to produce a final set of discriminant features.",
    "Discriminant features (group-level Welch's t-test results, FDR-corrected p-values; means reported PiB- then PiB+)": [
        {
            'Feature': 'Imageability (all word classes)',
            'PiB- mean': 5.62,
            'PiB+ mean': 5.19,
            'Welch_t': -5.05,
            'corrected_p': 0.0004
        },
        {
            'Feature': 'Imageability (nouns)',
            'PiB- mean': 6.32,
            'PiB+ mean': 6.04,
            'Welch_t': -4.59,
            'corrected_p': 0.001
        },
        {
            'Feature': 'ICU: mention of drink (binary/percent)',
            'PiB- mean': 0.6,
            'PiB+ mean': 0.26,
            'Welch_t': -3.95,
            'corrected_p': 0.005
        }
    ],
    'Additional reported results': 'Post-hoc regression analyses indicated discriminant variables retained significant association with PiB status after accounting for education.'
}

# Edge case tests
edge_cases = [
    ("None value", None),
    ("Empty string", ""),
    ("Empty dict", {}),
    ("Empty list", []),
    ("Simple string", "This is a simple finding."),
    ("Simple list", ["Finding 1", "Finding 2", "Finding 3"]),
    ("Mixed types", {"number": 42, "boolean": True, "none": None, "text": "Hello"}),
    ("Nested empty", {"outer": {"inner": {"deep": None}}}),
]

print("=" * 80)
print("TESTING EMPIRICAL FINDINGS FORMATTER")
print("=" * 80)

print("\n" + "=" * 80)
print("TEST 1: Complex Nested Data (User's Example)")
print("=" * 80)
result = format_findings_section(test_findings)
print(result)

print("\n" + "=" * 80)
print("EDGE CASE TESTS")
print("=" * 80)

for test_name, test_data in edge_cases:
    print(f"\n--- Test: {test_name} ---")
    print(f"Input: {test_data}")
    print(f"Output:\n{format_findings_section(test_data)}")

print("\n" + "=" * 80)
print("TEST 2: Table Formatting")
print("=" * 80)

table_data = [
    {'Name': 'Alice', 'Age': 30, 'Score': 95.5},
    {'Name': 'Bob', 'Age': 25, 'Score': 87.3},
    {'Name': 'Charlie', 'Age': None, 'Score': 92.1}
]

print(format_table(table_data))

print("\n" + "=" * 80)
print("ALL TESTS COMPLETED")
print("=" * 80)

print("\n" + "=" * 80)
print("TEST 3: Classification Results (Should be Table)")
print("=" * 80)

# Force table format for classification with all same keys
classification_uniform = [
    {
        'Classifier': 'Support Vector Machine (linear kernel)',
        'Class_weighting': 'PiB+ class weighted to 150%',
        'Accuracy': 0.77,
        'Sensitivity': 0.74,
        'Specificity': 0.79
    },
    {
        'Classifier': 'Logistic Regression (liblinear)',
        'Class_weighting': 'N/A',
        'Accuracy': 0.74,
        'Sensitivity': 0.72,
        'Specificity': 0.74
    }
]

print("\nWith uniform keys:")
print(format_nested_dict({'Classification': classification_uniform}))

print("\n" + "=" * 80)
