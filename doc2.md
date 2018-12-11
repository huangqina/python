#1. Prepare
prepare ubuntu18.0.4
##1.1  Image build
Install docker
Start docker service
Install docker-compose
Pull mongo image
Pull ubuntu image
```
sudo apt-get install -y docker.io
sudo service docker start
sudo pip install -U docker-compose
sudo docker pull mongo:3.6.9
sudo docker pull ubuntu:16.04
```
##1.1.2 Dockerfile
before start to build image, first write Dockerfile
make a directionary and copy the py file into it
install python, pip, and libs in requirements.txt
```
FROM ubuntu:16.04

RUN mkdir ./flask
RUN cd flask
COPY requirements.txt ./
COPY app.py ./
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

```
start to build image
```
sudo docker build -t ubuntu-flask .

```
##1.2 Create Container
First, we need to write docker-compose.yaml
this file tell the docker to create two containers, one is the database ,anther is interface.
We use the image mongo:3.6.9 to create the database container, and the image we just created as the interface.
```version: "3"

services:
  db:
    image: mongo:3.6.9

    volumes:
     - ./data:/data/db
    ports: 
     - "27017:27017"
  quotation_api:
    image: ubuntu-flask:latest
    volumes:
      - ./:/code
    network_mode: host
    ports:
      - "5000:5000"
    command: python3 code/app.py
#gunicorn app:app -c gunicorn.conf.py

```


#2. Interface
##2.1 Structure
>import libs
>connect to database
>insert indexes to mongodb
>add panel
>>judge and insert
>>return
>>
>find
>> aggregate
>> return
##2.2 lib
```
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_script import Manager
import json
```
connect to database
```
app.config['MONGO_URI'] = 'mongodb://10.42.119.168:27017/ttt'  #connect to mongodb
```
##2.3 Functions
###2.3.1 Add panel
####1. WD to Interface

key|type|description
--|:--:|:--:
barcode|str|panel barcode
cell_type|str|'mono','poly'
cell_size|str|'half','full'
cell_amount|int|60,72,120,144
el_no|str|
create_time|float|such as 1543560351.27383
ai_result|str|0 for NG; 1 for OK; another number for else
ai_defects|dict|list of 'cr','cs','bc','mr'
ai_time|float|such as 1543560351.27383
gui_result|str|0 for NG; 1 for OK; another number for else
gui_defects|dict|list of 'cr','cs','bc','mr'
gui_time|float|such as 1543560351.27383


####2. Interface to DB
#####2.1 Judge
Whether the type is right
#####2.2 insert panel
_id|Barcode|cell_type|cell_size|cell_amount|EL_no|create_time
---|:--:|:--:|:--:|:--:|:--:|:--:
Objectid|barcode|cell_type|cell_type|cell_amount|el_no|create_time

#####2.3 insert el
_id|EL_no
---|:--:
Objectid|el_no

#####2.4 insert panel_status
_id|Panel_ID|time|result|by
---|:--:|:--:|:--:|:--:
Objectid|panel _id|create_time|ai_result|AI

_id|Panel_ID|time|result|by
---|:--:|:--:|:--:|:--:
Objectid|panel _id|create_time|gui_result|OP

#####2.5 insert defect and panel_defect
######2.5.1 If the ai_defects val in gui_defects
defect
_id|Type|Position|by|time
---|:--:|:---:|:--:|:--:
Objectid|keys in ai_defects|list in keys|AI|ai_time
panel_defect
_id|Panel_ID|Defect_ID|by|Status
---|:--:|:--:|:--:|:--:
Objectid|panel _id|defect _id|ai_result|'true'

remove defect in gui_defects
######2.5.2 If the ai_defects val not in gui_defects
defect
_id|Type|Position|by|time
---|:--:|:---:|:--:|:--:
Objectid|keys in ai_defects|list in keys|AI|ai_time
panel_defect
_id|Panel_ID|Defect_ID|by|Status
---|:--:|:--:|:--:|:--:
Objectid|panel _id|defect _id|ai_result|'false'
######2.5.3 the defects in gui_defects
defect
_id|Type|Position|by|time
---|:--:|:---:|:--:|:--:
Objectid|keys in ai_defects|list in keys|OP|gui_time
panel_defect
_id|Panel_ID|Defect_ID|by|Status
---|:--:|:--:|:--:|:--:
Objectid|panel _id|defect _id|ai_result|'true'

###2.3.2 find defects of certain panel with given barcode
####1. WD to Interface

||key|type|description
--:|--|:--:|:--:
Dict|Barcode|str|panel barcode
>process
>>find the `_id` in panel with given barcode
>>match the `Panel_ID` in panel_defect
>>aggregate the `Defect_ID` in defect
>>return a json of list
```
[
  {
    "Barcode": "708", 
    "Defects": [
      {
        "Defect": [
          {
            "Position": [
              37, 
              41
            ], 
            "Type": "mr", 
            "by": "OP", 
            "time": 1543560569.856224
          }
        ], 
        "Status": "true", 
        "by": "OP"
      }, 
      {
        "Defect": [
          {
            "Position": [
              28, 
              74
            ], 
            "Type": "mr", 
            "by": "OP", 
            "time": 1543560569.856224
          }
        ], 
        "Status": "true", 
        "by": "OP"
      }
    ], 
    "EL_no": "131", 
    "cell_size": "half", 
    "cell_type": "mono", 
    "create_time": 1543560569.856224
  }
]
```

###2.3.3 find no. of OK and NG panel in given time period
####1. WD to Interface
||val1|val2|description
--:|--|:--:|:--:
List|float|float|start time and end time
>process
>>match the `time` in panel_status
>>aggregate the `result` and sum
>>return a json of list

```
[
  {
    "_id": 0, 
    "count": 108
  }, 
  {
    "_id": 1, 
    "count": 1608
  }
]

```
###2.3.4 find miss rate in given time period
####1. WD to Interface
||val1|val2|description
--:|--|:--:|:--:
List|float|float|start time and end time
>process
>>match the `time` in defect
>>match the `Defect_ID` in panel_defect with `_id` in defect
>>aggregate the `by` panel_defect in and sum
>>return a json of list
```
[
  {
    "_id": [
      "OP"
    ], 
    "count": 85916
  }, 
  {
    "_id": [
      "AI"
    ], 
    "count": 82588
  }
]
```
###2.3.5 find overkill rate in given time period
####1. WD to Interface
||val1|val2|description
--:|--|:--:|:--:
List|float|float|start time and end time
>process
>>match the `time` in defect
>>match the `Defect_ID` in panel_defect with `_id` in defect
>>aggregate the `Status` panel_defect in and sum
>>return a json of list
```
[
  {
    "_id": [
      "true"
    ], 
    "count": 86111
  }, 
  {
    "_id": [
      "false"
    ], 
    "count": 82393
  }
]
```
###2.3.6 no. of defect in given time period
####1. WD to Interface
||val1|val2|description
--:|--|:--:|:--:
List|float|float|start time and end time
>process
>>match the `time` in defect
>>match the `Defect_ID` in panel_defect with `_id` in defect
>>aggregate the `Status` panel_defect in and sum
>>return a json of list
```
[
  {
    "_id": [
      "true"
    ], 
    "count": 86111
  }, 
  {
    "_id": [
      "false"
    ], 
    "count": 82393
  }
]
```
#3. RUN
start the container
```
sudo docker-compose up
```
#4. Manage
Run rancher
```
sudo docker run -d --restart=unless-stopped -p 8080:8080 rancher/server:stable
```
![](./one.png)