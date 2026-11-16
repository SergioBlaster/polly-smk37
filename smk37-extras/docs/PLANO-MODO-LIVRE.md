# Plano: modo livre ("Free play") no Polly SMK-37

Data: 16/11/2026 · Branch: `smk37-nomes` (genki-port) · Só no build do SMK-37 (`BOARD_SMK37`)

**Situação:** concluído nas 3 fases, publicado na release v0.4.1-smk37.2 e testado no SMK-37 Pro (16/11/2026).

## O que é

Um modo para **tocar livremente** no teclado, sem a banda.

- **Som:** escolha qualquer um dos 128 timbres General MIDI. As 37 teclas tocam esse som, com velocity, rodas e oitavas.
- **Tela:** mostra **o nome da nota ou do acorde** (C4, Am7, G/B) e uma **partitura**: pauta dupla com clave de sol e de fá, e as notas desenhadas nela.
- **O que fica salvo:** só o **último timbre escolhido**. Músicas, progressões, grooves, mixer e Setup não mudam.

## Como funciona para quem toca

| Ação | O que faz |
| --- | --- |
| **Pad 7 de cima** (hoje apagado e sem uso) | Entra no modo livre. Apertar de novo sai e volta para a página onde você estava. |
| **PATCH** ou qualquer botão de página | Sai do modo livre e abre aquela página, como hoje. |
| Teclas (as 37) | Tocam o timbre escolhido, com a força do toque. |
| **K5** Sound | Escolhe o timbre (128 sons GM, por nome). Ao parar de girar, toca uma nota curta de amostra. |
| **K4** | Pula de família em família (pianos, órgãos, guitarras...), como na página Sound. |
| **K6** Volume | Volume do modo livre. Não fica salvo; volta a 100 ao entrar. |
| **K7** Staff | Partitura ligada ou desligada. Desligada, o nome da nota ou do acorde fica maior. Não fica salvo. |
| **K8** Spelling | Acidentes em ♯ ou ♭ (C♯ ou D♭). Não fica salvo; o padrão segue o acorde reconhecido. |
| **OCTAVE− / OCTAVE+** | Oitava das teclas, como hoje. |
| **Rodas PITCH e MOD** | Pitch bend e vibrato no som do modo livre. |
| Pads (exceto o 7), faders, SEQ PLAY, SEQ REC, BT | **Não fazem nada.** O rodapé avisa, e o cartão de ajuda (segurar 1 s) explica. Assim nada da banda muda sem querer. |
| Segurar qualquer botão 1 s | Cartão de ajuda, como no resto do firmware. Inclui um cartão novo para o pad 7. |

Ao entrar, **a banda para** (como apertar SEQ PLAY). Isso libera o canal de som e o processador. Ao sair, nada recomeça sozinho.

## A tela (240 × 240)

```
┌────────────────────────────────┐
│ [PAD 7] Free play     Piano 1  │  cabeçalho: o modo e o timbre
│                                │
│            Am7                 │  nome grande: acorde ou nota (A4)
│        A3 · C4 · E4 · G4       │  as notas tocadas, da grave à aguda
│ 𝄞 ─────────────o───────────    │
│   ───────────o─────────────    │  pauta dupla (clave de sol e de fá):
│   ─────────────────────────    │  as notas como semibreves, empilhadas
│ 𝄢 ──────o──────────────────    │  quando são acorde; linhas suplementares
│   ─────────────────────────    │  e ♯/♭ ao lado
│ Sound    Volume  Staff  Spell  │  faixa de knobs K5–K8 (como nas outras
│ Piano 1    100    on     ♯     │  páginas)
│ (K5)sound (K4)family [PAD7]exit│  rodapé com pílulas
└────────────────────────────────┘
```

