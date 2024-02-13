# Proyecto: C O W B O Y

## Descripción:

Cowboy es un juego construido sobre la libreria [Pygame](https://www.pygame.org/news).

El juego es un shooter muy simple con vista aerea que se trata de un vaquero que debe destruir la mayor cantidad de enemigos, a medida que pasa el tiempo es mayor la probabilidad de que aparezcan enemigos, es un juego infinito que se acaba cuando una planta rodadora o un demonio llega a tener contacto con el jugador.

## Funcionalidad - cowboy.py

El proyecto trabaja sobre un While loop que está constantemente rectificando una variable _game_state_, esta variable puede corresponder a diferentes strings que igualmente llaman a una función del mismo nombre presente en el archivo.

Estas funciones que llama este loop son:

- _main_menu()_:

  Esta función se encarga de mostrar y gestionar el menú principal del juego. Al inicio, carga una imagen de fondo y entra en un bucle que se ejecuta hasta que el jugador decide iniciar el juego, ver la información del juego o salir del juego. En cada ciclo del bucle, la función actualiza la posición del ratón, dibuja el fondo y el texto del menú principal, y crea tres botones: “PLAY”, “INFO” y “QUIT”. Si el jugador mueve el ratón sobre alguno de los botones, este cambia de color. Si el jugador hace clic en el botón “PLAY”, la función devuelve el string _“play”_, lo que indica que el juego debe comenzar. Si el jugador hace clic en el botón “INFO”, la función retona _"info"_, lo que lleva al jugador a la pantalla de información del juego. Si el jugador hace clic en el botón _“QUIT”_, el juego se cierra.

- _info()_:

  Esta función muestra la pantalla de información del juego. Primero, carga una imagen de fondo y luego entra en un bucle que se ejecuta hasta que el jugador decide volver al menú principal. En cada ciclo del bucle, la función actualiza la posición del ratón, dibuja el fondo y el texto de la pantalla de información, y muestra una serie de instrucciones. También crea un botón “BACK” que el jugador puede pulsar para volver al menú principal. Si el jugador mueve el ratón sobre el botón, este cambia de color. Si el jugador hace clic en el botón, la función devuelve el string _“main_menu”_, lo que indica que el juego debe volver al menú principal.

- _end_of_game()_:

  Esta función se ejecuta cuando el juego ha terminado. Al igual que info(), end*of_game() entra en un bucle que se ejecuta hasta que el jugador decide reiniciar el juego. En cada ciclo del bucle, la función actualiza la posición del ratón, muestra un mensaje indicando que el juego ha terminado y crea un botón “TRY AGAIN?”. Si el jugador mueve el ratón sobre el botón, este cambia de color. Si el jugador hace clic en el botón, la función devuelve el string *“play”\_, lo que indica que el juego debe reiniciarse.

- _play()_:

  Esta función es el corazón del juego, donde se maneja la lógica principal del juego y se actualiza el estado del juego. Al inicio, se declaran y crean varias clases heredadas del objeto Sprite de Pygame para el vaquero (**_Player_**) , los enemigos (**_Tumbleweed_** y **_Demon_**) y las balas que disparan(**_Bullets_**).

  Luego se crean varios grupos de sprites y se añade el jugador a all_sprites_group. Luego, se establecen varios eventos temporizados para spawnear TumbleWeed y aumentar la dificultad del juego. Dentro del bucle principal del juego, se manejan varios eventos de entrada del usuario y se actualiza el estado del juego en consecuencia. Si se dispara el evento **SPAWN_TUMBLEWEED**, se spawnea una cantidad aleatoria de TumbleWeed en posiciones aleatorias fuera de la pantalla. Si se dispara el evento **SPAWN_FREQUENCY**, se incrementa la cantidad de TumbleWeed que se spawnea cada vez, hasta un máximo de 4, y se spawnea un Demon en una posición aleatoria.

  Luego, se dibuja el fondo del juego y se manejan las colisiones entre las balas y los enemigos. Si una bala golpea a un enemigo, se reduce la vida del enemigo y se elimina la bala. Si la vida de un enemigo llega a 0, se elimina el enemigo. Si un enemigo colisiona con el jugador, el juego termina y la función devuelve el string _“end_of_game”_. Finalmente, se dibujan todos los sprites en la pantalla, se actualizan los sprites y se actualiza la pantalla. El bucle del juego se ejecuta a una velocidad constante determinada por FPS(60), esto para darle un techo de ejecución al programa.

### button.py

En este archivo está la clase **_Button_**, esta clase representa un botón interactivo en el juego; Cada objeto Button tiene una imagen(opcional), una posición, un texto, una fuente y dos colores (uno base y otro cuando el ratón está encima del botón). Es una clase creada para evitar repetir código a la hora de crear botonoes interactivos con el mouse en los menús del juego.

### setting.py

Este archivo es el encargado de manejar configuraciones de juego y _constantes_ para la ejecución del programa.

### Assets:

Aquí van links a los assets utilizados en el juego.

- https://opengameart.org/content/grass-land-tiles

- https://opengameart.org/content/stretchy-cowboy

- https://www.deviantart.com/jaylastar/art/Tumbleweed-Animation-Game-Jam-Asset-609215222

- https://opengameart.org/content/cowboy-with-rifle

- https://opengameart.org/content/seamless-desert-background-in-parts

### TODO:

- Estaría bueno implementar un puntaje/score y hasta un temporizador para que el jugador tenga más feedback de lo que ha ocurrido.

- Queda pendiente un menú de pausa que está apenas comenzándose.
