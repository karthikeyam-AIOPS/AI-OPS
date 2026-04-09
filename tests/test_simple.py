"""
Very simple test to make sure the basic setup works.
"""

def test_python_basics():
    """Test that Python basics work."""
    assert 2 + 2 == 4
    assert "hello".upper() == "HELLO"
    assert [1, 2, 3][1] == 2


def test_imports():
    """Test that we can do basic imports."""
    import sys
    import os
    assert sys is not None
    assert os is not None


if __name__ == "__main__":
    test_python_basics()
    test_imports()
    print("✅ All basic tests passed!")