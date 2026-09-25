# Delivery Modes

## quick
Use when the user wants a fast draft or preview.
Deliver:
- HTML deck.

Still run basic validation if Playwright is available.

## standard (default)
Deliver:
- HTML deck;
- standalone HTML;
- PDF (normally fidelity, vector on request).

Run validator before export.

## full
Deliver standard outputs plus useful project artifacts as requested:
- contact sheet;
- source manifest;
- speaker script;
- slide-by-slide technical explanation / Q&A.

Do not create long speech/Q&A documents if the user only needs slides.
