from faker import Faker             #zaimportuj Fakera
import random                       #zaimportuj generator liczb losowych
import datetime                     #zaimportuj daty

class Filmy:
    def __init__(self, tytul, rok, gatunek):
        self.tytul = tytul
        self.rok = rok
        self.gatunek = gatunek
        #Variables
        self.odtworzenia = 0
    def __str__(self):
        return f"{self.tytul} ({self.rok})"
    
    def play(self, step=1):
        self.odtworzenia += step
    
class Seriale(Filmy):
    def __init__(self, nr_sezonu, nr_odcinka, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nr_sezonu = nr_sezonu
        self.nr_odcinka = nr_odcinka
    def __str__(self):
        return f"{self.tytul} S{self.nr_sezonu:02}E{self.nr_odcinka:02}"
    
class Biblioteka(list):
    def __init__(self, *args):
        super().__init__(*args)

    #Funkcje zwracają listę filmów oraz listę seriali, posortowane po tytule
    def get_movies(self):
        result = [rekord for rekord in self if type(rekord)==Filmy]
        return sorted(result, key=lambda rekord: rekord.tytul)
    def get_series(self):
        result = [rekord for rekord in self if type(rekord)==Seriale]
        return sorted(result, key=lambda rekord: rekord.tytul)

    #Funkcja wyszukuje film lub serial po tytule
    def search(self, szukany_tytul):
        for rekord in self:
            if rekord.tytul == szukany_tytul:
                return rekord
        return "Brak filmu lub serialu"
    
    #Funkcja zwraca wybraną ilość najpopularniejszych tytułów z biblioteki
    def top_titles(self, ilosc, content_type=0):
        if content_type == 'f':
            rekordy = [rekord for rekord in self if type(rekord)==Filmy]
        elif content_type == 's':
            rekordy = [rekord for rekord in self if type(rekord)==Seriale]
        else:
            rekordy = self

        return sorted(rekordy, key=lambda rekord: rekord.odtworzenia, reverse=True)[:ilosc]

    #Funkcja losowo wybiera element z biblioteki, a następnie dodaje mu losową (z zakresu od 1 do 100) ilość odtworzeń
    def generate_views(self):
        random.choice(self).play(random.randint(1, 100))
    #Funkcja powtarza powyższe 10 razy
    def multi_generate_views(self, ilosc_powtorzen=10):
        for i in range(0, ilosc_powtorzen):
            self.generate_views()
    
    #Funkcja dodaje pełne sezony seriali do biblioteki
    def add_season(self, tytul, rok, gatunek, nr_sezonu, liczba_odcinkow):
        for i in range(0, liczba_odcinkow):
            self.append(Seriale(nr_sezonu, i+1, tytul, rok, gatunek))

    #Funkcja wyświetla liczbę odcinków danego serialu dostępnych w bibliotece
    def ile_odcinkow(self, szukany_tytul):
        return len([rekord for rekord in self if type(rekord)==Seriale and rekord.tytul == szukany_tytul])


#funkcja pomocnicza do wyświetlania wszystkich pozycji na liście:
def wypisz(pozycje):
    for poz in pozycje:
        print(f"{poz}  - odtwarzany {poz.odtworzenia} raz{koncowka(poz.odtworzenia)}")

def koncowka(i):
    if i == 1: return ''
    else: return 'y'



#------------------------------------------------------------------------------------------------------------------
#Część wykonywalna
print("Biblioteka filmów")

#wypełnij bibliotekę treścią
biblioteka = Biblioteka([
    Filmy('Crown', 2023, 'animacja'), 
    Filmy('Titanic', 1997, 'katastroficzny'), 
    Seriale(2, 45, 'Simpsonowie', 1995, 'animacja'),
    Filmy('Tombstone', 1980, 'western'),
    Filmy('Snow White', 2025, 'klapa'), 
    Filmy('Armageddon', 2000, 'katastroficzny'),
    Seriale(1, 3, 'House MD', 1997, 'horror')])
biblioteka.add_season('Futurama', 1999, 'sci-fi', 1, 13)

#wygeneruj odtworzenia
biblioteka.multi_generate_views()

#wyświetl listę top 3 najpopularniejszych tytułów
today = datetime.date.today().strftime("%d.%m.%Y")
print(f"Najpopularniejsze filmy i seriale dnia {today}")
wypisz(biblioteka.top_titles(3))

#print(biblioteka.ile_odcinkow('Tombstone'))