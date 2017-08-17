# auto-image-crop
------
auto crop a zip of images using http://imagesvc.timeincapp.com/

### NEED
- github account

### How To Use
in mac
1. clone this repo and make a new branch and push upstream to github
  ```bash
  cd auto-image-crop # if you arent there already
  git checkout <name of new branch>
  git push --set-upstream origin <name of new branch>
  ```
2. make sure you did the first step
3. !important make 'images' folder and inside put zip files containing the images
4. double click start.command
5. grab a coffee or do something else while the images get cropped and downloaded (3seconds per img)
6. (optional) double click clean.command just to make sure image folder gets deleted from github, this will also delete if from your local files

##### TODO:
- ~~lower processing time~~ test limits of github times
- check image are downloaded and are not junk
- update readme (always and forever)

###### Files:
- .gitignore
   ```
   ignore stuff like DS_STORED, images folder, and zip files
   ```
- README.md
   ```
   self explanatory
   ```
- clean.command
  ```
  script to run clean.py, just double click
  ```
- clean.py
  ```
  python script that deletes images folder from both github and locally
  ```
- crop.py
   ```
   python scrip that looks into images folder for zip files. 
   then it extracts them and uploads them to github. 
   from github it gets the links to be used in the image service to crop them. 
   this file contains the default crops.
   ```
- start.command 
  ```
  script to run crop.py, just double click
  ```
