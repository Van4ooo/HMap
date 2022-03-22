<h1>Project description</h1>

![logo](img/logo-2.png)

This utility will show the location of the server.  
And little information.

<h2>Installing</h3>
    
    git clone https://github.com/xacer2005/HMap.git

Install [poetry]("https://python-poetry.org/docs/") from the official site.
    
    cd hmap
    poetry install

<h3>Usage: python3 HMap.py [-h][-s][-b][-f]</h3>

-h, --help : Show this help message and exit  
-s, --site : Domain server to search  
-b : Google Maps settings: status[1/0] language[uk, en ...]  
-f, --file : Save response to json file

<h3>Example:</h3>
<h4>Windows</h4>

    python HMap.py -s google.com -b 1 en
    python HMap.py --site 142.250.186.206 -b 0 nn --file rez.json
    poetry run python HMap.py

<h4>Linux/Unix</h4>

    python3 HMap.py -s google.com -b 1 en
    python3 HMap.py --site 142.250.186.206 -b 0 nn --file rez.json
