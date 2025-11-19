#!/usr/bin/env python3
"""Test script for style parameter in scatterplot."""

import pandas as pd
import numpy as np
import sys
sys.path.insert(0, 'src')

import publiplots as pp

# Create sample data
np.random.seed(42)
n = 60
data = pd.DataFrame({
    'x': np.random.randn(n),
    'y': np.random.randn(n),
    'group': np.random.choice(['A', 'B', 'C'], n),
    'condition': np.random.choice(['Control', 'Treatment'], n),
    'size_val': np.random.uniform(10, 100, n)
})

print("Testing style parameter with scatterplot...")
print(f"Data shape: {data.shape}")
print(f"Unique groups: {data['group'].unique()}")
print(f"Unique conditions: {data['condition'].unique()}")

# Test 1: Basic style with default markers
print("\nTest 1: Basic style with default markers")
try:
    fig, ax = pp.scatterplot(
        data=data,
        x='x',
        y='y',
        hue='group',
        style='condition',
        figsize=(8, 6)
    )
    print("✓ Test 1 passed: Basic style with default markers")
    pp.savefig('/tmp/test_style_basic.png')
    print("  Saved to /tmp/test_style_basic.png")
except Exception as e:
    print(f"✗ Test 1 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Style with custom marker list
print("\nTest 2: Style with custom marker list")
try:
    fig, ax = pp.scatterplot(
        data=data,
        x='x',
        y='y',
        hue='group',
        style='condition',
        markers=['o', '^'],
        figsize=(8, 6)
    )
    print("✓ Test 2 passed: Style with custom marker list")
    pp.savefig('/tmp/test_style_custom_markers.png')
    print("  Saved to /tmp/test_style_custom_markers.png")
except Exception as e:
    print(f"✗ Test 2 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Style with marker dict
print("\nTest 3: Style with marker dict")
try:
    fig, ax = pp.scatterplot(
        data=data,
        x='x',
        y='y',
        hue='group',
        style='condition',
        markers={'Control': 's', 'Treatment': 'D'},
        figsize=(8, 6)
    )
    print("✓ Test 3 passed: Style with marker dict")
    pp.savefig('/tmp/test_style_marker_dict.png')
    print("  Saved to /tmp/test_style_marker_dict.png")
except Exception as e:
    print(f"✗ Test 3 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Style without hue
print("\nTest 4: Style without hue")
try:
    fig, ax = pp.scatterplot(
        data=data,
        x='x',
        y='y',
        style='condition',
        markers=['o', '^'],
        color='#e67e7e',
        figsize=(8, 6)
    )
    print("✓ Test 4 passed: Style without hue")
    pp.savefig('/tmp/test_style_no_hue.png')
    print("  Saved to /tmp/test_style_no_hue.png")
except Exception as e:
    print(f"✗ Test 4 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Style with size
print("\nTest 5: Style with size")
try:
    fig, ax = pp.scatterplot(
        data=data,
        x='x',
        y='y',
        hue='group',
        style='condition',
        size='size_val',
        markers=['o', '^'],
        figsize=(8, 6)
    )
    print("✓ Test 5 passed: Style with size")
    pp.savefig('/tmp/test_style_with_size.png')
    print("  Saved to /tmp/test_style_with_size.png")
except Exception as e:
    print(f"✗ Test 5 failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)
print("All tests completed!")
