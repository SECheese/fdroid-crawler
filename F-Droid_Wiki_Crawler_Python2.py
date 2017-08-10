from __future__ import absolute_import
import urllib2, urllib
import AdvancedHTMLParser as AdvancedHTMLParser
import lib3to2


urls = [u'com.uberspot.a2048', u'subreddit.android.appstore',
        u'de.j4velin.systemappmover', u'io.github.lonamiwebs.klooni',
        u'info.staticfree.android.twentyfourhour', u'com.twobuntu.twobuntu',
        u'nerd.tuxmobil.fahrplan.camp']
for url in urls:
    response = urllib2.urlopen(u'https://f-droid.org/wiki/page/' + url)
    html = response.read()

    parser = AdvancedHTMLParser.AdvancedHTMLParser()
    parser.parseStr(html)

    bodyDiv = parser.getElementById(u"mw-content-text")
    infoBox = bodyDiv
    for child in bodyDiv.children:
        if unicode(child.getAttribute(u'style')) == u"border: 2px solid rgb(41,93,144); background-color: rgb(167,215,249);" \
                                               u" float: right; width: 30%; border-top: solid 1px rgb(96,134,19); " \
                                               u"margin-left: 7px; margin-bottom: 10px; margin-top: 10px":
            infoBox = child

    infoBox = infoBox.children[1]
    for i in xrange(len(infoBox.children)):
        if u'href="/' in infoBox[i].innerHTML:
            data = infoBox[i].innerHTML.split()
            print data[0] + u" " + data[1]

        elif u'href="h' in infoBox[i].innerHTML:
            if u'href=' in infoBox[i].innerHTML:
                data = infoBox[i].innerHTML.split()
                data1 = infoBox[i].innerHTML.split(u"://")
                print data[0] + u" " + data1[1].split(u"\"")[0]

        else:
            print infoBox[i].innerHTML
    print
    des = bodyDiv.children
    for i in xrange(len(des)):
        if unicode(des[i].getAttribute(u'id')) == u"toc":
            j = 2
            while des[i+j].tagName != u"h1":
                print u"Description: " + des[i+j].innerHTML
                j += 1
