import fileinput
inputPodataka = fileinput.input()

ulazniNiz = inputPodataka.readline().strip()

stringNezavrsnih = ''
i = 0

def greskaKraj():
    print(stringNezavrsnih)
    print("NE")
    quit()

def S():
    # S → aAB | bBA
    global stringNezavrsnih, i
    stringNezavrsnih += 'S'

    if(i<len(ulazniNiz)):
        if(ulazniNiz[i]=='a'):
            i += 1
            A()
            B()
        elif (ulazniNiz[i]=='b'):
            i+= 1
            B()
            A()
        else:
            greskaKraj()
    else:
        greskaKraj()

def A():
    # A → bC | a
    global stringNezavrsnih, i
    stringNezavrsnih += 'A'
    if(i<len(ulazniNiz)):
        if(ulazniNiz[i]=='b'):
            i+= 1
            C()
        elif (ulazniNiz[i]=='a'):
            i += 1
        else:
            greskaKraj()
    else:
        greskaKraj()

def B():
    # B → ccSbc | ϵ
    global stringNezavrsnih, i
    stringNezavrsnih += 'B'

    if(i<len(ulazniNiz)):
        if(ulazniNiz[i]=='c'):
            if(ulazniNiz[i+1] =='c'):
                i=i+2
                S()
    if(i+1<len(ulazniNiz)):
        if(ulazniNiz[i]=='b'):
            if(ulazniNiz[i+1] =='c'):
                i=i+2

def C():
    # C → AA
    global stringNezavrsnih
    stringNezavrsnih += 'C'
    A()
    A()

#--------------------------------------------------------------------------
S()
if(i != len(ulazniNiz)):
    greskaKraj()
else:
    print(stringNezavrsnih)
    print("DA")