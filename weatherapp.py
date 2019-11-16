import requests
import matplotlib.pyplot as plt

# Lista dat bez roku, godzin, minut
new_data_list = []

def plot_weather(xs, ys, weather_parameter, unit, xticks):
    plt.clf()  # nowy, czysty wykres
    plt.plot(xs, ys)
    plt.suptitle('wykres zależności ' + weather_parameter + ' od czasu')
    plt.gcf().autofmt_xdate()
    plt.xlabel('data(miesiąc-dzień godzina)')
    plt.ylabel('wartość' + weather_parameter + '(' + unit + ')')
    plt.xticks([0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38], xticks)
    plt.savefig('E:\Programming\weather_application\plots/date ' + weather_parameter + ' plot.png')

def changeDateLength(dateList):
    for date_item in dateList:
        shortDateLength = date_item[5:13]
        new_data_list.append(shortDateLength)
    return new_data_list

class NotValidResponse (Exception):
    pass

KEY = "045180010bcc5e609eeaceed1de32341"
city_name = input ("Proszę podać nazwę miasta którego parametry pogodowe chceć poznać: ")

def weather_plots_creator ():
    try:
        web_adress = "https://api.openweathermap.org/data/2.5/forecast"

        r = requests.get(web_adress, params={'q': '{0},pl'.format(city_name), "appid" : KEY,"units" : "metric" #parametry params są dodawane do web_adress, parammetry są parami klucz : wartosć, klucz : wartość
                                             }) #"&units=metric" dodanie tego parametru do zapytania get powoduje ze dostajemy z API odpowiedź z temperaturą w C

        # Od razu po wysłaniu zapytania do api sprawdzam status code odpowiedzi z serwera, jeśli nie jest równa 200 wyskakuje komunikat o błedzie, program obsługuję ten wyjątek
        if r.status_code != 200:
            raise NotValidResponse()

        weather_data_dictionary = r.json()#przypisuje słownik r.json() do zmiennej, bo odpalanie r.json()powoduje dodatkową pracę programu, obciążając procesor, gdy wywołuję zmienną unikam tego obciążenia

        #Lista ciśnienia
        pressure_list = []
        for record in r.json()["list"]:
           pressure_list.append(record["main"]["pressure"])

        #lista temperatur
        temperature_list = []
        for record in r.json()["list"]:
           temperature_list.append(record["main"]["temp"])

        #Lista temperatur z usuniętym drugim wynikiem oraz usuniętymi kolejnymi co drugimi wynikammi
        temperature_list_every_second_reading = temperature_list[1::2]

        #lista wilgotności !!!!
        humidity_list = []
        for record in r.json()["list"]:
            humidity_list.append(record['main']['humidity'])

        #Lista dat co 6 godzin, skracanie daty
        dt_text_list = []
        for record in r.json()["list"]:#używamy record który oznacza każdy element listy "list", nie musimy teraz podawać numerów indeksu listy "list"
            dt_text_list.append(record['dt_txt'])#dodajemy do listy "dt_text_list" wartości kluczy "dt_txt", record oznacza poszczególne indeksy listy "list"
        dt_text_list_every_6_hours = []
        dt_text_list_every_second_reading = dt_text_list[1::2]

        date_list_x_line = changeDateLength(dt_text_list_every_second_reading)

        #Wykres daty od temperatury (co drugi wynik został usunięty z wykresu)
        plot_weather(dt_text_list,temperature_list,"temperatura", "C", date_list_x_line)

        #Wykres daty od wilgotnosci
        plot_weather(dt_text_list, humidity_list, "Wilgotność", "%", date_list_x_line)

        # #Wykres daty od ciśnienia
        plot_weather(dt_text_list, pressure_list, "ciśnienie", "hPa", date_list_x_line)

    except requests.exceptions.ConnectionError as e:
        print("Brak połączenia z internetem")
    except NotValidResponse as e:
        print("Nie uzyskałeś poprawnej odpopwiedzi z serwera, skontaktuj się z programistą")
    except Exception as e:
        print ("wystąpił błąd: ", type(e), e)#gdy pojawi się jakiś błąd użytkownić nie potrzebuje informacji o linii błędu, co jest nie tak w kodzie, lepiej mu dostarczyć informacje żeby skontaktował się z developerem bo jest nie tak w kodzieĆ

weather_plots_creator()