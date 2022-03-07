#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Prometheus exporter for temperatures measured by DS18B20 connected
via 1-wire

The web server is the BaseHTTPServer.
On metrics scrape time, the script reads the temperatures from a list of
predefined sensor ids one by one.
It then generates the prometheus metric (without any special module) for
all the answering sensors.
"""
__all__ = ['help']
__author__ = "Dr. Uwe Girlich <uwe.girlich@gmail.com>"

metric="temperature"
HEADER="""# HELP {0} The current temperature\r
# TYPE {0} gauge\r
"""

data=[
    { "labels": { "id": "28-3c01b5565288", "group": "1", "number": "1" },
        "value": 21.0, "valid": False },
    { "labels": { "id": "28-3c01b55659a4", "group": "1", "number": "2" },
        "value": 22.0, "valid": False },
    { "labels": { "id": "28-3c01b5565e0e", "group": "1", "number": "3" },
        "value": 23.0, "valid": False },
    { "labels": { "id": "28-3c01b556766c", "group": "1", "number": "4" },
        "value": 31.0, "valid": False },
    { "labels": { "id": "28-3c01b5568761", "group": "1", "number": "5" },
        "value": 32.0, "valid": False },
    { "labels": { "id": "28-3c01b55689a6", "group": "1", "number": "6" },
        "value": 33.0, "valid": False },
    { "labels": { "id": "28-3c01b5568c5b", "group": "2", "number": "1" },
        "value": 41.0, "valid": False },
    { "labels": { "id": "28-3c01b55699fe", "group": "2", "number": "2" },
        "value": 42.0, "valid": False },
    { "labels": { "id": "28-3c01b5569f29", "group": "2", "number": "3" },
        "value": 43.0, "valid": False },
    { "labels": { "id": "28-3c01b556b134", "group": "2", "number": "4" },
        "value": 51.0, "valid": False },
    { "labels": { "id": "28-3c01b556b495", "group": "2", "number": "5" },
        "value": 52.0, "valid": False },
    { "labels": { "id": "28-3c01b556e00b", "group": "2", "number": "6" },
        "value": 53.0, "valid": False },
    { "labels": { "id": "28-012044fe3f93", "group": "5", "number": "1" },
        "value": 53.0, "valid": False },
]

root_prefix='a'

def read_sensors():
    """
    Read the DS18B20 sensors defined in the array data.
    """
    import re
    for d in data:
        d['valid'] = False
        p="{}/sys/bus/w1/devices/{}/w1_slave".format(root_prefix, d['labels']['id'])
        try:
            with open(p,'r') as fd:
                for line in fd:
                    if " t=" in line:
                        mo = re.match(r'.*=(\d+)$', line)
                        d['value'] = float(mo.group(1)) / 1000
                        d['valid'] = True
        except IOError:
            # print("error opening {}".format(p))
            pass

from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    """
    This is the HTTP handler class needed to write a basic HTTP server.
    It is derived from BaseHTTPRequestHandler.
    """
    def do_GET(self):
        """
        Overwrite the GET method. Any HTTP GET request comes this way.
        We answer it by reading the sensors and generating prometheus metrics.
        """
        read_sensors()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        text = HEADER.format(metric)
        for d in data:
            if d['valid']:
                line = metric + "{" + ",".join(['{}="{}"'.format(k,v) for k,v in d["labels"].items()]) + "} " + str(d['value']) + "\r\n"
                text += line
        self.wfile.write(bytes(text,"utf-8"))

def server(args):
    """
    Start the HTTP server.

    :param args: The command line arguments of the main script.
    :return: returns nothing
    """
    global root_prefix
    root_prefix = args.root
    httpd = HTTPServer(('', args.port_number), Handler)
    print("root prefix='{}', listen on port {}".format(root_prefix, args.port_number))
    httpd.serve_forever()

def main():
    """The main function of the script."""
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-l", "--listen", dest="port_number", default=9090,
                    help="listen on given port", type=int)
    parser.add_argument("-r", "--root", dest="root", default="",
                    help="prefix sensor files with directory root", type=str)
    args = parser.parse_args()
    server(args)

if __name__== "__main__" :
    main()

