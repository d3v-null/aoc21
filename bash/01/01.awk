{
    r+=p<$0;
    p=$0
} END {
    print r
}

# {b=a;a=$0}b{s+=b<a}END{print s}


# p{s+=p<$0}{p=$0}END{print s}
# p{s+=p<$0}{p=$0}END{print s}

# thanks reddit

curl -Lb$c adventofcode.com/2021/day/1/input | awk 'b{s+=b<$0}d{r+=d<$0}{d=c;c=b;b=$0}END{print s,r}'
