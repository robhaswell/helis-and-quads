n = 0
c = 0
r = 0
i = 0

print("# led")

for n in range(24):
    print(f"led {n} {c},{r}::C:{i}")
    c += 1
    if c > 15:
        c = 0
        r += 1
    if n >= 4:
        i += 1
        if i > 15:
            i = 15

print()
print("# color")

h = 0
n = 0

while n < 16:
    hr = round(h)
    print(f"color {n} {hr},0,255")
    n += 1
    h += 20