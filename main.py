from interface.scraping import get_data
from interface.csv import save

if __name__ == '__main__':
    save(get_data())
