#Database Design
##1. Introduction
###1.1 Definitions


1) Docker: the CONTAINER we run the system
2) rancher: the platform we manage the Docker
3) mongodb: the database that we use
4) DB structure: the collections in mongodb
5) Info: the data that WD post to url


###1.2 References
## 2. Task Overview
### 2.1 Target

Develop a DB to save the data that WD send to DB, and allow the WD to get the data. The system should run on the docker, then we use rancher to manage it.
### 2.2 Needs
1) Write Dockerfile to build a container for the system
2) Insert the data that WD send to url to different collections
3) Aggregate the data in different collections and send to WD according to different requirement from WD
4) Use rancher to manage different container

## 3. General Design

### 3.1 Logic
1) First, the program will connect to the database.
2) Then it will provide the url for WD to post and get information.
3) When the WD post the data, the program will judge whether the structure is right. If it's right, the program will split the data to different collections and send OK to WD.
4) When the WD send get message to the program, it will aggregate the data in different collections, then send it to WD.


### 3.2 Functions
name|url|Description
---|:--:|:--:
show|ip:5000/|show the urls
add|ip:5000/add/panel|allow WD to add panel
find|ip:5000/find/barcode|give defects of certain panel with given barcode
findOK|ip:5000/find/OK|give no. of OK and NG panel in given time period
findNG|ip:5000/find/NG|give no. of OK and NG panel in given time period
missrate|ip:5000/find/missrate| give miss rate in given time period
overkillrate|ip:5000/find/overkillrate| give overkillrate in given time period
defecttime|ip:5000/find/defect|no. of defect in given time period


##4. DB structure


###defect
_id|Type|Position|by|time
---|:--:|:---:|:--:|:--:
Objectid|str|list|str|float


###el
_id|EL_no
---|:--:
Objectid|str


###panel
_id|Barcode|cell_type|cell_size|cell_amount|EL_no|create_time
---|:--:|:--:|:--:|:--:|:--:|:--:
Objectid|str|str|str|int|str|float


###panel_defect
_id|Panel_ID|Defect_ID|by|Status
---|:--:|:--:|:--:|:--:
Objectid|Objectid|Objectid|str|str


###panel_status
_id|Panel_ID|time|result|by
---|:--:|:--:|:--:|:--:
Objectid|Objectid|float|int|str

#5. WD to DB


##5.1 add panel
WD send all information about one panel 

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
for example

```
{'barcode':'13245', 'cell_type':'mono','cell_size':'half', 'cell_amount':60,'el_no':'131','create_time':0,'ai_result': 0, 'ai_defects':{'cr':[[1,1]],'bc':[[1,2],[5,5]]},'ai_time':0,'gui_result':0,'gui_defects':{'cr':[[1,1]],'bc':[[5,5],[6,6]]},'gui_time':0}
```
the api insert it to different collection
and return "OK"
##5.2 Search 
###5.2.1 Barcode 
key|type|description
--|:--:|:--:
Barcode|str|panel barcode
WD send Barcode to DB 
```
{'Barcode':'708'}
```
DB return defects of the Barcode
###5.2.2 Time
WD send a list with start time and end time to different url 
type|description
--|:--:|:--:
list|[starttime,endtime]
```
[11111.11,22222.22]
```
DB return different information

