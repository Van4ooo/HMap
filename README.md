<h1>Host Map</h1>

![logo](img/logo.png)

This utility will show the location of the server.  
And little information.

<h3>Usage: python3 HMap.py [-h][-s][-b][-f][-l]</h3>

>-h, --help : tutorial  
-s, --site : domain name or ip address  
-b : Google Maps settings: status[1/0] language[uk, en ...]  
-f, --file : save response to json file

<h3>Example:</h3>

    python3 HMap.py -s google.com -b 1 en
    python3 HMap.py --site google.com -b 0 nn --file rez.json
