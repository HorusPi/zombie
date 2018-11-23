import contextlib

from RRLStory.RoyalRoad import Story, Chapter

log_file = open("chrome_logs.log", 'a')
s = None

with contextlib.redirect_stdout(log_file):
    s = Story("https://www.royalroad.com/fiction/8894/everybody-loves-large-chests")

story_file = open(s.title.replace(" ", "-") + ".html", 'w',encoding="utf-8")
story_file.write("<h1>" + s.title + "</h1>\n")

for chap in s.chaptersUrl:
    c = Chapter(chap[1])
    print(c.title)
    story_file.write("<div>\n")
    story_file.write("<h2>" + c.title + "</h2>\n")
    story_file.write(c.content.text.replace('\n','<br />\n'))
    #story_file.write(c.content.text)
    story_file.write("</div>\n")
story_file.close()