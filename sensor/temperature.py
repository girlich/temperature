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
from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, HTTPServer
import re

__author__ = "Dr. Uwe Girlich <uwe.girlich@gmail.com>"

METRIC = "temperature"
HEADER = """# HELP {0} The current temperature
# TYPE {0} gauge
"""

data = [
    {"labels": {"id": "28-3c01b5565288", "group": "1", "number": "1"},
        "value": 21.0, "valid": False},
    {"labels": {"id": "28-3c01b55659a4", "group": "1", "number": "2"},
        "value": 22.0, "valid": False},
    {"labels": {"id": "28-3c01b5565e0e", "group": "1", "number": "3"},
        "value": 23.0, "valid": False},
    {"labels": {"id": "28-3c01b556766c", "group": "1", "number": "4"},
        "value": 31.0, "valid": False},
    {"labels": {"id": "28-3c01b5568761", "group": "1", "number": "5"},
        "value": 32.0, "valid": False},
    {"labels": {"id": "28-3c01b55689a6", "group": "1", "number": "6"},
        "value": 33.0, "valid": False},
    {"labels": {"id": "28-3c01b5568c5b", "group": "2", "number": "1"},
        "value": 41.0, "valid": False},
    {"labels": {"id": "28-3c01b55699fe", "group": "2", "number": "2"},
        "value": 42.0, "valid": False},
    {"labels": {"id": "28-3c01b5569f29", "group": "2", "number": "3"},
        "value": 43.0, "valid": False},
    {"labels": {"id": "28-3c01b556b134", "group": "2", "number": "4"},
        "value": 51.0, "valid": False},
    {"labels": {"id": "28-3c01b556b495", "group": "2", "number": "5"},
        "value": 52.0, "valid": False},
    {"labels": {"id": "28-3c01b556e00b", "group": "2", "number": "6"},
        "value": 53.0, "valid": False},
    {"labels": {"id": "28-012044fe3f93", "group": "5", "number": "1"},
        "value": 53.0, "valid": False},
]

def read_sensors(arguments):
    """
    Read the DS18B20 sensors defined in the array data.
    """
    for d in data:
        d['valid'] = False
        p = "{}/sys/bus/w1/devices/{}/w1_slave".format(
            arguments.root, d['labels']['id'])
        try:
            with open(p, 'r') as file_descriptor:
                for line in file_descriptor:
                    if " t=" in line:
                        mo = re.match(r'.*=(\d+)$', line)
                        d['value'] = float(mo.group(1)) / 1000
                        d['valid'] = True
        except IOError:
            # print("error opening {}".format(p))
            pass


class MyHandler(BaseHTTPRequestHandler):
    """
    This is the HTTP handler class needed to write a basic HTTP server.
    It is derived from BaseHTTPRequestHandler.
    """

    def __init__(self, arguments, *args):
        """

        Parameters
        ----------
        arguments : Namespace filled with parsed command line arguments
            parsed command line arguments.
        *args : TYPE
            rest if the base class constructor arguments.

        Returns
        -------
        None.

        """
        self.arguments = arguments # Remember the arguments.
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        """
        Overwrite the GET method. Any HTTP GET request comes this way.
        We answer it by reading the sensors and generating prometheus metrics.
        """
        read_sensors(self.arguments)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        text = HEADER.format(METRIC)
        for d in data:
            if d['valid']:
                line = METRIC + "{" + ",".join(['{}="{}"'.format(
                    k, v) for k, v in d["labels"].items()]) + "} " + str(d['value']) + "\n"
                text += line
        self.wfile.write(bytes(text, "utf-8"))


class HttpServer:
    """Start the HTTP server and remember the arguments in the handler"""
    def __init__(self, arguments):
        def handler(*args):
            MyHandler(arguments, *args)

        server = HTTPServer(('', arguments.port_number), handler)
        print("root prefix='{}', listen on port {}".format(
           arguments.root, arguments.port_number))
        server.serve_forever()


def main():
    """The main function of the script."""
    parser = ArgumentParser()
    parser.add_argument("-l", "--listen", dest="port_number", default=9090,
                        help="listen on given port", type=int)
    parser.add_argument("-r", "--root", dest="root", default="",
                        help="prefix sensor files with directory root", type=str)
    arguments = parser.parse_args()
    HttpServer(arguments)


if __name__ == "__main__":
    main()
