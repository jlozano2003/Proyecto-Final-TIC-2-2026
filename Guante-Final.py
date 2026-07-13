import serial
import pydirectinput
import time

# =================================================================
# MAGIA ANTI-LAG
pydirectinput.PAUSE = 0 
# =================================================================

# Configuración de la conexión
puertoComunicacionSerial = 'COM6'
velocidadDeTransmisionBaudios = 115200

print("Conectando al guante Acebott...")
conexionSerialESP32 = serial.Serial(puertoComunicacionSerial, velocidadDeTransmisionBaudios)
time.sleep(2)
print("¡Todo listo! A jugar Minecraft.")

# --- CONFIGURACIÓN DE SENSIBILIDAD ---
umbralDeActivacionFlexionDedo = 400

# Umbrales espaciales de reposo absoluto
zonaMuertaMirarHorizontalGrados = 45  
zonaMuertaMirarVerticalGrados = 45    

# Velocidad de cámara
velocidadMovimientoCamaraHorizontal = 12
velocidadMovimientoCamaraVertical = 8

# --- VARIABLES DE ESTADO PARA LOS DEDOS ---
estadoAnteriorDedoPulgarSaltar = False
estadoAnteriorDedoIndiceAvanzar = False
estadoAnteriorDedoMedioRomper = False
estadoAnteriorDedoAnularPoner = False
estadoAnteriorDedoMeniqueInventario = False

while True:
    try:
        if conexionSerialESP32.in_waiting > 0:
            lineaDeDatosRecibida = conexionSerialESP32.readline().decode('utf-8').strip()

            # Vaciamos el buffer para leer siempre en tiempo real
            conexionSerialESP32.reset_input_buffer() 

            if lineaDeDatosRecibida:
                listaDeValoresCompletos = lineaDeDatosRecibida.split(',')

                if len(listaDeValoresCompletos) == 7:
                    valorSensorDedoPulgar  = int(listaDeValoresCompletos[0])
                    valorSensorDedoIndice  = int(listaDeValoresCompletos[1])
                    valorSensorDedoMedio   = int(listaDeValoresCompletos[2])
                    valorSensorDedoAnular  = int(listaDeValoresCompletos[3])
                    valorSensorDedoMenique = int(listaDeValoresCompletos[4])

                    valorInclinacionManoAdelanteAtras = int(listaDeValoresCompletos[5])
                    valorInclinacionManoIzquierdaDerecha = int(listaDeValoresCompletos[6])

                    # ========================================================
                    # 1. CONTROL DE CÁMARA (Ejes Corregidos)
                    # ========================================================

                    # Control Horizontal - ¡AQUÍ ESTÁ LA CORRECCIÓN DE LOS SIGNOS!
                    if valorInclinacionManoIzquierdaDerecha > zonaMuertaMirarHorizontalGrados:
                        pydirectinput.moveRel(-velocidadMovimientoCamaraHorizontal, 0)
                    elif valorInclinacionManoIzquierdaDerecha < -zonaMuertaMirarHorizontalGrados:
                        pydirectinput.moveRel(velocidadMovimientoCamaraHorizontal, 0)

                    # Control Vertical
                    if valorInclinacionManoAdelanteAtras > zonaMuertaMirarVerticalGrados:
                        pydirectinput.moveRel(0, velocidadMovimientoCamaraVertical)
                    elif valorInclinacionManoAdelanteAtras < -zonaMuertaMirarVerticalGrados:
                        pydirectinput.moveRel(0, -velocidadMovimientoCamaraVertical)


                    # ========================================================
                    # 2. CONTROL DE ACCIONES (Dedos)
                    # ========================================================

                    # [PULGAR] -> SALTAR (Space)
                    estadoActualPulgar = valorSensorDedoPulgar > umbralDeActivacionFlexionDedo
                    if estadoActualPulgar and not estadoAnteriorDedoPulgarSaltar:
                        pydirectinput.keyDown('space')
                        estadoAnteriorDedoPulgarSaltar = True
                    elif not estadoActualPulgar and estadoAnteriorDedoPulgarSaltar:
                        pydirectinput.keyUp('space')
                        estadoAnteriorDedoPulgarSaltar = False

                    # [ÍNDICE] -> AVANZAR (W)
                    estadoActualIndice = valorSensorDedoIndice > umbralDeActivacionFlexionDedo
                    if estadoActualIndice and not estadoAnteriorDedoIndiceAvanzar:
                        pydirectinput.keyDown('w')
                        estadoAnteriorDedoIndiceAvanzar = True
                    elif not estadoActualIndice and estadoAnteriorDedoIndiceAvanzar:
                        pydirectinput.keyUp('w')
                        estadoAnteriorDedoIndiceAvanzar = False

                    # [MEDIO] -> ROMPER BLOQUE (Click Izquierdo)
                    estadoActualMedio = valorSensorDedoMedio > umbralDeActivacionFlexionDedo
                    if estadoActualMedio and not estadoAnteriorDedoMedioRomper:
                        pydirectinput.mouseDown(button='left')
                        estadoAnteriorDedoMedioRomper = True
                    elif not estadoActualMedio and estadoAnteriorDedoMedioRomper:
                        pydirectinput.mouseUp(button='left')
                        estadoAnteriorDedoMedioRomper = False

                    # [ANULAR] -> PONER BLOQUE (Click Derecho)
                    estadoActualAnular = valorSensorDedoAnular > umbralDeActivacionFlexionDedo
                    if estadoActualAnular and not estadoAnteriorDedoAnularPoner:
                        pydirectinput.mouseDown(button='right')
                        estadoAnteriorDedoAnularPoner = True
                    elif not estadoActualAnular and estadoAnteriorDedoAnularPoner:
                        pydirectinput.mouseUp(button='right')
                        estadoAnteriorDedoAnularPoner = False

                    # [MEÑIQUE] -> INVENTARIO (E)
                    estadoActualMenique = valorSensorDedoMenique > umbralDeActivacionFlexionDedo
                    if estadoActualMenique and not estadoAnteriorDedoMeniqueInventario:
                        pydirectinput.press('e')
                        estadoAnteriorDedoMeniqueInventario = True
                    elif not estadoActualMenique and estadoAnteriorDedoMeniqueInventario:
                        estadoAnteriorDedoMeniqueInventario = False

    except KeyboardInterrupt:
        print("Cerrando el software de control...")
        break
    except Exception:
        pass