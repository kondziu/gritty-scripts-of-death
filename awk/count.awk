#!/usr/bin/awk -f
{
    for (i = 1; i <= NF; i++) {
        word = $i;
        #insert punctuation here, between the square brackets.
        n = split(word, a, /[-,.?!~`';:"'|\/@#$%^&*_-+={}\[\]<>()]+/); 
        for (j = 1 ; j <= n; j++) {
            if (a[j] !~ /^[ \t\n]*$/) {                
                words++;
            }
        }
    }
}

BEGIN {
    words = 0;
}

END {
    print words;
}
