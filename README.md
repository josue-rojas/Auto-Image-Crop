# auto-image-crop
auto crop a zip of images using http://imagesvc.timeincapp.com/

### How To Use
In Mac
1. move all zips into images folder
2. double click on serv.command and copy the ngrok url
3. then in terminal run
```
python crop-script.py "<ngrok url>"
```
example:
`
python crop-script.py "http://f07f11a6.ngrok.io/"
`
4. grab a coffee or do something else while the images get cropped and downloaded

##### TODO:
- integrate ngrok python api to make more autonomous
  - update readme
- automate the serv (ngrok thingy)
