# Exact Cloudflare verification (draft)

On 2026-10-19 the site owner authorized preserving existing Cloudflare analytics
and email protection, and validating those transformations precisely before
enabling automatic publication. This draft needs independent review and actual
Pages recovery acceptance; it does not enable publication.

The existing `verify-public-deployment.py` and all original build/baseline guards
remain unchanged. Both normal and restore verification retain its raw result,
including failures. A second mandatory checker verifies the guarded original
export and public marker, then compares **every exported HTML file**, including
noindex, legacy direct HTML, Google verification and 404 pages.

The second checker accepts exact original bytes, or only these transformations:

1. Exactly the observed 367-byte beacon insertion immediately before the actual
   closing body tag, pinned by SHA256
   `161f2cbf38dc2d029b6223cae09efb59c27edd57a3932b62c320ce014c213795`.
   The pin includes the entire script, URL, integrity, public site configuration
   and following newline. Unknown updates, extra scripts or changed configuration
   fail closed. The fixture contains only that already-public beacon, no private
   reference material or credentials.
2. Exact email-protection href/span/plain-anchor templates in HTML element
   contexts. Each encoding must reversibly decode to the original ASCII address;
   all original attributes, whitespace and other content must remain byte-identical.
   Scripts, styles, comments, raw-text and inert containers are not rewritten.
3. Exactly one pinned email decoder when there are email rewrites, immediately
   before the first script following the protected emails. A decoder without
   corresponding reversible rewrites, duplicates, moved/modified decoders or
   unknown templates fail closed.

No general script removal, DOM serialization, text normalization or HTML
minification is used. After reconstructing just those transformations, equality
with the **entire original artifact bytes** is required. Each page records the
original/public hashes and transformation counts. The public version marker is
checked before and after the complete scan.

The original raw result may fail for these approved changes. Its report remains
immutable evidence under a distinct name; the original failure is never relabeled
as a raw-byte success. The draft workflow requires the separate exact checker to
pass and retains both reports for normal deployments and restores.

This does not verify browser functionality, third-party script execution,
independent review, recovery or publisher integration. The report expressly
denies publication authorization. Changes to the pinned Cloudflare configuration
or newly encountered email encodings require a fresh review; do not auto-accept
new forms. Current recovery source-workflow success requirements remain intact.
