# Changelog

## Version 3.2
**Date:** 25-11-2026

### Fixed / Improved
1. Fixed the authentication bug and connected Flask sessions with the navigation system.
2. Reworked the profile system to support persistent name updates through Supabase Auth.
3. Improved authentication compatibility across desktop and Android.

### Added
1. Integrated a functional newsletter subscription system into the footer.
2. Connected newsletter subscriptions to Supabase for email storage.
3. Added duplicate subscription detection and subscriber reactivation.
4. Added subscription success and error notifications.

## Version 3.1
**Date:** 24-11-2026

### Added
1. Added a global loading animation.
2. Integrated live Reliance market indices.

### Fixed / Improved
1. Improved website responsiveness across devices.
2. Made weather information dynamic and city-based.

### Removed
1. Removed hardcoded market indices.
2. Removed hardcoded weather information.
## Version 3.0

### Date
16-11-2026

### Added
1. Added dedicated news sections and topic-based discovery.
2. Added Trending Topic Desks.
3. Added Financial Intelligence Desk.
4. Added market index displays.
5. Added weather information.
6. Added Bureau section.

### Changed
1. Rebranded the website from Sloth Newz to SLOTH NEWS.
2. Redesigned the homepage with a newsroom-style layout.
3. Redesigned individual article pages.
4. Improved navigation and content organization.
5. Updated the overall visual identity and presentation.

---
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