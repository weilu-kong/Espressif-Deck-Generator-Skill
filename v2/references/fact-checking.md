# Fact Checking for Espressif Decks

## Source priority
1. Espressif official product page.
2. Current official Datasheet / Product Brief.
3. TRM / Programming Guide / API reference.
4. Espressif official GitHub repositories and release branches.
5. Standards organizations for protocol branding/version claims.
6. Partner/vendor primary documentation when discussing partner products.

## Time-sensitive facts
Always re-check when used:
- CPU frequency / core count if product is preliminary;
- memory sizes and supported external memory;
- Wi-Fi generation and bands;
- Bluetooth version / Classic Bluetooth support;
- 802.15.4 / Thread / Zigbee capability;
- Matter support version;
- TX power and current consumption;
- SDK / ESP-IDF / ESP-Matter release version;
- board/module availability and certification state.

## Examples are not sources
Old Decks, SKILL examples, blog summaries and previous model answers are useful leads but are not authoritative evidence.

## Preliminary products
When a source says Preliminary, mark it in source manifest and avoid implying the specification is final.

## Performance claims
Avoid fixed performance/time promises unless a reproducible benchmark or official measurement supports them.

Example for Fast Reflash:
> Fast Reflash can reduce repeated flashing time by rewriting only changed flash sectors. Actual improvement depends on the binary delta, interface, flash and environment.

## Source manifest
For `full` delivery, maintain per-topic entries:
- source name;
- URL or document identifier;
- revision/version;
- checked date;
- facts used;
- preliminary/final status.
