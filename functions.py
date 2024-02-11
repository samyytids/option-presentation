def long_call_option(option_price, strike_price, underlying_price):
    return -option_price if underlying_price - strike_price - option_price < -option_price else underlying_price - strike_price - option_price

def long_put_option(option_price, strike_price, underlying_price):
    return -option_price if strike_price - underlying_price - option_price < -option_price else strike_price - underlying_price - option_price

def long_stock(option_price, strike_price, underlying_price):
    return underlying_price-strike_price

def short_call_option(option_price, strike_price, underlying_price):
    return -(-option_price if underlying_price - strike_price - option_price < -option_price else underlying_price - strike_price - option_price)

def short_put_option(option_price, strike_price, underlying_price):
    return -(-option_price if strike_price - underlying_price - option_price < -option_price else strike_price - underlying_price - option_price)

def short_stock(option_price, strike_price, underlying_price):
    return -(underlying_price-strike_price)

function_map = {
    "long_call_option" : long_call_option,
    "long_put_option" : long_put_option,
    "long_stock" : long_stock,
    "short_call_option" : short_call_option,
    "short_put_option" : short_put_option,
    "short_stock" : short_stock,
}