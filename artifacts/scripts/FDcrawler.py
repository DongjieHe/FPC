#!/usr/bin/python3
import os, requests
from html.parser import HTMLParser

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
FDROID_HOST = "https://f-droid.org"

CATEGORIES = ['connectivity', 'development', 'games',
              'graphics', 'internet', 'money', 'multimedia',
              'navigation', 'phone-sms', 'reading',
              'science-education', 'security', 'sports-health',
              'system', 'theming', 'time', 'writing',]
NAV_MAP = {
    'connectivity': 9,
    'development': 6,
    'games': 14,
    'graphics': 3,
    'internet': 21,
    'money': 4,
    'multimedia': 16,
    'navigation': 8,
    'phone-sms': 4,
    'reading': 8,
    'science-education': 11,
    'security': 7,
    'sports-health': 6,
    'system': 21,
    'theming': 6,
    'time': 7,
    'writing': 8
}

def naviLists(category):
    navCnt = NAV_MAP[category]
    ret = []
    for i in range(1, navCnt + 1):
        if i != 1:
            url = os.path.join(FDROID_HOST, "en", "categories", category, str(i), "index.html")
        else:
            url = os.path.join(FDROID_HOST, "en", "categories", category, "index.html")
        ret.append(url)
    return ret

class FDroidPackageCollector(HTMLParser):
    def __init__(self):
        # super().__init__()
        HTMLParser.__init__(self)
        self.packages = []

    def handle_starttag(self, tag, attrs):
        if tag != "a" or len(attrs) != 2:
            return
        if attrs[0][0] != "class" or attrs[0][1] != "package-header":
            return
        pkg = attrs[1][1]
        self.packages.append(pkg)

    def getPackages(self):
        return self.packages

def packageList(navpage):
    r = requests.get(navpage)
    parser = FDroidPackageCollector()
    parser.feed(r.text)
    return parser.getPackages()

class FDroidAppUrlCollector(HTMLParser):
    def __init__(self):
        # super().__init__()
        HTMLParser.__init__(self)
        self.downloadUrl = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        if len(attrs) != 1:
            return
        attr = attrs[0]
        if len(attr) != 2:
            return
        if attr[0] != "href":
            return
        if not attr[1].endswith('.apk'):
            return
        self.downloadUrl.append(attr[1])

    def getDownloadUrls(self):
        return self.downloadUrl

def appDownloadURL(app):
    r = requests.get(app)
    parser = FDroidAppUrlCollector()
    parser.feed(r.text)
    return parser.getDownloadUrls()[0]

def downlaodApp(appUrl, saveToDir, fileName):
    r = requests.get(appUrl, allow_redirects = True)
    if not os.path.exists(saveToDir):
        os.makedirs(saveToDir)
    open(os.path.join(saveToDir, fileName), 'wb').write(r.content)

def crawlFlowDroid():
    for category in CATEGORIES:
        navilist = naviLists(category)
        for navpage in navilist:
            packages = packageList(navpage)
            for pkg in packages:
                app = FDROID_HOST + pkg
                appUrl = appDownloadURL(app)
                print("start downloading " + appUrl)
                downlaodApp(appUrl, os.path.join(CURRENT_DIR, "FDroid", category), appUrl.split("/")[-1])
                print("finish downloading " + appUrl)

# Main
if __name__ == '__main__':
    # print(naviLists('time'))
    # navpage = 'https://f-droid.org/en/categories/time/index.html'
    # print(packageList(navpage))
    # app = "https://f-droid.org/en/packages/com.nextcloud_cookbook_flutter/"
    # print(appDownloadURL(app))
    # appUrl = "https://f-droid.org/repo/com.nextcloud_cookbook_flutter_21.apk"
    # downlaodApp(appUrl, "/home/hedj/xx/", "xxx.apk")
    crawlFlowDroid()