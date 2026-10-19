# Deployment version marker

After the formal static build and both original guards, CI adds
`out/deployment-version.json`. The marker includes the exact checkout SHA,
Actions run ID and attempt, and a SHA256 digest of sorted `[relative path,
file SHA256]` records for every exported file before the marker is added.
UTF-8 JSON uses `ensure_ascii=False` and separators `(',', ':')`; no trailing
newline is included in the digest input. Paths use forward slashes.

The script refuses an existing marker, missing export index or symlinks.
Existing HTML and metadata are untouched. Only the version and aggregate digest
are public; paths, source references and credentials are not included.

This marker supports future cache/version comparisons. It is not a signature,
independent review, proof of guard implementation, full-page verification or a
rollback acceptance test. A successful public marker fetch alone cannot prove
that all HTML/assets are from the same export. Compare it with verified Actions
artifact evidence and separately validate affected public pages and functions.
When restoring an older artifact, retain its original marker/run identity;
do not relabel the old export as the restore workflow's source version.

Feature-branch dispatches build and package only; deployment requires master
and rechecks its latest SHA immediately before the Pages action. That check
does not make external deployments atomic. Automatic publication remains gated
outside this workflow; this draft does not enable it.

The integration draft adds `verify-public-deployment.py`: it first recomputes
the original export digest, compares the public marker with exact source/run/
attempt identity, then fetches every exported HTML file, including direct legacy
paths, verification files and noindex pages, and compares raw HTML bytes.
Directory index files use their public directory URL. It rechecks the marker afterwards.
Redirects, oversized replies, stale markers, modified HTML and missing legacy
markers fail closed. No browser scripts, analytics or chat widgets execute.
This checks HTML bytes, not all external images or browser functionality.
CDN rewriting is an unresolved verification failure, never normalized away.

Normal deployments and restores retain separate public-verification artifacts.
Each verification attempt uses a distinct artifact name so a failed attempt's
evidence is retained. Normal verification obtains the original marker attempt
from the successful build job's output. A partial rerun advances the workflow
attempt without rebuilding its retained export, so the current workflow attempt
must not be substituted for that original build identity. An isolated GitHub
Actions partial-rerun experiment (run 39088515104) confirmed this behavior.
Recovery preparation validates a marked retained export's original attempt
against the exact successful build job, required guard/upload steps, source SHA
and artifact creation time within that build. It still requires the source
workflow's overall success. A marked draft backup without original artifact
timing provenance is refused; legacy unmarked backups remain rehearsal-only.
An actual restore now requires a matching original marker before uploading a
recovery artifact; old backups lacking one remain usable for an isolated
artifact rehearsal, but are not accepted for automatic production restoration.
The integration changes still require an independent review and real Pages
acceptance. They do not enable automatic publication.

The 2026-10-19 owner-approved draft adds a separate exact Cloudflare checker;
see `cloudflare-exact-verification.md`. The raw checker and its failure reports
remain unchanged. The draft adds a mandatory reconstruction gate for precisely
pinned/reversible transformations, pending independent review and actual Pages
acceptance. It does not retroactively turn prior workflow failures into success.
