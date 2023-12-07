def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return 'Please enter a valid name!'
    return wrapper

@input_error
def capitalize_name(name: str):
    if name.isnumeric():
        raise ValueError()
    else:
        return name.capitalize()