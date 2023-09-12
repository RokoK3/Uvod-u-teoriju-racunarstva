import sys
import fileinput

def sortirajOdijeli(lista):
    lista.sort() #poredaj leksikografski
    return ','.join(lista) #odvoji zarezom sva trenutna stanja
    
def generirajKljuc(znak1, znak2):
    return znak1 + ',' + znak2

def iteracijaStanja(slijedece, trenutno):  
    for x in slijedece: #iz skupa sljedecih stanja
        if x not in trenutno: #gledam je li to stanje vec u trenutnim da ne bi bilo ponavljanja
            trenutno.append(x) #dodaj u trenutna

def prijelazStanja(stanje, znak, skupTrenutnihStanja):
    key = generirajKljuc(stanje, znak) #kljuc sa kojim cu provjeravati rjecnik
    if key in rjecnik:
        iducaStanja = rjecnik.get(key).split(',') #skup iducih stanja iz rjecnika, odma micem zareze izmedu njih
        iteracijaStanja(iducaStanja, skupTrenutnihStanja)    

inputPodataka = fileinput.input() #ulazni "stream" podataka

ulazniNizovi = inputPodataka.readline().strip().split('|') #makni \n i razmake(|) medu zadanim nizovima
skupStanja = inputPodataka.readline().strip()  #makni \n
simboliAbecede = inputPodataka.readline().strip()  #makni \n
prihvatljivaStanja = inputPodataka.readline().strip() #ovo je nebitno za zadatak??
pocetnoStanje = inputPodataka.readline().strip()  #makni \n

rjecnik = {} # u njemu drzim funckije prijelaza
for fjaPrijelaza in sys.stdin.readlines(): #nepoznati broj fja iz inputa, punim rjecnik fjama prijelaza
    odvojeniPodatci = fjaPrijelaza.strip().split('->') # makni \n iz svakog retka i odvoji podatke sa lijeve i desne strane strelice
    skupIducihStanja = odvojeniPodatci[1].split(',') #u c je skupIdućihStanja
    if '#' not in skupIducihStanja and '' not in skupIducihStanja: #ako sljedeće stanje nije prazno ili nenavedeno(u zad pise da je ovo moguce??)   
        rjecnik[str(odvojeniPodatci[0])] = odvojeniPodatci[1] #key=(trenutnoStanje,simbolAbecede) value=skupIducihStanja
    else:
       continue  #za sada zanemari i nastavi, to cu rijesiti ako ce mi skup stanja biti prazan

for niz in ulazniNizovi: #za svaki iz zadanih nizova

    niz = niz.split(',')  # dobijem listu bez zareza ('a', 'pnp', 'a') za npr prvi niz

    konacnaStanja = [] #skup svih stanja koja ću ispisati
    trenutnaStanja = [] # skup trenutnih stanja koja cu malo po malo dodavati u konacnaStanja
    trenutnaStanja.append(pocetnoStanje) #uvijek se krece iz pocetnog stanja koje je zadano(isto za sve nizove)

    for znak in niz: #znak po znak iz niza 
        if znak not in simboliAbecede:
            print('Simbol ne pripada abecedi')
        for stanje in trenutnaStanja:
            if stanje not in skupStanja:
                print("Dolazak u nepoznato stanje!")
            prijelazStanja(stanje, '$', trenutnaStanja) #prvo provjeriti epsilon okoline, nadopuniti trenutna stanja

        stringTrenutnihStanja = sortirajOdijeli(trenutnaStanja)

        konacnaStanja.append('#') if stringTrenutnihStanja == '' else konacnaStanja.append(stringTrenutnihStanja)

        novaTrenutnaSTanja = [] #ovdje cuvam stanja do kojih cu doci obicnim prijelazima

        for stanje in trenutnaStanja:
            if stanje not in skupStanja:
                print("Dolazak u nepoznato stanje!")
            prijelazStanja(stanje, znak, novaTrenutnaSTanja) #u nova stanja dodaj stanja u koja smo dosli obicnim prijelazom

        trenutnaStanja = [] #obrisi ono sta je bilo prije u trenutnim
        for x in novaTrenutnaSTanja:
                trenutnaStanja.append(x) #dodaj aktualna trenutna stanja u koja smo dosli prijelazima sa znakovima

    for stanje in trenutnaStanja: #za nova stanja ponovno pogledaj e-okolinu
        if stanje not in skupStanja:
            print("Dolazak u nepoznato stanje!")
        prijelazStanja(stanje, '$', trenutnaStanja)

    stringTrenutnihStanja = sortirajOdijeli(trenutnaStanja)
    konacnaStanja.append('#') if stringTrenutnihStanja == '' else konacnaStanja.append(stringTrenutnihStanja) 
    print('|'.join(konacnaStanja)) #nakon svakog niza znakova ispisi skup koji smo dobili te ih odvoji ravnom crtom