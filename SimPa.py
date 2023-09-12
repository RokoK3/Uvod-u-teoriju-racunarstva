import sys
import fileinput

inputPodataka = fileinput.input()

ulazniNizovi = inputPodataka.readline().strip().split('|')
skupStanja = inputPodataka.readline().strip()
ulazniZnakovi = inputPodataka.readline().strip()
znakoviStoga = inputPodataka.readline().strip()
prihvatljivaStanja = inputPodataka.readline().strip().split(',')
pocetnoStanje = inputPodataka.readline().strip()
pocetniStog = inputPodataka.readline().strip()

rjecnik = {}
for fjaPrijelaza in sys.stdin.readlines():
    odvojeniPodatci = fjaPrijelaza.strip().split('->')
    rjecnik[str(odvojeniPodatci[0])] = odvojeniPodatci[1]

for niz in ulazniNizovi:
    niz = niz.split(',')
    stog = '' + pocetniStog
    trenutnoStanje = pocetnoStanje
    pocetniIspis = pocetnoStanje + '#' + pocetniStog
    ispisLista = [pocetniIspis]
    fail = 0
    i = 0
    while i < len(niz):
        znak = niz[i]
        vrhStoga = stog[0]
        key = trenutnoStanje + ',' + znak + ',' + vrhStoga
        key2 = trenutnoStanje + ',' + '$' + ',' + vrhStoga
        if key in rjecnik:
            novo = rjecnik.get(key).split(',')
            trenutnoStanje = novo[0]
            if novo[1] == '$' :
                stog = stog[1:]
                if stog == '':
                    stog = stog + '$'
            else:
                stog = stog[1:]
                stog = novo[1] + stog
            stringIspis = trenutnoStanje + '#' + stog
            ispisLista.append(stringIspis)
            i+=1
        elif key2 in rjecnik:
            novo = rjecnik.get(key2).split(',')
            trenutnoStanje = novo[0]
            if novo[1] == '$':
                stog = stog[1:]
                if stog == '':
                    stog = stog + '$'
            else:
                stog = stog[1:]
                stog = novo[1] + stog
            stringIspis = trenutnoStanje + '#' + stog
            ispisLista.append(stringIspis)    
        else:
            ispisLista.append('fail')
            fail = 1
            break
        
        promjena = True
        while(promjena):
            promjena = False
            vrhStoga = stog[0]
            key2 = trenutnoStanje + ',' + '$' + ',' + vrhStoga
            if trenutnoStanje in prihvatljivaStanja:
                break
            if key2 in rjecnik:
                novo = rjecnik.get(key2).split(',')
                trenutnoStanje = novo[0]
                if novo[1] == '$':
                    stog = stog[1:]
                    if stog == '':
                        stog = stog + '$'
                else:
                    stog = stog[1:]
                    stog = novo[1] + stog
                stringIspis = trenutnoStanje + '#' + stog
                ispisLista.append(stringIspis)
                promjena = True
    
    if trenutnoStanje in prihvatljivaStanja  and fail != 1:
        ispisLista.append('1')
    else:
        ispisLista.append('0')
    print('|'.join(ispisLista))