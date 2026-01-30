# traductor.py
repositorio prueba demo
!/usr/bin/env python3
import sys
from googletrans import Translator

def traducir_cancion():
    translator = Translator()
    
    print("====================================================")
    print("   TRADUCTOR MULTI-IDIOMA (Auto -> Español)")
    print("   Soporta: Inglés, Italiano, Portugués, Japonés,")
    print("            Coreano, Francés y más...")
    print("====================================================")
    print("Pega la letra de la canción y presiona Ctrl+D para traducir:")
    
    try:
        # Captura múltiples líneas de texto hasta Ctrl+D
        lineas = sys.stdin.readlines()
        letra_original = "".join(lineas)

        if not letra_original.strip():
            print("\n[!] No ingresaste ningún texto.")
            return

        print("\n...Detectando idioma y traduciendo...\n")

        # src='auto' permite que Google detecte el idioma origen
        # dest='es' lo traduce siempre a español
        resultado = translator.translate(letra_original, src='auto', dest='es')

        # Detectamos qué idioma reconoció la IA
        idioma_detectado = resultado.src

        print(f"--- LETRA TRADUCIDA (Idioma detectado: {idioma_detectado}) ---")
        print(resultado.text)
        print("\n" + "="*50)

    except Exception as e:
        print(f"\n[!] Error técnico: {e}")

if __name__ == "__main__":
    traducir_cancion()

