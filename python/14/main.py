# here is my golfed version

from collections import Counter as C
def golf(ip):
    t,_,*rs = ip.splitlines()
    rs = [(l,r,i) for l,r,*_,i in rs]
    pc = C(__import__('more_itertools').windowed(t,2))
    for i in range(40):
        pc = sum([C({(l,i):(c:=pc[(l,r)]),(i,r):c}) for l,r,i in rs], C())
        if i in [9,39]: print(f"{i+1}:{((m:=sum([C({l:c})+C({r:c}) for (l,r),c in (pc+C({(t[0],t[-1]):1})).items()],C()).most_common())[0][1]-m[-1][1])//2}")

# Here is the longer version

import numpy as np
import networkx as nx
from more_itertools import windowed
from collections import Counter

def apply_rules(pair_count, rules):
    new_pair_count = Counter()
    for [left, right], insertion in rules:
        pair = ''.join([left, right])
        if count := pair_count[pair]:
            new_pair_count[f"{insertion}{right}"] += count
            new_pair_count[f"{left}{insertion}"] += count
    return new_pair_count

def score(pair_count, template_first, template_last):
    elements = Counter()
    for [left, right], count in pair_count.items():
        elements[left] += count
        elements[right] += count

    elements[template_first] += 1
    elements[template_last] += 1
    elements = Counter({k: v//2 for k,v in elements.items()})

    top_elements = sorted(elements.items(), key=lambda x: x[1], reverse=True)
    print("top_elements", top_elements)
    return top_elements[0][1] - top_elements[-1][1]

def main(input):
    lines = input.splitlines()
    template, rules = lines[0], lines[2:]
    rules = [tuple(r.split(' -> ')) for r in rules]
    pair_count = Counter([f'{l}{r}' for l, r in windowed(template, 2)])
    for i in range(40):
        print(f"{i=} {score(pair_count, template[0], template[-1])} {pair_count=}")
        pair_count = apply_rules(pair_count, rules)
        if i+1 == 10:
            print(f"after 10 iter {score(pair_count, template[0], template[-1])=}")
    print(f"after 40 iter {template=}, {score(pair_count, template[0], template[-1])=}")

if __name__ == "__main__":
    EXAMPLE = """NNCB

BB -> N
BC -> B
BH -> H
BN -> B
CB -> H
CC -> N
CH -> B
CN -> C
HB -> C
HC -> B
HH -> N
HN -> C
NB -> B
NC -> B
NH -> C
NN -> C
"""
    INPUT = """CFFPOHBCVVNPHCNBKVNV

KO -> F
CV -> H
CF -> P
FK -> B
BN -> P
VN -> K
BC -> H
OP -> S
HS -> V
HK -> N
CC -> F
CK -> V
OC -> S
SN -> C
PK -> H
BB -> S
PO -> F
HF -> K
BV -> P
HP -> F
VF -> H
BP -> H
CH -> C
KN -> O
NP -> F
FS -> F
BH -> B
VB -> P
OS -> S
KK -> O
SO -> P
NB -> O
PS -> O
KV -> O
CS -> P
PN -> O
HB -> V
NF -> P
SC -> S
NH -> N
HV -> K
FN -> V
KS -> P
BO -> C
KP -> V
OK -> B
OV -> P
CN -> C
SB -> H
VP -> C
HC -> P
FB -> F
VS -> K
PH -> C
VC -> H
KH -> B
SH -> B
BK -> N
SP -> P
SF -> B
OO -> B
VH -> K
PP -> C
FV -> P
KC -> P
CO -> S
NO -> O
FO -> K
SK -> O
ON -> K
VO -> H
VV -> H
CP -> P
FC -> B
FP -> N
FH -> C
KF -> F
PB -> C
NN -> K
SS -> O
CB -> C
HH -> S
FF -> S
KB -> N
HO -> O
BF -> N
PV -> K
OB -> B
OH -> N
VK -> V
NV -> H
SV -> F
NC -> P
OF -> V
NS -> V
PF -> N
HN -> K
BS -> S
NK -> H
PC -> O"""
    main(EXAMPLE)
    # main(INPUT)
