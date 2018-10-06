#! /usr/bin/env python3

"""
List all Firefox tabs with title and URL
Supported input: json or jsonlz4 recovery files
output is in HTML form with tabs.html name
"""

import sys
import pathlib
import lz4.block
import json
import fileinput
import re

# Initiating HTML creator for making a simple UI
class HtmlCreater:

    # Initiate header
    def header(self):
        hwrapper ="""<html lang="en">
        <head>
        <meta charset="utf-8">
        <title>Tabs list</title>
        <center>
        <div class="col-md-3"><h1>LIST OF TABS</h1></div> 
        </center>
        <hr></hr>
        <hr></hr>
        <h3>Mozila</h3>
        """
        return hwrapper

    # Initiate main part of html form that includes
    # Title of site, URL, Open and Delete button
    def content(self, siteheader, url, id):
        cwrapper = "<div class=\"col-md-4\" >\n" \
                   + "<ul>\n"\
                   + "<li id=0" + str(id) + "><font color=\"green\">" + siteheader + "</font></li>\n"\
                   + "</ul>\n"\
                   + "</div>"\
                   + "<form action = \"http://127.0.0.1/cgi-bin/linkrm.py\" method = \"post\" target = \"_self\">"\
                   + "<input type = \"hidden\" name = \"link\" value = \"" + url + "\" /> \n" \
                   + "<input type = \"hidden\" name = \"header\" value = \"" + siteheader + "\" />\n" \
                   + "<input type = \"hidden\" name = \"id\" value = \"" + str(id) + "\" />\n" \
                   + "<button id=" + str(id) + " onclick=\"window.open('" + url + "','_blank');\" type=\"button\">Open</button>\n" \
                   + "<input type = \"submit\" value = \"Delete\" />\n" \
                   + "</form>\n"\
                   + "<hr></hr>"
        return cwrapper

    # Initiate footer for closing main tags
    def footer(self):
        fwrapper ="""</head>
        </html>
        """
        return fwrapper

# If file is empty call header_builder
# for writing header
def file_not_exist(html_path):
    with open(html_path, 'r+') as tab:
        file = tab.readlines()
        if not file:
            header_builder()
        else:
            print("There is sum lines in the file that you should delete")

# Writing Header
def header_builder(html_path):
    hc = HtmlCreater()
    with open(html_path, 'w') as tab:
        tab.write(hc.header())

"""
 For writing main content first you
 need to remove footer after main
 content inserted you need to append
 footer at last.
"""
def footer_remover(html_path):
    r1 = r'(</he.*>)'
    r2 = r'(</ht.*>)'
    global pattern1
    global pattern2
    # Open file finding footer patterns
    with open(html_path, 'r') as tab:
        lines = tab.readlines()
        for line in lines:
            if re.search(r1, line):
                for item in re.findall(r1, line):
                    pattern1 = item
            elif re.search(r2, line):
                for item in re.findall(r2, line):
                    pattern2 = item
            else:
                pattern1 = None
                pattern2 = None
    # Finding lines that match with patterns
    # and replace delete them
    if pattern1 != None or pattern2 != None:
        with fileinput.FileInput(html_path, inplace=True) as file_:
            for line in file_:
                l = line.strip("\n").strip()
                if l == pattern1:
                    print(line.replace(line, ""))
                elif l == pattern2:
                    print(line.replace(line, ""), end="\n")
                else:
                    print(line, end="")
    else:
        pass
"""
Reading tabs database file and
writing them on the html file
with a simple design 
"""
def tabdumper(html_path):
    # Remove footer
    footer_remover(html_path)

    # Finding mozilla recovery db
    path = pathlib.Path.home().joinpath('.mozilla/firefox')
    files = path.glob('*default*/sessionstore-backups/recovery.js*')

    # Made an instance from HTML class and call footer for end
    hc = HtmlCreater()
    foot = hc.footer()

    # Extracting mozilla db, loading them in the
    # json form, finding tabs and write them in
    # tabs.html file
    with open (html_path, 'a') as tab:
        for f in files:
            b = f.read_bytes()
            if b[:8] == b'mozLz40\0':
                 b = lz4.block.decompress(b[8:])
            j = json.loads(b)
            for w in j['windows']:
                for index,t in enumerate(w['tabs']):
                    i = t['index'] - 1
                    tab.write(hc.content(str(t['entries'][i]['title'],),str(t['entries'][i]['url']), index) + "\n")
            tab.write(foot)


if __name__ == '__main__':
    # Path of tabs.html
    html_path = sys.argv[1]

    file_not_exist(html_path)
    tabdumper(html_path)
