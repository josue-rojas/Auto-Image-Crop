# auto-image-crop
------
auto crop a zip of images using http://imagesvc.timeincapp.com/

### NEED
- github account

### How To Use
in mac
1. clone this repo and make a new branch and push upstream to github
2. paste and replace new branch name in crop.py and clean.py (might make this an env variable)
3. !important make 'images' folder and inside put zip files containing the images
4. double click start.command
5. grab a coffee or do something else while the images get cropped and downloaded (3seconds per img)
6. (optional) double click clean.command just to make sure image folder gets deleted from github

##### TODO:
- use [pygit](http://www.pygit2.org/references.html#the-head) to check not master and get branch name automatically
- ~~lower processing time~~ test limits of github times
- check image are downloaded and are not junk
- update readme (always and forever)

###### a small explanation
main() in crop.py
- gets a list of all zips in images folder
- for each zip  
  - get all its images path
  - extract the zip
  - change the gitignore to be able to upload images folder to github and upload them
  - then for each img and each dimensions
    - make a url for the crop and download them
  - change gitignore to delete images from github
- and i think that is it
