#!/usr/bin/awk -f
#
# Creates a GPL comment (in proper comment characters
# for a given language), including the name of the 
# program, which the file is supposed to be a part of
# in the proper place.
#
# Supported languages include:
#   - XML, HTML,
#   - C, C++, Java, Javascript,
#   - Bash, Python, Ruby, AWK,
#   - ML, Ocaml,
#   - TeX, LaTeX,
#   - SQL.
# Parameters:
#   program - name of the program main program
#   language - language to generate comment for
#   name - author of the program
#   date - copyright date
#   attach - file to append to comment
# Standard input - the template of the comment, where:
#   $name is replaced with the value of name
#   $date is replaced with the value of date
#   $program is replaced with program name
# Author:
#   Konrad Siek

# Add style definition for language to global styles.
function add_style(languages, style) {
    for (l in languages) {
        for (s in style) {
            styles[l,s]=style[s];
        }
    }
}

BEGIN {
    # Variables
    begin="begin";
    line="line";
    end="end";
    SUBSEP="~";

    # Try autodetecting type by extension
    if (language == "" && attach != "") {
        split(attach, arr, /\./);
        for (i=2; i in arr; i++) {
            language=arr[i];
        }
    }

    # Define C-style comment languages
    c_style[begin]="/* ";
    c_style[line]=" * ";
    c_style[end]=" */";

    c_languages["c"];
    c_languages["c++"];
    c_languages["cpp"];
    c_languages["java"];
    c_languages["javascript"];
    c_languages["js"];

    add_style(c_languages, c_style);

    # Define Unix-style comment languages
    unix_style[begin]="# ";
    unix_style[line]="# ";
    unix_style[end]="# ";

    unix_languages["bash"];
    unix_languages["python"];
    unix_languages["ruby"];
    unix_languages["awk"];

    add_style(unix_languages, unix_style);

    # Define ML-style comment languages
    ml_style[begin]="(* ";
    ml_style[line]=" * ";
    ml_style[end]=" *)";

    ml_languages["ml"];
    ml_languages["ocaml"];
    ml_languages["caml"];

    add_style(ml_languages, ml_style);

    # Defin HTML-style comment languages
    html_style[begin]="<!-- ";
    html_style[line]="  -- ";
    html_style[end]="  --> ";

    html_languages["html"];
    html_languages["xml"];
    html_languages["svg"];

    add_style(html_languages, html_style);

    # Define TeX-style comment languages
    tex_style[begin]="% ";
    tex_style[line]="% ";
    tex_style[end]="% ";

    tex_languages["tex"];
    tex_languages["latex"];

    add_style(tex_languages, tex_style);

    # Define SQL-style comment languages
    sql_style[begin]="-- ";
    sql_style[line]="-- ";
    sql_style[end]="-- ";

    sql_languages["sql"];

    add_style(sql_languages, sql_style);

    # Select language
    language=tolower(language);

    # Print first line
    print styles[language, begin];
}

END {
    # Add final comment
    print styles[language, end];

    # Attach file if needed
    if (attach != "") {
        # Read file
        while ((r=getline < attach) > 0) {
            print $0;        
        }
        # Report error.
        if (r == -1) {
            print "Can't read '"attach"'." > "/dev/stderr";
        }
    }
}
    
{
    # Read template from standard input 
    input = $0;

    # Apply substitution to template
    gsub("\$name", name, input);
    gsub("\$date", date, input);
    gsub("\$program", program, input);            

    # Apply comments and print to output
    print styles[language, line]""input;
}
