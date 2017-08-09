#need https://github.com/Imgur/imgurpython
import zipfile, re, urllib, os, sys, getopt, json, pyimgur

CLIENT_ID = "8d55bba5f3ea0c8" #for imgur

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

def downloadImg(url, name=None):
    name = name.split('/')[-1] if name and name.split('/')[-1] else url.split('/')[-1]
    # add extension (guessing) if there isnt any
    name+= '.' + re.findall(re.compile('(png|gif|jpe?g)'), url)[-1] if not re.search(re.compile('\.(png|gif|jpe?g)'), name) else ''
    urllib.urlretrieve(url, filename='test/'+ name)
    return 'Downloaded %s' %(url)

def extractZip(fileZip, imgs=None):
    fileZip.extractall(members=imgs)
    return True #should change this to try catch

def makePath(filePath, pathRoot='test/'):
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

def makeNewName(imgName, conc):
    name = imgName.split('.')
    if len(name) < 2:
        return  imgName
    else:
        # imgName=''
        imgName= ''.join(x for x in name[:-1]) + conc + '.' + name[-1]
    return imgName

#NEED TOP UPDATE TO CATCH ERROR AND DEFAULT
#COMMENTED OUT TO FIGURE OUT BETTER WAY, IN THE MEAN TIME USING BASIC METHOD
# def getArgumentZip(arguments):
#     helpOut = 'Usage: \n -f list of zipfile names \n -h/-help help'
#     zipList = None
#     dimensionList = None
#     if len(arguments) < 2:
#         print helpOut
#         return None
#     opts, args = getopt.getopt(arguments[1:],'f:hd:')
#     for option, arg in opts:
#         if option == '-h':
#             print helpOut
#         elif option == '-f' and not arg:
#             print 'missing list of zipfile ex. "a.zip, b.zip, ..., q.zip"\n'
#         elif option == '-f' and arg:
#             zipList = arg.split(',')
#         elif option == '-d' and not arg:
#             print 'missing dimension list ex. "[30,30],[0,49],...,[300,300]"'
#         elif option == '-d':
#             dimensionList = [d for d in arg.split(',')]
#         else:
#             print helpOut
#     return zipList, dimensionList if zipList and dimensionList else None

def getArgumentZip(arguments):
    if len(arguments) < 3:
        return None, None
    zipList = arguments[1].split(',')
    dimensions = [[d for d in dimension.split(' ')] for dimension in arguments[2].split(',')]
    return zipList, dimensions

def main():
    zipList, dimension = getArgumentZip(sys.argv)
    if zipList is None and dimension is None:
        print 'no ziplist or dimensions'
        return

    for filename in zipList:
        # first make zipfile object and get img filepaths
        zipFile = getZip(filename)
        imgPaths = getFilePaths(zipFile, filename.split('/')[-1], True)

        # extract images
        print 'done' if extractZip(zipFile, imgPaths) else 'not done'

        # crop images and download
        for img in imgPaths:
            #upload img to get url
            link, image = toURLImg(img)
            for w, h in dimension:
                # print link
                # print getCropURL(img, w, h)
                newNameAdd = '-' + w + 'x' + h
                print downloadImg( getCropURL(link, w, h), makeNewName(img, newNameAdd))
                # deleteURLImg(image)


main()
