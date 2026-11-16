# Gera o instalador web local do Polly SMK-37 (pasta "instalador"), a partir do instalador do próprio projeto
# (web/polly_installer.html + fm1pkg.js + fm1ota.js) e do firmware em firmware/polly-smk37.fwsc.
# A página grava pelo USB-MIDI do Chrome/Edge, como o instalador do genkigenki. Em português e em inglês (um botão
# troca; abre no idioma do navegador), sem a parte de "voltar ao firmware do FM-1" (para o SMK-37 a volta é pelo
# M-UPGRADE ou pelo site do genkigenki).
#
# Builds the local Polly SMK-37 web installer (folder "instalador") from the project's own installer and the
# firmware, in Portuguese and English (a button switches; it opens in the browser's language).
import json
import re
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
# (na pasta local SMK37Polly o código está em genki-port/; no repositório, esta pasta é smk37-extras/ dentro dele)
WEB = RAIZ / "genki-port" / "web" if (RAIZ / "genki-port").is_dir() else RAIZ.parent / "web"
sys.path.insert(0, str(WEB))
from make_site import product_of, strip_module  # noqa: E402

pkg = RAIZ / "firmware" / "polly-smk37.fwsc"
raw = pkg.read_bytes()
produto = product_of(raw)
if not re.fullmatch(r"SMK-37 Pro_\d+", produto):
    sys.exit(f"{pkg}: identidade {produto!r} não é de SMK-37 Pro")
if b"FELUCCA-LOADER-1" not in raw:
    sys.exit(f"{pkg}: sem o carregador de atualização")

saida = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "instalador"   # (another folder: to try it out)
saida.mkdir(exist_ok=True)
shutil.copy(pkg, saida / "polly-smk37.fwsc")

html = (WEB / "polly_installer.html").read_text(encoding="utf-8")
lib = strip_module((WEB / "fm1pkg.js").read_text(encoding="utf-8")) + "\n" + \
    strip_module((WEB / "fm1ota.js").read_text(encoding="utf-8"))
meta = json.dumps({"version": "SMK-37", "product": produto, "pkg": "polly-smk37.fwsc"})
html = html.replace("/*LIB*/", lib).replace("/*META*/", meta)


def troca(antigo, novo, n=1):
    global html
    if html.count(antigo) != n:
        sys.exit(f"esperava {n}x: {antigo[:60]!r} (achei {html.count(antigo)})")
    html = html.replace(antigo, novo)


# a parte do FM-1 que não vale para o SMK-37: recuperação por Mac e a volta ao firmware V15 do FM-1
troca(html[html.index('  <p class="small"><span data-t="brick">'):html.index('  <p><button id="go"')], "")
troca(html[html.index('  <h2 data-t="stockh">'):html.index('  <p><a href="../"')], "")
troca('  <p><a href="../" style="color:inherit" data-t="manual"></a></p>\n', '  <p class="small" data-t="back"></p>\n')
troca("<h1>Install Polly</h1>", '<h1 data-t="title"></h1>')
troca("<title>Polly installer</title>", "<title>Polly SMK-37</title>")
# o "stockfile" não existe mais na página: o código dele não pode quebrar o resto
troca('$("stockfile").addEventListener(', '$("stockfile") && $("stockfile").addEventListener(')
troca('$("stockgo").addEventListener(', '$("stockgo") && $("stockgo").addEventListener(')
troca('$("go").disabled = $("stockgo").disabled = true;', '$("go").disabled = true;')
troca('  $("stockgo").disabled = !stock;\n', '')

