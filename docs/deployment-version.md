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
