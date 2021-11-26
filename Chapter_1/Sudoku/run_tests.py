if __name__ == "__main__":
    import pytest 
    fail = pytest.main()
    if not fail:
        print('all tests passed!')