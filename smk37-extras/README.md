# Polly no SMK-37 Pro — extras

*English version below: [Polly on the SMK-37 Pro — extras](#polly-on-the-smk-37-pro--extras).*

Este repositório é o [Polly](https://github.com/charlesvestal/fm1-polly) (arranjador para o M-VAVE FM-1, de
Charles Vestal) no **M-Vave SMK-37 Pro**, a partir do port de
[genkigenki/fm1-polly](https://github.com/genkigenki/fm1-polly) (branch `smk37`). O branch `smk37-nomes`
acrescenta:

- **Nomes do SMK-37 na tela:** PATCH, SCALE, PARA, K2–K8, BT... em vez dos nomes do FM-1
  (`firmware/src/app/btn_names.h`). O build do FM-1 continua com os nomes dele.
- **Tela que se explica sozinha:** cada knob mostra o nome (K5–K8). KNOB BANK, FADER BANK, `<` e `>` têm cartão
  de ajuda quando segurados por 1 segundo. O K1 mostra o volume.
- **Três temas de tela:** claro, escuro e neon. Para trocar: GLOBE, `>`, K5.
- **Emulador no navegador** (`web/emu/smk37.html`) e CI no GitHub Actions (`.github/workflows/smk37.yml`), que
  compila o firmware, roda os testes e tira capturas de todas as telas nos três temas.

Firmware não oficial e experimental: use por sua conta e risco.

## O que há nesta pasta

| Arquivo | O que é |
| --- | --- |
| `firmware/polly-smk37.fwsc` | O firmware pronto para gravar no SMK-37 Pro. |
| `Abrir instalador.bat` | Abre o instalador local no navegador (Chrome ou Edge) e grava o firmware pelo USB. |
| `Abrir emulador.bat` | Abre o emulador: o mesmo firmware rodando no navegador, sem o teclado. |
| `docs/Guia-Polly-SMK37-iniciantes.pdf` | Guia para iniciantes, em português, com o guia de teclas. |
| `docs/Polly-SMK37-beginners-guide.pdf` | O mesmo guia, em inglês. |
| `docs/PLANO.md` | O plano do port (rotas, fases, riscos). |
| `firmware/*.png` | Capturas das telas (nomes, temas, cartões de ajuda). |
| `gerar-instalador.py` | Remonta `instalador/` a partir de `web/polly_installer.html` e do `.fwsc`. |
| `servidor-emulador.py` | Servidor local sem cache usado pelos dois `.bat`. |

Os `.bat` precisam do Python 3 no Windows. O instalador web do genkigenki (genkigenki.github.io/smk37) só grava
os firmwares do catálogo dele; este build se instala pelo `Abrir instalador.bat`.

## Instalar

1. Desligue o Bluetooth do PC e remova o pareamento do SMK-37.
2. Ligue o teclado direto no PC com um cabo USB de dados.
3. Abra `Abrir instalador.bat` (a página abre no idioma do navegador; o botão no canto troca entre português e
   inglês), confira se ela diz "Pronto para gravar", clique em **Instalar** e permita o
   MIDI.
4. Espere a mensagem "Pronto!" e só então feche a aba e a janela preta.

Para voltar ao firmware original, use o M-UPGRADE da M-Vave com o `SMK-37 Pro_016.fwsc` (m-vave.com/download).
O firmware nunca grava nas áreas de calibração e de Bluetooth do teclado.

## Licença

GPL-3.0, como o Polly. Créditos: Polly de Charles Vestal; port do SMK-37 de genkigenki; Felucca de Leo Kuroshita
(Hügelton Instruments).

---

# Polly on the SMK-37 Pro — extras

This repository is [Polly](https://github.com/charlesvestal/fm1-polly), Charles Vestal's arranger for the M-VAVE
FM-1, running on the **M-Vave SMK-37 Pro**. It starts from the port in
[genkigenki/fm1-polly](https://github.com/genkigenki/fm1-polly) (branch `smk37`). The `smk37-nomes` branch adds:

- **The SMK-37's names on screen:** PATCH, SCALE, PARA, K2–K8, BT and so on, in place of the FM-1's names
  (`firmware/src/app/btn_names.h`). The FM-1 build keeps its own names.
- **A screen that explains itself:** each knob shows its name (K5–K8). KNOB BANK, FADER BANK, `<` and `>` show a
  help card when held for a second. K1 shows the volume.
- **Three screen themes:** light, dark and neon. To switch: GLOBE, `>`, K5.
- **A browser emulator** (`web/emu/smk37.html`) and CI on GitHub Actions (`.github/workflows/smk37.yml`). The CI
  builds the firmware, runs the tests and takes screenshots of every screen in the three themes.

Unofficial, experimental firmware: use it at your own risk.

## What's in this folder

| File | What it is |
| --- | --- |
| `firmware/polly-smk37.fwsc` | The firmware, ready to write to the SMK-37 Pro. |
| `Abrir instalador.bat` | Opens the local installer in the browser (Chrome or Edge) and writes the firmware over USB. |
| `Abrir emulador.bat` | Opens the emulator: the same firmware running in the browser, without the keyboard. |
| `docs/Polly-SMK37-beginners-guide.pdf` | Beginner's guide with a key guide, in English. |
| `docs/Guia-Polly-SMK37-iniciantes.pdf` | The same guide, in Portuguese. |
| `docs/PLANO.md` | The port plan (routes, phases, risks), in Portuguese. |
| `firmware/*.png` | Screenshots (names, themes, help cards). |
| `gerar-instalador.py` | Rebuilds `instalador/` from `web/polly_installer.html` and the `.fwsc`. |
| `servidor-emulador.py` | A local server without caching, used by both `.bat` files. |

The `.bat` files need Python 3 on Windows. genkigenki's web installer (genkigenki.github.io/smk37) only writes the
firmwares in its own catalogue, so this build is installed with `Abrir instalador.bat`.

## Install

The installer page opens in the browser's language (English or Portuguese); the button at the top right switches.

1. Turn off the computer's Bluetooth and remove the SMK-37's pairing.
2. Connect the keyboard straight to the computer with a USB data cable.
3. Open `Abrir instalador.bat`. Check that the page says "Ready to write", click **Install** and allow
   MIDI.
4. Wait for "Done!", then close the tab and the black window.

On another system, `python3 tools/fm1_install.py smk37-extras/firmware/polly-smk37.fwsc` does the same. It needs
`pip install mido python-rtmidi`.

To go back to the stock firmware, use M-Vave's M-UPGRADE with `SMK-37 Pro_016.fwsc` (m-vave.com/download). The
firmware never writes the keyboard's calibration or Bluetooth areas.

## License

GPL-3.0, like Polly. Credits: Polly by Charles Vestal; the SMK-37 port by genkigenki; Felucca by Leo Kuroshita
(Hügelton Instruments).
