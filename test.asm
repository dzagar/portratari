    processor 6502
    include vcs.h
    include macro.h
	; include colour.asm

	SEG
    org $F000

Start

    CLEAN_START

	lda #$00
    sta COLUBK  ;background
    lda #$ff
    sta COLUPF  ;white playfield
	;lda #$44
	;sta COLUP0
	;lda #$da
	;sta COLUP1

;MainLoop starts with usual VBLANK code,
;and the usual timer seeding
MainLoop
    VERTICAL_SYNC
    lda #43
    sta TIM64T
;


WaitForVblankEnd
    lda INTIM
    bne WaitForVblankEnd
    sta VBLANK


;TitlePreLoop , TitleShowLoop, TitlePostLoop
;



pixelHeightOfTitle = #190
scanlinesPerTitlePixel = #1


    ldy #20
TitlePreLoop
    sta WSYNC
    dey
    bne TitlePreLoop


    ldx #pixelHeightOfTitle ; X will hold what letter pixel we're on
    ldy #scanlinesPerTitlePixel ; Y will hold which scan line we're on for each pixel



TitleShowLoop
    sta WSYNC
    lda mask_STRIP_0-1,X           ;[0]+4
    sta PF0                 ;[4]+3 = *7*   < 23 ;PF0 visible
    lda mask_STRIP_1-1,X           ;[7]+4
    sta PF1                 ;[11]+3 = *14*  < 29    ;PF1 visible
    lda mask_STRIP_2-1,X           ;[14]+4
    sta PF2                 ;[18]+3 = *21*  < 40    ;PF2 visible
    nop         ;[21]+2
    nop         ;[23]+2
    nop         ;[25]+2
    ;six cycles available  Might be able to do something here
    lda mask_STRIP_3-1,X          ;[27]+4
    ;PF0 no longer visible, safe to rewrite
    sta PF0                 ;[31]+3 = *34*
    lda mask_STRIP_4-1,X        ;[34]+4
    ;PF1 no longer visible, safe to rewrite
    sta PF1         ;[38]+3 = *41*
    lda mask_STRIP_5-1,X        ;[41]+4
    ;PF2 rewrite must begin at exactly cycle 45!!, no more, no less
    sta PF2         ;[45]+2 = *47*  ; >



    dey ;
    bne NotChangingWhatTitlePixel
    dex ;

    beq DoneWithTitle ;

    ldy #scanlinesPerTitlePixel ;
NotChangingWhatTitlePixel

    jmp TitleShowLoop

DoneWithTitle

    lda #0
    sta PF2
    sta PF0
    sta PF1

    ldy #50
TitlePostLoop
    sta WSYNC
    dey
    bne TitlePostLoop

; usual vblank
    lda #2
    sta VBLANK
    ldx #30
OverScanWait
    sta WSYNC
    dex
    bne OverScanWait
    jmp  MainLoop

	include "mask.asm"

    org $FFFC
    .word Start
    .word Start
