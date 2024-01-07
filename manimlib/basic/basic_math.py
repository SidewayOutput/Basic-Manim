import numpy as np

def decimal_place(number):
    strings=str(number)
    decimalplace=strings.find(".")
    if decimalplace>=0:
        return len(strings)-decimalplace-1
    else:
        return 0
def log10(x):
    if x<0:
        raise Exception("error")
    if x==0:
        x=1E-4
    return np.log10(x)

def exp10(x):
    return 10**x

def linear(x):
    return x

def baseint(num,base):
    return base*int(num/base)

def baseceil(num,base):
    return base*np.ceil(num/base)

def baseround(num,base):
    return base*np.round(num/base)

def basefloor(num,base):
    return base*np.floor(num/base)

def funcceil(num,func,inv_func):
        return inv_func(np.ceil(func(num)))

def funcround(num,func,inv_func):
        return inv_func(np.round(func(num)))

def funcfloor(num,func,inv_func):
    return inv_func(np.floor(func(num)))
