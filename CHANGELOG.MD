# Changelog

## Version 2.5

### Date
16-9-2026

### Added
1. Added article tags and tag-based filtering.
2. Finance article generation is now working.
3. Finance articles now support tags.

### Fixed
1. Restored the tags functionality that was removed/lost from Version 1.
2. Fixed the finance pipeline database insertion issue.
3. Updated the finance pipeline to use the shared OpenRouter configuration.

### Changes

1. The news pipeline now generates 4 articles per run.
2. The finance pipeline now generates 6 articles per run.
---

## Version 2.1

### Date
13-8-2026

### Fixed
1. Navbar all links are working.
2. Worked on the Crypto page.

### Added
1. About Us page has been added.
2. Added AI image generation for news articles.
3. Added password protection for running the news pipeline.
4. Added individual article pages.
5. Added Supabase Storage for storing article images.

### Fixed
1. Fixed homepage UI issues.
2. Fixed routing issues.
3. Fixed API issues.

### Changed
1. Reduced article generation from 6 articles at a time to 3 articles at a time.
2. Tag schema from V1 was lost and had not yet been recreated, so tag-based filtering was temporarily unavailable.