<h1>Host Map</h1>

![logo](img/logo.png)

This utility will show the location of the server.  
And little information.

###Usage: python3 HMap.py [-h][-s][-b][-f][-l]

>-h, --help : tutorial  
-s, --site : domain name or ip address  
-b, --browser : default 1 open browser, 0 don't open  
-f, --file : save response to file.json  
-l, --language : language google maps, default uk  

###Example:

    python3 HMap.py -s google.com -b 1 -l en
    python3 HMap.py --site google.com --browser 0 --file rez.json
