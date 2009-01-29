#!/usr/bin/awk -f
#
# Gallerizer
#
# Create an extremely simple gallery, with places to insert 
# descriptions, or even insert descriptions on the fly with 
# the bash read command or zenity.
# 
# Parameters
#   interactive: 'yes' or 'true' turns on the interctive
#               mode with zenity input windows.
# Requires
#   zenity (for displaying dialogs in interactive mode)
# Author
#   Konrad Siek

# Print HTML header
BEGIN {
    print "<html>"
    print "\t<head>"
    print "\t\t<title>"title"</title>"
    print "\t\t<style>"
    print "\t\t\tbody {"
    print "\t\t\t\ttext-align: center;"
    print "\t\t\t}"
    print "\t\t\tp {"
    print "\t\t\t\tmargin-bottom: 50px;"
    print "\t\t\t}"
    print "\t\t</style>"
    print "\t</head>"
    print "\t<body>"
    if (title !~ /^[ \t\n]*$/) {
        print "\t\t<h1>"title"</h1>"
    }

    is_interactive = interactive ~ /^(yes|true)$/
}

# Print HTML footer
END {
    print "\t</body>"
    print "</html>"
}

# Ignore all temporary (files ending in '~')
/~$/ {
    next;
}

# Include all PNG or JPG files as images
/\.(png|PNG|jpg|JPG)$/    {
    print "\t\t<img id=\""$0"\" src=\""$0"\" alt=\""$0"\" />"
    print "\t\t<p>";    
    # Prompt for description in interactive mode
    if (is_interactive) {
        printf("\t\t\t")
        r = system("zenity --entry --title=\""$0"\"")
        if (r != 0) {
            printf("\n")
        }
    }
    print "\t\t</p>";    
    # Kill off the script on cancel
    if(r != 0 && is_interactive) {
        exit
    }
}
