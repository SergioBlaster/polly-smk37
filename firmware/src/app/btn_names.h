/* SPDX-License-Identifier: GPL-3.0-only */
/* The controls' names on the screen, by board. The FM-1 build keeps its printed names; the SMK-37 build says the
 * SMK-37 Pro's printed names, for the same functions (panel.c PANEL_DEFAULT: which SMK button does which FM-1 job).
 *
 *   N_*  the name in words: help cards, questions, messages, the header's keycap, HARDWARE CALIBRATION
 *   F_*  the name as a footer pill (pages.c page_footer, enc_line): one word, '_' drawn as a space ("SEQ_PLAY"),
 *        because the footer's parser takes a part's first word as the control
 *
 * Strings only, joined at compile time ("Hold " N_SAVE " and ..."): the FM-1 build is unchanged byte for byte. */
#pragma once

#if defined(BOARD_SMK37) && BOARD_SMK37
#define N_HOME "PATCH"
#define N_SEL "SCALE"
#define N_ARP "ARP"
#define N_SEQ "SEQ"
#define N_EDIT "PARA"
#define N_LFO "NOTE REPEAT"
#define N_FX "FX"
#define N_ENV "CHORD"
#define N_GLO "GLOBE"
#define N_SAVE "BT"
#define N_PLAY "SEQ PLAY"
#define N_REC "SEQ REC"
#define N_OCTDN "OCT-"
#define N_OCTUP "OCT+"
#define N_SELECT "K2"                                /* the encoders: K1 is MASTER, K2..K4 the FM-1's top row */
#define N_ALGORITHM "K3"
#define N_PRESETS "K4"
#define N_KNOB1 "K5"                                 /* K5..K8: the FM-1's KNOB 1..4 */
#define N_KNOB2 "K6"
#define N_KNOB3 "K7"
#define N_KNOB4 "K8"
#define F_PLAY "SEQ_PLAY"
#define F_REC "SEQ_REC"
#define F_ALGO "K3"
#define F_PRESET "K4"
#else
#define N_HOME "HOME"
#define N_SEL "SEL"
#define N_ARP "ARP"
#define N_SEQ "SEQ"
#define N_EDIT "EDIT"
#define N_LFO "LFO"
#define N_FX "FX"
#define N_ENV "ENV"
#define N_GLO "GLO"
#define N_SAVE "SAVE"
#define N_PLAY "PLAY"
#define N_REC "REC"
#define N_OCTDN "OCT-"
#define N_OCTUP "OCT+"
#define N_SELECT "SELECT"
#define N_ALGORITHM "ALGORITHM"
#define N_PRESETS "PRESETS"
#define N_KNOB1 "KNOB 1"
#define N_KNOB2 "KNOB 2"
#define N_KNOB3 "KNOB 3"
#define N_KNOB4 "KNOB 4"
#define F_PLAY "PLAY"
#define F_REC "REC"
#define F_ALGO "ALGO"
#define F_PRESET "PRESET"
#endif
/* the footer's pills that are one word on both boards */
#define F_HOME N_HOME
#define F_SEL N_SEL
#define F_SAVE N_SAVE
#define F_EDIT N_EDIT
#define F_SEQ N_SEQ
#define F_SELECT N_SELECT
#define F_OCT "OCT"                                  /* OCT- and OCT+ together ("OCT cursor") */