| Situação | O que aparece |
| --- | --- |
| **Uma nota** | Nome com oitava ("C4", "F♯5"). |
| **Duas notas** | As duas e o intervalo ("C4 + G4 · 5ª justa"). |
| **Três ou mais formando acorde** | Nome do acorde ("Am7", "C/E"), pelo mesmo reconhecedor da banda (`chord_recognize` / `chord_name`, 25 tipos e baixo invertido). |
| **Três ou mais sem acorde conhecido** | Só a lista de notas. |
| **Depois de soltar** | O último nome e as notas ficam na tela, mais claros, até a próxima tecla. Dá tempo de ler. |
| **Notas fora da pauta** | Até 3 linhas suplementares. Acima disso, a nota vai uma oitava para baixo com "8va" (ou para cima com "8vb"). |
| **Segundas no mesmo acorde** | Notas vizinhas (C e D juntos) ficam lado a lado, como na partitura impressa. |
| **Cores** | Seguem os 3 temas: linhas em tinta, notas tocando em teal, nome em tinta forte. Claro, escuro e neon funcionam sem mudança. |

## Como fica no código

| Parte | Onde | O que muda |
| --- | --- | --- |
| **Estado do modo** | `app/ui.c` | `ui.free_on`, a página de onde veio, volume, staff, spelling, últimas notas. Nada disso é salvo. |
| **Entrada e saída** | `app/ui.c`, `smk_pad()` | O pad índice 6 (hoje "pad 6 free" no código) liga e desliga. Os botões de página saem do modo antes de abrir a página. |
| **Teclas** | `app/ui.c`, `key_down()` / `key_up()` | Com o modo ligado, um desvio no começo: nota direto no sintetizador (`gm_midi`). Não passa por `arr_key` nem pelo reconhecimento da banda. Nada é gravado. |
| **Canal de som** | | Canal 16 (`ARR_CLICK_CHAN`), que só o metrônomo usa. Com a banda parada ele fica livre, e o metrônomo já reenvia o próprio timbre a cada clique. Os canais 1–15 da banda e do MIDI in não são tocados. Ao sair: all-notes-off no canal 16. |
| **Rodas** | `smk_wheels_send()` | Já envia para todos os canais menos o 10, então o canal 16 já recebe. Só conferir. |
| **Timbre salvo** | `app/app.h` | Um dos bytes livres de `project_t` (`rsv[3]`) vira `uint8_t free_prog`. Saves antigos leem 0, que é o Acoustic Grand Piano, um bom padrão. O formato não muda (`PROJ_FORMAT` fica 5). Trocar o timbre chama `mark_dirty()`; o salvamento automático grava o projeto, e como só esse byte mudou, nada mais muda. |
| **Página nova** | `app/pages.c` | Um `P_FREE` no fim de `enum` das páginas, com nome "Free play", fora de `PAGE_BTN` (nenhum botão de página leva até ela; só o pad 7). `draw_free()` em `draw_page()`, `song_page_knobs()` para K5–K8, e as pílulas do rodapé. |
| **Nome da nota ou acorde** | `app/pages.c` | `chord_recognize()` e `chord_name()` (`dsp/chords.h`), já usados pela banda. Para nota solta: `KEY_NAME[]` + oitava. Intervalos: uma tabela de 12 nomes. |
| **Partitura** | `app/pages.c` | `draw_staff()` com `cv_line` / `cv_rect` / `cv_pset` (`gfx.c`). Notas como ovais de 7×5 px. Linhas a cada 6 px. Claves de sol e de fá como bitmaps de 1 bit (≈ 12×34 e 12×14 px). ♯ e ♭ como bitmaps 5×7, porque a fonte não tem esses símbolos. Posição: nota MIDI para posição na pauta pela escala diatônica, com o acidente conforme o spelling. Redesenha só quando as notas mudam (como as outras faixas da tela, por `ui.sig`). |
| **Cartões de ajuda** | `app/pages.c`, `CARD[]` | Pad 7 ("Free play"), e K5–K8 e os botões sem função no modo livre ("Does nothing in Free play"). O simulador já reprova cartões com texto fora da caixa. |
| **Mapa dos pads** | `draw_home_held()` / KNOB BANK | O pad 7 passa a aparecer como "FREE". |
| **Luz do pad 7** | `smk_pads()` | Apagado fora do modo, aceso (por exemplo branco) dentro. Os outros pads ficam apagados no modo livre, para mostrar que não fazem nada. |

