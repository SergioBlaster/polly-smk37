# Polly no SMK-37 Pro — plano de port

Data: 15/11/2026 · Alvo: M-VAVE SMK-37 Pro (o teclado do Sergio) · Origem: [charlesvestal/fm1-polly](https://github.com/charlesvestal/fm1-polly) v0.6.4

## 1. O que já existe (descoberto no levantamento)

| Fato | Consequência |
|---|---|
| **Já existe um port**: [genkigenki/fm1-polly](https://github.com/genkigenki/fm1-polly), branch `smk37` (7 commits, ~3.200 linhas, 13/10/2026). Instalador web: genkigenki.github.io/smk37 | Não começamos do zero: a camada de placa (teclado com velocidade, 18 botões, 8 encoders, 16 pads RGB, faders, rodas, LEDs, tela, mapa de flash, loader) já está escrita e testada em hardware. |
| Esse port é do **Polly 0.4**, no layout antigo (`firmware/hal`, `firmware/src`). | O Polly atual (**0.6.4**, 291 commits) foi reestruturado: o app fica em `app/` e a plataforma em submódulos **fm1-base** (`base/`) + **felucca-bsp** (`base/bsp/`). O código do genki **não aplica direto**. |
| fm1-base e felucca-bsp **não têm placa SMK-37** (o README do felucca-bsp lista o SMK-37 Pro como "Planned. No board support yet"). | O trabalho real do port é **levar a camada de placa do genki para dentro de fm1-base/felucca-bsp**. |
| Mesmo chip do FM-1: JieLi **AC791N (WL82)**. Tela de 1,54" (mesmo ST7789), mas em **outros pinos** (SPI1 grupo A: PB6/PB7/PC8/PB5) e o SPI1 é compartilhado com os LEDs dos pads (PC10). | Driver da tela é ajuste de pinos, não driver novo. |
| Áreas protegidas na flash do SMK (calibração em 0xC1000, pareamento BT, mapa de teclas). | Mapa de flash próprio; o banco QY70 (64 setores) **não cabe** — fica fora, como no port do genki. |
| Toda a comunidade SMK (Skiff, ChoralRoot, OberVave…) usa a camada do genki no layout antigo. Ninguém tem SMK em fm1-base ainda. | Seríamos os primeiros: risco maior, mas o resultado (placa SMK no fm1-base) serve para portar qualquer app do fm1-base depois. |

Licenças: Polly e o port do genki são GPL-3.0-only; felucca-bsp é MPL-2.0. A camada SMK do genki é GPL, então no nosso fork ela entra como GPL (tudo bem para nós; só não dá para devolvê-la ao felucca-bsp como MPL sem permissão do autor).

## 2. Caminhos possíveis

| | A. Usar o port do genki (0.4) | **B. Port do Polly atual sobre fm1-base (recomendado)** | C. Rebase do 0.4 até o 0.6.4 |
|---|---|---|---|
| Esforço | baixo | médio-alto | alto e frágil |
| Versão do Polly | 0.4 (sem 2 meses de melhorias) | 0.6.4 e futuras (só `git pull` do upstream) | 0.6.4, mas cada atualização repete o rebase |
| Aproveita | tudo | camada de placa e lógica de pads/faders do genki | idem |

**Recomendo B**, usando A como **fase 0** (instalar o build pronto do genki para validar o teclado e ter uma referência de comportamento).

## 3. Fases

### Fase 0 — Preparação e referência (sem código)
1. **Ambiente de build no Windows**: WSL2 (Ubuntu x86-64) — o toolchain JieLi roda nativo, sem Docker. Instalar `base/tools/get_toolchain.sh`, o AC79 SDK (3 arquivos usados), Python + Pillow, e opcionalmente Emscripten para o emulador web.
2. **Backup da flash** do SMK-37 Pro e ter à mão o `SMK-37 Pro_016.fwsc` + Workbench (lembrar: Bluetooth do PC desligado e pareamentos removidos, senão o flash dá "target is ambiguous").
3. Instalar o **Polly SMK-37 do genki** pelo instalador web, usar um pouco, anotar o que funciona e o que incomoda. Voltar ao V016 depois.
4. Conferir **a serigrafia real** dos botões do SMK-37 Pro (fotos do painel) — é a fonte dos nomes da Fase 3.

### Fase 1 — Placa SMK-37 no felucca-bsp / fm1-base (fork nosso)
- Fork de `fm1-polly`, `fm1-base` e `felucca-bsp`; submódulos apontando para os forks, branch `smk37`.
- `base/bsp/boards/smk37/`: trazer do genki `smk_input.h` (matriz 74HC595, velocidade, encoders, pads, ADC mux), os pinos da tela e `padled_send`, mantendo a **mesma API** que `boards/fm1/` expõe (o resto do fm1-base não deve perceber a troca).
- `fm1_flash_map`: regiões protegidas do SMK, recusadas em tempo de compilação e no driver (como o genki faz). Recalcular onde cabem: app, loader, store, **região de recursos dos estilos (43 KB)**.
- Loader de update: janela/identidade do SMK (`SMK-37 Pro_3xx`) para o M-UPGRADE continuar aceitando o firmware de fábrica depois.
- `tools/build.py`: opção `board = "smk37"` (ou `BOARD=smk37`), que escolhe placa, linker script, identidade e nome USB ("Polly SMK-37").
- Instalador (`fm1_install.py` + web): aceitar pacote SMK só em SMK, recusar FM-1 ↔ SMK.
- **Marco**: firmware de teste do fm1-base (`examples/hwtest`) liga no SMK — tela, botões, teclas, encoders, áudio, USB MIDI.

### Fase 2 — Polly 0.6.4 rodando no SMK
- Build do Polly com a placa nova; mesma interface do FM-1 (teclas do meio F3..G5 = as 27 do FM-1, K5..K8 = KNOB 1..4 etc.).
- Portar do genki a parte de app específica do SMK (`ui.c`/`pages.c`, ~300 linhas): pads (seções, FOLLOW, P1-P16 em duas metades), FADER BANK (volumes/reverb/chorus), rodas (pitch bend, vibrato), teclas externas, velocidade.
- Simulador (`--host`) com uma variante SMK para os testes de cenário (`tests/scenarios/smk37/`).
- Bluetooth MIDI/áudio e áudio USB do fm1-base: testar no SMK (o port do genki é anterior a isso — **risco**; se não couber em RAM/flash, desligar no `fm1.toml` do SMK).
- **Marco**: Polly toca, grava, salva e reabre uma música no SMK; testes do host passando para FM-1 e SMK.

### Fase 3 — Nomes dos controles do SMK-37 na tela (primeira mudança pedida)
Hoje o Polly (e o port do genki, de propósito) escreve na tela os nomes do FM-1. São **~100 textos** em `app/ui.c` e `app/pages.c` (rodapés tipo `"KEYS chords|REC stop"`, cartões de ajuda, perguntas tipo `"CLEAR P3? SEL: yes. HOME: no."`, a tela de atalhos do HOME).

Abordagem:
1. Criar `app/btn_names.h` com um macro por controle, escolhido pela placa:
   ```c
   #ifdef BOARD_SMK37
   #define BTN_HOME "PATCH"
   #define BTN_SEL  "SCALE"
   ...
   #else
   #define BTN_HOME "HOME"
   ...
   ```
2. Trocar cada literal por concatenação: `"CLEAR P3? " BTN_SEL ": yes. " BTN_HOME ": no."`. Zero custo em tempo de execução e o build do FM-1 continua idêntico (dá para comparar o binário FM-1 antes/depois para provar).
3. Textos que falam do **teclado do FM-1** ("white keys 1–16", "black keys 1–5") viram "pads" no SMK, porque lá esses atalhos estão nos pads.
4. Nomes mais longos (NOTE REPEAT no lugar de LFO, OCTAVE− no lugar de OCT−): conferir que cabem com as **capturas de tela do simulador** em todas as páginas; onde não couber, usar abreviação definida na tabela.
5. Atualizar `words.tsv` (leitor de tela) e a calibração ("teach the buttons", que hoje pergunta pelos nomes do FM-1).
6. Um teste que procura nomes do FM-1 sobrando nas strings do build SMK.

Tabela inicial (mapa do genki; **confirmar com a serigrafia na Fase 0**):

| FM-1 (tela hoje) | SMK-37 Pro (tela nova) | Função no Polly |
|---|---|---|
| HOME | PATCH | Home / Song; segurado: atalhos |
| SEL | SCALE | página como lista |
| ARP / SEQ | ARP / SEQ | Progressão / Band |
| EDIT | PARA | Sound |
| LFO / FX | NOTE REPEAT / FX | Mixer / Effects |
| ENV / GLO | CHORD / GLOBE | Style / Setup |
| SAVE | BT | salvar |
| PLAY / REC | SEQ PLAY / SEQ REC (ou PLAY / REC, se couber melhor) | tocar / gravar |
| OCT− / OCT+ | OCTAVE− / OCTAVE+ | oitava / cursor |
| SELECT / ALGORITHM / PRESETS | K2 / K3 / K4 | página, instrumento, música |
| KNOB 1..4 | K5..K8 | os quatro parâmetros da página |
| white keys 1–16 / black keys 1–5 (com HOME) | pads de baixo (P1–P16) / pads de cima 1–5 | progressões / Intro, Grooves, Fill, Ending |

Os botões que o FM-1 não tem (`<` `>`, KNOB BANK, FADER BANK, K1 = volume) já aparecem com o nome certo no código do genki.

**Atalho possível**: a Fase 3 também pode ser feita primeiro em cima do port 0.4 do genki (é só a troca de strings), para ter algo no teclado em poucos dias enquanto as Fases 1–2 andam.

### Fase 4 — Empacotar e manter
- `SMK37.md` em português e inglês, pacote `polly-smk37.fwsc`, instalação pelo `fm1_install.py` / instalador web.
- Rotina de atualização: `git pull` do upstream → resolver conflitos só nos textos da Fase 3 → build FM-1 e SMK → testes.
- Opcional: oferecer a placa SMK ao fm1-base/felucca-bsp e a troca de nomes ao Polly (PR), se os autores quiserem.

## 4. Riscos

| Risco | Mitigação |
|---|---|
| Brickar o teclado | Backup da flash; nunca escrever calibração/BT/mapa de teclas (bloqueio no compilador e no driver); Restore factory V16 com Force flash pelo Workbench; modo de update OCTAVE− + OCTAVE+ 5 s. |
| fm1-base 2026-11 usa recursos que o SMK não tem igual (BT próprio, áudio USB, LED de teclas, jack de fone PB5) | Fase 1 com hwtest antes do Polly; desligar recurso por recurso no `fm1.toml` do SMK. |
| Flash do SMK menor por causa das áreas protegidas | Calcular o mapa no começo da Fase 1; QY70 fora; se os estilos (43 KB) não couberem, compilar no app. |
| Upstream muda rápido (fm1-base é beta, "expect changes") | Fixar versões dos submódulos; atualizar em lotes. |

## 5. Decisões em aberto
1. Caminho: B com fase 0 (recomendado) ou ficar no 0.4 do genki (A)?
2. Fazer a troca de nomes primeiro sobre o 0.4 (resultado rápido) ou só depois da Fase 2?
3. Manter o mapeamento de botões do genki (ex.: SAVE no botão BT) ou redesenhar algum?
4. Textos da tela: inglês (como hoje) ou também traduzir para português?

## Referências
- Upstream: https://github.com/charlesvestal/fm1-polly · fm1-base: https://github.com/charlesvestal/fm1-base · felucca-bsp: https://github.com/hugelton/felucca-bsp
- Port SMK do genki: https://github.com/genkigenki/fm1-polly (branch `smk37`), notas de hardware: https://github.com/genkigenki/fm1-to-smk37
- Catálogo de firmwares SMK-37: https://altstrument.org/devices/m-vave-smk-37
- Clones locais: `SMK37Polly/upstream` (com submódulos) e `SMK37Polly/genki-port` (branch `smk37`)
