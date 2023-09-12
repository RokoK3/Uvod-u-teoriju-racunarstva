import sys
import fileinput

def generirajKljuc(znak1, znak2):
    return znak1 + ',' + znak2

inputPodataka = fileinput.input() #ulazni "stream" podataka

svaStanja = inputPodataka.readline().strip().split(',') #makni \n i zareze medu zadanim stanjima
simboliAbecede = inputPodataka.readline().strip().split(',')   #makni \n i zareze
prihvatljivaStanja = inputPodataka.readline().strip().split(',')  #makni \n i zareze
pocetnoStanje = inputPodataka.readline().strip()  #makni \n 
 
rjecnik = {} # u njemu drzim funckije prijelaza
for fjaPrijelaza in sys.stdin.readlines():
    odvojeniPodatci = fjaPrijelaza.strip().split('->') #makni \n iz svakog retka i odvoji podatke sa lijeve i desne strane strelice
    rjecnik[str(odvojeniPodatci[0])] = odvojeniPodatci[1] #key=(trenutnoStanje,simbolAbecede) value=iduceStanje

dohvatljivaStanja = [pocetnoStanje] #lista za dohvatljiva stanja, u nju odmah dodam pocetno 

promjena = True
while(promjena == True): #sve dok ima novih dohvatljivih stanja
    promjena = False
    novaStanja = [] # u ovu listu dodajem nova dohvatljiva stanja
    for stanje in dohvatljivaStanja: #iteriram po dohvatljivim
        for simbol in simboliAbecede:
            key = generirajKljuc(stanje,simbol)
            if key in rjecnik:  #(stanje,simbol) : noviSimbol
                if rjecnik.get(key) not in dohvatljivaStanja:
                    novaStanja.append(rjecnik.get(key))
                    promjena = True
    for novoStanje in novaStanja:
        if novoStanje not in dohvatljivaStanja: #ako vec nije u dohvatljivim dodaj ga
            dohvatljivaStanja.append(novoStanje)

dohvatljivaStanja.sort()

nedohvatljivaStanja = []
for stanje in svaStanja: #ako nije u dohvatljivim onda je nedohvatljiv
    if stanje not in dohvatljivaStanja:
        nedohvatljivaStanja.append(stanje)

for stanje in nedohvatljivaStanja:
    if stanje in prihvatljivaStanja:
        prihvatljivaStanja.remove(stanje) #izbaci iz prihvatljivih stanja
    for key,value in rjecnik.copy().items():
        if stanje == value:
            rjecnik.pop(key)  #izbaci fju prijelaza u kojoj se pojavljuje nedohvatljivo stanje
    for simbol in simboliAbecede:
        key = generirajKljuc(stanje,simbol)
        if key in rjecnik:
            rjecnik.pop(key)   #izbaci fju prijelaza u kojoj se pojavljuje nedohvatljivo stanje

table = {} #dictionary u kojem cu drzati par stanja, ako ih u tablici X-am onda im je vrijednost True
for i in range(len(dohvatljivaStanja)-1):
    for j in range(i+1, len(dohvatljivaStanja)):
        komb = dohvatljivaStanja[i]+','+dohvatljivaStanja[j]
        if dohvatljivaStanja[i] not in prihvatljivaStanja and dohvatljivaStanja[j] in prihvatljivaStanja: #ispitujem uvjet podudarnosti 
            table[komb] = True  # X u tablici          
        elif dohvatljivaStanja[i] in prihvatljivaStanja and dohvatljivaStanja[j] not in prihvatljivaStanja: #ispitujem uvjet podudarnosti 
            table[komb] = True
        else: 
            table[komb] = False

promjena = True         
while(promjena == True): #vrti petlju sve dok se desava promjena u tablici kako bi se mogli provjeriti novi eventualni X-evi
    promjena = False
    for i in range(len(dohvatljivaStanja)-1):
        for j in range(i+1,len(dohvatljivaStanja)):
            for simbol in simboliAbecede:
                stanjeI = generirajKljuc(dohvatljivaStanja[i],simbol)
                stanjeJ = generirajKljuc(dohvatljivaStanja[j],simbol)
                komb = str(rjecnik.get(stanjeI)) + ',' + str(rjecnik.get(stanjeJ)) #par stanja u koji se za simbol prelazi
                obrnutaKomb = str(rjecnik.get(stanjeJ)) + ',' + str(rjecnik.get(stanjeI))#obrnuti poredak para stanja u koji se za simbol prelazi
                if table.get(komb) == True: #ako je taj par X u tablici
                    parTablice = generirajKljuc(dohvatljivaStanja[i],dohvatljivaStanja[j])
                    if table[parTablice] == False: #ovo mi samo provjerava da ga X-am prvi put
                        table[parTablice] = True #oznaci taj par sa X
                        promjena = True #vrti ponovno jer mozda taj X utjece na neki drugi par
                elif table.get(obrnutaKomb) == True: #sve isto samo za obrnuti poredak
                    parTablice = generirajKljuc(dohvatljivaStanja[i],dohvatljivaStanja[j])
                    if table[parTablice] == False:
                        table[parTablice] = True
                        promjena = True
  
istovjetnaStanja = []
for key, value in table.items(): #za svaki par tablice
    parStanja = key.split(',')    
    if value == False: #ako nije X
        istovjetnaStanja.append(parStanja[1]) #u istovjetna dodaj leksikograski vece stanje
        for key2,value2 in rjecnik.items(): # iteracija po fjama prijelaza
            if value2 == parStanja[1]: # ako je sa desne strane fje prijalaz istovjetno stanje
                rjecnik[key2] = parStanja[0] #promjeni ga
        if pocetnoStanje == parStanja[1]:
            pocetnoStanje = parStanja[0]

for istovjetno in istovjetnaStanja: #micem istovjetna stanja sa svih mjesta gdje mi vise ne trebaju
    for simbol in simboliAbecede: # iz simbola abecede
        key = generirajKljuc(istovjetno,simbol)
        if key in rjecnik:
            rjecnik.pop(key) #iz fja prijelaza          
    if istovjetno in prihvatljivaStanja: #iz prihvatljivih stanje
        prihvatljivaStanja.remove(istovjetno)
    if istovjetno in dohvatljivaStanja: #iz dohvatljivih stanja
        dohvatljivaStanja.remove(istovjetno)

print(','.join(dohvatljivaStanja)) #ispisi sve u svoj redak odvojeno zarezom
print(','.join(simboliAbecede))
print(','.join(prihvatljivaStanja))
print(pocetnoStanje)
for key,value in rjecnik.items():
    print(key + '->' + value)