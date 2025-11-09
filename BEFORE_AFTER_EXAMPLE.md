# Before & After: Empirical Findings Formatting

## ❌ BEFORE (Old Format)

Your empirical findings output looked like this:

```markdown
## 📊 Empirical Findings

{'Sample counts': '117 transcripts (from 113 patients); PiB+ n = 47; PiB- n = 70.', 'Classification (LOOCV, feature selection nested per fold)': [{'Classifier': 'Support Vector Machine (linear kernel)', 'Class weighting': 'PiB+ class weighted to 150% to balance sensitivity/specificity', 'Accuracy': 0.77, 'Sensitivity': 0.74, 'Specificity': 0.79}, {'Classifier': 'Logistic Regression (liblinear)', 'Accuracy': 0.74, 'Sensitivity': 0.72, 'Specificity': 0.74}], 'Feature-selection & statistical testing procedure (for group-level differences)': "Welch's t-tests across PiB groups, Benjamini-Hochberg FDR correction (q=0.05), stepwise removal of multicollinearity (>0.75 correlation) to produce a final set of discriminant features.", "Discriminant features (group-level Welch's t-test results, FDR-corrected p-values; means reported PiB- then PiB+)": [{'Feature': 'Imageability (all word classes)', 'PiB- mean': 5.62, 'PiB+ mean': 5.19, 'Welch_t': -5.05, 'corrected_p': 0.0004}]}
```

**Problems:**
- Raw Python dict syntax visible
- No formatting or structure
- Nested data completely unreadable
- Tables displayed as dict strings
- Very difficult to read and understand

---

## ✅ AFTER (New Format)

Now it looks like this:

```markdown
## 📊 Empirical Findings

**Sample counts:** 117 transcripts (from 113 patients); PiB+ n = 47; PiB- n = 70.

**Classification (LOOCV, feature selection nested per fold):**

| Classifier | Class weighting | Accuracy | Sensitivity | Specificity |
| --- | --- | --- | --- | --- |
| Support Vector Machine (linear kernel) | PiB+ class weighted to 150% to balance sensitivity/specificity | 0.77 | 0.74 | 0.79 |
| Logistic Regression (liblinear) | N/A | 0.74 | 0.72 | 0.74 |

**Feature-selection & statistical testing procedure (for group-level differences):** Welch's t-tests across PiB groups, Benjamini-Hochberg FDR correction (q=0.05), stepwise removal of multicollinearity (>0.75 correlation) to produce a final set of discriminant features.

**Discriminant features (group-level Welch's t-test results, FDR-corrected p-values; means reported PiB- then PiB+):**

| Feature | PiB- mean | PiB+ mean | Welch_t | corrected_p |
| --- | --- | --- | --- | --- |
| Imageability (all word classes) | 5.62 | 5.19 | -5.05 | 0.0004 |
| Imageability (nouns) | 6.32 | 6.04 | -4.59 | 0.001 |
| ICU: mention of drink (binary/percent) | 0.6 | 0.26 | -3.95 | 0.005 |
| Dominance (adjectives) | 3.91 | 5.4 | 3.66 | 0.01 |
| Uncertainties (proportion of words) | 0.02 | 0.04 | 3.52 | 0.01 |

**Additional reported results:** Post-hoc regression analyses indicated discriminant variables retained significant association with PiB status after accounting for education.
```

**Improvements:**
- ✅ Clean, readable markdown formatting
- ✅ Proper tables for statistical results
- ✅ Hierarchical structure with bold headers
- ✅ Missing values shown as "N/A"
- ✅ Easy to read, scan, and understand
- ✅ Exports beautifully to Word/Obsidian

---

## How It Renders

### In Markdown Viewer / Obsidian

The tables render as actual formatted tables:

**Sample counts:** 117 transcripts (from 113 patients); PiB+ n = 47; PiB- n = 70.

**Classification (LOOCV, feature selection nested per fold):**

| Classifier | Class weighting | Accuracy | Sensitivity | Specificity |
| --- | --- | --- | --- | --- |
| Support Vector Machine (linear kernel) | PiB+ class weighted to 150% to balance sensitivity/specificity | 0.77 | 0.74 | 0.79 |
| Logistic Regression (liblinear) | N/A | 0.74 | 0.72 | 0.74 |

**Discriminant features:**

| Feature | PiB- mean | PiB+ mean | Welch_t | corrected_p |
| --- | --- | --- | --- | --- |
| Imageability (all word classes) | 5.62 | 5.19 | -5.05 | 0.0004 |

---

## Edge Cases Also Fixed

### Handling None Values

**Before:**
```
None
```

**After:**
```
N/A
```

### Handling Empty Data

**Before:**
```
{}
[]
```

**After:**
```
No findings available.
```

### Handling Mixed Types

**Before:**
```
{'number': 42, 'boolean': True, 'none': None, 'text': 'Hello'}
```

**After:**
```markdown
**number:** 42

**boolean:** Yes

**none:** N/A

**text:** Hello
```

---

## Summary of Improvements

| Feature | Before | After |
|---------|--------|-------|
| **Tables** | Raw dict strings | Beautiful markdown tables |
| **None values** | "None" | "N/A" |
| **Booleans** | True/False | Yes/No |
| **Empty data** | "{}" or "[]" | Graceful empty or "No findings available" |
| **Nested dicts** | Unreadable single line | Proper hierarchy and indentation |
| **Missing keys** | Crashes or errors | Fills with "N/A" |
| **Readability** | ❌ Poor | ✅ Excellent |
| **Export quality** | ❌ Unusable | ✅ Publication-ready |

---

**The formatting is now publication-ready and works perfectly with Obsidian, Word, and any markdown viewer!**
