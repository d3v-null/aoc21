# all scalars start at zero, and all arrays start at []
# whether or not you declare them.
# a window of 4 is needed to contain two sliding windows of 3 offset by 1:
#
# 199 A
# 200 A B
# 208 A B
# 210   B
#
# the first sliding window, A contains 199, 200, 208, 𝚺=607
# the second sliding window, B contains 200, 208, 210, 𝚺=618
# r += 𝚺A < 𝚺B  # (which is true = 1)
# then we shift the buffer to the left
#
# 200 B
# 208 B C
# 210 B C
# 200   C
#
# the first sliding window, B contains 200, 208, 210 𝚺=618
# the second sliding window, C contains 208, 210, 200 𝚺=618
# r += 𝚺A < 𝚺B  # (which is true = 1)

# now the total r = 1

#
# {
#     # < DEBUG
#     print "\nstart",NR,$0
#     for(i in b) print "start b[",i,"]=",b[i];
#     print "start i",i+0
#     # > DEBUG

#     # shift the buffer to the left
#     for(i in b) {
#         # if(i>=0) b[i-1]=b[j]
#         # b[i]=b[i+1]
#         # if (i+1<NR) b[i]=b[i+1]
#         if (i>1) b[i-1]=b[i]
#         # print "for i",i,"in b. b[i]", b[i]," = ",b[i+1]
#         print "for i",i,"in b. b[i]",b[i]
#     }
#     # i=NR<4
#     # b[NR<4?NR:4]=
#     # b[i<2?i+1:0]=$0
#     b[i+1]=$0
#     print "b[i+1",i+1,"]=",$0
#     print "i",i
#     if (i>3) {
#         s1= b[0] + b[1] + b[2];
#         s2= b[1] + b[2] + b[3];
#         r+= s1<s2;
#         print "s1",s1,"s2",s2,"r",r
#     }

#     # < DEBUG
#     print "end",$0
#     for(i in b) print "end b[",i,"]=",b[i];
#     print "end i",i+0
#     # > DEBUG
# } END {
#     print r
# }


# {b[NR]=$0;c=NR-3}(c>0){r+=b[c+0]+b[c+1]+b[c+2]<b[c+1]+b[c+2]+b[c+3]}END{print r}

# {b[NR]=$0;c=NR-3}(c>0){
#     m=b[c+1]+b[c+2];
#     r+=b[c+0]+m<m+b[c+3]
# }END{print r}

# {b[NR]=$0;c=NR-3}(c>0){r+=b[c+0]<b[c+3]}END{print r}
# {b[NR]=$0}(NR>3){r+=b[NR-3]<b[NR]}END{print r}
{b[NR]=$0}(NR>3){r+=b[NR-3]<$0}END{print r}
# this doesn't work:
# {b[NR]=$0}{r+=b[NR-3]<$0}END{print r}


# Combined
# {d=c;c=b;b=a;a=$0}NR>1{s+=b<a}NR>3{r+=d<a}END{print r,s}
{d=c;c=b;b=a;a=$0}b{s+=b<a}d{r+=d<a}END{print r,s}

# To beat:
# sum((x<y)+1j*(x<z) for x,y,z in zip(a,a[1:],a[3:]))

# {d=c;c=b;b=a;a=$0}d{r+=d<a}END{print r}

# p{s+=p<$0}{p=$0}END{print s}

# {d=c;c=b;b=a}d{r+=d<$0}{a=$0}END{print r}
{d=c;c=b;b=a}b{s+=b<$0}d{r+=d<$0}{a=$0}END{print r,s}
