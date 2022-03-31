#!/usr/bin/env python3

from fake_useragent import UserAgent
from pyfiglet import Figlet
from colorama import Fore
from argparse import ArgumentParser
import requests

from socket import gethostbyname, socket, gaierror, error, AF_INET, SOCK_STREAM
from time import sleep
from webbrowser import open as op
import json


class HostMap:
    def __init__(self, args):
        self.args = args
        self.ip = self.get_ip_by_domain()

        if self.ip:
            self.response_date = self.get_info()
            if self.response_date:
                self.href = self.google_map_generation_href()
            else:
                print('[!] Please check your connection!')
                exit()
        else:
            print("[!] Ops, please check the address")
            exit()

    def get_ip_by_domain(self) -> str:
        try:
            return gethostbyname(self.args.site)
        except gaierror:
            return ""

    def get_ip(self) -> str:
        return self.ip

    def get_info(self) -> dict:
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
                '[* link]': None
            }

            return response_date

        except requests.exceptions.ConnectionError:
            return {}

    def print_response(self) -> None:
        print(*[f'{key}  << {values} >>' for key, values in self.response_date.items()], sep="\n", end="\n")

    def google_map_generation_href(self) -> str:
        href = f"https://www.google.com.ua/maps/@{self.response_date.get('[* Lat]')}," + \
              f"{self.response_date.get('[* Lon]')},12z"

        self.response_date["[* link]"] = href

        return href

    def google_maps_open(self) -> None:
        op(self.href)


class CheckHostAPI:
    def __init__(self, ip: str):
        self.ip: str = ip

        self.time_sleep_ping: float = 10.0
        self.time_sleep_tcp: float = 5.0

        self.request: dict = {}
        self.request_id: dict = {}

        self.printing_dict: dict = {}

    def request_to_api(self, method: str, port_ch: str = "") -> None:
        if method == "ping":
            print(f"[!] Ping {self.ip} started")

        elif method == "tcp":
            port_ch = ":" + (port_ch if port_ch.isdigit() else "443")
            print(f"[!] TCP connect {self.ip}{port_ch} started")

        ua = UserAgent()

        href = f"https://check-host.net/check-{method}?host={self.ip}{port_ch}"
        headers = {
            'User-agent': ua.random,
            'Accept': 'application/json'
        }

        self.request = requests.post(href, headers=headers).json()
        href = f'https://check-host.net/check-result/{self.request.get("request_id")}'

        sleep(self.time_sleep_ping if method == "ping" else self.time_sleep_tcp)

        self.request_id = requests.post(href, headers=headers).json()

    def ping_parser(self) -> None:
        for server in self.request_id:
            if self.request_id.get(server) and self.request_id.get(server)[0] and self.request_id.get(server)[0][0]:
                status = 0
                time = []

                for x in self.request_id.get(server)[0]:
                    status += x[0] == "OK"
                    time.append(x[1])

                self.printing_dict[(self.request["nodes"].get(server)[1], self.request["nodes"].get(server)[2])] = {
                    "status": status,
                    "time-avg": round(sum(time) / 4, 3),
                    "time-min": round(min(time), 3),
                    "time-max": "> 3.0" if round(max(time)) == 3 else round(max(time), 3)
                }

            else:
                self.printing_dict[(self.request["nodes"].get(server)[1], self.request["nodes"].get(server)[2])] = {
                    "status": 0,
                    "time-avg": "> 3.0",
                    "time-min": "> 3.0",
                    "time-max": "> 3.0"
                }

    def print_ping(self) -> None:
        print("Country/Siti                  Servers     time_avg    time_min    time_max")
        print("=" * 74, end="\n\n")

        count_suc = [0, 0]
        for k, v in self.printing_dict.items():
            text = f"{k[0]}/{k[1]}"
            text += " " * (30 - len(text))

            text += f"{v['status']}/4" + " " * 9
            status = v['status']

            count_suc[0] += status
            count_suc[1] += 4

            del v['status']

            text += "".join([f"{x}s" + " " * (11 - len(x)) for x in map(str, v.values())])
            color = Fore.GREEN if status == 4 else Fore.YELLOW \
                if status > 1 else Fore.RED

            print(color + f"{text}" + Fore.RESET)

        cof_work = round((count_suc[0]/count_suc[1])*100)
        color = Fore.GREEN if cof_work > 80 else Fore.YELLOW if cof_work > 33 else Fore.RED

        print(color + f"\nServer work on {cof_work}%" + Fore.RESET)

    def tcp_parser(self) -> None:
        for server in self.request_id:
            if self.request_id.get(server):
                self.printing_dict[(self.request["nodes"].get(server)[1], self.request["nodes"].get(server)[2])] = {
                    "time": self.request_id.get(server)[0].get("time", "timeout"),
                    "status": (
                        "Connection successful" if self.request_id.get(server)[0].get("time") else
                        "Connection failed")
                }

    def print_tcp(self) -> None:
        print("Country/Siti             Status                    time")
        print("=" * 59, end="\n\n")

        works_server = [0, 0]
        for k, v in self.printing_dict.items():
            text = f"{k[0]}/{k[1]}"

            text += " " * (25 - len(text))
            text += v['status'] + (" " * (26 - len(v['status'])))
            text += str(v['time'])

            works_server[0] += 1

            if "successful" in v['status']:
                color = Fore.GREEN
                works_server[1] += 1
            else:
                color = Fore.RED

            print(color + text + Fore.RESET)

        status = round((works_server[1]/works_server[0])*100)
        color = Fore.GREEN if status > 80 else Fore.YELLOW if status > 33 else Fore.RED

        print(color + f"\n[+] Server works on {status}%" + Fore.RESET)


