import os
from flask import Flask , render_template, request, redirect, url_for
from Scripts.funciones import *

barrios = lista_valores_unicos('BARRIO')
tipos_accidentes = lista_valores_unicos('CLASE_ACCIDENTE')
cluster_0 = lista_cluster(0)
cluster_1 = lista_cluster(1)
cluster_2 = lista_cluster(2)
cluster_3 = lista_cluster(3)
cluster_4 = lista_cluster(4)
cluster_5 = lista_cluster(5)

TEXT = {
    "Todos": {
        "general": "Recomendaciones generales de seguridad vial",
        "estrategia1": "Se les aconseja mantener una conducción segura y respetuosa en todo momento, prestando especial atención a las normas de tráfico y a las condiciones locales de la vía. Además, es importante que estén alerta a la presencia de peatones y ciclistas, ya que las zonas urbanas suelen tener una mayor interacción entre los diferentes tipos de usuarios de la vía. Esto contribuirá a la seguridad de todos y a la convivencia en el tráfico de la ciudad.",
        "estrategia2": "Prestar mayor atención a la cantidad de accidentes que han ocurrido en estos barrios y asignar más agentes de tránsito para que ayuden a establecer un orden en la vía.",
        "estrategia3":"",
    },
    "Grupo 0": {
        "general": "Este grupo se compone de barrios con calles estrechas y pendientes, por tal motivo se propone lo siguiente:",
        "estrategia1": "Crear una campaña con inteligencia artificial que sea llamativa para los conductores, motivando la responsabilidad vial y el buen control de accidentes que se le puede brindar a los barrios en pro de la conciencia vial. ",
        "estrategia2": "Establecer cámaras de fotomultas y de velocidad en las intersecciones y en los tramos de vías con mayor cantidad de choques, permitiendo a los conductores saber de su cercanía a estas mismas y poder manejar más conscientes. ",
        "estrategia3":"",
        },
    "Grupo 1": {
        "general": "Este grupo se compone de áreas instituciones, laborales y sociales, por eso se propone lo siguiente:",
        "estrategia1": "Crear campañas de concientización para los estudiantes de universidades, trabajadores  y en empresas del sector, con publicidad creativa y con gran alcance en redes sociales, dando a conocer las consecuencias de conducir trasnochado, tomado o distraído. ",
        "estrategia2": "Crear uno o varios robots de realidad virtual que se establezcan en los parqueaderos de lugares públicos, universidades y empresas para que brinden estrategias de prevención de choques y permita la  interacción con la misma.",
        "estrategia3":"",
        },
    "Grupo 2": {
        "general": "Este grupo se caracteriza por tener más espacios deportivos y parques, por eso, se propone lo siguiente:",
        "estrategia1": "Implementar más señalizaciones y luces tanto de día y de noche que resalten y sean visibles para los conductores. ",
        "estrategia2": "En los parques y espacios deportivos poner robots que hagan un recorrido en un pequeño vehículo con el fin de llamar la atención de las personas y que estos incentiven conducir sin afanes y conscientes.",
        "estrategia3":"",
        },
    "Grupo 3": {
        "general": "Los barrios de este grupo se caracterizan por tener plazas muy importantes para la ciudad como por ejemplo la plaza de botero, la iglesia del perpetuo socorro, sitios turísticos y por talleres y bodegas, por lo tanto ser muy concurridos tanto por habitantes de la ciudad como turistas, por ello se proponen las siguientes estrategias para disminuir la gran cantidad de accidentes que ocurren en estos barrios.",
        "estrategia1": " Por medio de la secretaría de movilidad y la alcaldía, brindar la posibilidad de tener acceso a sistemas avanzados de detección de colisiones que puedan advertir a los conductores de situaciones de peligro de choque, como sensores de proximidad y sistemas de frenado automático. Esta medida aplica para personas con vehículos en estos barrios como para la ciudad en general.",
        "estrategia2": "Prestar mayor atención a la cantidad de accidentes que han ocurrido en estos barrios y asignar más agentes de tránsito para que ayuden a establecer un orden en la vía.",
        "estrategia3": "Ubicar estratégicamente grúas, que están disponibles en los tramos de vía con mayor accidentalidad para brindar una pronta atención al conductor y el vehículo, logrando reducir la congestión cuando ocurre un choque y posibles accidentes que pueden ocurrir en cadena.",
        },
    "Grupo 4": {
        "general": "Los barrios pertenecientes a este grupo se caracterizan por ser residenciales y comerciales, cuenta con centros comerciales y locales de venta, por ello se propone lo siguiente: ",
        "estrategia1": "Ubicar estratégicamente grúas, que están disponibles en los tramos de vía con mayor accidentalidad para brindar una pronta atención al conductor y el vehículo, logrando reducir la congestión cuando ocurre un choque y posibles accidentes que pueden ocurrir en cadena. ",
        "estrategia2": "Trabajar en conjunto con la industria automotriz para incorporar tecnologías de seguridad avanzadas en los vehículos y promover la fabricación de vehículos más seguros.",
        "estrategia3": "Compartir en las unidades y cerca a los hogares, información de cómo prevenir accidentes.",
        },
    "Grupo 5": {
        "general": "Este grupo en particular se caracteriza por tener un gran cantidad de barrios académicos, específicamente escolares, también con vías con integración al metro, tranvía y metroplús, por ello se propone lo siguiente:",
        "estrategia1": "Ubicar agentes de tránsito en las principales intersecciones con el fin de que ayuden a la movilización y control de las vías.",
        "estrategia2": "Trabajar de la mano con la secretaría de movilidad de Medellín para mejorar las señalizaciones en intersecciones y en los tramos de vía en los sectores académicos.",
        "estrategia3": "Crear uno o varios robots de realidad virtual que se establezcan en los parqueaderos de lugares públicos de universidades para que brinden estrategias de prevención de choques y permita la  interacción con la misma.",
        },
}

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template('inicio.html')

