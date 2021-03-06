import numpy as np


def MSE(y, f):
    """
    Mean squared error (MSE).

    .. math:: MSE(y, f) = \\frac{1}{n} \sum_{i=1:n} (y_i-f_i)^2

    The optimal point forecast to minimize the MSE is the mean.

    .. code::

        k = 1
        MSE(y[forecast_start + k - 1:forecast_end + k], mean(samples))

    :param y: Observation vector
    :param f: Point forecast vector
    :return: Mean squared error (MSE)
    """

    y = np.ravel(y)
    f = np.ravel(f)
    return np.mean((y - f)**2)


def MAD(y, f):
    """
    Mean absolute deviation (MAD).

    .. math:: MAD(y, f) = \\frac{1}{n} \sum_{i=1:n} |y_i-f_i|

    The optimal point forecast to minimize the MAD is the median.

    .. code::

        k = 1
        MAD(y[forecast_start + k - 1:forecast_end + k], median(samples))

    :param y: Observation vector
    :param f: Point forecast vector
    :return: Mean absolute deviation (MAD)
    """

    y = np.ravel(y)
    f = np.ravel(f)
    return np.mean(np.abs(y-f))


def MAPE(y, f):
    """
    Mean absolute percent error (MAPE).

    .. math:: MAPE(y, f) = \\frac{1}{n} \sum_{i=1:n} |y_i-f_i| / y_i

    The optimal point forecast to minimize the MAPE is the (-1)-median. However, it is common to use the median point forecast, which is similar.

    .. code::

        k = 1
        MAPE(y[forecast_start + k - 1:forecast_end + k], m_one_median(samples))

    :param y: Observation vector
    :param f: Point forecast vector
    :return: Mean absolute percent error (MAPE)
    """
    y = np.ravel(y)
    f = np.ravel(f)
    return 100*np.mean(np.abs((y - f)) / y)


def WAPE(y, f):
    """
    Weighted Absolute Percent Error (WAPE).

    .. math:: WAPE(y, f) =  \\frac{\sum_{i=1:n} |y_i-f_i|}{\sum_{i=1:n} y_i}

    The weighted absolute percent error solves the issues of division by 0 in the MAPE.

    The optimal point forecase to minimize the WAPE is the joint (-1)-median.

    .. code::

        k = 1
        WAPE(y[forecast_start + k - 1:forecast_end + k], joint_m_one_median(samples))

    :param y: Observation vector
    :param f: Point forecast vector
    :return: Weighted absolute percent error (WAPE)
    """

    y = np.ravel(y)
    f = np.ravel(f)
    return 100*np.sum(np.abs(y-f)) / np.sum(y)


def WAFE(y, f):
    """
    Weighted Absolute Forecast Error (WAFE).

    .. math:: WAFE(y, f) =  \\frac{\sum_{i=1:n} |y_i-f_i|}{\sum_{i=1:n} \\frac{1}{2}(y_i + f_i)}

    Similar to WAPE, the weighted absolute forecast error solves the issues of division by 0 in the MAPE.
    It  balances between the observations (:math:`y_i`) and forecasts (:math:`f_i`) in the denominator.

    .. code::

        k = 1
        WAFE(y[forecast_start + k - 1:forecast_end + k], median(samples))

    :param y: Observation vector
    :param f: Point forecast vector
    :return: Weighted absolute forecast error (WAFE)
    """

    y = np.ravel(y)
    f = np.ravel(f)
    return 100*np.sum(np.abs(y-f)) / ((np.sum(y) + np.sum(f))/2)


def ZAPE(y, f):
    """
    Zero-Adjusted Absolute Percent Error (ZAPE).

    .. math:: ZAPE(y, f) = \\frac{1}{n} \sum_{i=1:n} I(y_i = 0) * f_i + I(y_i = 1) * |y_i-f_i| / y_i

    The zero-adjusted absolute percent error is an similar to absolute percent error (APE), but sets the loss equal to :math:`f_i` when :math:`y_i=0`, to avoid division by 0.

    Finding the optimal point forecast for ZAPE requires a simple numerical optimization, and lies between the median and (-1)-median.

    .. code::

        k = 1
        ZAPE(y[forecast_start + k - 1:forecast_end + k], median(samples))

    :param y: Observation vector
    :param f: Point forecast vector
    :return: The mean Zero-Adjusted absolute percent error (ZAPE)
    """

    y = np.ravel(y)
    f = np.ravel(f)
    nonzeros = y.nonzero()[0]
    n = len(y)
    loss = np.copy(f)
    loss[nonzeros] = np.abs(y[nonzeros] - f[nonzeros]) / y[nonzeros]
    return 100*np.mean(loss)


def scaledMSE(y, f, ymean = None):
    y = np.ravel(y)
    f = np.ravel(f)
    if ymean is None:
        # First check if the 'y' vector is longer than f
        ny = len(y)
        nf = len(f)
        ymean = np.cumsum(y) / np.arange(1, ny+1)
        # Assume that the forecasts and y vector terminate at the same point
        y = y[-nf:]
        ymean = ymean[-nf:]
    return np.mean(((y.reshape(-1) - f.reshape(-1)) ** 2 / (ymean.reshape(-1) ** 2)))
