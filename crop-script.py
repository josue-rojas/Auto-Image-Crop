# NEED https://github.com/Imgur/imgurpython
import zipfile, re, urllib, os, sys, getopt, json, time

# constants
#NEED TO UPDATE USAGE
notes = 'USAGE: \nzip file must be in the same folder as this .py \ndownloaded images will be located in their repsected folders with the dimensions on their title \nto use run in terminal with <zip files> <dimensions> like: \npython crop-scrypt.py "example.zip" "84 74,300 300"'
noZip = 'No zip or not zip either way exitting....'
CLIENT_ID = "8d55bba5f3ea0c8" #for imgur

'''
python crop-script.py "http://93963860.ngrok.io/" "test.zip" "84 74,300 300"
'''

# note if foldersOnly is True it will override imgOnly
def getFilePaths(fileZip, filename, imgOnly=False, foldersOnly=False):
    root = re.compile(filename.split('.')[0])
    imgRe = re.compile('\.(png|gif|jpe?g)') if imgOnly else ''
    if foldersOnly:
        return [path for path in fileZip.namelist() if re.match(root, path) and path[-1] is '/']
    return [path for path in fileZip.namelist() if re.match(root, path) and re.search(imgRe, path)]

def getZip(filename):
    return zipfile.ZipFile(filename, 'r') if zipfile.is_zipfile(filename) else None

def getCropURL(imgURL, width, height, cropType='cc'):
    return 'http://imagesvc.timeincapp.com/?url=%s&h=%s&w=%s&c=%s' %(imgURL, height, width, cropType)

def downloadImg(url, name=None, noPath=False):
    if noPath:
        name = name.split('/')[-1] if name and name.split('/')[-1] else url.split('/')[-1]
    # add extension (guessing) if there isnt any
    name+= '.' + re.findall(re.compile('(png|gif|jpe?g)'), url)[-1] if not re.search(re.compile('\.(png|gif|jpe?g)'), name) else ''
    urllib.urlretrieve(url, filename=name)
    return 'Downloaded %s' %(url)

def extractZip(fileZip, imgs=None):
    fileZip.extractall(members=imgs)
    return True #should change this to try catch

# not used but useful if you need to make empty folders of paths
def makePath(filePath, pathRoot=''):
    filePath = pathRoot + filePath
    if not os.path.isdir(filePath):
        os.makedirs(filePath)
    else:
        return 'exist already'

def toURLImg(path):
    upload_image = pyimgur.Imgur(CLIENT_ID).upload_image(path,title=path.split('/')[-1])
    return upload_image.link, upload_image

def deleteURLImg(upload_image):
    upload_image.delete()

# add to the name before the extension for example makeNewName(cat.jpg, 4x4) -> cat4x4.jpg
def makeNewName(imgName, conc):
    name = imgName.split('.')
    if len(name) < 2:
        return  imgName
    else:
        imgName= ''.join(x for x in name[:-1]) + conc + '.' + name[-1]
    return imgName

def getArgumentZip(arguments):
    if len(arguments) < 4:
        return None, None, None
    baseURL = arguments[1]
    zipList = arguments[2].split(',')
    dimensions = [[d for d in dimension.split(' ')] for dimension in arguments[3].split(',')]
    return baseURL, zipList, dimensions

def main():

    baseURL, zipList, dimension = getArgumentZip(sys.argv) if getArgumentZip(sys.argv) != (None,None,None) else sys.exit(notes)
    print baseURL

    for filename in zipList:
        # first make zipfile object and get img filepaths
        zipFile = getZip(filename) if getZip(filename) != None else sys.exit(noZip)
        imgPaths = getFilePaths(zipFile, filename.split('/')[-1], True)
        folderPaths = getFilePaths(zipFile, filename.split('/')[-1], foldersOnly=True)

        # extract images
        print 'done extract' if extractZip(zipFile, imgPaths) else 'not done'

        # crop images and download
        for img in imgPaths:
            #upload img to get url
            # link, image = toURLImg(img)
            link = baseURL + img
            for w, h in dimension:
                newNameAdd = '-' + w + 'x' + h
                print makeNewName(img, newNameAdd)
                print downloadImg( getCropURL(link, w, h), makeNewName(img, newNameAdd))
            #     time.sleep(60) #wait cause someone doesn't like too much work
            # deleteURLImg(image)


main()
