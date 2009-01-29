#!/usr/bin/awk -f 
# 
# SQL Embedder
# 
# Wraps SQL statements so that they become string literals
# in various languages. You sometimes have to do that, and
# it's probably the most boring part of low-level database
# development.
# 
# Parameters
#   language - select the output language, takes values
#               'java', 'php'; Java is the default
#   prefix - include this string before each output line
#   indent - include indentation in the output strings 
#               (i.e. output "\tselect *\n"), takes values
#               'true'/'false' or 'yes'/'no'
#   replace - if the specified token is found, replace it 
#               with the specified string, it takes the
#               following syntax:
#                   "p0->s0,...,pn->sn"
#                   p0-pn are placeholders and s0-sn are
#                   substitutions. Placeholders cannot 
#                   contain any whitespaces and they are
#                   treated as POSIX regular expressions.
#               (i.e. to insert the string 'joe' for '$':
#                   "$->joe" 
#                it's really easier than it looks)
#   rule_separator - modify the rule separator of the 
#               'replace' clause; comma by default
#   implication - modify the rule implication of the 
#               'replace' clause; '->' by default
#
# Author
#   Konrad Siek

# Do all those tedious pre-op things
BEGIN {

    # Select language and define tokens
    if (language == "java" || language == "") {
        # Java (acts as default settings)
        STRING_TOKEN = "\""
        CONCATENATION_TOKEN = "+"
        INSTRUCTION_TERMINATOR = ";"
    } else if (language == "php") {
        # PHP
        STRING_TOKEN = "\""
        CONCATENATION_TOKEN = "."
        INSTRUCTION_TERMINATOR = ";"
    } else {
        print "Unsupported language: " language
        exit
    }

    # Rename the variables
    OUTPUT_INDENTATION = (indent ~ /(true|yes)/)
    PREFIX = prefix

    # Initiate rule separator
    if (rule_separator == "") {
        RULE_SEPARATOR = ","
    } else {
        RULE_SEPARATOR = rule_separator
    }
    
    # Initiate separators within rules
    if (implication == "") {
        IMPLICATION = "->"
    } else {
        IMPLICATION = implication
    }

    # Initialize replacement table
    if (length(replace) > 0) {
        split(replace, rules, RULE_SEPARATOR)
        for (r in rules) {
            split(rules[r], a, IMPLICATION)
            key = a[1]
            value = a[2]
            REPLACEMENTS[key] = value
        }                 
    }
}

# Print terminator
END {
    print INSTRUCTION_TERMINATOR
}

# Ignore empty lines
/^[ \t]*$/ {
    next
}

# Concatenate previous line to this one
NR > 1 {
    printf("%s\n", CONCATENATION_TOKEN)
    indentation = ""
    if (OUTPUT_INDENTATION) {
        code_indentation = ""
    }
}

# Mimic original indentation
/^[ \t]+/ {
    line_length = length($0)
    for(i = 1; i < line_length; i++) {
        char = substr($0, i, i)
        if (char ~ /^[ \t]*$/) {
            indentation = indentation char
            if (OUTPUT_INDENTATION) {
                if(indentation == "\t") {
                    code_indentation = code_indentation "\\t"
                } else {
                    code_indentation = code_indentation char
                }
            }
        } else {
            break;
        }
    }
}

# Print a line of the statement word-by-word
{
    printf("%s", PREFIX)
    printf("%s", indentation)
    printf("%s", STRING_TOKEN)
    if (OUTPUT_INDENTATION) {
        printf("%s", code_indentation)    
    }        
    for (i = 1; i <= NF; i++) {
        word = $i
        for (p in REPLACEMENTS) {
            s = REPLACEMENTS[p]
            gsub(p, s, word)
        }
        printf("%s ", word)
    }
    if (OUTPUT_INDENTATION) {
        printf("\\n")
    }
    printf("%s ", STRING_TOKEN)    
}