class PortScanner:
    def __init__(self, ip: str):
        self.ip: str = ip
        self.port: int = 443

        self.server_timeout: float = 0.15
        self.number_connections: int = 1

    def ports_scanner(self, ports=None) -> None:
        with open("date.json") as date_f:
            ports_d = json.load(date_f)["Ports"]
            ports = tuple(ports_d.keys()) if not ports else ports

        try:
            print("PORT     Protocol        Transport layer    Status")
            print("="*50, end="\n\n")

            for p in ports:
                text = f"{p}" + " "*(9-len(p))

                if ports_d.get(p, None):
                    text += f"{ports_d.get(p)['name']}" + " "*(16-(len(ports_d[p]['name'])))

                    layer_4 = "/".join(ports_d[p]['protocol'])
                    text += f"{layer_4}" + " " * (19 - len(layer_4))
                else:
                    text += "unknown" + " "*9 + "unknown" + " "*12

                self.port = int(p)

                if self.port_scanner():
                    color = Fore.GREEN
                    text += "OPEN"
                else:
                    color = Fore.RED
                    text += "CLOSE"

                print(color + text + Fore.RESET)

        except gaierror:
            print("\n[!]Hostname Could Not Be Resolved")

        except error:
            print("\n[!]Server not responding")

    def port_scanner(self) -> bool:
        for _ in range(self.number_connections):
            server = socket(AF_INET, SOCK_STREAM)
            server.settimeout(self.server_timeout)

            if not server.connect_ex((self.ip, self.port)):
                return True
            server.close()

        return False


class ParseArgs:
    parser = ArgumentParser(
        epilog="This utility will show the location of the server. "
               "And little information.")

    def __init__(self):
        caption_tx = Figlet(font="doom")
        print(caption_tx.renderText("Host  Map"))

        self.parser.add_argument(
            '-s',
            '--site',
            dest="site",
            help='Domain server to search',
        )

    def tutorial(self):
        self.parser.print_help()


if __name__ == '__main__':
    args_m = ParseArgs()
    ar = args_m.parser.parse_args()

    if ar.site:
        hmap = HostMap(args=ar)
        hmap.print_response()

        checkAPI = CheckHostAPI(ip=hmap.get_ip())

        while True:
            print("\n[1] Open Google Maps")
            print("[2] Ping site")
            print("[3] Check TCP port")
            print("[4] Port scaner")
            print("[5] Exit")

            command = input("select an option: ")
            print()

            match command:
                case "1":
                    hmap.google_maps_open()
                    print("[+] Browser opened")
                case "2":
                    checkAPI.request_to_api(method="ping", port_ch="")

                    checkAPI.ping_parser()
                    checkAPI.print_ping()
                case "3":
                    port = input("[?] TCP порт для перевірки: ").split()[0]

                    checkAPI.request_to_api(method="tcp", port_ch=port)

                    checkAPI.tcp_parser()
                    checkAPI.print_tcp()
                case "4":

                    ports_input = tuple(filter(
                        lambda x: x.isdigit() and 1 <= int(x) <= 65535,
                        input("[?] Порти для перевірки: ").split()
                    ))

                    print()

                    ps = PortScanner(ip=hmap.get_ip())
                    ps.ports_scanner(ports_input if ports_input else None)
                case _:
                    exit()

    else:
        args_m.tutorial()
