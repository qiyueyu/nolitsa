# -*- coding: utf-8 -*-

import numpy as np
from nolitsa import delay
from numpy.testing import assert_, assert_allclose, run_module_suite


class TestAcorr:
    # Test delay.acorr()

    def test_random(self):
        # Test by calculating autocorrelation by brute force.
        n = 32
        x = np.random.random(n)
        x = x - x.mean()

        desired = np.empty(n)
        desired[0] = np.sum(x ** 2)

        for i in xrange(1, n):
            desired[i] = np.sum(x[:-i] * x[i:])

        desired = desired / desired[0]
        assert_allclose(delay.acorr(x), desired, atol=1E-8)

    def test_sin(self):
        # Test using a finite sine wave.
        #
        # Autocorrelation function of a /finite/ sine wave over n
        # cycles is:
        #
        #   r(tau) = [(2*n*pi - tau)*cos(tau) + sin(tau)] / 2*n*pi
        #
        # As n -> infty, r(tau) = cos(tau) as expected.
        n = 2 ** 5
        t = np.linspace(0, n * 2 * np.pi, n * 2 ** 10)
        x = np.sin(t)

        desired = ((np.cos(t) * (2 * n * np.pi - t) + np.sin(t)) /
                   (2 * n * np.pi))
        assert_allclose(delay.acorr(x), desired, atol=1E-5)

if __name__ == '__main__':
    run_module_suite()