Tudo fica atrás de `#if BOARD_SMK37`: o build do FM-1 não muda, e o CI confere isso.

## Testes

- **Cenário novo** `tests/scenarios/smk37/free.polly`, no simulador do PC (o mesmo do CI):
  - entra pelo pad 7 e confere a página e que a banda parou;
  - toca C–E–G e confere "C";
  - toca A–C–E–G e confere "Am7";
  - toca uma nota e confere "C4" com a oitava certa;
  - gira K5 e confere `free_prog`;
  - sai e confere que voltou à página anterior.
- **Nada mudou fora do timbre:** o simulador ganha `expect` para `free_prog` e um resumo (hash) de `songs` e dos padrões. O cenário guarda o resumo antes de entrar e confere que é igual depois de sair.
- **Capturas no CI:** o modo livre com nota, acorde, acidente, linha suplementar e 8va, nos 3 temas. Entram em `smk37-screens`, como as outras telas.
- **Emulador:** o pad 7 já existe na página do emulador. Basta testar tocando.
- **No teclado:** você confere o som, a velocity e se a partitura fica legível na tela real de 240 px.

## Fases

| Fase | O que entrega | Tamanho |
| --- | --- | --- |
| **1. Tocar** | Pad 7 entra e sai; as teclas tocam no canal 16 com o timbre de K5; o timbre fica salvo; os outros controles não fazem nada. Tela simples: nome da nota ou do acorde, grande. | Pequena |
| **2. Partitura** | Pauta dupla, claves, notas, linhas suplementares, ♯/♭, 8va/8vb, segundas lado a lado. K7 e K8. | Média, a maior parte do trabalho |
| **3. Acabamento** | Cartões de ajuda, mapa dos pads, luz do pad 7, capturas nos 3 temas, guia (PT e EN) e README atualizados, nova release. | Pequena |

Cada fase passa no CI, vai para o emulador e gera um firmware que você pode testar antes da próxima.

## Riscos

| Risco | O que fazer |
| --- | --- |
| Partitura apertada em 240 px com cabeçalho, knobs e rodapé | Pauta com linhas a cada 6 px (≈ 70 px de altura para as duas pautas). Se ficar apertado, K7 "off" esconde a pauta, e o nome fica grande. A fase 2 começa com uma captura para avaliar antes de seguir. |
| Canal 16 compartilhado com o metrônomo | Só se a banda tocasse junto, e o modo para a banda. Se algum dia o modo livre permitir a banda tocando, troca para um canal livre. |
| Alguma coisa da banda mudar sem querer | O desvio nas teclas vem antes de qualquer lógica da banda; pads, faders, PLAY e REC são ignorados; o teste de hash confere. |
| Acorde com nome "estranho" (o reconhecedor é o da banda, 25 tipos) | Quando não reconhece, mostra só as notas. Melhorar o reconhecedor fica fora deste plano, porque mudaria a banda. |
| Desenho a cada quadro pesar no processador | Redesenhar só quando as notas mudam. |

## Decisões em aberto (para você)

1. **Entrada pelo pad 7 de cima** (hoje livre)? Outras opções: segurar PATCH + KNOB BANK, ou uma página dentro de GLOBE.
2. **Parar a banda ao entrar?** O plano para. Tocar por cima da banda tocando seria outro modo, com mais riscos.
3. **K6–K8 (volume, partitura on/off, ♯/♭):** valem a pena, ou só K5 (timbre)?
4. **Pads no modo livre:** ficam sem função (plano atual), ou poderiam tocar sons de bateria em cima do que você toca, sem salvar nada?
5. **Também no FM-1?** O plano é só para o SMK-37. No FM-1 precisaria de outra entrada, porque não há pads.
