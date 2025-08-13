Algoritmo codigo_inventado //  mision car
	Escribir " _____ mision carro ____"
	Para avanza<-1 Hasta 20 Con Paso 1 Hacer
		Escribir " avanzo " , avanza
		Si avanza MOD 3=0 Entonces
			Escribir " gira a la izquierda"
		Fin Si
		Si avanza MOD 5 = 0 Entonces
			Escribir "pitar"
		Fin Si
		Si avanza MOD 4=0 Entonces
			Escribir " gira a la derecha"
		Fin Si
	Fin Para
	Escribir " has llegado a tu destino "
	
FinAlgoritmo
