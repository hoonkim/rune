

def a():
    print("aa!")
    return True

def b():
    print("bb!")
    return False

def c():
    print("cc!")
    return False

def d(req):
    print("dd", req)
    return req


h = {}

h["a"] = a
h["b"] = b
h["c"] = c
h["d"] = d


if "e" in list(h.keys()):
    print("g")
else:
    print("f")