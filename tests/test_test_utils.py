import numpy as np
from mobula_op.test_utils import assert_almost_equal

def check_almost_euqal_expection_raise(a, b, info, atol = 1e-5, rtol = 1e-8):
    try:
        assert_almost_equal(a, b, atol = atol, rtol = rtol)
        raise Exception(info)
    except AssertionError:
        pass

def test_almost_equal_shape():
    shape1 = (2,2,3)
    a = np.random.random(shape1) 
    b = a.copy() 
    c = a[1]
    assert_almost_equal(a, b)
    check_almost_euqal_expection_raise(a, c, "No exception raised")

def test_almost_equal_value():
    shape1 = (2,2,3)
    a = np.random.random(shape1) 
    b = a.copy()
    atol = 1e-5
    assert_almost_equal(a, b, atol = 0)
    assert_almost_equal(a, b, atol = atol)
    b[0, 0, 0] += atol
    b[0, 1, 2] -= atol
    assert_almost_equal(a, b, atol = atol * 2.0)
    assert_almost_equal(a, b, atol = atol / 2.0)
    check_almost_euqal_expection_raise(a, b, "Absolute Error Check failed")
    rtol = np.max(np.abs((a - b) / (b + FLT_MIN))) 
    assert_almost_equal(a, b, atol = atol * 2.0, rtol = rtol * 2.0)
    check_almost_euqal_expection_raise(a, b, atol = atol * 2.0, rtol = rtol / 2.0) 
