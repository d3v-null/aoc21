# $1~/^d/{d+=$2;a+=$2}$1~/^u/{d-=$2;a-=$2}$1~/^f/{p+=$2;q+=a*$2}END{print p*d,p*q}
/d/{d+=$2;a+=$2}/u/{d-=$2;a-=$2}/f/{p+=$2;q+=a*$2}END{print p*d,p*q}
