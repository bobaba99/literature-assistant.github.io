# Empirical Findings Formatting Improvements

## Summary

Enhanced the backend to properly format complex nested JSON data in empirical findings sections, with robust edge case handling and automatic table generation for statistical results.

## Changes Made

### 1. New Helper Functions

#### `safe_str(value)`
- Safely converts any value to string
- Handles `None` → "N/A"
- Handles booleans → "Yes"/"No"
- Handles empty strings → "N/A"
- Prevents crashes from unexpected data types

#### `format_table(data, headers=None)`
- Creates markdown tables from lists of dictionaries
- Auto-detects headers from all items (handles missing keys)
- Escapes pipe characters (`|`) in cell values
- Maintains key order from first item
- Fills missing values with "N/A"

#### `format_nested_dict(data, indent_level=0)`
- Recursively formats nested dictionaries
- Auto-detects table-like structures (list of dicts)
- Handles mixed data types gracefully
- Proper indentation for nested structures
- Smart detection: creates tables when ≥50% of keys match

#### `format_findings_section(findings)`
- Main function for formatting empirical findings
- Handles all data types: dict, list, string, None
- Delegates to appropriate formatter
- Special handling for statistical results

### 2. Updated Formatting Logic

**Before:**
```python
if isinstance(findings, list):
    for finding in findings:
        markdown += f"- {finding}\n"
else:
    markdown += f"{findings}\n"
```

**After:**
- Tables for lists of dictionaries with similar keys
- Nested formatting for complex structures
- Bullet lists for simple arrays
- Key-value pairs for dictionaries
- Edge case handling for None/empty values

## Examples

### Input: Complex Nested Dictionary
```json
{
  "Sample counts": "117 transcripts (from 113 patients); PiB+ n = 47; PiB- n = 70.",
  "Classification (LOOCV, feature selection nested per fold)": [
    {
      "Classifier": "Support Vector Machine (linear kernel)",
      "Class weighting": "PiB+ class weighted to 150%",
      "Accuracy": 0.77,
      "Sensitivity": 0.74,
      "Specificity": 0.79
    },
    {
      "Classifier": "Logistic Regression (liblinear)",
      "Accuracy": 0.74,
      "Sensitivity": 0.72,
      "Specificity": 0.74
    }
  ],
  "Discriminant features": [
    {
      "Feature": "Imageability (all word classes)",
      "PiB- mean": 5.62,
      "PiB+ mean": 5.19,
      "Welch_t": -5.05,
      "corrected_p": 0.0004
    }
  ]
}
```

### Output: Formatted Markdown
```markdown
**Sample counts:** 117 transcripts (from 113 patients); PiB+ n = 47; PiB- n = 70.

**Classification (LOOCV, feature selection nested per fold):**

| Classifier | Class weighting | Accuracy | Sensitivity | Specificity |
| --- | --- | --- | --- | --- |
| Support Vector Machine (linear kernel) | PiB+ class weighted to 150% | 0.77 | 0.74 | 0.79 |
| Logistic Regression (liblinear) | N/A | 0.74 | 0.72 | 0.74 |

**Discriminant features:**

| Feature | PiB- mean | PiB+ mean | Welch_t | corrected_p |
| --- | --- | --- | --- | --- |
| Imageability (all word classes) | 5.62 | 5.19 | -5.05 | 0.0004 |
```

## Edge Cases Handled

| Input Type | Handling |
|------------|----------|
| `None` | Returns "No findings available." |
| Empty string `""` | Returns empty output (graceful) |
| Empty dict `{}` | Returns empty output |
| Empty list `[]` | Returns empty output |
| Simple string | Returns as-is |
| Simple list | Bullet points |
| Mixed types | Key-value pairs with type conversion |
| Nested None | Shows "N/A" for missing values |
| Missing dict keys | Fills with "N/A" in tables |
| Pipe chars in values | Escapes as `\|` |
| Deeply nested dicts | Proper indentation |

## Testing

Run comprehensive tests:
```bash
python test_formatting.py
```

Tests include:
1. Complex nested data (user's actual example)
2. Edge cases (None, empty, mixed types)
3. Table formatting
4. Classification results
5. Statistical results with varying keys

## Benefits

✅ **Readable Tables**: Statistical results automatically formatted as tables
✅ **Robust**: Handles all edge cases without crashing
✅ **Smart Detection**: Auto-detects table-like structures
✅ **Flexible**: Works with varying JSON structures
✅ **Maintainable**: Clean, well-documented functions
✅ **Safe**: Prevents crashes from malformed data

## Files Modified

- `backend/api/app.py` - Added 4 new functions, updated `format_analysis_as_markdown()`
- `test_formatting.py` - Comprehensive test suite

## Backward Compatibility

✅ Fully backward compatible - handles all previous formats plus new complex structures

---

**Status**: ✅ Complete and tested
**Date**: 2025-11-09
