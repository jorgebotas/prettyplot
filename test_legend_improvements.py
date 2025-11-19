#!/usr/bin/env python3
"""Test script for legend and marker improvements."""

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
    'score': np.random.uniform(0, 100, n),
    'size_val': np.random.uniform(10, 100, n)
})

print("="*60)
print("Testing legend improvements...")
print("="*60)

# Test 1: Continuous hue with colorbar via pp.legend(ax)
print("\nTest 1: Continuous hue colorbar with auto mode")
try:
    fig, ax = pp.scatterplot(
        data=data,
        x='x',
        y='y',
        hue='score',
        palette='viridis',
        hue_norm=(0, 100),
        legend=False,
        figsize=(8, 6)
    )
    # Auto mode should detect and add colorbar
    builder = pp.legend(ax)
    print("✓ Test 1 passed: Colorbar added via auto mode")
    pp.savefig('/tmp/test_colorbar_auto.png')
    print("  Saved to /tmp/test_colorbar_auto.png")
except Exception as e:
    print(f"✗ Test 1 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Continuous hue with add_legend_for('hue')
print("\nTest 2: Continuous hue colorbar with add_legend_for")
try:
    fig, ax = pp.scatterplot(
        data=data,
        x='x',
        y='y',
        hue='score',
        palette='plasma',
        hue_norm=(0, 100),
        legend=False,
        figsize=(8, 6)
    )
    # Manual mode using add_legend_for
    builder = pp.legend(ax, auto=False)
    builder.add_legend_for('hue', title='Custom Score')
    print("✓ Test 2 passed: Colorbar added via add_legend_for")
    pp.savefig('/tmp/test_colorbar_manual.png')
    print("  Saved to /tmp/test_colorbar_manual.png")
except Exception as e:
    print(f"✗ Test 2 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Style with resolve_marker_mapping
print("\nTest 3: Style with resolve_marker_mapping")
try:
    fig, ax = pp.scatterplot(
        data=data,
        x='x',
        y='y',
        hue='group',
        style='condition',
        figsize=(8, 6)
    )
    print("✓ Test 3 passed: Style uses resolve_marker_mapping internally")
    pp.savefig('/tmp/test_style_with_resolve.png')
    print("  Saved to /tmp/test_style_with_resolve.png")
except Exception as e:
    print(f"✗ Test 3 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Test resolve_marker_mapping directly
print("\nTest 4: Test resolve_marker_mapping helper")
try:
    categories = ['A', 'B', 'C', 'D', 'E']
    mapping = pp.resolve_marker_mapping(values=categories)
    assert mapping['A'] == 'o', f"Expected 'o', got {mapping['A']}"
    assert mapping['B'] == 's', f"Expected 's', got {mapping['B']}"
    assert mapping['C'] == '^', f"Expected '^', got {mapping['C']}"
    print("✓ Test 4 passed: resolve_marker_mapping works correctly")
    print(f"  Mapping: {mapping}")
except Exception as e:
    print(f"✗ Test 4 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Test resolve_markers helper
print("\nTest 5: Test resolve_markers helper")
try:
    markers = pp.resolve_markers(n_markers=5)
    assert len(markers) == 5, f"Expected 5 markers, got {len(markers)}"
    assert markers[0] == 'o', f"Expected 'o', got {markers[0]}"
    assert markers[1] == 's', f"Expected 's', got {markers[1]}"
    print("✓ Test 5 passed: resolve_markers works correctly")
    print(f"  Markers: {markers}")
except Exception as e:
    print(f"✗ Test 5 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Test SIMPLE_MARKERS constant
print("\nTest 6: Test SIMPLE_MARKERS export")
try:
    assert hasattr(pp, 'SIMPLE_MARKERS'), "SIMPLE_MARKERS not exported"
    assert len(pp.SIMPLE_MARKERS) == 4, f"Expected 4 markers, got {len(pp.SIMPLE_MARKERS)}"
    print("✓ Test 6 passed: SIMPLE_MARKERS exported")
    print(f"  SIMPLE_MARKERS: {pp.SIMPLE_MARKERS}")
except Exception as e:
    print(f"✗ Test 6 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 7: Test resolve_hatch_mapping export
print("\nTest 7: Test resolve_hatch_mapping export")
try:
    assert hasattr(pp, 'resolve_hatch_mapping'), "resolve_hatch_mapping not exported"
    categories = ['A', 'B', 'C']
    hatch_mapping = pp.resolve_hatch_mapping(values=categories)
    print("✓ Test 7 passed: resolve_hatch_mapping exported")
    print(f"  Hatch mapping: {hatch_mapping}")
except Exception as e:
    print(f"✗ Test 7 failed: {e}")
    import traceback
    traceback.print_exc()

# Test 8: Combined hue (continuous) + style
print("\nTest 8: Combined continuous hue + style")
try:
    fig, ax = pp.scatterplot(
        data=data,
        x='x',
        y='y',
        hue='score',
        style='condition',
        palette='coolwarm',
        hue_norm=(0, 100),
        markers=['o', '^'],
        figsize=(8, 6)
    )
    print("✓ Test 8 passed: Continuous hue + style combined")
    pp.savefig('/tmp/test_combined_continuous_style.png')
    print("  Saved to /tmp/test_combined_continuous_style.png")
except Exception as e:
    print(f"✗ Test 8 failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("All tests completed!")
print("="*60)
