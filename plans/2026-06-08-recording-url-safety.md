# Recording URL Safety

## Problem

The recorder built output paths with `URL(string:)`, force-unwrapped the
resulting path string, persisted finished recording URLs with `description`, and
the last-recording tab force-unwrapped `videos[0].url`. A first launch, missing
recording, malformed URL, or document-directory lookup failure could crash the
sample.

## TDD Evidence

1. Extended `scripts/check-capture-source.py --mode behavior` to reject
   force-unwrapped recording playback, unsafe path-string URL creation, and
   noncanonical persisted recording URL strings.
2. Updated `MovieRecorder` to resolve the document directory with
   `FileManager.default.urls` and guard output URL creation.
3. Persisted completed recording URLs via `absoluteString` and made the
   last-recording tab show an empty state unless a valid saved URL is present.

## Verification

- `make lint`
- `make test`
- `make verify`
- `git diff --check`

`make build` runs the shared Xcode scheme when `xcodebuild` is installed;
otherwise it reports that static checks completed.
