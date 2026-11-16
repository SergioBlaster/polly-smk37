# Polly no SMK-37 Pro — extras

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
| `docs/PLANO.md` | O plano do port (rotas, fases, riscos). |
| `firmware/*.png` | Capturas das telas (nomes, temas, cartões de ajuda). |
| `gerar-instalador.py` | Remonta `instalador/` a partir de `web/polly_installer.html` e do `.fwsc`. |
| `servidor-emulador.py` | Servidor local sem cache usado pelos dois `.bat`. |

Os `.bat` precisam do Python 3 no Windows. O instalador web do genkigenki (genkigenki.github.io/smk37) só grava
os firmwares do catálogo dele; este build se instala pelo `Abrir instalador.bat`.

## Instalar

1. Desligue o Bluetooth do PC e remova o pareamento do SMK-37.
2. Ligue o teclado direto no PC com um cabo USB de dados.
3. Abra `Abrir instalador.bat`, confira se a página diz "Pronto para gravar", clique em **Instalar** e permita o
   MIDI.
4. Espere a mensagem "Pronto!" e só então feche a aba e a janela preta.

Para voltar ao firmware original, use o M-UPGRADE da M-Vave com o `SMK-37 Pro_016.fwsc` (m-vave.com/download).
O firmware nunca grava nas áreas de calibração e de Bluetooth do teclado.

## Licença

GPL-3.0, como o Polly. Créditos: Polly de Charles Vestal; port do SMK-37 de genkigenki; Felucca de Leo Kuroshita
(Hügelton Instruments).
