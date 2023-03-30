from wcag_contrast_ratio import rgb, passes_AA, passes_AAA
import numpy as np
import random
import json

def random_color():
    return '#' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def is_wcag_compliant(color1, color2, level='AAA', size='normal'):
    color1_rgb = hex_to_rgb(color1)
    color2_rgb = hex_to_rgb(color2)

    # Normalize the RGB values to a range of 0 to 1
    color1_rgb_normalized = tuple(x / 255 for x in color1_rgb)
    color2_rgb_normalized = tuple(x / 255 for x in color2_rgb)

    # Calculate contrast ratio
    ratio = rgb(color1_rgb_normalized, color2_rgb_normalized)

    # Check compliance

    if level == 'AA':
        return passes_AA(ratio, large=(size != 'normal'))
    else:
        return passes_AAA(ratio, large=(size != 'normal'))


def wcag_contrast_ratio(color1, color2):
    color1_rgb = hex_to_rgb(color1)
    color2_rgb = hex_to_rgb(color2)

    # Normalize the RGB values to a range of 0 to 1
    color1_rgb_normalized = tuple(x / 255 for x in color1_rgb)
    color2_rgb_normalized = tuple(x / 255 for x in color2_rgb)

    # Calculate contrast ratio
    return rgb(color1_rgb_normalized, color2_rgb_normalized)


def jprint(input):
    json_formatted_str = json.dumps(input, indent=2)
    print(json_formatted_str)


def dict_diff(dict1, dict2):
    diff = {}
    for key in dict1.keys():
        value1 = dict1[key]
        value2 = dict2[key]
        # print(key)
        if isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
            # value_diff = abs(value1 - value2)
            value_diff = value1 - value2
            # print("value_diff", value_diff, value1, value2)
            if value_diff != 0:
                diff[key] = value_diff
        elif isinstance(value1, str) and isinstance(value2, str):
            if value1 != value2:
                diff[key] = (value1, value2)
        else:
            diff[key] = "Incompatible types"
            
    return diff