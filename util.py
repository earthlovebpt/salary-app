# Group minor countires into "Other".
def remove_minor_categories(categories, cutoff):
    categories_dict = {}
    for c,value in categories.items():
        if value >= cutoff:
            categories_dict[c] = c
        else:
            categories_dict[c] = 'Other'
    return categories_dict

# Change years of experience into number.
def experience2number(year, year_max):
    if year == "Less than 1 year":
        return 0
    elif year == "More than 50 years":
        return year_max
    elif int(year) >= year_max:
        return year_max
    return year