#! /usr/bin/env python3
import cgi, cgitb
import re

""" 
delete action when
clicking on Delete Button
"""

def link_remover():
    # Make an instance from Field Storage of CGI
    form = cgi.FieldStorage()
    # After deleting, page should redirect to the main page
    redirectURL = "/tabs.html"

    # Variables should be defined
    # variables for pattern1, 2, 3, 4 and
    # for id of button and title
    rx1 = ""
    rx2 = ""
    rx3 = ""
    rx4 = ""
    id = ""

    # If submit the key and an id returned
    if form.getvalue('id'):
        id = form.getvalue('id')

    # Finding patterns that we want delete
    r1 = r'(<li id=0' + str(id) + '.*</li>)'
    r2 = r'(<button id=' + str(id) + ' .*</button>)'
    r3 = r'(<input type = "submit" value = "Delete" />)'
    r4 = r'<hr></hr>'

    # Checking html file and finding target patterns
    with open('/var/www/html/tabs.html', 'r') as file1:
        lines = file1.readlines()
        for line in lines:
            if re.search(r1, line):
                for item in re.findall(r1, line):
                    rx1 = item
            elif re.search(r2, line):
                for item in re.findall(r2, line):
                    rx2 = item
            elif re.search(r3, line):
                for item in re.findall(r3, line):
                    rx3 = item
            elif re.search(r4, line):
                for item in re.findall(r4, line):
                    rx4 = item

    # Opening the same html file for deleting lines
    # that match with patterns
    with open('/var/www/html/tabs.html', 'w') as file2:
        try:
            lines = iter(lines)
            for line in lines:
                if line.strip("\n").strip() == rx1:
                    line = next(lines)
                    file2.write(line)
                elif line.strip("\n").strip() == rx2:
                    line = next(lines)
                    if line:
                        line = next(lines)
                        file2.write(line)
                        line = next(lines)
                        if line:
                            if line.strip("\n").strip() == rx3:
                                line = next(lines)
                                file2.write(line)
                                line = next(lines)
                                if line:
                                    if line.strip("\n").strip() == rx4:
                                        line = next(lines)
                                        file2.write(line)
                                    else:
                                        file2.write(line)
                                else:
                                    file2.write(line)
                else:
                    file2.write(line)
        except Exception as e:
            print(e)

    # Redirecting page to main tabs.html
    # after deleting patterns
    print()
    print('Location: %s' % redirectURL)
    print('<html>')
    print('  <head>')
    print('    <meta http-equiv="refresh" content="0;url=%s" />' % redirectURL)
    print('    <title>You are going to be redirected</title>')
    print('  </head>')
    print('  <body>')
    print('    Redirecting... <a href="%s">Click here if you are not redirected</a>' % redirectURL)
    print('  </body>')
    print('</html>')


if __name__ == '__main__':

    # Header for figuring this is a
    # CGI file by browser
    print("Content-type: text/html\r\n\r\n")

    # For debugging
    # cgitb.enable(format='text')

    link_remover()


