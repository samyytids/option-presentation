def long_call(underlying_price, option_price, strike_price):        
    if not strike_price:
        strike_price = 0
    
    if underlying_price - strike_price < 0:
        result = 0
    else:
        result = underlying_price - strike_price
    
    return result + option_price
    
    # return -option_price if underlying_price - strike_price - option_price < -option_price else underlying_price - strike_price - option_price

def long_put(underlying_price, option_price, strike_price):
    if not strike_price:
        strike_price = 0
        
    if strike_price - underlying_price < 0:
        result = 0
    else:
        result = strike_price - underlying_price
        
    return result + option_price
        
    # return -option_price if strike_price - underlying_price - option_price < -option_price else strike_price - underlying_price - option_price

def long_stock(underlying_price, option_price, strike_price):        
    if not strike_price:
        strike_price = 0
        
    return underlying_price-strike_price

def short_call(underlying_price, option_price, strike_price):        
    if not strike_price:
        strike_price = 0
    
    if strike_price - underlying_price < 0:
        result = strike_price - underlying_price + option_price
    else:
        result = option_price
        
    return result

def short_put(underlying_price, option_price, strike_price):
    if not strike_price:
        strike_price = 0
        
    if underlying_price - strike_price < 0:
        result = underlying_price - strike_price + option_price
    else:
        result = option_price
        
    return result

def short_stock(underlying_price, option_price, strike_price):
    if not option_price:
        option_price = 1
        
    if not strike_price:
        strike_price = 0
        
    return -(underlying_price-strike_price)

function_map = {
    "long_call" : long_call,
    "long_put" : long_put,
    "long_stock" : long_stock,
    "short_call" : short_call,
    "short_put" : short_put,
    "short_stock" : short_stock,
}