PT = {
    "title": "Instalar o Polly no SMK-37 Pro", "langname": "English",
    "intro": "Ligue o SMK-37 Pro a este computador com um cabo USB. Esta página funciona no Chrome ou no Edge.",
    "warn": "Até terminar, deixe o computador acordado, o cabo USB conectado e esta aba aberta. Leva alguns minutos; a gravação é a parte mais longa.",
    "install": "Instalar",
    "direct": "Ligue o cabo direto no computador (sem hub). Antes, desligue o Bluetooth do PC e feche outros programas que usam MIDI.",
    "beta": "Firmware não oficial e experimental: use por sua conta e risco.",
    "back": "Para voltar ao firmware original, use o M-UPGRADE da M-Vave com o arquivo SMK-37 Pro_016.fwsc, ou a seção \"Back to the M-Vave firmware\" do site genkigenki.github.io/smk37.",
    "ready": "Pronto para gravar: ",
    "nomidi": "Este navegador não instala firmware. Abra a página no Chrome ou no Edge.",
    "loadfail": "Não consegui carregar o firmware: ",
    "start": "Começando", "verify": "Conferindo", "loader": "Entrando no modo de atualização", "write": "Gravando",
    "reboot": "Reiniciando", "done": "Pronto! O teclado reiniciou com o Polly.",
    "stopped": "Parou. Tire o cabo USB, ligue de novo e aperte Instalar outra vez.",
    "error": "Erro: ",
    "denied": "O navegador não liberou MIDI com SysEx. Libere o MIDI nas configurações do site (ícone ao lado do endereço) e aperte Instalar de novo.",
    "notfound": "A página não achou o teclado. Confira se o cabo USB é de dados, feche outros programas de MIDI e aperte Instalar de novo.",
    "other": "Este teclado está com um firmware que tem atualizador próprio (Felucca SMK, Sloop SMK, Melodee SMK, Doom); daqui não dá para gravar por cima. Nada foi gravado.",
    "foreign": "O teclado está no modo de atualização de outro firmware: nada foi gravado. Termine essa atualização com o atualizador dele: ",
    "model": "O aparelho conectado não é um SMK-37 (ou modelo irmão).",
    "lost": "A conexão USB caiu. Ligue o cabo de novo e aperte Instalar outra vez.",
    "noloader": "A página não achou o teclado no modo de atualização. Tire o cabo USB, ligue de novo e aperte Instalar outra vez.",
    "noreturn": "O teclado não voltou. Desligue e ligue de novo.",
    "mismatch": "A gravação terminou, mas o teclado informa outra versão: ",
    "badpkg": "O arquivo do firmware está com problema. Recarregue a página.",
    "leave": "Gravando. Não feche a página.",
    "license": "GPL-3.0, sem garantia. Código:",
    "details": "Detalhes (cada passo)",
}
EN = {
    "title": "Install Polly on the SMK-37 Pro", "langname": "Português",
    "intro": "Connect the SMK-37 Pro to this computer with a USB cable. This page works in Chrome or Edge.",
    "warn": "Until it's done, keep the computer awake, the USB cable in and this tab open. It takes a few minutes; writing is the longest part.",
    "install": "Install",
    "direct": "Connect the cable straight to the computer (no hub). First, turn off the computer's Bluetooth and close other apps that use MIDI.",
    "beta": "Unofficial, experimental firmware: use it at your own risk.",
    "back": "To go back to the stock firmware, use M-Vave's M-UPGRADE with the file SMK-37 Pro_016.fwsc, or the \"Back to the M-Vave firmware\" section of genkigenki.github.io/smk37.",
    "ready": "Ready to write: ",
    "nomidi": "This browser can't install firmware. Open the page in Chrome or Edge.",
    "loadfail": "Could not load the firmware: ",
    "start": "Starting", "verify": "Checking", "loader": "Switching to update mode", "write": "Writing",
    "reboot": "Restarting", "done": "Done! The keyboard has restarted with Polly.",
    "stopped": "Stopped. Unplug the USB cable, plug it back in and press Install again.",
    "error": "Error: ",
    "denied": "The browser didn't allow MIDI with SysEx. Allow MIDI in the site settings (the icon by the address) and press Install again.",
    "notfound": "The page can't find the keyboard. Make sure the USB cable is a data cable, close other MIDI apps and press Install again.",
    "other": "This keyboard runs a firmware with its own updater (Felucca SMK, Sloop SMK, Melodee SMK, Doom); it can't be written over from here. Nothing was written.",
    "foreign": "The keyboard is in the update mode of another firmware: nothing was written. Finish that update with its own updater: ",
    "model": "The connected device is not an SMK-37 (or a sister model).",
    "lost": "The USB connection was lost. Plug the cable back in and press Install again.",
    "noloader": "The page can't find the keyboard in update mode. Unplug the USB cable, plug it back in and press Install again.",
    "noreturn": "The keyboard didn't come back. Switch it off and on again.",
    "mismatch": "The install finished, but the keyboard reports another version: ",
    "badpkg": "The firmware file is damaged. Reload the page.",
    "leave": "Writing. Don't close the page.",
    "license": "GPL-3.0, no warranty. Source:",
    "details": "Details (every step)",
}
assert PT.keys() == EN.keys()
texto = "const TEXT = " + json.dumps({"pt": PT, "en": EN}, ensure_ascii=False, indent=2) + ";\n"
ini = html.index("const TEXT = {")
fim = html.index('let lang = "en";')
troca(html[ini:fim], texto)
troca(html[html.index('let lang = "en";'):html.index("\n", html.index('let lang = "en";'))],
      'let lang = /^pt/i.test(navigator.language || "") ? "pt" : "en";   /* the browser\'s language; a click switches */')
troca('$("lang").textContent = t("other");', '$("lang").textContent = t("langname"); document.title = t("title");')
troca('lang = lang === "ja" ? "en" : "ja";', 'lang = lang === "pt" ? "en" : "pt";')
troca("say(`Polly ${meta.version}`);", 'sayK("ready", `Polly ${meta.version} (${meta.product})`);')

# the progress on one line ("Gravando 42%"), the bar, and the step-by-step log folded away (it listed every block)
troca("  pre { color: var(--dim); font-size: 12px; white-space: pre-wrap; margin-top: 16px; }",
      "  pre { color: var(--dim); font-size: 12px; white-space: pre-wrap; margin: 8px 0 0; max-height: 14em; overflow: auto; }\n"
      "  details { margin-top: 16px; color: var(--dim); font-size: 13px; }\n"
      "  summary { cursor: pointer; }\n"
      "  #status { font-weight: 600; }")
troca('  <pre id="log"></pre>', '  <details><summary data-t="details"></summary><pre id="log"></pre></details>')
troca("      log(`${k} ${a ?? \"\"}`);",
      "      if (k !== \"verify\" && k !== \"write\") log(`${k} ${a ?? \"\"}`);   /* (the blocks: in the percentage) */")
troca('      if (k === "verify") { sayK("verify"); $("bar").value = (a / total) * 100; }',
      '      if (k === "verify") { $("bar").value = (a / total) * 100; sayK("verify", ` ${Math.round($("bar").value)}%`); }')
troca('      if (k === "write") { sayK("write"); $("bar").value = ((74 + a) / total) * 100; }',
      '      if (k === "write") { $("bar").value = ((74 + a) / total) * 100; sayK("write", ` ${Math.round($("bar").value)}%`); }')

(saida / "index.html").write_text(html, encoding="utf-8")
print(f"instalador: {saida / 'index.html'} ({len(html)} B), firmware {produto}, {len(raw)} B")
