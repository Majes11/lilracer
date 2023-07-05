import sys
import time
import keyboard
import random

def draw_banner():
    banner = """
      :::        ::::::::::: :::       :::          :::::::::      :::      ::::::::  :::::::::: ::::::::: 
     :+:            :+:     :+:       :+:           :+:    :+:   :+: :+:   :+:    :+: :+:        :+:    :+: 
    +:+            +:+     +:+                    +:+    +:+  +:+   +:+  +:+        +:+        +:+    +:+  
   +#+            +#+     +#+                    +#++:++#:  +#++:++#++: +#+        +#++:++#   +#++:++#:    
  +#+            +#+     +#+                    +#+    +#+ +#+     +#+ +#+        +#+        +#+    +#+    
 #+#            #+#     #+#                    #+#    #+# #+#     #+# #+#    #+# #+#        #+#    #+#     
########## ########### ##########             ###    ### ###     ###  ########  ########## ###    ###      
    """
    
    author = "by Maik Jeschke"
    print(banner)
    print(author)
    print()

def draw_track(car_position, car_row, obstacles, score):
    track_width = 30
    track_height = 10
    track_border = '|'
    track_blank = ' '
    track_obstacle = 'X'
    track_score = '#'

    track = track_border + track_blank * (track_width - 2) + track_border

    # Obere Planke zeichnen
    print(track)

    # Mittlere Spur mit Auto und Hindernissen zeichnen
    for i in range(track_height):
        if i == car_row:
            car_row_str = track_border + track_blank * (car_position - 2) + '🚗' + track_blank * (track_width - car_position - 1) + track_border
            print(car_row_str)
        elif i in obstacles:
            obstacle_row = track_border + track_blank * (obstacles[i] - 1) + track_obstacle + track_blank * (track_width - obstacles[i] - 2) + track_border
            print(obstacle_row)
        else:
            print(track)

    # Untere Planke zeichnen
    print(track)

    # Punktzahl anzeigen
    print("Punkte:", score)

def main():
    while True:
        car_position = 15  # Startposition des Autos
        car_row = 5  # Startreihe des Autos
        obstacles = {}  # Wörterbuch zur Speicherung der Hindernispositionen
        score = 0
        speed = 0.1
        paused = False

        try:
            while True:
                # Bildschirm leeren
                sys.stdout.write('\033[2J\033[H')

                draw_banner()

                # Zufällige Hindernisse generieren
                if not paused and random.random() < 0.2:  # Wahrscheinlichkeit, dass ein Hindernis erscheint
                    row = random.randint(0, 9)
                    obstacles[row] = random.randint(2, 29)

                # Hindernisse bewegen
                for row in obstacles:
                    obstacles[row] -= 1

                # Hindernisse entfernen, die aus der Spur herausbewegt sind
                obstacles = {row: pos for row, pos in obstacles.items() if pos > 1}

                draw_track(car_position, car_row, obstacles, score)

                # Tastatureingaben überprüfen
                if keyboard.is_pressed('left') and car_position > 2:
                    car_position -= 1
                elif keyboard.is_pressed('right') and car_position < 29:
                    car_position += 1
                elif keyboard.is_pressed('up') and car_row > 0:
                    car_row -= 1
                elif keyboard.is_pressed('down') and car_row < 9:
                    car_row += 1
                elif keyboard.is_pressed('space'):
                    paused = not paused
                    time.sleep(0.5)  # Pause, um Tastendruck zu erkennen

                if paused:
                    print("Spiel pausiert. Drücke Leertaste erneut, um fortzufahren.")
                    time.sleep(0.1)
                    continue

                # Kollision mit Hindernissen überprüfen
                if (car_row, car_position) in obstacles.items():
                    print("Kollision mit Hindernis! Du hast", score, "Punkte erreicht.")
                    print("Drücke Enter, um es erneut zu versuchen.")
                    while True:
                        if keyboard.is_pressed('enter'):
                            break
                        time.sleep(0.1)
                    break

                # Kollision mit Leitplanken überprüfen
                if car_position == 2 or car_position == 29:
                    print("Kollision mit der Leitplanke! Du hast", score, "Punkte erreicht.")
                    print("Drücke Enter, um es erneut zu versuchen.")
                    while True:
                        if keyboard.is_pressed('enter'):
                            break
                        time.sleep(0.1)
                    break

                # Punktzahl erhöhen, wenn Hindernissen erfolgreich ausgewichen wurde
                if obstacles:
                    score += 1

                # Anpassung der Spielgeschwindigkeit
                if speed < 0.2:  # Maximale Geschwindigkeitsgrenze
                    speed += 0.0001  # Langsame Erhöhung der Geschwindigkeit

                time.sleep(speed)

        except Exception as e:
            print("Ein Fehler ist aufgetreten:", str(e))

if __name__ == '__main__':
    main()
