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