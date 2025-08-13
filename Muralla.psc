Algoritmo Muralla // es un codigo en el cual voy a utilizar variable
	Definir num Como Entero
	pares <- 0
	impares <- 0
	Para i <-1 Hasta 10 Con Paso 1 Hacer
		Leer num
		Si num MOD  2=0 Entonces
			pares <- pares +1
		SiNo
			impares <- impares + 1
		Fin Si
	Fin Para
	Escribir  " pares " , pares  " impares " , impares
FinAlgoritmo
