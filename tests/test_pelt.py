import numpy as np
from ruptures.pelt import Pelt
from ruptures.costs import gaussmean, linear_mse, NotEnoughPoints
from ruptures.datasets import pw_linear, pw_constant
from nose.tools import raises


def test1_ruptures1D():
    n_regimes = 5
    n_samples = 500

    # Piecewise constant signal
    signal, chg_pts = pw_constant(n=n_samples, clusters=n_regimes,
                                  min_size=50, noisy=True, snr=0.1)

    func_to_minimize = gaussmean(signal)  # - log likelihood
    for pen in np.linspace(0.1, 100, 20):
        pe = Pelt(func_to_minimize, penalty=pen, n=signal.shape[0], K=0)
        pe.fit()

    # Piecewise linear signal
    signal, chg_pts = pw_linear(n=n_samples, clusters=n_regimes,
                                min_size=50, noisy=True, snr=0.1)

    func_to_minimize = linear_mse(signal)  # mean squared error
    for pen in np.linspace(0.1, 100, 20):
        pe = Pelt(func_to_minimize, penalty=pen,
                  n=signal.shape[0], K=0, min_size=3)
        pe.fit()


@raises(NotEnoughPoints)
def test2_ruptures1D():
    n_regimes = 5
    n_samples = 500

    # Piecewise constant signal
    signal, chg_pts = pw_constant(n=n_samples, clusters=n_regimes,
                                  min_size=50, noisy=True, snr=0.1)

    func_to_minimize = gaussmean(signal)  # - log likelihood
    pen = 10
    pe = Pelt(func_to_minimize, penalty=pen,
              n=signal.shape[0], K=0, min_size=1)
    pe.fit()

    # Piecewise linear signal
    signal, chg_pts = pw_linear(n=n_samples, clusters=n_regimes,
                                min_size=50, noisy=True, snr=0.1)

    func_to_minimize = linear_mse(signal)  # mean squared error
    for pen in np.linspace(0.1, 100, 20):
        pe = Pelt(func_to_minimize, penalty=pen, n=signal.shape[0], K=0)
        pe.fit()


@raises(NotEnoughPoints)
def test3_ruptures1D():
    n_regimes = 5
    n_samples = 500

    # Piecewise linear signal
    signal, chg_pts = pw_linear(n=n_samples, clusters=n_regimes,
                                min_size=50, noisy=True, snr=0.1)

    func_to_minimize = linear_mse(signal)  # mean squared error
    pen = 10
    pe = Pelt(func_to_minimize, penalty=pen,
              n=signal.shape[0], K=0, min_size=2)
    pe.fit()


def test4_ruptures1D():
    n_regimes = 5
    n_samples = 500

    # Piecewise constant signal
    signal, chg_pts = pw_constant(n=n_samples, clusters=n_regimes,
                                  min_size=50, noisy=True, snr=0.001)

    func_to_minimize = gaussmean(signal)  # - log likelihood
    pen = 50
    pe = Pelt(func_to_minimize, penalty=pen, n=signal.shape[0], K=0)
    my_chg_pts = pe.fit()

    assert np.array_equal(np.sort(chg_pts), np.sort(my_chg_pts))