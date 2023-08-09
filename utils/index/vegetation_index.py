import numpy as np


def evi_index(blue, red, nir):
    a = 2.5 * (nir - red)
    b = (nir + (6.0 * red) - (7.5 * blue) + 1.0)
    evi = np.divide(a, b, where=(b != 0))
    return evi


def ndvi_index(red, nir):
    a = (nir - red)
    b = (nir + red)
    ndvi = np.divide(a, b, out=np.full_like(a, 0), where=(b != 0))
    return ndvi


def psri_index(red, nir):
    a = (red - nir)
    b = (red + nir)
    psri = np.divide(a, b, out=np.full_like(a, 0), where=(b != 0))
    return psri


def savi_index(red, nir, l):
    a = (nir - red)
    b = (nir + red + l) * (1.0 + l)
    savi = np.divide(a, b, where=b != 0)
    return savi


"""
(Shi and Xu, 2019)
Shi, T. and Xu, H. (2019).
Derivation of Tasseled Cap Transformation Coefficients for Sentinel-2 MSI At-Sensor Reflectance Data.
IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 12(10), pp.4038–4048.
doi:https://doi.org/10.1109/jstars.2019.2938388.
"""


def brightness_sentinel_2_tasseled_cap(blue, green, red, nir, mir1, mir2):
    brightness = (blue * 0.3510) + (green * 0.3813) + (red * 0.3437) + \
        (nir * 0.7196) + (mir1 * 0.2396) + (mir2 * 0.1949)
    return brightness


def greeness_sentinel_2_tasseled_cap(blue, green, red, nir, mir1, mir2):
    greeness = (blue * -0.3599) + (green * -0.3533) + (red * -0.4734) + \
        (nir * 0.6633) + (mir1 * 0.0087) + (mir2 * -0.2856)
    return greeness


def wetness_sentinel_2_tasseled_cap(blue, green, red, nir, mir1, mir2):
    wetness = (blue * 0.2578) + (green * 0.2305) + (red * 0.0883) + \
        (nir * 0.1071) + (mir1 * -0.7611) + (mir2 * -0.5308)
    return wetness
