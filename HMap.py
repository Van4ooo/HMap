#!/usr/bin/env python3

import argparse
import requests
from pyfiglet import Figlet
import webbrowser
import socket
import json


class HostMap:
    def __init__(self, args):
        self.args = args
        self.ip = self.get_ip_by_domain()

        if self.ip:
            self.response_date = self.get_info()
            if self.response_date:
                self.href = self.google_map_generation_href()
                print(f"[+] link on google map: {self.href}", end="\n\n")
            else:
                print('[!] Please check your connection!')
        else:
            print("[!] Ops, please check the address")

    def get_ip_by_domain(self) -> str | None:
        try:
            return socket.gethostbyname(self.args.site)
        except socket.gaierror:
            return None

    def get_info(self) -> bool | dict:
        try:
            response = requests.get(url=f'http://ip-api.com/json/{self.ip}').json()

            response_date = {
                '[* IP]': response.get('query'),
                '[* Int prov]': response.get('isp'),
                '[* Org]': response.get('org'),
                '[* Country]': response.get('country'),
                '[* Region Name]': response.get('regionName'),
                '[* City]': response.get('city'),
                '[* ZIP]': response.get('zip'),
                '[* Lat]': response.get('lat'),
                '[* Lon]': response.get('lon'),
            }

            print(*[f'{key}  << {values} >>' for key, values in response_date.items()], sep="\n", end="\n\n")

            """self.google_map([response_date.get("[* Lat]"), response_date.get("[* Lon]")])
            self.save_response(response_date)"""
            return response_date

        except requests.exceptions.ConnectionError:
            return False

    def google_map_generation_href(self) -> str:
        href = f"https://www.google.com.ua/maps/@{self.response_date.get('[* Lat]')}," + \
              f"{self.response_date.get('[* Lon]')},15z?hl={self.args.settings[1]}"

        return href

    def google_maps_open(self) -> None:
        webbrowser.open(self.href)

    def save_response(self) -> None:
        with open(self.args.file, mode="w") as write_file:
            json.dump(self.response_date, write_file, indent=4)


class ParseArgs:
    parser = argparse.ArgumentParser(
        epilog="This utility will show the location of the server. "
               "And little information.")

    def __init__(self):
        caption_tx = Figlet(font="doom")
        print(caption_tx.renderText("Host  Map"))

        self.parser.add_argument(
            '-s',
            '--site',
            dest="site",
            help='domain server to search',
        )

        self.parser.add_argument(
            '-b',
            nargs=2,
            dest="settings",
            default=[1, 'uk'],
            help='google maps settings: status[1/0] language[uk, en ...]',
        )

        self.parser.add_argument(
            '-f',
            '--file',
            dest="file",
            default='',
            help='save response to json file',
        )

    def tutorial(self):
        self.parser.print_help()


if __name__ == '__main__':
    args_m = ParseArgs()
    ar = args_m.parser.parse_args()

    if ar.site:
        hmap = HostMap(args=ar)

        if int(ar.settings[0]):
            hmap.google_maps_open()
            print("[+] Browser opened")

        if ar.file:
            hmap.save_response()
            print(f"[+] Response saved to {ar.file}")
    else:
        args_m.tutorial()
