# Servidor local do emulador (http://localhost:8737) e do instalador. Igual ao "python -m http.server", mas manda o
# navegador não guardar cópia (Cache-Control: no-store): assim um emulador novo copiado para a pasta aparece no
# próximo F5. Com --abrir, abre o navegador só depois que o servidor já está no ar (antes disso a página falharia).
# Uso: servidor-emulador.py [PORTA] [PASTA] [--abrir]   (padrão: 8737, emulador)
import functools
import http.server
import os
import sys
import webbrowser

args = [a for a in sys.argv[1:] if not a.startswith("--")]
PORTA = int(args[0]) if args else 8737
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), args[1] if len(args) > 1 else "emulador")


class SemCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


try:
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORTA), functools.partial(SemCache, directory=PASTA))
except OSError:
    # já há um servidor nesta porta (uma janela aberta antes): só abre a página
    print(f"A porta {PORTA} já está em uso; abrindo a página do servidor que já está ligado.")
    if "--abrir" in sys.argv:
        webbrowser.open(f"http://localhost:{PORTA}/")
    input("Aperte Enter para fechar.")
    sys.exit(0)
url = f"http://localhost:{PORTA}/"
print(f"Servidor ligado em {url}  (pasta {PASTA})")
print("Deixe esta janela aberta enquanto usa a página. Feche-a no fim.")
if "--abrir" in sys.argv:
    webbrowser.open(url)
srv.serve_forever()
