# Gera o instalador web local do Polly SMK-37 (pasta "instalador"), a partir do instalador do próprio projeto
# (genki-port/web/polly_installer.html + fm1pkg.js + fm1ota.js) e do firmware em firmware/polly-smk37.fwsc.
# A página grava pelo USB-MIDI do Chrome/Edge, como o instalador do genkigenki. Textos em português, sem a parte
# de "voltar ao firmware do FM-1" (para o SMK-37 a volta é pelo M-UPGRADE ou pelo site do genkigenki).
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

saida = RAIZ / "instalador"
saida.mkdir(exist_ok=True)
shutil.copy(pkg, saida / "polly-smk37.fwsc")

html = (WEB / "polly_installer.html").read_text(encoding="utf-8")
lib = strip_module((WEB / "fm1pkg.js").read_text(encoding="utf-8")) + "\n" + \
    strip_module((WEB / "fm1ota.js").read_text(encoding="utf-8"))
meta = json.dumps({"version": "SMK-37 (nomes do SMK, temas)", "product": produto, "pkg": "polly-smk37.fwsc"})
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
troca('<button class="lang" id="lang"></button>', '<button class="lang" id="lang" hidden></button>')
troca("<h1>Install Polly</h1>", "<h1>Instalar o Polly no SMK-37 Pro</h1>")
troca('<html lang="en">', '<html lang="pt-BR">')
troca("<title>Polly installer</title>", "<title>Instalador Polly SMK-37</title>")
# o "stockfile" não existe mais na página: o código dele não pode quebrar o resto
troca('$("stockfile").addEventListener(', '$("stockfile") && $("stockfile").addEventListener(')
troca('$("stockgo").addEventListener(', '$("stockgo") && $("stockgo").addEventListener(')
troca('$("go").disabled = $("stockgo").disabled = true;', '$("go").disabled = true;')
troca('  $("stockgo").disabled = !stock;\n', '')

PT = {
    "intro": "Ligue o SMK-37 Pro a este computador com um cabo USB. Esta página funciona no Chrome ou no Edge.",
    "warn": "Até terminar, deixe o computador acordado, o cabo USB conectado e esta aba aberta.",
    "install": "Instalar",
    "direct": "Ligue o cabo direto no computador (sem hub). Antes, desligue o Bluetooth do PC e feche outros programas que usam MIDI.",
    "beta": "Firmware não oficial e experimental: use por sua conta e risco. Esta versão ainda não foi testada num SMK-37 de verdade.",
    "back": "Para voltar ao firmware original, use o M-UPGRADE da M-Vave com o arquivo SMK-37 Pro_016.fwsc, ou a seção \"Back to the M-Vave firmware\" do site genkigenki.github.io/smk37.",
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
}
ini = html.index("  en: {")
fim = html.index("\n  },", ini)
bloco = html[ini:fim]
for k, v in PT.items():
    novo, n = re.subn(r'(\b%s: )"(?:[^"\\]|\\.)*"' % re.escape(k), lambda m: m.group(1) + json.dumps(v, ensure_ascii=False), bloco, count=1)
    if n != 1:
        sys.exit(f"texto {k} não encontrado")
    bloco = novo
html = html[:ini] + bloco + html[fim:]
troca("say(`Polly ${meta.version}`);", "say(`Pronto para gravar: Polly ${meta.version} (${meta.product}).`);")

(saida / "index.html").write_text(html, encoding="utf-8")
print(f"instalador: {saida / 'index.html'} ({len(html)} B), firmware {produto}, {len(raw)} B")
