RESET = "\033[0m"            # Reinicia el color del text
BLANCO = "\033[97m"          # Color blanc per a peces blanques
NEGRO = "\033[34m"           # Color blau per a peces negres
FONDO_CLARO = "\033[47m"     # Fons clar del tauler
FONDO_OSCURO = "\033[100m"   # Fons fosc del tauler

tauler = [
    ["r","n","b","q","k","b","n","r"],  # Peces negres
    ["p","p","p","p","p","p","p","p"],  # Peons negres
    [" "," "," "," "," "," "," "," "],  # Files buides
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    ["P","P","P","P","P","P","P","P"],  # Peons blancs
    ["R","N","B","Q","K","B","N","R"]   # Peces blanques
]

#Mostrar el tauler del escacs
def mostrar_tauler():
    for i, fila in enumerate(tauler):  # Recorre cada fila
        for j, pieza in enumerate(fila):  # Recorre cada columna
            fondo = FONDO_CLARO if (i + j) % 2 == 0 else FONDO_OSCURO  # Alterna colors del tauler

            if pieza.isupper():
                color = BLANCO  # Peces blanques
            elif pieza.islower():
                color = NEGRO   # Peces negres
            else:
                color = ""      # Casella buida

            print(fondo + color + f" {pieza} " + RESET, end="")  # Mostra la peça amb color
        print()
    print()


def dentro_tablero(x, y):
    return 0 <= x < 8 and 0 <= y < 8  # Comprova que la posició està dins del tauler


def camino_libre(x1, y1, x2, y2):
    dx = x2 - x1  # Diferència vertical
    dy = y2 - y1  # Diferència horitzontal

    if dx > 0:
        paso_x = 1
    elif dx < 0:
        paso_x = -1
    else:
        paso_x = 0

    if dy > 0:
        paso_y = 1
    elif dy < 0:
        paso_y = -1
    else:
        paso_y = 0

    x = x1 + paso_x  # Avança una posició
    y = y1 + paso_y

    while x != x2 or y != y2:  # Mentre no arribi al destí
        if tauler[x][y] != " ":  # Si hi ha una peça al mig
            return False         # El camí no està lliure
        x += paso_x
        y += paso_y

    return True  # El camí està lliure


def mover_peon(x1, y1, x2, y2):
    pieza = tauler[x1][y1]

    direccion = -1 if pieza.isupper() else 1  # Direcció segons color

    if y1 == y2 and tauler[x2][y2] == " ":  # Moviment recte
        if x2 == x1 + direccion:
            return True

        if pieza.isupper() and x1 == 6:  # Moviment doble inicial blanc
            if x2 == x1 - 2 and tauler[5][y1] == " ":
                return True

        if pieza.islower() and x1 == 1:  # Moviment doble inicial negre
            if x2 == x1 + 2 and tauler[2][y1] == " ":
                return True

    if (y2 == y1 + 1 or y2 == y1 - 1) and x2 == x1 + direccion:  # Captura diagonal
        if tauler[x2][y2] != " " and tauler[x2][y2].isupper() != pieza.isupper():
            return True

    return False  # Moviment no vàlid


def mover_caballo(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx < 0: dx = -dx
    if dy < 0: dy = -dy

    return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)  # Moviment en L


def mover_torre(x1, y1, x2, y2):
    if x1 == x2 or y1 == y2:  # Moviment recte
        return camino_libre(x1,y1,x2,y2)
    return False


def mover_alfil(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx < 0: dx = -dx
    if dy < 0: dy = -dy

    if dx == dy:  # Moviment diagonal
        return camino_libre(x1,y1,x2,y2)

    return False



def movimiento_valido(x1, y1, x2, y2, turno_blanco):

    if not dentro_tablero(x1,y1) or not dentro_tablero(x2,y2):  # Fora del tauler
        return False

    pieza = tauler[x1][y1]

    if pieza == " ":  # Casella buida
        return False

    if pieza.isupper() != turno_blanco:  # No és el seu torn
        return False

    destino = tauler[x2][y2]

    if destino != " " and destino.isupper() == pieza.isupper():  # No pot menjar peça pròpia
        return False

    pieza = pieza.lower()

    if pieza == "p":
        return mover_peon(x1,y1,x2,y2)
    elif pieza == "n":
        return mover_caballo(x1,y1,x2,y2)
    elif pieza == "r":
        return mover_torre(x1,y1,x2,y2)
    elif pieza == "b":
        return mover_alfil(x1,y1,x2,y2)

    return False


def mover(x1, y1, x2, y2):
    tauler[x2][y2] = tauler[x1][y1]  # Mou la peça
    tauler[x1][y1] = " "             # Deixa buida la posició original



def main():

    jugadors = []

    for i in range(2):
        nom = input(f"Nom jugador {i+1}: ")  # Demana nom
        jugadors.append(nom)                 # Guarda nom

    turno_blanco = True        # Comencen les blanques
    partida_activa = True      # La partida està activa

    while partida_activa:

        mostrar_tauler()  # Mostra el tauler

        torn_actual = 0 if turno_blanco else 1
        color_text = "Blanques" if turno_blanco else "Negres"

        print(f"Torn de {jugadors[torn_actual]} ({color_text})")  # Mostra torn
        print("1 - Rendirse")
        print("2 - Moure")

        opcio = int(input("Opció: "))  # Llegeix opció

        if opcio == 1:  # Si es rendeix
            guanyador = 1 - torn_actual
            print(f"\nHa guanyat {jugadors[guanyador]}!")  # Mostra guanyador
            partida_activa = False  # Finalitza partida

        elif opcio == 2:  # Si vol moure
            try:
                x1 = int(input("Fila origen: "))
                y1 = int(input("Columna origen: "))
                x2 = int(input("Fila destí: "))
                y2 = int(input("Columna destí: "))

                if movimiento_valido(x1,y1,x2,y2,turno_blanco):
                    mover(x1,y1,x2,y2)       # Fa el moviment
                    turno_blanco = not turno_blanco  # Canvia torn
                else:
                    print("Moviment invàlid")  # Si el moviment no és correcte

            except:
                print("Error en les dades")  # Si hi ha error d’entrada

        else:  # Si l’opció no és 1 ni 2
            print("Opció incorrecta")  # Mostra missatge d’error

if __name__ == "__main__":
    main()
