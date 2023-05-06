n = 0
c = 0
r = 0
i = 0

for n in range(24):
    print(f"led {n} {c},{r}::CT{i}")
    c += 1
    if c > 15:
        c = 0
        r += 1
    if n >= 3:
        i += 1
        if i > 15:
            i = 15
            