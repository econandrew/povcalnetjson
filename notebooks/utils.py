import numpy as np
import scipy.interpolate
import scipy.optimize

def inverse(f, domain=(0.0, 1.0-1e-6), extrapolate=(float("NaN"), float("NaN"))):
    def inner(x):
        if f(domain[0]) >= x:
            return extrapolate[0]
        if f(domain[1]) <= x:
            return extrapolate[1]
        else:
            try:
                return scipy.optimize.brentq(lambda y: f(y)-x, a=domain[0], b=domain[1])
            except ValueError:
                return float("NaN")

    return np.vectorize(inner)

import scipy.misc
def derivative(f, dx=1e-6):
    return np.vectorize(lambda x: scipy.misc.derivative(f, x, dx))

def integral(f, lower=0.0):
    return np.vectorize(lambda x: scipy.integrate.quad(f, lower, x)[0])

from termcolor import colored
from math import log10
LEVELS = [(0.01, "green"), (0.05, "yellow"), (float("inf"), "red")]
def myassert(caption, actual, baseline):
    pc_diff = abs(actual - baseline)/baseline
    for cutoff, color in LEVELS:
        if pc_diff < cutoff:
            break

    try:
        rounding = max(4 - int(log10(abs(baseline))), 0)
    except:
        rounding = 4
    print(colored("{}\tcomputed = {}\tgiven = {}\tdifference = {}%".format(
                    caption.ljust(20),
                    str(round(actual,rounding)).rjust(12),
                    str(round(baseline,rounding)).rjust(12),
                    round(pc_diff*100,3)),
                  color))