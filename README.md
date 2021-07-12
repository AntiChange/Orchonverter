# SheetMusicConverter
Project Program  Group G

## Run Melody Seperator Docker Container
go to folder ../melody_seperator
```
cd melody_separator
```
download model from https://drive.google.com/file/d/1FeelPlTMdCidVh7PILsbDFA781I6elhx/view?usp=sharing 
and save in the folder ../melody_seperator/src


build docker image
```
docker build -t python-flask .
```
run docker container
```
docker run -p 8000:8000 python-flask
```
server will be hosted on: http://127.0.0.1:8000/