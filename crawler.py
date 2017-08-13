import AdvancedHTMLParser as AdvancedHTMLParser
import urllib

from datetime import datetime
from pymongo import MongoClient


def insert_to_database(collection, document):
    if (collection.find({"_id": document['_id']}).count() == 0):
        print(collection.insert_one(document).inserted_id + " has been inserted to db")
    else:
        old = collection.find_one({"_id": document['_id']})
        # merge older versions with new one
        old_versions = old.get('versions')
        old_versions.update(document.get('versions'))
        # merge older links with new one
        old_links = old.get('links')
        old_links.update(document.get('links'))
        print(str(collection.update({"_id": document['_id']}, {"$set": {"versions": old_versions, "links": old_links}},
                                    upsert=True)) + " id: " + str(document.get('_id')))


def get_description(package_class):
    description = ""
    package_description = package_class.getElementsByClassName("package-description")
    for description_part in package_description[0].children:
        description += str(description_part)
    return description


def get_links(package_class):
    links = package_class[0][3]
    wiki_address = package_class[0][4][0].__getattribute__('href')
    link_dic = {"wiki": wiki_address}
    for i in range(1, len(links.children), 3):
        link_dic[links[i - 1].text] = links[i].__getattribute__('href')
    return link_dic


def get_version_info(package_version_class):
    version_dic = {}

    for package_version in package_version_class[0].children:
        package_version_header_class = package_version.getElementsByClassName("package-version-header")
        version = str(package_version_header_class[0][0].text.split()[1])
        added_on = package_version_header_class[0].text.split()

        version = version.replace('.', '_')
        n = len(added_on[5])
        added_on[5] = added_on[5][0: n - 1]
        added_on = str(added_on[4]) + " " + str(added_on[5]) + " " + str(added_on[6])
        added_on = datetime.strptime(added_on, '%b %d %Y')

        package_version_permission_class = package_version.getElementsByClassName(
            "package-version-permissions")
        permission_list = []
        for j in range(len(package_version_permission_class[0][1].children)):
            permission_list += [package_version_permission_class[0][1][j].text.split()[0]]

        package_version_source = package_version.getElementsByClassName("package-version-source")
        source_tarball = package_version_source[0][0].__getattribute__('href')
        package_version_download = package_version.getElementsByClassName("package-version-download")
        apk_address = package_version_download[0][0].__getattribute__('href')
        pgp_signature = package_version_download[0][1].__getattribute__('href')
        package_version_requirement = package_version.getElementsByClassName("package-version-requirement")
        required_version = package_version_requirement[0].text.split()[4]
        required_version = required_version.replace('.', '_')

        version_dic[version] = {}
        version_dic[version]['version'] = version
        version_dic[version]['addedOn'] = added_on
        version_dic[version]['permissionsList'] = permission_list
        version_dic[version]['sourceTarball'] = source_tarball
        version_dic[version]['apkAddress'] = apk_address
        version_dic[version]['pgpSignature'] = pgp_signature
        version_dic[version]['requirementVersion'] = required_version


def crawl(address):
    response = urllib.urlopen(address)
    html_of_the_page = response.read()

    html_parser = AdvancedHTMLParser.AdvancedHTMLParser()

    html_parser.parseStr(html_of_the_page)

    # All data about app are in 'package' class
    package_class = html_parser.getElementsByClassName('package')

    description = get_description(package_class)
    links = get_links(package_class)

    # All data about app versions are in 'package-version-class' class
    package_version_class = html_parser.getElementsByClassName('package-versions-list')
    version_dic = get_version_info(package_version_class)

    document = {'_id': address.split('/')[-1], 'description': description, 'links': links, 'versions': version_dic}
    return document


main_url = 'https://f-droid.org/'

parser = AdvancedHTMLParser.AdvancedHTMLParser()

# database connection
# login information can be passed to MongoClient
print("Waiting for mongodb connection")
client = MongoClient()
print("MongoClient connected successfully")
db = client.fdroid
apps = db.apps

crawl("https://f-droid.org/packages/org.adw.launcher/")

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
        document = crawl(main_url + package_header_class[i].__getattribute__('href'))
        insert_to_database(apps, document)
