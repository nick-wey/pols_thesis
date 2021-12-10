year = '2000'
pacs = {}

while int(year) < 2020:
    f = open(year + '_pacs.txt')
    for line in f.readlines():
        pac = line.strip()
        if pac in pacs:
            pacs[pac] += 1
        else:
            pacs[pac] = 1
    year = str(int(year) + 6)
    print(year)
print(pacs)
idx1 = 0
idx2 = 0
for pac in pacs:
    if pacs[pac] == 4 or pacs[pac] == 2 or pacs[pac] == 3:
        idx1 += 1
    else:
        idx2 += 1

print(idx1)
print(idx2)
