#!/usr/bin/env python3
"""
Test script to validate the refactored bolted joint analyzer code.
"""

import sys
from classes import Bolt, Member, BoltedJoint
from resources import bolt_sizes, materials, clearance_holes
from plotter import plot_bolted_joint
import matplotlib.pyplot as plt

def test_data_loading():
    """Test that all data files load correctly."""
    print("Testing data loading...")
    try:
        bolt_data = bolt_sizes()
        material_data = materials()
        clearance_data = clearance_holes()
        print("✓ All data files loaded successfully")
        print(f"  - {len(bolt_data)} bolt sizes available")
        print(f"  - {len(material_data)} materials available")
        print(f"  - {len(clearance_data)} clearance hole configurations")
        return True
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return False

def test_bolt_creation():
    """Test bolt creation with validation."""
    print("\nTesting bolt creation...")
    try:
        # Test valid bolt
        bolt = Bolt('#10', '24', 'A-286 Alloy')
        print(f"✓ Valid bolt created: {bolt}")
        
        # Test invalid size
        try:
            invalid_bolt = Bolt('invalid-size', '20', 'A-286 Alloy')
            print("✗ Should have failed with invalid bolt size")
            return False
        except ValueError:
            print("✓ Correctly rejected invalid bolt size")
        
        return True
    except Exception as e:
        print(f"✗ Error in bolt creation: {e}")
        return False

def test_member_creation():
    """Test member creation with validation."""
    print("\nTesting member creation...")
    try:
        # Test valid members
        member1 = Member(0.25, 'A-286 Alloy')
        member2 = Member(0.375, 'A-286 Alloy')
        print(f"✓ Valid members created: {member1}, {member2}")
        
        # Test invalid thickness
        try:
            invalid_member = Member(-0.1, 'A-286 Alloy')
            print("✗ Should have failed with negative thickness")
            return False
        except ValueError:
            print("✓ Correctly rejected negative thickness")
        
        return True
    except Exception as e:
        print(f"✗ Error in member creation: {e}")
        return False

def test_joint_creation():
    """Test bolted joint creation."""
    print("\nTesting joint creation...")
    try:
        bolt = Bolt('#10', '24', 'A-286 Alloy')
        member1 = Member(0.25, 'A-286 Alloy')
        member2 = Member(0.375, 'A-286 Alloy')
        
        joint = BoltedJoint(bolt, [member1, member2], 0.281)
        print(f"✓ Valid joint created: {joint}")
        
        # Test bolt stiffness calculation
        stiffness = joint.bolt_stiffness()
        print(f"✓ Bolt stiffness calculated: {stiffness:.0f} N/m")
        
        return True
    except Exception as e:
        print(f"✗ Error in joint creation: {e}")
        return False

def test_visualization():
    """Test plot generation."""
    print("\nTesting visualization...")
    try:
        bolt = Bolt('#10', '24', 'A-286 Alloy')
        member1 = Member(0.25, 'A-286 Alloy')
        member2 = Member(0.375, 'A-286 Alloy')
        joint = BoltedJoint(bolt, [member1, member2], 0.281)
        
        fig, ax = plot_bolted_joint(joint)
        plt.close(fig)  # Clean up
        print("✓ Visualization generated successfully")
        return True
    except Exception as e:
        print(f"✗ Error in visualization: {e}")
        return False

def main():
    """Run all tests."""
    print("Running refactored code validation tests...\n")
    
    tests = [
        test_data_loading,
        test_bolt_creation,
        test_member_creation,
        test_joint_creation,
        test_visualization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Refactoring successful.")
        return 0
    else:
        print("✗ Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())