@app.route("/historico",methods=['GET', 'POST'])
def historico():
    fecha_inicio = ""
    fecha_fin = ""
    barrio = ""
    tipo_accidente = ""
    cantidad = 0
    mostrar_mapa = False
    diccionario = {'barrios':barrios,'tipos_accidentes':tipos_accidentes}
    if request.method == 'POST':
        if 'Filtrar' in request.form['submit_button']:
            fecha_inicio = request.form.get("fecha-inicio")
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").strftime("%d/%m/%Y")
            inicio = fecha_inicio.replace('-','/')
            fecha_fin = request.form.get("fecha-fin")
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").strftime("%d/%m/%Y")
            fin = fecha_fin.replace('-','/')
            barrio = request.form.get("barrio")
            tipo_accidente = request.form.get("tipo-accidente")
            lista,cantidad = crear_lista(f'{inicio} 00:00:00',f'{fin} 23:59:59',barrio,tipo_accidente)
            mapa = crear_mapa_historico(lista,barrio)
            mostrar_mapa = True

        elif 'Borrar filtros' in request.form['submit_button']:
            fecha_inicio = ""
            fecha_fin = ""
            barrio = ""
            tipo_accidente = ""
            # mapa = crear_mapa_(lista,barrio)
            mostrar_mapa = False
            cantidad = 0
    diccionario['fecha_inicio'] = fecha_inicio
    diccionario['fecha_fin'] = fecha_fin
    diccionario['barrio'] = barrio
    diccionario['tipo_accidente'] = tipo_accidente
    diccionario['mostrar_mapa'] = mostrar_mapa
    diccionario['cantidad'] = cantidad

    return render_template('historico.html',datos = diccionario)



@app.route("/prediccion", methods=['GET', 'POST'])
def prediccion():
    predict = 0  
    rutas_graficos = {}  
    error = None  

    if request.method == 'POST':
        try:
            fecha_inicial = request.form.get("fecha_inicial")
            fecha_final = request.form.get("fecha_final")
            inicio = datetime.strptime(fecha_inicial, '%Y-%m-%d').strftime('%d/%m/%Y')
            final = datetime.strptime(fecha_final, '%Y-%m-%d').strftime('%d/%m/%Y')
            predict, rutas_graficos = prediccion_modelo(inicio, final)
        except ValueError as e:
            # Capturar y manejar errores de valor, como un formato de fecha incorrecto
            error = f"Error en el formato de la fecha: {e}"
        except Exception as e:
            # Capturar cualquier otro tipo de error
            error = f"Error al calcular la predicción: {e}"
    return render_template('prediccion.html', predict=predict, rutas_graficos=rutas_graficos, error=error)




@app.route("/agrupamiento", methods=['GET', 'POST'])
def agrupamiento():
    if request.method == 'POST':
        name = request.form.get('seleccion')
        print(name)
    else:
        # Define un valor predeterminado si no se ha enviado el formulario
        name = "Todos"
    diccionario = {'cluster_0':cluster_0,'cluster_1':cluster_1,'cluster_2':cluster_2,'cluster_3':cluster_3,'cluster_4':cluster_4,'cluster_5':cluster_5}
    diccionario["general"] = TEXT[name]["general"]
    diccionario["estrategia1"] = TEXT[name]["estrategia1"]
    diccionario["estrategia2"] = TEXT[name]["estrategia2"]
    diccionario["estrategia3"] = TEXT[name]["estrategia3"]
    diccionario['name'] = name
    
    return render_template('agrupamiento.html',datos = diccionario)

@app.errorhandler(Exception)
def handle_error(e):
    return redirect(url_for('inicio'))
