import sqlite3
from multiprocessing import Process, Queue
import time

# Función para inicializar la base de datos
def inicializar_bd(nombre_bd):
    conexion = sqlite3.connect(nombre_bd)
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cuenta (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        balance REAL NOT NULL)''')
    cursor.execute('''INSERT INTO cuenta (nombre, balance) VALUES
                      ('Abigail', 1001),
                      ('victor', 1500),
                      ('nelida', 2000)''')
    conexion.commit()
    conexion.close()

# Función para mostrar los datos de la base de datos
def mostrar_datos(nombre_bd):
    conexion = sqlite3.connect(nombre_bd)
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM cuenta')
    for fila in cursor.fetchall():
        print(fila)
    conexion.close()

# Función para replicar datos
def replicar_datos(nombre_bd_origen, nombre_bd_destino, cola):
    while True:
        # Esperar por una actualización
        mensaje = cola.get()
        if mensaje == 'REPLICAR':
            # Conectar a ambas bases de datos
            conexion_origen = sqlite3.connect(nombre_bd_origen)
            conexion_destino = sqlite3.connect(nombre_bd_destino)

            cursor_origen = conexion_origen.cursor()
            cursor_destino = conexion_destino.cursor()

            # Obtener todos los datos de la base de datos origen
            cursor_origen.execute('SELECT * FROM cuenta')
            filas = cursor_origen.fetchall()

            # Reemplazar datos en la base de datos destino
            cursor_destino.execute('DELETE FROM cuenta')
            cursor_destino.executemany('INSERT INTO cuenta (id, nombre, balance) VALUES (?, ?, ?)', filas)

            conexion_destino.commit()
            conexion_origen.close()
            conexion_destino.close()

        if mensaje == 'TERMINAR':
            break

if __name__ == '__main__':
    # Inicializar la base de datos principal
    inicializar_bd('principal.db')

    # Inicializar la base de datos secundaria
    inicializar_bd('replica.db')

    # Crear una cola para la comunicación entre procesos
    cola = Queue()

    # Crear y empezar el proceso de replicación
    proceso_replicacion = Process(target=replicar_datos, args=('principal.db', 'replica.db', cola))
    proceso_replicacion.start()

    # Simular cambios en la base de datos principal y replicar
    conexion = sqlite3.connect('principal.db')
    cursor = conexion.cursor()
    cursor.execute('UPDATE cuenta SET balance = balance + 500 WHERE nombre = "Abigail"')
    conexion.commit()
    conexion.close()

    # Notificar al proceso de replicación
    cola.put('REPLICAR')

    # Esperar un momento para asegurar que la replicación se haya completado
    time.sleep(2)

    # Mostrar los datos replicados
    print("Datos en la base de datos secundaria:")
    mostrar_datos('replica.db')

    # Terminar el proceso de replicación
    cola.put('TERMINAR')
    proceso_replicacion.join()
