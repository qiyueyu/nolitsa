# -*- coding: utf-8 -*-

from __future__ import division

import itertools
import numpy as np

from nolitsa import d2, data
from numpy.testing import assert_, assert_allclose, run_module_suite


def test_c2():
    # Test d2.c2()
    # Particle moving uniformly in 5d: y(t) = a + b*t
    a = np.random.random(5)
    b = np.random.random(5)

    n = 250
    window = 15
    t = np.arange(n)
    y = a + b * t[:, np.newaxis]

    for metric in ('chebyshev', 'cityblock', 'euclidean'):
        if metric == 'chebyshev':
            modb = np.max(np.abs(b))
        elif metric == 'cityblock':
            modb = np.sum(np.abs(b))
        elif metric == 'euclidean':
            modb = np.sqrt(np.sum(b ** 2))

        minr = (window + 1) * modb
        maxr = (n - 1) * modb

        # We need to offset the r values a bit so that the half-open
        # bins used in np.histogram get closed.
        r = np.arange(window + 1, n) * modb + 1e-10

        c = d2.c2(y, r=r, window=window, metric=metric)[1]
        desired = (np.cumsum(np.arange(n - window - 1, 0, -1)) /
                   (0.5 * (n - window - 1) * (n - window)))
        assert_allclose(c, desired)


def test_c2_embed():
    # Test d2.c2_embed()
    t = np.linspace(0, 10 * 2 * np.pi, 5000)
    y = np.array([np.sin(t), np.cos(t)]).T
    desired = d2.c2(y)[1]

    dim = [2]
    tau = 125
    x = y[:, 0]

    assert_allclose(desired, d2.c2_embed(x, dim=dim, tau=tau)[0][1], atol=1e-3)

if __name__ == '__main__':
    run_module_suite()