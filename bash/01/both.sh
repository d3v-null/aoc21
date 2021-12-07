#!/bin/bash
# curl -b$c https://adventofcode.com/2021/day/1/input | awk '{r+=p<$0;p=$0}END{print r}'

# curl -b$c https://adventofcode.com/2021/day/1/input >i
# awk '{r+=p<$0;p=$0}END{print r}' i
# awk '{b[NR]=$0}(NR>3){r+=b[NR-3]<$0}END{print r}' i

# curl -b$c https://adventofcode.com/2021/day/1/input | awk '{b[NR]=$0}(NR>1){s+=b[NR-1]<$0}(NR>3){r+=b[NR-3]<$0}END{print s,r}'

# final final final
curl -Lb$c adventofcode.com/2021/day/1/input | awk 'b{s+=b<$0}d{r+=d<$0}{d=c;c=b;b=$0}END{print s,r}'
