import sys
from deep_translator import GoogleTranslator

def traducir():
    try:
        texto = sys.stdin.read()
        if not texto.strip():
            print("El archivo letra.txt está vacío.")
            return
        
        print("\n--- TRADUCIENDO ---")
        resultado = GoogleTranslator(source='auto', target='es').translate(texto)
        print(resultado)
        print("\n" + "="*50)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    traducir()
