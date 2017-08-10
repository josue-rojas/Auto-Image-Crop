# auto-image-crop
auto crop a zip of images using http://imagesvc.timeincapp.com/

### How To Use
in mac
1. double click on serv.command and copy the ngrok url
2. move all zips into images folder
3. then in terminal run
```bash
python crop-script.py "<ngrok url>"
```
example:
```bash
python crop-script.py "http://f07f11a6.ngrok.io/"
```
4. grab a coffee or do something else while the images get cropped and downloaded

##### TODO:
-  ~~integrate ngrok python api to make more autonomous~~
- scrape ngrok url from http://localhost:4040
  - make auto everything
  - update readme
