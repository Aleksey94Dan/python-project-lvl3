


from page_loader import cli
from page_loader import loader


def main():
    path_to_file, url = cli.parse()
    loader.load(url, path_to_file)