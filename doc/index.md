# DroneLib documentation

DroneLIB is python package for raspberry-pi microcomputers. It is capable of communicating with the Betaflight 4 powered boards, send them controll data, recieve 


# Examples

All ready to launch exapmles are placed in the folder examples. 

## avoidWalls.py
This code takes off and avoids obstacles around the drone. Example usage of sensorArray library.

...behaviour...

..toto...

## resetBoard.py
Example code, which resets the drone board. Resseting the board is called after each \_\_init\_\_  of the DroneLib class.


# How it works?


```mermaid
graph TD  
classDef main fill:#f96;
A(Your drone controller code):::main -- includes --> B(dronelib.dronelib)
A -- can include --> C(dronelib.sensorArray)
```
- dronelib.dronelib
	> Contains class ```DroneLib```, which is responsible for all communication with the betaflight board.
	> One instance of this class represents one drone connection, contructor requires one parameter - serial port of the drone, default is ```"/dev/ttyACM0"```

- dronelib.sensorArray
	> Before starting to sync files, you must link an account in the **Synchronize** sub-menu.


## Communication diagram

This diagram shows communication in avoidWalls.py exmaple program. 

```mermaid
sequenceDiagram
avoidWalls ->> DroneLib: Creates one instance on port /dev/ttyACM0
DroneLib ->> Betaflight: Resets the board
DroneLib ->> Betaflight: Performs the first update
Betaflight -->> DroneLib: Telemetry data<br>Battery capacity

avoidWalls ->> DroneLib: Arm
DroneLib ->> Betaflight: Arm
Note right of DroneLib: 5 sec safety delay
Note right of avoidWalls: Every cicle:
avoidWalls ->> DroneLib: Periodicly calls update method with flight command
DroneLib ->> Betaflight: Updates the motor values
DroneLib ->> Betaflight: Flight data request
Betaflight ->> DroneLib: Altitude, angle data
DroneLib ->> avoidWalls: Performs update based on incomming data

```
# Drone specifications




## Open a file

You can open a file from **Google Drive**, **Dropbox** or **GitHub** by opening the **Synchronize** sub-menu and clicking **Open from**. Once opened in the workspace, any modification in the file will be automatically synced.

## Save a file

You can save any file of the workspace to **Google Drive**, **Dropbox** or **GitHub** by opening the **Synchronize** sub-menu and clicking **Save on**. Even if a file in the workspace is already synced, you can save it to another location. StackEdit can sync one file with multiple locations and accounts.

## Synchronize a file

Once your file is linked to a synchronized location, StackEdit will periodically synchronize it by downloading/uploading any modification. A merge will be performed if necessary and conflicts will be resolved.

If you just have modified your file and you want to force syncing, click the **Synchronize now** button in the navigation bar.

> **Note:** The **Synchronize now** button is disabled if you have no file to synchronize.

## Manage file synchronization

Since one file can be synced with multiple locations, you can list and manage synchronized locations by clicking **File synchronization** in the **Synchronize** sub-menu. This allows you to list and remove synchronized locations that are linked to your file.


# Publication

Publishing in StackEdit makes it simple for you to publish online your files. Once you're happy with a file, you can publish it to different hosting platforms like **Blogger**, **Dropbox**, **Gist**, **GitHub**, **Google Drive**, **WordPress** and **Zendesk**. With [Handlebars templates](http://handlebarsjs.com/), you have full control over what you export.

> Before starting to publish, you must link an account in the **Publish** sub-menu.

## Publish a File

You can publish your file by opening the **Publish** sub-menu and by clicking **Publish to**. For some locations, you can choose between the following formats:

- Markdown: publish the Markdown text on a website that can interpret it (**GitHub** for instance),
- HTML: publish the file converted to HTML via a Handlebars template (on a blog for example).

## Update a publication

After publishing, StackEdit keeps your file linked to that publication which makes it easy for you to re-publish it. Once you have modified your file and you want to update your publication, click on the **Publish now** button in the navigation bar.

> **Note:** The **Publish now** button is disabled if your file has not been published yet.

## Manage file publication

Since one file can be published to multiple locations, you can list and manage publish locations by clicking **File publication** in the **Publish** sub-menu. This allows you to list and remove publication locations that are linked to your file.


# Markdown extensions

StackEdit extends the standard Markdown syntax by adding extra **Markdown extensions**, providing you with some nice features.

> **ProTip:** You can disable any **Markdown extension** in the **File properties** dialog.


## SmartyPants

SmartyPants converts ASCII punctuation characters into "smart" typographic punctuation HTML entities. For example:

|                |ASCII                          |HTML                         |
|----------------|-------------------------------|-----------------------------|
|Single backticks|`'Isn't this fun?'`            |'Isn't this fun?'            |
|Quotes          |`"Isn't this fun?"`            |"Isn't this fun?"            |
|Dashes          |`-- is en-dash, --- is em-dash`|-- is en-dash, --- is em-dash|
