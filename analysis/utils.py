from datafetch.utils import bookie_probability_real


def divide_without_errors(dividend, divisor):
    try:
        result = dividend / divisor
    except (TypeError, ZeroDivisionError):
        result = 0
    return result

def color_if_higher_lower(value1, value2):
    if value1 > value2:
        return 'text-success'
    elif value1 < value2:
        return 'text-danger'
    else:
        return 'text-info'

def get_real_h_a_odds_difference(odds_home, odds_draw, odds_away, datafetch_settings):
    """
    :return: True if game is within the difference range
    """

    coef_probability = bookie_probability_real(odds_home, odds_draw, odds_away)
    difference = round(
        (coef_probability['bookie_probabilty_real_1']) - (coef_probability['bookie_probabilty_real_2']), 3)
    result = (datafetch_settings.difference_x_range_min <= difference <= datafetch_settings.difference_x_range_max)

    return result
