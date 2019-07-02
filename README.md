# CryptoMonedas


Creamos un contenedor que contendrá MongoDB 
--------------------------------------------
Para guardar toda la información de las criptomonedas.
$ docker run -d --name=mongo-crypto mongo:3.4

Correr contenedor con MongoDB
-----------------------------
$ docker start mongo-crypto

Correr agente
-------------
$ cd app/agent
$ ./agent.sh

Correr app
-------------
$ cd app/app
$ ./api.sh
