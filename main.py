hoi = [1,2,4,56,7,7854,435,5673465346,45674576,34534]
hoi2 = [1,233,4324,534,653,234,234]
lst = []

def gdrfg(hoi):
    add = "a"
    for i in range(len(hoi)):
        hoi[i] += 1
        if hoi[i] > 3:
            lst.append(add)
    return hoi, hoi2


hoi, hoi2 = gdrfg(hoi)

print(hoi)
print(hoi2)
print(lst)
