import pytest
from analyze_water import calc_turbidity, calc_min_time

def test_calc_turbidity():
    # test with random data
    data = [{'detector_current':0.5,'calibration_constant': 2.0}, {'detector_current':0.5,'calibration_constant': 2.0}, {'detector_current':1.5,'calibration_constant': 2.0}, {'detector_current':1.5,'calibration_constant': 2.0}, {'detector_current':1.0,'calibration_constant': 2.0}]
    assert calc_turbidity(data) == 2.0

    #test with sample of first 5
    data = [{'detector_current':1.137,'calibration_constant': 1.022}, {'detector_current': 1.141,'calibration_constant': 0.975}, {'detector_current':1.1300000000000001,'calibration_constant': 1.022}, {'detector_current':1.129,'calibration_constant': 0.989}, {'detector_current':1.189,'calibration_constant': 1.029}]
    assert calc_turbidity(data) == 1.1538822

def test_calc_min_time():
    # test with sample
    assert calc_min_time(1.1538822, 1.0, 0.02) == 7.084797146399919

    # test with random values
    assert calc_min_time(2.0, 1.0, 0.25)== 2.409420839653209
    assert calc_min_time(1.5, 2.0, 0.02) == 0


