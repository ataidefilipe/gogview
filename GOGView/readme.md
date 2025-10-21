#About Dataset

GOG.com (formerly Good Old Games) is a digital distribution platform for video games and films, known for its DRM-free policy that allows users full ownership of their purchases. It offers a wide range of titles, from classic retro games to modern indie and AAA releases, often bundled with extras like soundtracks and manuals. Operated by CD Projekt, the company behind The Witcher series, GOG emphasizes user-friendly access and preservation of gaming history. Its Galaxy client also provides optional features like cloud saves and multiplayer integration without compromising its DRM-free philosophy.

This dataset includes data about 10k+ units (video games, DLC, additional materials) being available on GOG.com. Data was extracted by GOG.com API in June 2025.

#Columns description:

id - game store identifier (integer)
developer - developer name (string)
publisher - publisher name (string)
gallery - list of images/screenshots (string -> list). Please note that screenshot links are placed without file extension - to access it, you need to add ".png" to the end.
video - id of video (dict with two fields - "id" and "provider") 
supportedOperatingSystems - supported OS (string -> list)
genres - list of genres (string -> list)
globalReleaseDate - release date timestamp (integer)
isTBA - is TBA status (system variable, boolean)
isDiscounted_main - flag for discounted status (boolean)
isInDevelopment - flag for development status (boolean)
releaseDate - release date timestamp (similar to globalReleaseDate, integer)
availability - availability status (dict with fields 'isAvailable', 'isAvailableInAccount')
salesVisibility - sales visibility status (dict)
buyable - flag for buyability (boolean)
title - video game title (string)
image - title primary image (string). Please note that image link is placed without file extension - to access it, you need to add ".png" to the end.
url - title URL (sting)
supportUrl - tittle support URL (string)
forumUrl - title forum URL (string)
worksOn - nested field for supported OS (similar to supportedOperationSystems, but as dictionary)
category - primary genre (string)
originalCategory - original genre (similar to category, but less up-to-date) (string)
rating - system rating value, hard to interpret (integer)
type - type of title, 1 for games, 2 for bundles, 3 for DLC (integer)
isComingSoon - coming soon flag (boolean)
isPriceVisible - flag for price visibility (boolean)
isMovie - flag for movie status (boolean)
isGame flag for game status (boolean)
slug - title slug (part of URL defining game location) (string)
isWishlistable - flag for ability to add game to wishlist (boolean)
ageLimit - age restriction (integer)
boxImage - game key image / box image (string). Please note that image link is placed without file extension - to access it, you need to add ".png" to the end.
isMod - a flag for mod status (boolean)
currency - currency type (string)
amount - actual price (float)
baseAmount - base amount (without discounts) (float)
finalAmount - final amount (with discounts) (float)
isDiscounted - a field similar to isDiscounted_main (boolean)
discountPercentage - discount percentage (float)
discountDifference - discount difference (float)
discount - discount percentage (similar to discountPercentage) (float)
isFree - is game is free-to-play (boolean)
promoId - campaign name (string)
filteredAvgRating - average rating for English Location/Language (float)
overallAvgRating - average rating for all locations (float)
reviewsCount - number of reviews (integer)
isReviewable - flag for ability to add review (boolean)
reviewPages - number of pages with reviews (10 reviews per page) (integer)
dateGlobal - game release date (datetime)
dateReleaseDate - game release time, a bit more accurate values (datetime)