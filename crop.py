import zipfile, re, urllib, os, sys, time

# constants
noZip = 'No zip or not zip either way exitting....'
dimensions = [[84,74],[50,50],[40,40],[400,400],[328,278],[300,300]]
imageFolder = 'images'
cropType = 'sc'
poi = 'face'
onlyResize = False
#checkout to different branch name to your own and make sure it has upstream
def getBranchName():
    with open('.git/HEAD','r') as head:
        branch = head.readline().split('/')[-1].rstrip()
        return branch if branch != 'master' else sys.exit('checkout to different branch then run again')
branchName = getBranchName()
uploadCommands = 'git add *; git commit -m "added images for cropping"; git push;'
deleteCommands = 'git rm -r --cached .; git add .; git commit -m "deleted images"; git push;'

# note if foldersOnly is True it will override imgOnly
def getFilePaths(fileZip, filename, imgOnly=False, foldersOnly=False):
    hiddenroot = re.compile('__MACOSX')
    imgRe = re.compile('\.(png|gif|jpe?g)') if imgOnly else ''
    if foldersOnly:
        return [path for path in fileZip.namelist() if not re.match(hiddenroot, path) and path[-1] is '/']
    return [path for path in fileZip.namelist() if not re.match(hiddenroot, path) and re.search(imgRe, path)]

def getZip(filename):
    return zipfile.ZipFile(filename, 'r') if zipfile.is_zipfile(filename) else None

def getCropURL(imgURL, width, height, cropType=cropType, poi=poi, onlyResize=onlyResize):
    if onlyResize:
        return 'http://imagesvc.timeincapp.com/?url=%s&h=%s&w=%s'%(imgURL, height, width)
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
# this might need more testing something about the first if is....
def makeNewName(imgName, conc):
    name = imgName.split('.')
    if len(name) < 2:
        return  imgName
    else:
        imgName= '.'.join(x for x in name[:-1]) + conc + '.' + name[-1]
    return imgName

def zipList():
    zips = []
    for file in os.listdir(os.getcwd() + '/' +imageFolder):
        if file.endswith(".zip"):
            zips.append(os.path.join(imageFolder, file))
    # os.chdir(os.getcwd() + '/' +imageFolder) #cd so extract will happen here
    return zips

def gitignoreImages(igImg):
    with open('.gitignore','r') as gitignore:
        newIgnore = gitignore.readlines()
    newIgnore[2] = 'images/*' if igImg else ' # images/*'
    with open('.gitignore','w') as gitignore:
        gitignore.writelines(newIgnore)
        gitignore.close()

def main():
    zips = zipList() if zipList() else sys.exit('No Zips Found')
    for filename in zipList():
        # first make zipfile object and get img filepaths
        zipFile = getZip(filename) if getZip(filename) != None else sys.exit(noZip)
        imgPaths = getFilePaths(zipFile, filename.split('/')[-1], True)
        # extract images and upload to github
        print 'done extract' if extractZip(zipFile, imgPaths) else 'not done'
        gitignoreImages(igImg=False)
        os.system(uploadCommands)
        print 'done upload to github'
        # crop images and download
        for img in imgPaths:
            for w, h in dimensions:
                newNameAdd = '-' + str(w) + 'x' + str(h)
                # imgURL = baseURL + imageFolder + '/'+ img
                imgURL = 'https://raw.githubusercontent.com/josuerojasrojas/auto-image-crop/' + branchName + '/' + imageFolder + '/' + img
                print downloadImg( getCropURL((imgURL), w, h), makeNewName(img, newNameAdd))
                # time.sleep(1) #avoid  'Too many'
        #delete images from github
        gitignoreImages(igImg=True)
        os.system(deleteCommands)
        print 'cropped and deleted from github'


main()
# gitignoreImages(True)
