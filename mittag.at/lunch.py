import requests
from bs4 import BeautifulSoup

mittag_base = "https://www.mittag.at"


class RestaurantMenu:
    def __init__(self, name: str, items: str):
        self.name = name
        self.items = items


def get(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        raise "Can't access mittag.at"

    return response.text


def parse_mittag(text: str) -> [RestaurantMenu]:
    content = BeautifulSoup(text, features="html.parser")
    restaurants = content \
        .find("section", {"id": "menus"}) \
        .find_all("dl")
    parsed_restaurants = []
    for restaurant in restaurants:
        name_link = restaurant.find("a", {"class": "details"})
        name = name_link.next
        path_to_full_menu = f"{mittag_base}{name_link['href']}"
        menu_text = parse_menu(path_to_full_menu)
        parsed_restaurants += [RestaurantMenu(name, menu_text)]
    return parsed_restaurants


def parse_menu(path_to_full_menu) -> str:
    individual_menu = BeautifulSoup(get(path_to_full_menu), features="html.parser")
    menu_html = individual_menu.find("div", {"class": "current-menu"}).find_all(text=True)
    menu_html = [x.strip() for x in menu_html if x != ' ']
    menu_text = '\n'.join(menu_html)
    return menu_text


def print_menus(menus: [RestaurantMenu]):
    bold = '\033[1m'
    cyan = '\033[96m'
    end = '\033[0m'
    for menu in menus:
        print(bold + cyan + menu.name + end)
        print(menu.items)
        print()


if __name__ == "__main__":
    hagenberg = "/a/hagenberg"
    page = get(f"{mittag_base}{hagenberg}")
    menus = parse_mittag(page)
    print_menus(menus)
