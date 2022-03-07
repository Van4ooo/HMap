#!/usr/bin/env python3

import sys
import requests
from pyfiglet import Figlet
import webbrowser
import socket
import json


class HostMap:
    def __init__(self):
        caption_text()
        self.args, status = parse_args()

        if self.args.get(('-h', '--help')) or not status:
            tutorial()
        else:
            if self.args.get(("-s", "--site")):
                self.ip = self.get_ip_by_domain()
                self.get_info()
            else:
                print("[!] address not found")

    def get_ip_by_domain(self):
        try:
            return socket.gethostbyname(self.args.get(("-s", "--site")))
        except socket.gaierror:
            print("[!] Ops, please check the address")

    def get_info(self):
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

            print(*[f'{key}  << {values} >>' for key, values in response_date.items()], sep="\n")

            self.google_map([response_date.get("[* Lat]"), response_date.get("[* Lon]")])
            self.save_response(response_date)

        except requests.exceptions.ConnectionError:
            print('[!] Please check your connection!')

    def google_map(self, location: list):
        if int(self.args.get(("-b", "--browser"))):
            webbrowser.open(f"https://www.google.com.ua/maps/@{location[0]}," +
                            f"{location[1]},15z?hl={self.args.get(('-l', '--language'))}")

            print("\n[+] Browser opened")

    def save_response(self, date: dict):
        if self.args.get(("-f", "--file")):
            with open(self.args.get(("-f", "--file")), mode="w") as write_file:
                json.dump(date, write_file, indent=4)

            print("\n[+] file saved")


def parse_args() -> list:
    command_dict = {
        ("-s", "--site"): None,
        ("-h", "--help"): False,
        ("-b", "--browser"): "1",
        ("-l", "--language"): "uk",
        ("-f", "--file"): None
    }
    status = False
    mass = sys.argv[1:]

    for i in range(0, len(mass), 2):
        for k in command_dict:
            if mass[i] in k:
                command_dict[k] = True if mass[i] in ("-h", "--help") else mass[i + 1]
                status = True

    return [command_dict, status]


def tutorial():
    with open("date.json") as f:
        date = json.load(f)['help']

    print(*date, sep="\n")


def caption_text():
    caption_tx = Figlet(font="doom")
    print(caption_tx.renderText("Host  Map"))


if __name__ == '__main__':
    server = HostMap()
