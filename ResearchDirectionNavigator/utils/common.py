from decimal import Decimal
def split_keywords_by_comma(text):
    cleaned_text=(text or "").strip()
    if not cleaned_text:
        return []
    keyword_list=[]
    for keyword in cleaned_text.split(","):
        one_keyword=keyword.strip()
        if one_keyword:
            keyword_list.append(one_keyword)
    return keyword_list


def pick_first_keyword(text):
    keyword_list=split_keywords_by_comma(text)
    if not keyword_list:
        return ""
    return keyword_list[0]


def parse_int(value):
    if value is None:
        return None
    if isinstance(value, Decimal):
        if not value.is_finite():
            return None
        numerator, denominator=value.as_integer_ratio()
        if denominator!=1:
            return None
        return numerator
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if value.is_integer():
            return int(value)
        return None
    if isinstance(value, str):
        cleaned_value=value.strip()
        if cleaned_value.isdigit():
            return int(cleaned_value)
        if cleaned_value.startswith("-") and cleaned_value[1:].isdigit():
            return int(cleaned_value)
        return None
    return None


def to_int(value, default=0):
    parsed_value=parse_int(value)
    if parsed_value is None:
        return default
    return parsed_value


def make_gradient_colors(number_of_bars, dark_color=(44, 81, 110), light_color=(209, 234, 229)):
    if number_of_bars<=0:
        return []
    if number_of_bars==1:
        return [f"rgb({dark_color[0]},{dark_color[1]},{dark_color[2]})"]

    color_list=[]
    for index in range(number_of_bars):
        blend_ratio=index / (number_of_bars - 1)
        red=int(dark_color[0] + (light_color[0] - dark_color[0]) * blend_ratio)
        green=int(dark_color[1] + (light_color[1] - dark_color[1]) * blend_ratio)
        blue=int(dark_color[2] + (light_color[2] - dark_color[2]) * blend_ratio)
        color_list.append(f"rgb({red},{green},{blue})")
    return color_list


def neo4j_faculty_id_to_mysql_id(neo4j_faculty_id):
    cleaned_value=str(neo4j_faculty_id or "").strip()
    if cleaned_value.startswith("f"):
        cleaned_value=cleaned_value[1:]
    if cleaned_value.isdigit():
        return int(cleaned_value)
    return None
