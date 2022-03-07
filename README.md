Host Map,
        This utility will show the location of the server
        And a little information\n
        Usage: python3 HMap.py [-h][-s][-b][-l]
            -h, --help : tutorial
            -s, --site : domain name or ip address
            -b, --browser : default 1 open browser, 0 don't open
            -f, --file : save response to file.json
            -l, --language : language google maps, default uk\n
        Example:
            python3 HMap.py -s google.com -b 1 -l en
            python3 HMap.py --site google.com --browser 0 --file rez.json\n