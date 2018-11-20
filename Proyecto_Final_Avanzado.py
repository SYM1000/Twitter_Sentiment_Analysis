def main():
    """
    Funcion principal, que da inicio al programa
    """
    import twitter
    from textblob import TextBlob
    import matplotlib.pyplot as plt
    import time, sys
    from os import system, name

    api = twitter.Api(consumer_key='ivVd9RCTRNO3ciBHCmngdXpVd',
      consumer_secret='0SVJvyCb86IiIehZFAXLprRWMy6Tqv3io9l9ZqZJsnuLLXnlbH',
      access_token_key='1090865726-tjqJrWAQD9O0AqEDztNdvALzJg6kzT0DIN8hhhh',
      access_token_secret='9afD1qMx7Wg69TPNeOQvgOL12SuCwgNsjuwVnfkTEosco')

    def clear():
        """
        Esta funcion sirve para limpiar la terminal
        """
        if name == "posix":
            _ = system("clear")


    def regresar():
        """
        Esta es una funcion que le permitira al usuario regresar al menu
        """
        usuario = input("\nQuieres regresar al menú principal? ").lower()

        if usuario == "si":
            main()
            menu()

        elif usuario == "no":
            print("\nGracias por usar mi programa :)")
            time.sleep(1)
            exit()

        else:
            print("Dato invalido. Las opciones son NO y SI")
            time.sleep(2)
            regresar()


    def imprimir_lista(lista):
        """
        Esta funcion sirve para imprimir listas separando cada elemento por un salto
        de linea
        """
        for x in lista:
             print("\n")
             print(x)


    def loading():
        """
        Esta funcion imprime un simulador de ua contador cargando
        """
        print ("Cargando...")
        for i in range(0, 100):
            time.sleep(0.06)
            sys.stdout.write(u"\u001b[1000D")
            sys.stdout.flush()
            time.sleep(0.00)
            sys.stdout.write(str(i + 1) + "%")
            sys.stdout.flush()
        print()


    def obtener_tweets(palabra):
        """
        Esta funcion utiliza la API de twitter para buscar los twitts que contengan
        una palabra o un hashtag o un usuario
        """
        search = api.GetSearch(palabra)
        tweets_text = []
        for tweet in search:
            tweets_text.append(tweet.text)
        return tweets_text


    def traducir_tweets(lista):
        """
        Esta funcion traduce los tweets de cualquier idioma al ingles, para poder
        ser analizados. Esta funcion regresa la misma lista que recibe, solo traduce
        cada elemento
        """
        for n, x in enumerate(lista):
            analysis = TextBlob(x)
            try:
                lista[n] = analysis.translate(to="en")
            except:
                lista[n] = analysis
        return lista


    def traducir_tweets_espa(lista):
        """
        Esta funcion traduce los tweets de cualquier idioma al español, para poder
        ser mostrados al usuario
        """
        lista_traducida = []
        for n, x in enumerate(lista):
            analysis = TextBlob(x)
            try:
                lista_traducida.append(analysis.translate(to="es"))
            except:
                lista_traducida.append(analysis)

        return lista_traducida


    def analizar_sentimientos(lista):
        """
        Esta funcion es la que se encarga de analizar los sentimientos de cada tweet
        """
        lista_analizada = []
        for n, x in enumerate(lista):
            #analysis = TextBlob(x)
            analysis = x
            analisis = analysis.sentiment
            lista_analizada.append(analisis)
        return lista_analizada


    def limpiador_de_datos(lista_de_tuplas):
        """
        Esta funcion sirve para eliminar los datos que no sirvan para anlizar
        Ejemplo: sentiment(polarity = 0.0, subjectivity = 0.0)
        """

        for n, x in enumerate(lista_de_tuplas):
            if x[0] == 0 and x[1] == 0:
                lista_de_tuplas.remove(x)
                continue
        return lista_de_tuplas


    def promedio_de_datos(lista_de_tuplas):
        """
        Esta funcion recibe la lista de datos analizados depues de la limpieza y nos
        regresa una lista con el promedio de la polaridad y la subjetividad
        """
        lista_de_resultados = []
        polaridad = 0
        subjetividad = 0

        if len(lista_de_tuplas) == 0:
            return False

        else:
            for x in lista_de_tuplas:
                polaridad = polaridad + x.polarity
                subjetividad = subjetividad + x.subjectivity

            polaridad = polaridad/len(lista_de_tuplas)
            subjetividad = subjetividad/len(lista_de_tuplas)

            lista_de_resultados.append(polaridad)
            lista_de_resultados.append(subjetividad)

            return lista_de_resultados


    def grafica_de_datos(lista_de_tuplas,promedio):
        """
        Esta funcion grafica los datos obtenidos
        """
        x = [] #Polaridad es x en la grafica
        y = [] #Subjetivdad es y en la grafica
        x_promedio = [promedio[0]] #Polaridad promedio en la grafica
        y_promedio = [promedio[1]] #Subjetivdad promedio en la grafica

        for dato in lista_de_tuplas:
            x.append(dato.polarity)
            y.append(dato.subjectivity)

        plt.scatter(x,y, label="Sentimiento por tweet", color = "red", s=50, marker=".")
        plt.scatter(x_promedio,y_promedio, label = "Promedio", color = "blue", s=75, marker = "o")
        plt.ylabel("Subjetividad")
        plt.xlabel("Polaridad")
        plt.title("Análisis de Sentimientos en Twitter\n")
        plt.legend()
        plt.show()

    #---------------------------------------------------------------------------
    def menu():
        """
        Esta funcion muestra el menu
        """

        clear()
        titulo = "     TWITTER SENTIMENT ANALYSER     ".center(80, "-")
        opc_1 = "[1] - Iniciar Programa".center(80)
        opc_3 = "[3] - Salir".center(80)
        opc_2 = "[2] - Creditos".center(80)

        print(titulo)
        print("\n\n")
        print(opc_1)
        print(opc_2)
        print(opc_3)

        usuario = input("\nSelecciona la opción que deseas correr: ")

        if usuario == "1":
            clear()
            print(titulo)
            palabra =  input("\n\nPalabra a buscar en twitter: ")
            promedio = promedio_de_datos(limpiador_de_datos(analizar_sentimientos(traducir_tweets(obtener_tweets(palabra)))))

            if promedio == False:
                clear()
                print(titulo)
                print("\n\n")
                loading()
                time.sleep(1)
                clear()
                print(titulo)
                print("\nNo se encontrarón tweets para la busqueda:", palabra)
                time.sleep(3)
                regresar()

            else:
                #Aqui se validan los datos
                while True:
                    datos = input("\nQuieres ver los tweets obtenidos? ")
                    if datos.lower() == "si" or datos.lower() == "no":
                        break
                    else:
                        print("---> respuesta invalida <---")
                        continue

                while True:
                    grafica = input("\nQuieres ver la gráfica de los datos obtenidos? ")
                    if grafica.lower() == "si" or grafica.lower() == "no":
                        break
                    else:
                        print("---> respuesta invalida <---")
                        continue
                clear()

                if datos.lower() == "si" or grafica.lower() == "si":
                    print(titulo)
                    print("\n\n")
                    loading()
                    print("Analisis completado satisfactoriamente")
                    time.sleep(3)
                    clear()
                else:
                    print(titulo)
                    regresar()


                if datos == "si":
                    print(titulo)
                    print("\n\nTweets obtenidos:")
                    print(imprimir_lista(traducir_tweets_espa(obtener_tweets(palabra))))


                if grafica == "si":
                    print(titulo)
                    print(grafica_de_datos(limpiador_de_datos(analizar_sentimientos(traducir_tweets(obtener_tweets(palabra)))),promedio))

                regresar()

        elif usuario == "3":
            clear()
            print(titulo)
            print("\n\nGracias por usar mi programa ")
            exit()

        elif usuario == "2":
            clear()
            print(titulo)
            print("\nCreado por: Santiago Yeomans")
            print("Fecha: Sábado 18 de Noviembre")
            print("Lugar: Guadalajara")
            print("Lenguaje: Python 3")
            regresar()

        else:
            print("\nDato Invaldio")
            time.sleep(2.5)
            clear()
            menu()
    menu()


main() #Aqui iniciara el programa
