import zipfile, re, urllib, os, sys, json, time, requests, json

# constants
noZip = 'No zip or not zip either way exitting....'
dimensions = [[84,74],[50,50],[40,40],[400,400],[328,278],[300,300]]
imageFolder = 'images'
#
tunnelName = 'default'
tunnels = ['http://localhost:4040/api/tunnels/default%20%28http%29', 'http://localhost:4040/api/tunnels/default']

# note if foldersOnly is True it will override imgOnly
def getFilePaths(fileZip, filename, imgOnly=False, foldersOnly=False):
    # root = re.compile(filename.split('.')[0])
    hiddenroot = re.compile('__MACOSX')
    imgRe = re.compile('\.(png|gif|jpe?g)') if imgOnly else ''
    if foldersOnly:
        return [path for path in fileZip.namelist() if not re.match(hiddenroot, path) and path[-1] is '/']
    return [path for path in fileZip.namelist() if not re.match(hiddenroot, path) and re.search(imgRe, path)]

def getZip(filename):
    return zipfile.ZipFile(filename, 'r') if zipfile.is_zipfile(filename) else None

def getCropURL(imgURL, width, height, cropType='sc', poi='face'):
    return 'http://imagesvc.timeincapp.com/?url=%s&h=%s&w=%s&c=%s&poi=%s'%(imgURL, height, width, cropType, poi)

def downloadImg(url, name=None, noPath=False, root=imageFolder):
    if noPath:
        name = name.split('/')[-1] if name and name.split('/')[-1] else url.split('/')[-1]
    # add extension (guessing) if there isnt any
    name+= '.' + re.findall(re.compile('(png|gif|jpe?g)'), url)[-1] if not re.search(re.compile('\.(png|gif|jpe?g)'), name) else ''
    urllib.urlretrieve(url, filename=(root + '/' + name))
    return 'Downloaded %s' %(url)

def extractZip(fileZip, imgs=None):
    fileZip.extractall(members=imgs, path=imageFolder+'/')
    return True #should change this to try catch

# not used but useful if you need to make empty folders of paths
def makePath(filePath, pathRoot=''):
    filePath = pathRoot + filePath
    if not os.path.isdir(filePath):
        os.makedirs(filePath)
    else:
        return 'exist already'

# add to the name before the extension for example makeNewName(cat.jpg, 4x4) -> cat4x4.jpg
def makeNewName(imgName, conc):
    name = imgName.split('.')
    if len(name) < 2:
        return  imgName
    else:
        imgName= ''.join(x for x in name[:-1]) + conc + '.' + name[-1]
    return imgName

def zipList():
    zips = []
    for file in os.listdir(os.getcwd() + '/' +imageFolder):
        if file.endswith(".zip"):
            zips.append(os.path.join(imageFolder, file))
    # os.chdir(os.getcwd() + '/' +imageFolder) #cd so extract will happen here
    return zips

def refreshBaseURL():
    tunnels = json.loads(requests.get('http://localhost:4040/api/tunnels').text)['tunnels']
    for tunnel in tunnels:
        requests.delete('http://localhost:4040' + tunnel['uri'].replace('+','%20'))
    r = requests.post('http://localhost:4040/api/tunnels', json={'addr':'8080','proto':'http','name':'default'})
    return json.loads(r.text)['public_url'] + '/'

def main():
    baseURL = refreshBaseURL(True)
    refresh = 0
    zips = zipList() if zipList() else sys.exit('No Zips Found')
    for filename in zipList():
        # first make zipfile object and get img filepaths
        zipFile = getZip(filename) if getZip(filename) != None else sys.exit(noZip)
        imgPaths = getFilePaths(zipFile, filename.split('/')[-1], True)
        folderPaths = getFilePaths(zipFile, filename.split('/')[-1], foldersOnly=True)
        # extract images
        print 'done extract' if extractZip(zipFile, imgPaths) else 'not done'
        # crop images and download
        for img in imgPaths:
            for w, h in dimensions:
                newNameAdd = '-' + str(w) + 'x' + str(h)
                downloadImg( getCropURL((baseURL + imageFolder + '/'+ img), w, h), makeNewName(img, newNameAdd))
                refresh+=1
                print 'refresh ' + str(refresh)
                if refresh == 20:
                    refresh = 0
                    baseURL = refreshBaseURL()
                    print baseURL
                    time.sleep(3) #avoid  'Too many'
        print 'FINALLY DONE CROPPING'


# main()
def test():
    print 'starttt'
    '''
    this wont work to avoid overflow session. this does not reset session id! darn
    that is why there is a time.sleep
    '''
    while True:
        url = refreshBaseURL()
        print 'change ' + url
        for i in range(0, 21):
            print i
            urllib.urlretrieve(url,'images/'+str(i) + '.junk')
            time.sleep(2)

test()
