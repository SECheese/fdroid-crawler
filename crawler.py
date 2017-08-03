import AdvancedHTMLParser as AdvancedHTMLParser
import urllib


def crawl(address):
    response = urllib.urlopen(address)
    html_of_the_page = response.read()

    html_parser = AdvancedHTMLParser.AdvancedHTMLParser()

    html_parser.parseStr(html_of_the_page)

    package_class = html_parser.getElementsByClassName('package')
    links = package_class[0][3]

    link_dic = {}
    link_dic[address] = {}

    for i in range(1, len(links.children), 3):
        link_dic[address][links[i - 1].text] = links[i].__getattribute__('href')

    wiki_address = package_class[0][4][0].__getattribute__('href')
    package_version_class = html_parser.getElementsByClassName('package-versions-list')
    version_dic = {}
    version_dic[address] = []

    for i in range(len(package_version_class[0].children)):
        version_dic[address] += [{}]
        package_version_header_class = package_version_class[0][i].getElementsByClassName("package-version-header")
        version = package_version_header_class[0][0].text.split()
        added_on = package_version_header_class[0].text.split()

        n = len(added_on[5])
        added_on[5] = added_on[5][0: n - 1]
        added_on = str(added_on[4]) + "-" + str(added_on[5]) + "-" + str(added_on[6])

        # TODO addedOn split
        package_version_permission_class = package_version_class[0][i].getElementsByClassName(
            "package-version-permissions")
        permission_list = []
        for j in range(len(package_version_permission_class[0][1].children)):
            permission_list += [package_version_permission_class[0][1][j].text.split()[0]]

        package_version_source = package_version_class[0][i].getElementsByClassName("package-version-source")
        source_tarball = package_version_source[0][0].__getattribute__('href')
        package_version_download = package_version_class[0][i].getElementsByClassName("package-version-download")
        apk_address = package_version_download[0][0].__getattribute__('href')
        pgp_signature = package_version_download[0][1].__getattribute__('href')
        package_version_requirement = package_version_class[0][i].getElementsByClassName("package-version-requirement")
        requirement_version = package_version_requirement[0].text.split()[4]

        version_dic[address][i]['version'] = version
        version_dic[address][i]['addedOn'] = added_on
        version_dic[address][i]['permissionsList'] = permission_list
        version_dic[address][i]['sourceTarball'] = source_tarball
        version_dic[address][i]['apkAddress'] = apk_address
        version_dic[address][i]['pgpSignature'] = pgp_signature
        version_dic[address][i]['requirementVersion'] = requirement_version

    return link_dic, wiki_address, version_dic


main_url = 'https://f-droid.org/'

parser = AdvancedHTMLParser.AdvancedHTMLParser()

response = urllib.urlopen(main_url + '/packages/')
html = response.read()
parser.parseStr(html)
browse_navigation_class = parser.getElementsByClassName("browse-navigation")

pageCount = int(browse_navigation_class[0][-2][0].text)
for page in range(1, pageCount + 1):
    if page == 1:
        response = urllib.urlopen(main_url + '/packages/')
    else:
        response = urllib.urlopen(main_url + '/packages/' + str(page))
    html = response.read()
    parser.parseStr(html)
    post_content_class = parser.getElementsByClassName("post-content")
    package_header_class = post_content_class.getElementsByClassName("package-header")
    url_size = len(package_header_class)
    for i in range(url_size):
        crawl(main_url + package_header_class[i].__getattribute__('href'))
        # TODO saving the output in a data set
