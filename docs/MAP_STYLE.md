# The map style of *The Roots of Ramallah* (v76)

All drawn maps in the book follow this guide. The guide is implemented in code: `src/map_style.py` holds the colours, symbols, type, furniture and terrain, and `src/build_atlas.py` holds the projections (`Sheet`, `Flat`, `Lin`). If a map needs something this guide does not cover, add it here and in `map_style.py` before using it.

## 1. What a mark means

These symbols mean the same thing on every map in the book.

| Mark | Meaning | Code |
|---|---|---|
| Green filled dot, white edge | **Documented**: the place is named in a document, an inscription or an excavation report | `sym_documented` |
| Green dashed ring | Documented, but the position is uncertain | `sym_documented(uncertain=True)` |
| Ochre filled dot | **Remembered**: the family's or the church's tradition, no document | `sym_remembered` |
| Ochre dashed ring | Tradition only, and the place itself is uncertain (pilgrim identifications) | `sym_remembered(uncertain=True)` |
| Grey dot | **Context**: named for orientation only | `sym_context` |
| Open diamond | **Standing evidence**: a monument, church, mosaic or inscription that can still be seen | `sym_monument` |
| Red ringed dot | **Ramallah**, on every map, so the reader can always find home | `sym_ramallah` |
| Red ring, empty | The site of Ramallah before the town existed (before 1562) | `sym_ramallah(empty=True)` |
| Small blue dot | A spring (*ʿayn*) | `sym_spring` |

Routes:
- a solid green line is a documented move;
- a dashed ochre line is a remembered move;
- a dotted line is approximate;
- a broad tan band is a road on the ground.

A map whose subject is a category rather than evidence (archaeological period, for example) uses the **thematic ramp** `ERA` (violet to lilac). It never uses green or ochre, so the evidence colours keep their meaning.

## 2. Type

The plate is 860 units wide and is shown at about 720 px on a phone, so 13 units is 11 px. **Nothing a reader needs is set below 11 units.**

| Class | Style | Size (units) |
|---|---|---|
| Ramallah and the map's subject towns | bold roman, capitals | 13.5 |
| Other towns and villages | bold roman, upper and lower case | 13 |
| Regions | spaced capitals, brown | 13 |
| Water (seas, rivers, wadis, springs) | italic, blue `#3B6A86` | 12–13 |
| Notes beside a label (distance, date) | italic, grey | 11.5 |
| Furniture (scale, ticks, legend) | roman, grey | 11 |

Every label sits on a white halo, so it reads over terrain. Arabic names use the book's transliteration.

## 3. Frame and furniture

- **Neatline**: a 1-unit hairline in `#8A7E6A`.
- **Graticule**: ticks on the neatline only, not lines across the ground. Labels go outside, below and to the left.
- **Scale bar**: bottom-left, inside the frame, on a white tab, in two segments, in kilometres.
- **North arrow**: only on plans (the town plan) and on sheets where north is not up. Every other sheet is north-up and says so through its graticule.
- **Locator inset**: top-right on large-scale sheets (district and town). It shows the southern Levant, with the sheet as a red box and Ramallah as a red dot.
- **Legend**: under the map, one row, using the same symbol functions as the map.
- **Source line**: one italic grey line naming the sources, the projection, and "terrain from SRTM/Copernicus via AWS Terrain Tiles" where terrain is drawn.

## 4. Terrain

The land is evidence in this story: the ridge, the watershed road, the wadis falling east to the Jordan and west to the coast. Terrain is therefore drawn on every regional and district map. It is not drawn on the world map (fig. 32) or on the schematic town plan.

- **Hypsometric tints**, muted, from green-grey below sea level through cream at sea level to warm tan on the ridge (`HYPSO`).
- **Hillshade**, lit from the north-west at 45°, multiplied in at 70–106 %, so it never goes darker than 70 %. Vertical exaggeration is 2× on regional sheets and 1× on district sheets.
- **Contours**: 100 m or 200 m on district sheets. The **800 m contour is bolder** (`CONTOUR_INDEX`), because that line is "the ridge". There are no contours on regional sheets.
- The raster is one JPEG per map, cached in `data/terrain/<key>.json` together with the vector contours and wadis. It is kept under 150 KB. Delete the file to regenerate it.

## 5. Water

One blue family:
- sea `#D5E5EC`;
- lake `#C6DCE6`;
- shoreline `#6E9BB3`;
- rivers `#4F86A6`;
- wadis `#7DA7BE`;
- water text `#3B6A86`.

- **Rivers** (Natural Earth): 1.5 units.
- **Wadis** are derived from the elevation model (D8 flow accumulation over a filled DEM) and drawn in three weights by catchment size. A wadi is **named only where the book or its cited survey names it**. Unnamed channels stay unnamed.
- **Springs** are drawn only where a source in the book names them.
- **The Dead Sea**: Natural Earth's lake outline is the modern, shrunken sea, and its southern basin is now dry evaporation pans. On maps of periods before 1948 the source line says the shoreline is modern.

## 6. Colour palette

- Paper `#FCFBF8`.
- Ink `#1A1915`, body `#3D3A35`, notes `#6B6760`.
- Documented `#007A3D` (dark `#004A26`); remembered `#9A6324`; context `#8F8A80`.
- Ramallah `#B3261E`.
- Thematic ramp `ERA`: `#2E2A4A`, `#5A4E8C`, `#8676B8`, `#B0A3D6`.

These are the family-tree book's "Tree Book Classic" green and ochre. Red is reserved for Ramallah.

## 7. Honesty rules (unchanged)

- Every drawn route says whether it is documented, remembered or approximate.
- Every map carries its sources.
- A schematic is called a schematic and has no scale bar.
- Names come from the book's text, never invented for the map.
