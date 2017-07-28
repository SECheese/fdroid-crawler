import AdvancedHTMLParser as AdvancedHTMLParser
import urllib

def crawl(address):
    response = urllib.urlopen(address)
    html = response.read()

    parser = AdvancedHTMLParser.AdvancedHTMLParser()

    # Parse an HTML string into the document

    parser.parseStr(html)
    # print(parser.getHTML())
    # Parse an HTML file into the document

    # parser.parseFile("index.php")
    temp = parser.getElementsByClassName('package')
    temp2 = temp[0][3]

    linkDic = {}
    linkDic[address] = {}

    for i in range(1, len(temp2.children), 3):
        linkDic[address][temp2[i-1].text] = temp2[i].__getattribute__('href')
    temp2 = temp[0][4]
    print(temp2[0].__getattribute__('href'))
    temp = parser.getElementsByClassName('package-versions-list')
    versionDic = {}
    versionDic[address] = []

    for i in range(len(temp[0].children)):
        versionDic[address] += [{}]
        temp2 = temp[0][i].getElementsByClassName("package-version-header")
        version = temp2[0][0].text.split()
        addedOn = temp2[0].text.split()
        # TODO addedOn split
        temp2 = temp[0][i].getElementsByClassName("package-version-permissions")
        permissionList = []
        for j in range(len(temp2[0][1].children)):
            permissionList += [temp2[0][1][j].text.split()[0]]

        temp2 = temp[0][i].getElementsByClassName("package-version-source")
        sourceTarball = temp2[0][0].__getattribute__('href')
        temp2 = temp[0][i].getElementsByClassName("package-version-download")
        apkAddress = temp2[0][0].__getattribute__('href')
        pgpSignature = temp2[0][1].__getattribute__('href')
        temp2 = temp[0][i].getElementsByClassName("package-version-requirement")
        requirementVersion = temp2[0].text.split()[4]

        versionDic[address][i]['version'] = version
        versionDic[address][i]['addedOn'] = addedOn
        versionDic[address][i]['permissionsList'] = permissionList
        versionDic[address][i]['sourceTarball'] = sourceTarball
        versionDic[address][i]['apkAddress'] = apkAddress
        versionDic[address][i]['pgpSignature'] = pgpSignature
        versionDic[address][i]['requirementVersion'] = requirementVersion

main_url = 'https://f-droid.org/'

parser = AdvancedHTMLParser.AdvancedHTMLParser()

response = urllib.urlopen(main_url + '/packages/')
html = response.read()
parser.parseStr(html)
temp = parser.getElementsByClassName("browse-navigation")

pageCount = int(temp[0][-2][0].text)
for page in range (1, pageCount + 1):
    if page == 1:
        response = urllib.urlopen(main_url + '/packages/')
    else:
        response = urllib.urlopen(main_url + '/packages/' + str(page))
    html = response.read()
    parser.parseStr(html)
    temp = parser.getElementsByClassName("post-content")
    temp = temp.getElementsByClassName("package-header")
    url_size = len(temp)
    print(url_size)
    for i in range(min(30, url_size)):
crawl(main_url + temp[i].__getattribute__('href'))
