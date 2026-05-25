"""
Google Flow Video Prompt Generator
Cinematographic prompt builder for Google Flow video generation.
"""

import json
from dataclasses import dataclass

import streamlit as st
import streamlit.components.v1 as components

CUSTOM = "✏️ Custom (type below)"

# ── Character profile constants ──────────────────────────────────────────────

CHAR_GENDERS: tuple[str, ...] = ("Unspecified", "Male", "Female", "Non-binary")

CHAR_AGE_RANGES: tuple[str, ...] = (
    "Unspecified",
    "Teen (13–17)",
    "Young Adult (18–29)",
    "Adult (30–45)",
    "Middle-Aged (46–60)",
    "Senior (60+)",
)

CHAR_AGE_WORDS: dict[str, str] = {
    "Unspecified":         "",
    "Teen (13–17)":        "teenage",
    "Young Adult (18–29)": "young adult",
    "Adult (30–45)":       "adult",
    "Middle-Aged (46–60)": "middle-aged",
    "Senior (60+)":        "senior",
}

CHAR_BODY_TYPES: tuple[str, ...] = (
    "Unspecified",
    "Athletic",
    "Slender",
    "Curvy",
    "Muscular",
    "Average build",
    "Plus-size",
    "Petite",
    "Stocky",
    "Lean and wiry",
)

CHAR_BODY_TYPES_MATURE: tuple[str, ...] = (
    "Voluptuous hourglass figure",
    "Well-built and chiseled physique",
    "Full-figured with prominent curves",
    "Lean and toned with defined muscle",
)

CHAR_SKIN_TONES: tuple[str, ...] = (
    "Unspecified",
    "Fair / porcelain",
    "Light",
    "Medium",
    "Olive",
    "Tan",
    "Brown",
    "Dark",
    "Deep ebony",
)

CHAR_HAIR_STYLES: tuple[str, ...] = (
    "Unspecified",
    "Short cropped",
    "Undercut / fade",
    "Medium length",
    "Long flowing",
    "Curly",
    "Wavy",
    "Braided / plaited",
    "Afro",
    "Bun / updo",
    "Ponytail / half-up",
    "Shaved / buzz cut",
    "Dreadlocks",
    "Bob cut",
    "Slicked back",
)

CHAR_HAIR_COLORS: tuple[str, ...] = (
    "Unspecified",
    "Jet black",
    "Dark brown",
    "Medium brown",
    "Light brown",
    "Blonde",
    "Platinum blonde",
    "Auburn",
    "Red",
    "Gray / silver",
    "White",
    "Vibrant dyed — blue",
    "Vibrant dyed — purple",
    "Vibrant dyed — red",
)

CHAR_EYE_COLORS: tuple[str, ...] = (
    "Unspecified",
    "Brown",
    "Dark brown",
    "Blue",
    "Light blue",
    "Green",
    "Hazel",
    "Amber",
    "Gray",
    "Heterochromia",
)

CHAR_FACIAL_FEATURES: tuple[str, ...] = (
    "Unspecified",
    "Strong jawline",
    "Soft / delicate features",
    "High cheekbones",
    "Sharp angular features",
    "Round face",
    "Oval face",
    "Full lips",
    "Freckled",
    "Bearded — short stubble",
    "Bearded — full beard",
    "Clean-shaven",
    "Scar across face",
    "Dimples",
)

CHAR_ETHNICITY: tuple[str, ...] = (
    "Unspecified",
    "Caucasian / European",
    "East Asian",
    "South Asian",
    "Southeast Asian",
    "Middle Eastern",
    "African / Black",
    "Latino / Hispanic",
    "Indigenous",
    "Mixed / Multiracial",
)

CHAR_ACTIONS: tuple[str, ...] = (
    "Unspecified",
    "standing still, facing camera",
    "walking slowly toward camera",
    "running at full sprint",
    "sitting and observing quietly",
    "turning to look over shoulder",
    "reaching out toward camera",
    "looking up toward the sky",
    "in a confident hero stance",
    "fighting in a combat stance",
    "embracing someone",
    "speaking / delivering dialogue",
    "laughing naturally",
    "looking down contemplatively",
    "crouching and hiding",
    "dancing freely",
    "working at a focused task",
    "reacting in shock or fear",
    "sprinting away from camera",
)

GENRES = [
    "Sci-Fi & Cyberpunk",
    "Horror & Supernatural",
    "Romance & Drama",
    "Action & Thriller",
    "Fantasy & Mythic",
    "Noir & Crime",
    "Documentary & Realism",
    "Comedy & Satire",
    "Historical & Period",
    "Anime & Stylized",
    "Nature & Landscape",
    "Racing & Motorsport",
    "Aviation & Aerial",
]

THEMES = [
    "Dystopian Future",
    "Forbidden Love",
    "Revenge Arc",
    "Survival / Last Stand",
    "Coming of Age",
    "Heist & Betrayal",
    "Cosmic Wonder",
    "Urban Isolation",
    "War & Sacrifice",
    "Surreal Dreamscape",
    "Celebration & Joy",
    "Hunt / Pursuit",
]

CONTENT_RATINGS = {
    "Censored (all audiences)": "censored",
    "Uncensored 18+ (mature)": "mature",
}

# Veo 3.1 / Google Flow style anchors (woven into every generated prompt)
GENRE_STYLE: dict[str, str] = {
    "Sci-Fi & Cyberpunk": "sci-fi cinematic realism, premium VFX polish",
    "Horror & Supernatural": "horror cinematic realism, practical dread",
    "Romance & Drama": "prestige romance-drama cinematography",
    "Action & Thriller": "high-impact action cinematography, kinetic clarity",
    "Fantasy & Mythic": "epic fantasy cinematic scale",
    "Noir & Crime": "classic noir crime cinematography",
    "Documentary & Realism": "documentary vérité realism",
    "Comedy & Satire": "sharp comedic framing with clean readability",
    "Historical & Period": "period-accurate historical cinematic texture",
    "Anime & Stylized": "stylized animated cinematic composition",
    "Nature & Landscape": "nature documentary cinematic realism, BBC Planet Earth scale",
    "Racing & Motorsport": "high-octane motorsport cinematography, kinetic broadcast clarity",
    "Aviation & Aerial": "aerial cinematography at epic scale, breathtaking altitude perspective",
}

THEME_MOOD: dict[str, str] = {
    "Dystopian Future": "dystopian tension and societal decay",
    "Forbidden Love": "forbidden desire and emotional restraint",
    "Revenge Arc": "vengeful intensity and rising stakes",
    "Survival / Last Stand": "survival desperation and physical strain",
    "Coming of Age": "youthful transition and bittersweet growth",
    "Heist & Betrayal": "covert tension and double-cross energy",
    "Cosmic Wonder": "awe-filled cosmic scale",
    "Urban Isolation": "lonely urban melancholy",
    "War & Sacrifice": "wartime gravity and moral weight",
    "Surreal Dreamscape": "surreal dream logic and uncanny calm",
    "Celebration & Joy": "joyful uplift and communal energy",
    "Hunt / Pursuit": "relentless pursuit and escalating pace",
}

PRO_BASELINE = (
    "Photorealistic cinematic video, stable camera motion, coherent anatomy, "
    "natural movement, sharp subject focus, high detail, filmic color grade."
)
PRO_EXCLUDE_SAFE = (
    "Family-safe framing. No logos, no on-screen text, no watermarks, "
    "no distorted faces or hands, no flicker."
)
PRO_EXCLUDE_MATURE = (
    "Adults-only tone. No logos, no on-screen text, no watermarks, "
    "no distorted faces or hands, no flicker."
)


@dataclass(frozen=True)
class OptionPack:
    shots: tuple[str, ...]
    subjects: tuple[str, ...]
    environments: tuple[str, ...]
    lighting: tuple[str, ...]
    atmospheres: tuple[str, ...]


# --- Genre base libraries ---------------------------------------------------

GENRE_PACKS: dict[str, OptionPack] = {
    "Sci-Fi & Cyberpunk": OptionPack(
        shots=(
            "Low-angle tracking shot, tracking",
            "FPV drone fly-through, weaving past",
            "Eye-level dolly shot, pushing in on",
            "Macro close-up, rack-focusing on",
            "Wide establishing aerial shot, orbiting",
            "Dutch-angle steadicam shot, circling",
            "Slow-motion bullet-time orbit around",
            "Whip-pan transition into close-up of",
            "Top-down God's-eye view of",
            "Snorricam body-mounted shot of",
            "Static locked-off medium shot of",
            "Jib arm rising reveal of",
        ),
        subjects=(
            "a matte black 1969 Mustang fastback with underglow",
            "a cybernetic detective in a hologram-lined trench coat",
            "a chrome android with exposed servo joints",
            "a street hacker in AR visor and reflective puffer",
            "a rogue AI avatar materializing as liquid mercury",
            "a courier on a mag-lev hover bike",
            "a lab-grown replicant with serial numbers on the neck",
            "a corporate assassin in seamless black smart-fabric",
            "a junkyard mech being welded by spark showers",
            "a neon-lit geisha drone with porcelain faceplate",
            "a cryo-pod passenger waking with condensation breath",
            "a swarm of micro-drones forming a human silhouette",
        ),
        environments=(
            "neon-lit rainy cyberpunk alleyway with kanji holo-ads",
            "zero-gravity space station corridor with flickering panels",
            "brutalist megastructure interior with endless escalators",
            "Tokyo Shibuya crossing at rush hour with holographic billboards",
            "underground black-market bazaar beneath reactor pipes",
            "orbital ring habitat overlooking a gas giant",
            "abandoned server farm cathedral with blinking racks",
            "smog-choked megacity rooftop with drone traffic lanes",
            "bioluminescent fungal tunnel in a terraforming dome",
            "chrome subway platform with arriving maglev blur",
            "rain-slicked parking garage with cyan exit signs",
            "desert highway at night with laser billboard horizons",
        ),
        lighting=(
            "neon magenta and cyan cross-lighting with wet reflections",
            "LED panel matrix with specular highlights on chrome",
            "intense anamorphic lens flare from oncoming traffic",
            "harsh overhead fluorescent practicals with green cast",
            "backlit silhouette with blown highlights and haze",
            "motivated window light with dust motes in smoke",
            "strobing club lights with haze and laser scatter",
            "cool moonlight with silver fill on wet asphalt",
            "RGB rim light tracing body contours",
            "practical hologram glow as soft key",
            "high-contrast noir venetian-blind shadows",
            "UV blacklight revealing fluorescent graffiti",
        ),
        atmospheres=(
            "volumetric fog, cinematic ultra-realism",
            "chromatic aberration, retro VHS nostalgia",
            "clean clinical sharpness, commercial polish",
            "rain streaks on lens, melancholic mood",
            "motion blur trails, kinetic energy",
            "anamorphic oval bokeh, prestige drama",
            "particle dust, epic blockbuster scale",
            "lens distortion at edges, surreal unease",
            "film grain, Kodak Vision3 500T aesthetic",
            "heat shimmer, documentary vérité",
            "smoke wisps, tense thriller atmosphere",
            "double-exposure ghosting, ethereal memory",
        ),
    ),
    "Horror & Supernatural": OptionPack(
        shots=(
            "Slow creeping dolly-in on",
            "Handheld shaky close-up on",
            "Low-angle ominous push-in on",
            "Over-the-shoulder peek around corner at",
            "Wide static frame holding on",
            "Rack-focus from foreground claw to",
            "Dutch-angle tilt discovering",
            "Steadicam following behind",
            "Extreme macro on eye reflecting",
            "Crane descending through fog onto",
            "Mirror reflection reveal of",
            "Flashlight beam POV scanning",
        ),
        subjects=(
            "a pale figure in a tattered Victorian nightgown",
            "a porcelain doll with cracked half-smile",
            "a hooded cultist holding a black candle",
            "a feral werewolf mid-transformation silhouette",
            "a drowned spirit with waterlogged hair",
            "a scarecrow with burlap face stitched wrong",
            "a priest clutching a tarnished silver crucifix",
            "a child standing motionless at the end of a hall",
            "a swarm of moths erupting from a wardrobe",
            "a skeletal hand pushing through drywall",
            "a vintage TV static face whispering",
            "a twisted tree root shaped like a reaching arm",
        ),
        environments=(
            "abandoned Victorian asylum corridor with peeling wallpaper",
            "moonlit cornfield with rows closing in",
            "suburban basement with one bare swinging bulb",
            "fog-drowned New England lighthouse stairs",
            "ritual circle drawn in salt in a barn",
            "overgrown cemetery with sinking headstones",
            "1970s suburban kitchen at 3 AM",
            "sewer tunnel with ankle-deep black water",
            "attic stuffed with wax figures and cobwebs",
            "forest cabin with boards nailed over windows",
            "hotel hallway that repeats infinitely",
            "chapel nave with shattered stained glass",
        ),
        lighting=(
            "single bare bulb chiaroscuro with deep black falloff",
            "cold moonlight with sickly green fill",
            "flickering candlelight with jumping shadows",
            "flashlight cone cutting through particulate haze",
            "red emergency lamp pulsing in darkness",
            "lightning strobe freezing rain mid-air",
            "TV static glow as sole key on a face",
            "backlit doorway silhouette with no visible source",
            "underlight from floor grate casting upward shadows",
            "practical lantern swaying on a hook",
            "high-contrast noir venetian-blind shadows",
            "sodium vapor sickly amber in fog",
        ),
        atmospheres=(
            "film grain, high-ISO noise and crushed blacks",
            "smoke wisps, tense thriller atmosphere",
            "lens distortion at edges, surreal unease",
            "rain streaks on lens, melancholic mood",
            "chromatic aberration, retro VHS nostalgia",
            "volumetric fog, cinematic ultra-realism",
            "double-exposure ghosting, ethereal memory",
            "snow flurries, fairy-tale wonder turned uncanny",
            "particle dust, epic blockbuster scale",
            "dreamy bokeh, shallow depth of field",
            "heat shimmer, documentary vérité",
            "anamorphic oval bokeh, prestige drama",
        ),
    ),
    "Romance & Drama": OptionPack(
        shots=(
            "Soft shoulder-level two-shot drifting around",
            "Slow push-in on faces inches apart",
            "Handheld intimate close-up on",
            "Golden-hour silhouette wide of",
            "Over-the-shoulder conversation framing",
            "Crane pulling back from embrace revealing",
            "Shallow-focus walk-and-talk alongside",
            "Reflection in rain-streaked window of",
            "Steadicam circling a slow dance between",
            "Macro on intertwined hands with",
            "Static tableau framing",
            "Gentle pan following",
        ),
        subjects=(
            "two lovers sharing an umbrella in drizzle",
            "a violinist performing on a fire escape",
            "a letter being opened with trembling hands",
            "a couple aging across a park bench montage",
            "a dancer in rehearsal tights at the barre",
            "a chef plating dessert for a blind date",
            "a soldier returning to a porch light embrace",
            "a painter studying their muse by north light",
            "a widow clutching a worn wedding album",
            "a teen stealing a first kiss at a carnival",
            "a pianist and cellist in duet eye contact",
            "a florist arranging peonies before opening",
        ),
        environments=(
            "Parisian café terrace at blue hour with bistro lights",
            "rain-soaked bus stop with blurred headlight bokeh",
            "sunlit wheat field with wind ripples",
            "empty theatre stage with single ghost light",
            "coastal cliff path with wildflowers",
            "snowy Central Park bridge with fairy lights",
            "Rome apartment balcony with laundry lines",
            "vintage train compartment with passing landscape blur",
            "greenhouse filled with orchids and mist",
            "rooftop garden overlooking a soft city glow",
            "bookshop aisle between towering shelves",
            "harbor promenade with gentle wave lap",
        ),
        lighting=(
            "warm golden-hour rim lighting with soft skin falloff",
            "candlelit warmth with deep amber tones",
            "soft Rembrandt key light with deep shadows",
            "diffused overcast skylight, flattering and even",
            "practical string lights as bokeh key",
            "window light with lace curtain pattern",
            "sunset bounce off water as fill",
            "single spotlight pool on dancers",
            "fireplace flicker with orange bounce",
            "moonlight silver kiss on hair edges",
            "motivated café practicals with warm gel",
            "backlit silhouette with gentle flare",
        ),
        atmospheres=(
            "dreamy bokeh, shallow depth of field",
            "anamorphic oval bokeh, prestige drama",
            "film grain, Kodak Vision3 500T aesthetic",
            "lens breathing, indie arthouse intimacy",
            "clean clinical sharpness, commercial polish",
            "snow flurries, fairy-tale wonder",
            "volumetric fog, cinematic ultra-realism",
            "double-exposure ghosting, ethereal memory",
            "rain streaks on lens, melancholic mood",
            "particle dust, epic blockbuster scale",
            "motion blur trails, kinetic energy",
            "heat shimmer, documentary vérité",
        ),
    ),
    "Action & Thriller": OptionPack(
        shots=(
            "Low-angle tracking shot, tracking",
            "Handheld chase cam sprinting after",
            "Whip-pan transition into close-up of",
            "Snorricam body-mounted shot of",
            "High-speed vehicle mount alongside",
            "Crash-zoom into eyes of",
            "Steadicam burst through doorway behind",
            "Aerial pursuit drone over",
            "Slow-motion impact orbit around",
            "Dutch-angle steadicam shot, circling",
            "Over-the-shoulder aim-down-sights on",
            "Jib drop into chaos revealing",
        ),
        subjects=(
            "a tactical operative breaching with suppressed rifle",
            "a parkour runner vaulting a market stall",
            "a Formula 1 car at full throttle",
            "a helicopter rescue winch operator",
            "a motorcycle courier clipping side mirrors",
            "a spy exchanging a briefcase on a moving train",
            "a boxer snapping a combination in the ring",
            "an avalanche survivor sprinting from a collapsing ridge",
            "a speedboat captain cutting through chop",
            "a bomb tech in EOD suit approaching a device",
            "a riot shield line advancing through smoke",
            "a wingsuit flyer clearing a cliff gap",
        ),
        environments=(
            "multi-lane highway chase with overturned trucks",
            "industrial dockyard with shipping containers",
            "glass atrium lobby with shattering skylight",
            "mountain switchback road with guardrail scrape sparks",
            "subway tunnel with arriving headlight glare",
            "rooftop helipad in crosswind and rotor wash",
            "rain-soaked noir city rooftop",
            "abandoned factory with chain hoists swinging",
            "airport tarmac with spinning beacon lights",
            "casino floor erupting into panic scatter",
            "jungle river crossing on a fraying rope bridge",
            "skyscraper construction crane walkway",
        ),
        lighting=(
            "strobing club lights with haze",
            "harsh overhead fluorescent practicals",
            "intense anamorphic lens flare from explosions",
            "firelight flicker with orange bounce",
            "red and blue police light alternation",
            "headlight streaks with motion blur",
            "muzzle flash strobe freezing particles",
            "LED panel matrix with specular highlights",
            "lightning strobe freezing rain mid-air",
            "backlit silhouette with blown highlights",
            "cool moonlight with silver fill",
            "warm golden-hour rim lighting",
        ),
        atmospheres=(
            "motion blur trails, kinetic energy",
            "particle dust, epic blockbuster scale",
            "smoke wisps, tense thriller atmosphere",
            "rain streaks on lens, melancholic mood",
            "heat shimmer, documentary vérité",
            "volumetric fog, cinematic ultra-realism",
            "film grain, Kodak Vision3 500T aesthetic",
            "clean clinical sharpness, commercial polish",
            "lens breathing, indie arthouse intimacy",
            "chromatic aberration, retro VHS nostalgia",
            "anamorphic oval bokeh, prestige drama",
            "double-exposure ghosting, ethereal memory",
        ),
    ),
    "Fantasy & Mythic": OptionPack(
        shots=(
            "Crane rising through clouds to reveal",
            "Slow orbit around floating",
            "Wide establishing aerial shot, orbiting",
            "Low-angle hero push-in on",
            "Steadicam through torch-lit corridor toward",
            "Macro on rune-glow engraving on",
            "Underwater bubble-rise reveal of",
            "Silhouette against enormous moon framing",
            "Whip-pan from dragon shadow to",
            "Top-down God's-eye view of battle map with",
            "Dolly alongside galloping",
            "Rack-focus from fairy lights to",
        ),
        subjects=(
            "a silver-armored knight on an armored warhorse",
            "an elven archer with glowing arrow nock",
            "a dragon coiled on a hoard of obsidian coins",
            "a witch stirring a cauldron of emerald vapor",
            "a golem of moss-covered stone awakening",
            "a phoenix erupting from ash in mid-flight",
            "a mermaid breaching through a moonlit swell",
            "a wizard with constellation-threaded robes",
            "a faun leading children through an enchanted glade",
            "a giant with birch-bark skin crossing a fjord",
            "a cursed prince with thorned antlers",
            "a floating castle chain anchored to a cliff",
        ),
        environments=(
            "misty bamboo forest at dawn with spirit lanterns",
            "volcanic black-sand beach at golden hour",
            "bioluminescent cave with stalactites",
            "floating islands chained over a waterfall abyss",
            "ancient library with scrolls orbiting on magic",
            "battlefield after rain with broken banners",
            "enchanted village market with pixie vendors",
            "crystal desert under twin moons",
            "underwater coral reef cathedral",
            "thorn maze with walls taller than towers",
            "cloud sea viewed from a sky temple terrace",
            "frozen lake reflecting aurora and castle spires",
        ),
        lighting=(
            "cool moonlight with silver fill",
            "firelight flicker with orange bounce",
            "bioluminescent practical glow as key",
            "lightning strobe freezing rain mid-air",
            "candlelit warmth with deep amber tones",
            "god-ray sun shafts through canopy gaps",
            "magic rune pulse as motivated color rim",
            "aurora wash with shifting green-magenta",
            "torch wall rhythm with dancing shadows",
            "soft Rembrandt key light with deep shadows",
            "backlit silhouette with blown highlights",
            "warm golden-hour rim lighting",
        ),
        atmospheres=(
            "snow flurries, fairy-tale wonder",
            "volumetric fog, cinematic ultra-realism",
            "particle dust, epic blockbuster scale",
            "dreamy bokeh, shallow depth of field",
            "double-exposure ghosting, ethereal memory",
            "film grain, Kodak Vision3 500T aesthetic",
            "anamorphic oval bokeh, prestige drama",
            "lens distortion at edges, surreal unease",
            "chromatic aberration, retro VHS nostalgia",
            "clean clinical sharpness, commercial polish",
            "rain streaks on lens, melancholic mood",
            "heat shimmer, documentary vérité",
        ),
    ),
    "Noir & Crime": OptionPack(
        shots=(
            "High-angle crane shot, descending on",
            "Static locked-off medium shot of",
            "Over-the-shoulder handheld shot, following",
            "Low-angle tracking shot, tracking",
            "Smoke-wreathed silhouette frame of",
            "Venetian blind shadow stripe across",
            "Slow dolly past interrogation lamp toward",
            "Rain-streaked window reflection shot of",
            "Footstep POV approaching",
            "Mirror split showing two faces of",
            "Wide street lamp pool isolating",
            "Close-up on ticking pocket watch near",
        ),
        subjects=(
            "a fedora detective lighting a match",
            "a femme fatale in satin gloves and cigarette smoke",
            "a trench-coated informant under a streetlamp",
            "a getaway driver gripping a thin steering wheel",
            "a corrupt politician shredding documents",
            "a jazz singer at a mic in a basement club",
            "a body outline chalked on wet pavement",
            "a safecracker listening with a stethoscope",
            "a newsboy selling late editions with scandal headline",
            "a double-crossing partner sliding a envelope",
            "a snitch glancing over shoulder in a diner booth",
            "a hitman assembling a silencer at a desk",
        ),
        environments=(
            "rain-soaked noir city rooftop",
            "smoke-filled private detective office with blinds",
            "1940s train station platform under steam",
            "underground speakeasy behind a bookcase door",
            "pier warehouse with swinging bare bulbs",
            "foggy dock with moored fishing boats",
            "interrogation room with one hanging lamp",
            "neon motel sign buzzing in the rain",
            "city hall marble steps at night",
            "parking garage echo with footsteps",
            "river barge casino with card tables",
            "alley dumpster fire casting orange flicker",
        ),
        lighting=(
            "high-contrast noir venetian-blind shadows",
            "single bare bulb chiaroscuro",
            "neon magenta and cyan cross-lighting",
            "backlit silhouette with blown highlights",
            "motivated window light with dust motes",
            "harsh overhead fluorescent practicals",
            "cigarette ember as tiny warm key",
            "streetlamp pool with hard falloff",
            "cool moonlight with silver fill",
            "practical desk lamp cone on evidence photos",
            "intense anamorphic lens flare",
            "sodium vapor sickly amber in fog",
        ),
        atmospheres=(
            "smoke wisps, tense thriller atmosphere",
            "rain streaks on lens, melancholic mood",
            "film grain, Kodak Vision3 500T aesthetic",
            "high-contrast noir venetian-blind shadows",
            "volumetric fog, cinematic ultra-realism",
            "chromatic aberration, retro VHS nostalgia",
            "anamorphic oval bokeh, prestige drama",
            "lens breathing, indie arthouse intimacy",
            "double-exposure ghosting, ethereal memory",
            "particle dust, epic blockbuster scale",
            "dreamy bokeh, shallow depth of field",
            "heat shimmer, documentary vérité",
        ),
    ),
    "Documentary & Realism": OptionPack(
        shots=(
            "Handheld observational follow of",
            "Shoulder-mounted vérité pan across",
            "Long lens compressed telephoto of",
            "Establishing wide holding on",
            "Interview frame medium close on",
            "B-roll insert detail of",
            "Time-lapse locked tripod on",
            "Drone ascending reveal of landscape behind",
            "Walk-and-talk through crowd toward",
            "Split-diopter focus on foreground and",
            "Slow zoom from crowd to individual",
            "Static surveillance-style angle on",
        ),
        subjects=(
            "a street food vendor flipping noodles",
            "a protestor holding a handmade sign",
            "a farmer inspecting drought-cracked soil",
            "a surgeon scrubbing in under harsh lamps",
            "a child releasing a sky lantern at dusk",
            "a fisherman mending nets at dawn",
            "a factory worker at an assembly line",
            "a refugee family at a border crossing",
            "a scientist labeling samples in a field lab",
            "an elder teaching traditional weaving",
            "a firefighter resting after a call",
            "a musician busking in a subway",
        ),
        environments=(
            "sun-baked Moroccan medina marketplace",
            "Tokyo Shibuya crossing at rush hour",
            "frozen Arctic tundra under aurora",
            "dusty Wild West ghost town main street",
            "Victorian greenhouse overrun with vines",
            "Saharan dunes at blue hour",
            "favela hillside stairs with laundry lines",
            "hospital corridor with gurney rush",
            "rice terrace flooded mirror at sunrise",
            "shipping port crane yard at shift change",
            "community kitchen during meal prep",
            "climate march filling a boulevard",
        ),
        lighting=(
            "diffused overcast skylight",
            "natural available light only, no artificial fill",
            "harsh midday sun with hard shadows",
            "practical fluorescent in institutional space",
            "golden-hour warm side light, honest skin texture",
            "window light with lace curtain pattern",
            "headlamp cone in pre-dawn fieldwork",
            "campfire circle warmth on faces",
            "overcast soft box effect on ocean spray",
            "street sodium mix with storefront LEDs",
            "bounce card fill simulating news interview",
            "heat shimmer, documentary vérité",
        ),
        atmospheres=(
            "heat shimmer, documentary vérité",
            "film grain, Kodak Vision3 500T aesthetic",
            "clean clinical sharpness, commercial polish",
            "lens breathing, indie arthouse intimacy",
            "motion blur trails, kinetic energy",
            "particle dust, epic blockbuster scale",
            "rain streaks on lens, melancholic mood",
            "snow flurries, fairy-tale wonder",
            "volumetric fog, cinematic ultra-realism",
            "chromatic aberration, retro VHS nostalgia",
            "smoke wisps, tense thriller atmosphere",
            "anamorphic oval bokeh, prestige drama",
        ),
    ),
    "Comedy & Satire": OptionPack(
        shots=(
            "Wide static frame holding on awkward pause around",
            "Quick zoom snap into surprised face of",
            "Low-angle making hero look pompous on",
            "Split-screen symmetry gag framing",
            "Overhead tabletop chaos circling",
            "Whip-pan missing the punchline landing on",
            "Steadicam pratfall follow of",
            "Fish-eye exaggerated perspective on",
            "Mockumentary interview zoom on",
            "Slow-motion failed stunt replay of",
            "Reaction shot cutaway close on",
            "Center-framed deadpan portrait of",
        ),
        subjects=(
            "a groom tangled in a runaway helium balloon arch",
            "an office worker covered in Post-it notes",
            "a dog wearing sunglasses driving a tiny car prop",
            "an influencer failing a viral dance challenge",
            "a medieval knight stuck in a revolving door",
            "a chef with exploding soufflé splatter",
            "a superhero in ill-fitting homemade costume",
            "a politician with toilet paper on shoe",
            "a yoga class participant collapsing tree pose",
            "a robot butler spilling tray of champagne",
            "a toddler in a CEO blazer at a board table",
            "a mime trapped in a real glass door",
        ),
        environments=(
            "bright suburban living room with sitcom lighting",
            "open-plan office with birthday cake disaster",
            "wedding reception dance floor mishap zone",
            "supermarket aisle with toppled pyramid display",
            "theme park queue under cartoon mascots",
            "sitcom apartment with unmistakable couch center",
            "courtroom with surprised jury reactions",
            "gym locker room steam and slapstick",
            "food truck festival with sauce splatter",
            "elevator stuck between floors",
            "green screen studio visible by accident",
            "pool party with synchronized flop entry",
        ),
        lighting=(
            "high-key even sitcom lighting, minimal shadows",
            "bright commercial softbox, saturated colors",
            "ring light beauty harsh on pores for parody",
            "practical party string lights, cheerful",
            "flat overhead office panels, sterile",
            "warm golden-hour rim lighting",
            "strobing club lights with haze",
            "flash photography paparazzi strobe",
            "neon magenta and cyan cross-lighting",
            "diffused overcast skylight",
            "LED panel matrix with specular highlights",
            "motivated window light with dust motes",
        ),
        atmospheres=(
            "clean clinical sharpness, commercial polish",
            "chromatic aberration, retro VHS nostalgia",
            "motion blur trails, kinetic energy",
            "film grain, Kodak Vision3 500T aesthetic",
            "lens breathing, indie arthouse intimacy",
            "particle dust, epic blockbuster scale",
            "dreamy bokeh, shallow depth of field",
            "snow flurries, fairy-tale wonder",
            "rain streaks on lens, melancholic mood",
            "smoke wisps, tense thriller atmosphere",
            "volumetric fog, cinematic ultra-realism",
            "heat shimmer, documentary vérité",
        ),
    ),
    "Historical & Period": OptionPack(
        shots=(
            "Steadicam through candlelit corridor toward",
            "Crane over ballroom revealing",
            "Locked tableau reminiscent of oil painting of",
            "Horse-mounted lateral tracking alongside",
            "Slow push-in on letter seal held by",
            "Wide battlefield smoke reveal of",
            "Handheld period appropriate jitter on",
            "Top-down God's-eye view of feast table with",
            "Silhouette in doorway against courtyard sun",
            "Macro on quill ink pooling beside",
            "Pan across war tent map strategy figures",
            "Dolly past period extras blurring foreground",
        ),
        subjects=(
            "a samurai in lacquered armor kneeling before dawn",
            "a Victorian lady adjusting corset lace in mirror",
            "a Roman legionary in bronze galea formation",
            "a flapper dancing Charleston under fringe",
            "a plague doctor with beaked mask in empty square",
            "a cowboy spinning revolver cylinder at high noon",
            "a WWI soldier reading a creased letter in trench",
            "a pharaoh procession bearers with gold mask",
            "a Renaissance painter mixing lapis pigment",
            "a pirate captain on crow's nest through spyglass",
            "a 1920s aviator in leather cap and goggles",
            "a court composer conducting a candle orchestra",
        ),
        environments=(
            "misty bamboo forest at dawn",
            "abandoned Art Deco ballroom",
            "sun-baked Moroccan medina marketplace",
            "dusty Wild West ghost town main street",
            "Victorian greenhouse overrun with vines",
            "castle great hall with roaring hearth",
            "trench maze with barbed wire silhouettes",
            "galleon deck with creaking rigging",
            "coliseum sand arena with distant crowd murmur",
            "colonial tea parlor with porcelain clink",
            "silk road caravan halt at oasis",
            "revolution barricade cobblestone street",
        ),
        lighting=(
            "candlelit warmth with deep amber tones",
            "firelight flicker with orange bounce",
            "soft Rembrandt key light with deep shadows",
            "diffused overcast skylight",
            "warm golden-hour rim lighting",
            "torch wall rhythm with dancing shadows",
            "window light with lace curtain pattern",
            "cool moonlight with silver fill",
            "practical oil lamp halo",
            "harsh midday sun with hard shadows",
            "motivated window light with dust motes",
            "high-contrast noir venetian-blind shadows",
        ),
        atmospheres=(
            "film grain, Kodak Vision3 500T aesthetic",
            "particle dust, epic blockbuster scale",
            "volumetric fog, cinematic ultra-realism",
            "smoke wisps, tense thriller atmosphere",
            "snow flurries, fairy-tale wonder",
            "rain streaks on lens, melancholic mood",
            "anamorphic oval bokeh, prestige drama",
            "dreamy bokeh, shallow depth of field",
            "heat shimmer, documentary vérité",
            "lens breathing, indie arthouse intimacy",
            "double-exposure ghosting, ethereal memory",
            "clean clinical sharpness, commercial polish",
        ),
    ),
    "Anime & Stylized": OptionPack(
        shots=(
            "Speed-line impact frame on",
            "Dramatic low-angle hero pose hold on",
            "Sakura petal parallax drift past",
            "Split-screen dual-wield stance of",
            "Orbital magical circle activation around",
            "Impact freeze-frame with kanji title card vibe on",
            "Whiplash motion smear trailing",
            "School rooftop wind gust wide on",
            "Eye glint extreme close-up of",
            "Transformation sequence light pillar engulfing",
            "Chibi-scale gag zoom on",
            "Mecha cockpit HUD overlay tracking",
        ),
        subjects=(
            "a spiky-haired duelist charging aura energy",
            "a magical girl mid-ribbon transformation",
            "a mecha pilot gripping throttle with alert HUD",
            "a student with toast in mouth running late",
            "a fox spirit with floating sakura orbs",
            "a cyborg samurai with katana plasma edge",
            "an idol singer on stadium stage with light sticks sea",
            "an isekai hero with oversized sword and cloak",
            "a villain monologuing on throne with cape billow",
            "a catgirl barista with bell collar charm",
            "a sports captain mid-impossible spike leap",
            "an alchemist drawing transmutation circle glow",
        ),
        environments=(
            "Tokyo school rooftop at sunset with city sprawl",
            "neon arcade street with pachinko glare",
            "floating dungeon gate in a crystal cavern",
            "shrine steps with torii and fox statues",
            "space colony colony interior with kanji warnings",
            "training dojo with wooden floor squeak",
            "festival night with yukata crowd and stalls",
            "mecha hangar with spotlights and fuel mist",
            "cherry blossom riverbank picnic spread",
            "digital glitch world with wireframe horizon",
            "volcanic black-sand beach at golden hour stylized",
            "cloud kingdom with impossible architecture",
        ),
        lighting=(
            "cel-shaded rim with flat fill, bold outlines implied",
            "neon magenta and cyan cross-lighting",
            "anime sunset gradient sky wash",
            "magic circle motivated bloom overexposure",
            "lightning strobe freezing rain mid-air stylized",
            "sparkle highlight starburst on eyes",
            "RGB rim light tracing body contours",
            "backlit silhouette with blown highlights",
            "soft Rembrandt key light with deep shadows",
            "strobing club lights with haze",
            "warm golden-hour rim lighting",
            "practical lantern swaying on a hook",
        ),
        atmospheres=(
            "chromatic aberration, retro VHS nostalgia",
            "motion blur trails, kinetic energy",
            "particle dust, epic blockbuster scale",
            "dreamy bokeh, shallow depth of field",
            "snow flurries, fairy-tale wonder",
            "volumetric fog, cinematic ultra-realism",
            "lens distortion at edges, surreal unease",
            "double-exposure ghosting, ethereal memory",
            "clean clinical sharpness, commercial polish",
            "film grain, Kodak Vision3 500T aesthetic",
            "rain streaks on lens, melancholic mood",
            "anamorphic oval bokeh, prestige drama",
        ),
    ),
    "Nature & Landscape": OptionPack(
        shots=(
            "Drone glide low over",
            "Wide locked landscape revealing",
            "Macro rack-focus blooming across",
            "Time-lapse accelerated sky above",
            "Slow crane rising above",
            "Ground-level parallax drift past",
            "Aerial wide orbit around",
            "Handheld wading through",
            "Long lens compressed telephoto of",
            "Ultra-wide horizon encompassing",
            "Underwater upward tilt toward surface beside",
            "Extreme close-up dewdrop refracting",
        ),
        subjects=(
            "a cherry blossom canopy in peak bloom shedding pink petals",
            "a lavender field stretching to the horizon in rolling purple waves",
            "a snow-capped mountain peak rising above a sea of clouds",
            "a cascading waterfall plunging into a turquoise pool",
            "a coral reef teeming with tropical fish in crystal water",
            "a desert sand dune field at golden hour with long blue shadows",
            "a northern lights aurora rippling across a frozen mirror lake",
            "a sunflower meadow turning to face the rising sun",
            "a mangrove forest with mirror-still water reflections",
            "a volcanic crater emitting sulfurous plumes with lava glow",
            "a giant sequoia canopy filtering emerald cathedral light",
            "a Dutch tulip field in diagonal rows with windmill on horizon",
        ),
        environments=(
            "Alpine meadow with wildflowers and distant snow peaks",
            "Maldivian overwater bungalow turquoise lagoon at sunrise",
            "Amazon rainforest canopy shrouded in morning mist",
            "Norwegian fjord with mirror-still water and ribbon waterfalls",
            "Saharan dune sea at blue hour with crescent moon rising",
            "Japanese cherry blossom park path in full hanami bloom",
            "Provençal lavender field rows at golden hour",
            "Icelandic black sand beach with crashing Atlantic waves",
            "Himalayan ridge trail above cloud line at sunrise",
            "Great Barrier Reef coral garden bathed in ambient blue light",
            "Scottish Highlands heather moor under dramatic cloud sky",
            "Patagonian glacier calving into a turquoise fjord lake",
        ),
        lighting=(
            "warm golden-hour rim lighting with long landscape shadows",
            "blue-hour ambient dusk with last light touching peaks",
            "diffused overcast soft skylight, even and serene",
            "high noon hard sun casting graphic nature shadows",
            "God-ray sun shaft breaking through storm cloud",
            "underwater caustic light rippling on coral and sand",
            "backlit translucent petals with direct sun rim halo",
            "aurora borealis ambient green-magenta colour wash",
            "magic-hour warm side light sculpting mountain face",
            "misty morning low-angle rake across dew and grass",
            "moonlit silver on ocean wave crests in darkness",
            "macro ring-light on dewdrop refracting full landscape",
        ),
        atmospheres=(
            "nature documentary vérité, BBC Planet Earth cinematic",
            "anamorphic oval bokeh, prestige drama",
            "volumetric fog, cinematic ultra-realism",
            "macro dreamscape, shallow depth of field wonder",
            "time-lapse motion blur, epic blockbuster scale",
            "heat shimmer above desert sand, documentary vérité",
            "rain streaks on lens, melancholic mood",
            "snow flurries, fairy-tale wonder",
            "pollen particle dust, cinematic golden haze",
            "film grain, Kodak Vision3 500T aesthetic",
            "clean crisp sharpness, premium nature photography",
            "double-exposure ghosting, ethereal memory",
        ),
    ),
    "Racing & Motorsport": OptionPack(
        shots=(
            "Low-angle tracking shot, tracking",
            "High-speed vehicle mount alongside",
            "Overhead drone shot circling",
            "Pit lane dolly following",
            "Crash-zoom into cockpit of",
            "Bump-cam wheel-mounted alongside",
            "Helicopter aerial pursuit of",
            "Slow-motion impact orbit around",
            "Over-the-barrier wide static holding on",
            "FPV drone threading through pack of",
            "Steadicam grid walk revealing",
            "Snorricam body-mounted behind driver in",
        ),
        subjects=(
            "a Formula 1 car at full throttle exiting a hairpin",
            "a MotoGP rider knee-down through a sweeping bend",
            "a rally car cresting a dirt jump in a rooster-tail dust plume",
            "a drag racer launching with tire smoke billowing at the line",
            "a Le Mans prototype banking through a night chicane",
            "a speedboat hydroplaning through a tight buoy slalom",
            "a NASCAR pack drafting three-wide at a superspeedway",
            "a mountain stage cyclist sprinting over a col summit",
            "a pit crew executing a four-tire change in under three seconds",
            "a drifting car sliding sideways in a controlled smoke arc",
            "a Bonneville salt flat land speed record attempt at dawn",
            "a go-kart pack scrambling into the first corner under braking",
        ),
        environments=(
            "Monaco Grand Prix street circuit at golden hour with yacht harbor",
            "Nürburgring Nordschleife forest section in wet overcast conditions",
            "Dakar Rally open desert stage with sand rooster tails",
            "Le Mans 24 Hours Circuit de la Sarthe at 2 AM under floodlights",
            "Pikes Peak hillclimb mountain road above cloud line",
            "Bonneville salt flats at sunrise with heat shimmer horizon",
            "WRC stage road through foggy Scottish forest hairpins",
            "Monza circuit banking through the famous Lesmo curves",
            "Macau street circuit through the Lisboa bend concrete walls",
            "NHRA drag strip under Christmas tree starting lights at night",
            "Isle of Man TT mountain section with stone walls at speed",
            "offshore powerboat race with Atlantic chop and spray",
        ),
        lighting=(
            "intense anamorphic lens flare from opposing headlights",
            "golden-hour rim light catching dust clouds and debris",
            "night circuit floodlights with motion blur streaks",
            "backlit silhouette with tire smoke haloed in setting sun",
            "wet track reflections of circuit lights in rain",
            "camera flash strobe on drag race launch",
            "hard midday overhead casting driver shadow in cockpit",
            "dusk pink sky over start-finish straight",
            "LED pit-lane panel wash with specular highlights on bodywork",
            "strobing pit crew pneumatic gun flash and sparks",
            "headlamp cone cutting forest darkness on night rally stage",
            "warm sunset rim on chrome exhaust and carbon fiber",
        ),
        atmospheres=(
            "motion blur trails, kinetic energy, motorsport broadcast",
            "particle dust and gravel, epic blockbuster scale",
            "heat shimmer above hot asphalt, documentary vérité",
            "anamorphic oval bokeh, prestige motorsport drama",
            "slow-motion hydrocarbon haze, cinematic ultra-realism",
            "rain streaks on lens, wet race tension",
            "chromatic aberration, retro onboard footage nostalgia",
            "film grain, Kodak Vision3 500T vintage race aesthetic",
            "clean clinical sharpness, premium broadcast polish",
            "tire smoke volumetric haze, cinematic ultra-realism",
            "lens flare starburst on wet bodywork, prestige drama",
            "sharp HDR clarity, modern motorsport production",
        ),
    ),
    "Aviation & Aerial": OptionPack(
        shots=(
            "Cockpit POV pushing through cloud layer toward",
            "Aerial wide orbit around",
            "Wingtip-mounted camera tracking alongside",
            "Drone ascending vertically revealing",
            "Chase plane formation alongside",
            "Low-pass ground-level up-tilt tracking",
            "Long lens telephoto ground-to-air tracking of",
            "Free-fall body-mounted POV on",
            "Slow crane lifting off into sky revealing",
            "Gyro-stabilized aerial telephoto on",
            "Hot air balloon basket wide establishing shot of",
            "Extreme wide altitude hold above",
        ),
        subjects=(
            "a fighter jet pulling a vertical climb trailing a white contrail",
            "a wingsuit pilot threading a narrow mountain ridge gap at speed",
            "a hot air balloon drifting over Cappadocia fairy chimneys at sunrise",
            "a paraglider soaring on a thermal above coastal chalk cliffs",
            "a formation of aerobatic jets trailing colored smoke arcs",
            "a vintage biplane looping over patchwork English countryside",
            "a base jumper launching from a sheer vertical granite face",
            "a commercial airliner breaking through cloud layer into clear blue",
            "a hang glider riding ridge lift above ocean",
            "a skydiver in free fall over patchwork farmland below",
            "a seaplane banking over a tropical island atoll",
            "a helicopter banking hard over urban skyline at dusk",
        ),
        environments=(
            "Cappadocia valley at sunrise with balloon fleet ascending",
            "Swiss Alps above cloud inversion with summit islands",
            "Scottish Highland glen below at low-altitude pass",
            "New Zealand South Island glaciers viewed from aerial",
            "Venetian lagoon from low-altitude seaplane at blue hour",
            "Arizona canyon system with river glinting far below",
            "Norwegian fjord flyover at dawn with mist in valleys",
            "open ocean at altitude with cloud shadow patterns below",
            "Namib desert red dunes aerial abstract at golden hour",
            "urban cityscape at night from helicopter door",
            "Arctic ice field from altitude with crevasse patterns",
            "tropical atoll from above with coral reef visible in water",
        ),
        lighting=(
            "above-cloud sunrise with underlit cumulus and pink sky",
            "God-ray sun shafts breaking through cloud layer",
            "cockpit instrument amber glow as soft interior key",
            "golden-hour rim on aircraft fuselage and contrail",
            "backlit cloud formations with silver edge-lighting",
            "storm cell lightning illuminating cloud interior",
            "moonlit night flight with instrument panel amber fill",
            "low sun raking light across mountain range from above",
            "atmospheric haze diffusing horizon to pale gold",
            "blue-hour high altitude with deep indigo sky gradient",
            "wing shadow casting dramatic pattern on ground below",
            "early morning under-cloud diffusion, even and pale",
        ),
        atmospheres=(
            "anamorphic oval bokeh, prestige aerial drama",
            "volumetric cloud layers, cinematic ultra-realism",
            "clean crisp above-cloud sharpness, premium aerial photography",
            "contrail motion blur, epic blockbuster scale",
            "lens breathing, indie arthouse aerial intimacy",
            "snow flurries at altitude, alpine wonder",
            "heat shimmer, high-altitude documentary vérité",
            "ice crystal particle haze, epic blockbuster scale",
            "film grain, Kodak Vision3 500T vintage aviation aesthetic",
            "double-exposure sky layering, ethereal memory",
            "rain on cockpit canopy, cinematic tension",
            "sharp HDR sky clarity, premium aerial broadcast",
        ),
    ),
}

# --- Theme overlays (prepended when selected) -----------------------------

THEME_OVERLAYS: dict[str, dict[str, tuple[str, ...]]] = {
    "Dystopian Future": {
        "subjects": (
            "a ration-line citizen with barcode tattoo",
            "a surveillance drone operator in opaque visor",
        ),
        "environments": (
            "concrete hab-block interior with propaganda screens",
            "acid rain plaza under a collapsed megastructure",
        ),
        "atmospheres": ("smoke wisps, tense thriller atmosphere",),
    },
    "Forbidden Love": {
        "subjects": (
            "two rivals from opposing houses sharing a secret glance",
            "a monarch and a commoner hands almost touching",
        ),
        "environments": (
            "moonlit garden maze with forbidden footsteps",
            "rain-soaked alley where they must not be seen together",
        ),
        "lighting": ("candlelit warmth with deep amber tones",),
    },
    "Revenge Arc": {
        "shots": ("Slow push-in on clenched jaw of", "Low-angle hero rise of"),
        "subjects": ("a burned survivor tightening leather gloves",),
        "atmospheres": ("smoke wisps, tense thriller atmosphere",),
    },
    "Survival / Last Stand": {
        "environments": (
            "collapsed bridge last barricade at dusk",
            "blizzard ridge with a single intact shelter",
        ),
        "atmospheres": ("particle dust, epic blockbuster scale",),
    },
    "Coming of Age": {
        "subjects": (
            "a graduate tossing cap into wind",
            "a teen on a bicycle leaving small-town main street",
        ),
        "environments": ("suburban driveway with packed boxes",),
    },
    "Heist & Betrayal": {
        "shots": ("Top-down God's-eye view of vault blueprint table with",),
        "subjects": ("a vault team in matching suits swapping an envelope",),
        "environments": ("laser-grid museum gallery at midnight",),
    },
    "Cosmic Wonder": {
        "environments": (
            "nebula nursery visible through observatory dome",
            "ringed planet rising over a silent moon surface",
        ),
        "atmospheres": ("double-exposure ghosting, ethereal memory",),
    },
    "Urban Isolation": {
        "environments": (
            "empty metro car at last train hour",
            "high-rise window reflecting lonely city glow",
        ),
        "atmospheres": ("rain streaks on lens, melancholic mood",),
    },
    "War & Sacrifice": {
        "subjects": ("a medic dragging a wounded soldier through mud",),
        "environments": ("no-man's-land crater field under flares",),
        "lighting": ("firelight flicker with orange bounce",),
    },
    "Surreal Dreamscape": {
        "shots": ("Dutch-angle steadicam shot, circling",),
        "environments": (
            "impossible staircase Escher architecture",
            "clock melting over a desert dune",
        ),
        "atmospheres": ("lens distortion at edges, surreal unease",),
    },
    "Celebration & Joy": {
        "environments": (
            "confetti canyon street parade route",
            "festival main stage with pyrotechnic finale",
        ),
        "atmospheres": ("snow flurries, fairy-tale wonder",),
    },
    "Hunt / Pursuit": {
        "shots": (
            "Long lens compressed telephoto of",
            "Handheld chase cam sprinting after",
        ),
        "environments": ("dense forest with snapped branches trail",),
        "atmospheres": ("motion blur trails, kinetic energy",),
    },
}

# --- Mature 18+ extensions (merged only when uncensored) ------------------

MATURE_OVERLAYS: dict[str, dict[str, tuple[str, ...]]] = {
    "_global": {
        "shots": (
            "Languid shallow rack-focus caressing across",
            "Unblinking intimate close-up lingering on",
            "Slow push-in through parted curtains toward",
            "Slow trailing tilt from feet upward along bare skin",
            "Breathless extreme close-up trembling on",
            "Voyeuristic long-lens compressed gaze at",
        ),
        "lighting": (
            "sultry boudoir practicals with deep shadow falloff sculpting form",
            "a single bedside lamp with warm honeyed skin tones and soft falloff",
            "warm candlelight with soft key tracing collarbones in velvet darkness",
            "low-key chiaroscuro with bare skin half in shadow half in honey warmth",
        ),
        "atmospheres": (
            "sensual 35mm film grain, shallow depth of field, after-midnight intimacy",
            "unfiltered vérité texture, skin-close framing, prestige R-rated polish",
            "charged intimacy with subtle lens breathing and cinematic motion blur",
            "NC-17 prestige tone, raw and unflinching, arthouse intimacy",
        ),
    },
    "Sci-Fi & Cyberpunk": {
        "subjects": (
            "a cyberpunk escort in translucent smart-fabric with neon body underlighting",
            "two androids in erotic neural-link interface with cascading digital sparks",
            "a nude synthetic human awakening in a cryo-pod draped in condensation mist",
            "a biomechanical figure with exposed organic tissue glistening under circuit glow",
            "a flesh-revealing alien organism dripping with bioluminescent fluid",
        ),
        "environments": (
            "neon-lit cyberpunk brothel with holographic adult entertainment displays",
            "underground adult district with pulsing neon corridor and club haze",
            "private zero-gravity pleasure chamber with silk suspension apparatus",
        ),
        "atmospheres": (
            "neon-soaked eroticism with clinical metallic undertone, R-rated polish",
            "wet chrome and skin, forbidden synthetic desire, prestige adult sci-fi",
        ),
    },
    "Horror & Supernatural": {
        "subjects": (
            "a flesh-revealing creature glistening with wet muscle and sinew",
            "a crimson-splashed silhouette dissolving in practical blood mist",
            "a bare-shouldered survivor pressed against a blood-streaked wall",
            "a vampire feeding on a willing bare-throated victim in ecstatic close-up",
            "a succubus in sheer shadow fabric coiling hungrily around her prey",
            "a gore-drenched figure rising from visceral carnage with hollow eyes",
        ),
        "atmospheres": (
            "crushed blacks, visceral gore haze you can almost taste",
            "wet leather and copper breath, forbidden midnight appetite",
            "slick visceral horror, practical-effects blood and body horror in full detail",
        ),
    },
    "Romance & Drama": {
        "subjects": (
            "entwined lovers swaying in silk-sheet silhouette behind billowing gauze",
            "lovers locked in a fevered embrace fogging a steam-clouded bathroom mirror",
            "a woman with bare shoulders and parted lips exhaling in post-kiss candlelight",
            "fingers slowly tracing a collarbone through tangled bed sheets",
            "two bodies entwined in slow passionate motion under soft linen",
            "a nude figure emerging from a bath wreathed in golden backlight steam",
            "lovers in explicit tender embrace, prestige arthouse framing",
        ),
        "lighting": (
            "molten backlight through sheer linen with glowing skin rim",
            "golden-hour rim light with soft sweat highlights on bare shoulders",
            "low candle key with deep shadow and velvet skin falloff",
        ),
        "atmospheres": (
            "breath on glass, aching desire, prestige R-rated sensuality, shallow depth of field",
            "NC-17 prestige tone, explicit yet artistic, arthouse eroticism",
        ),
    },
    "Action & Thriller": {
        "subjects": (
            "a battered antihero dragging blood-smeared knuckles across jawline",
            "a disheveled operative peeling off a soaked tank top in rain",
            "an assassin delivering a brutal kill in graphic close-up with arterial spray",
            "a fighter with split lip and blood-soaked shirt refusing to fall",
            "a torture survivor with raw wrist abrasions struggling under harsh lamp",
        ),
        "atmospheres": (
            "practical squib mist hanging thick, R-rated impact viscerality",
            "sweat-slick adrenaline, bruised glamour, dangerous magnetism",
            "hyper-realistic R-rated violence, bone-crunch realism implied in every detail",
        ),
    },
    "Fantasy & Mythic": {
        "subjects": (
            "a nude nymph bathing in a moonlit forest pool with bioluminescent ripples",
            "a succubus queen on a throne of bones draped in sheer dark silk",
            "a deity and mortal in forbidden erotic union shrouded in divine radiance",
            "a warrior stripped bare after battle washing wounds in a forest river",
            "a siren luring sailors with bare form and hypnotic song on a moonlit rock",
        ),
        "environments": (
            "enchanted boudoir chamber with floating rose petals and sheer silk drapes",
            "ancient bathhouse temple with ritual participants wreathed in steam",
            "pleasure gardens of an immortal realm with unclothed attendants",
        ),
        "atmospheres": (
            "mythic eroticism, divine and earthly desire intertwined",
            "fantasy R-rated prestige, otherworldly sensuality and forbidden beauty",
        ),
    },
    "Noir & Crime": {
        "subjects": (
            "a femme fatale slowly rolling a silk stocking up her bare thigh in a shadowed motel",
            "a suspect sweating through a tense confession under a swaying bare bulb",
            "a femme fatale lighting a lipstick-stained cigarette beside an undone blouse",
            "a showgirl backstage in corset being unlaced by a shadowed figure",
            "a crime boss with a mistress draped languidly across his dim-lit desk",
            "a hitman with blood-soaked hands washing up in a gritty motel sink close-up",
        ),
        "lighting": (
            "smoke-wreathed key light with hard noir contrast and deep shadows",
            "venetian blind stripes slicing across bare skin in a motel room",
        ),
    },
    "Historical & Period": {
        "subjects": (
            "a Victorian courtesan reclining in sheer silk on a velvet chaise longue",
            "ancient bathhouse bathers in explicit classical fresco-style composition",
            "a geisha in half-undone kimono in a lantern-lit private chamber",
            "a Roman bathhouse intimate scene in marble steam and mosaic tiles",
            "a Renaissance nude reclining in golden light in painterly fine-art style",
            "period lovers in passionate embrace behind heavy four-poster drapes",
        ),
        "environments": (
            "Victorian brothel parlor with red velvet walls and gaslight amber glow",
            "ancient Roman bathhouse with marble columns and billowing steam",
            "Edo-period teahouse private room with paper screen shadow play",
        ),
        "atmospheres": (
            "period-authentic sensuality, classical fine-art nude realism",
            "historical R-rated prestige, painterly period eroticism",
        ),
    },
    "Anime & Stylized": {
        "subjects": (
            "an adult magical girl in torn battle outfit post-combat with heaving breath",
            "a stylized adult couple in explicit anime-aesthetic intimate moment",
            "a demon lord in sheer black silk draped across a stone throne provocatively",
            "an ecchi protagonist in comedic undress situation with exaggerated reaction",
        ),
        "environments": (
            "onsen hot springs with adult anime aesthetic and uncensored billowing steam",
            "intimate room with soft warm lamp light and disheveled futon",
        ),
        "atmospheres": (
            "adult anime aesthetic, explicit yet stylized with mature cel-shade eroticism",
            "uncensored mature anime composition, adult artistry over stylized forms",
        ),
    },
    "Documentary & Realism": {
        "subjects": (
            "a sex worker in a candid documentary close-up interview under practical light",
            "a nude life-drawing model posing for an art class in honest natural light",
            "a combat medic removing shrapnel from a conscious patient in graphic documentary detail",
            "a crime scene with realistic blood pooling and forensic marker documentation",
        ),
        "atmospheres": (
            "raw uncensored documentary realism, no editorial softening",
            "vérité adult content, unfiltered human reality in all its rawness",
        ),
    },
    "Comedy & Satire": {
        "subjects": (
            "a nudist colony member caught in an escalating slapstick wardrobe situation",
            "an adult film parody set with exaggerated props and visible boom mic mishap",
            "a strip club act going comically wrong with cascading wardrobe malfunction",
        ),
        "atmospheres": (
            "raunchy R-rated adult comedy tone, visual punchline with satirical edge",
        ),
    },
}

# --- Context-aware presets (genre → name → indices) -------------------------

CONTEXT_PRESETS: dict[str, dict[str, tuple[int, int, int, int, int]]] = {
    "Sci-Fi & Cyberpunk": {
        "Neon Alley Chase": (0, 0, 0, 0, 0),
        "Orbital Heist": (3, 6, 5, 9, 4),
    },
    "Horror & Supernatural": {
        "Asylum Walk": (0, 0, 0, 0, 0),
        "Midnight Cornfield": (4, 3, 1, 1, 2),
    },
    "Romance & Drama": {
        "Blue Hour Café": (3, 0, 0, 0, 0),
        "Train Goodbye": (7, 7, 7, 6, 3),
    },
    "Action & Thriller": {
        "Highway Pursuit": (0, 2, 0, 5, 0),
        "Rooftop Extraction": (8, 3, 6, 3, 2),
    },
    "Fantasy & Mythic": {
        "Dragon Reveal": (2, 2, 0, 6, 0),
        "Enchanted Forest": (5, 8, 0, 0, 1),
    },
    "Noir & Crime": {
        "Rain Interrogation": (6, 0, 6, 0, 0),
        "Speakeasy Deal": (2, 6, 3, 8, 1),
    },
    "Documentary & Realism": {
        "Market Morning": (1, 0, 0, 4, 0),
        "Climate March": (0, 11, 11, 0, 0),
    },
    "Comedy & Satire": {
        "Wedding Disaster": (0, 0, 1, 0, 0),
        "Office Chaos": (1, 1, 1, 1, 0),
    },
    "Historical & Period": {
        "Samurai Dawn": (0, 0, 0, 0, 0),
        "Ballroom Waltz": (1, 1, 1, 0, 3),
    },
    "Anime & Stylized": {
        "Rooftop Duel": (0, 0, 0, 1, 0),
        "Mecha Launch": (11, 2, 7, 3, 2),
    },
    "Nature & Landscape": {
        "Golden Hour Bloom": (2, 0, 5, 0, 0),
        "Arctic Aurora": (0, 6, 7, 7, 11),
    },
    "Racing & Motorsport": {
        "Monaco Lap": (0, 0, 0, 0, 0),
        "Rally Dust": (2, 2, 2, 1, 1),
    },
    "Aviation & Aerial": {
        "Balloon Dawn": (10, 2, 0, 0, 0),
        "Fighter Climb": (0, 0, 1, 3, 2),
    },
}


# ── Genre-specific clothing libraries ────────────────────────────────────────

GENRE_CLOTHING: dict[str, tuple[str, ...]] = {
    "Sci-Fi & Cyberpunk": (
        "hologram-lined trench coat with LED accent strips",
        "tactical smart-fabric bodysuit with neon piping",
        "AR visor and reflective puffer jacket",
        "chrome-paneled armored exosuit with glowing joints",
        "shredded denim with glow-mesh underlayers",
        "corporate all-black seamless suit with rank pins",
        "hacker hoodie with embedded circuitry patterns",
        "biomechanical tactical vest over thermal underlayer",
    ),
    "Horror & Supernatural": (
        "tattered Victorian nightgown",
        "long dark hooded ritual robe",
        "blood-soaked hospital gown",
        "worn leather trench coat",
        "Victorian mourning dress in black silk",
        "period undergarments disheveled and soiled",
        "nun's habit with stained hem",
        "burial shroud loosely wrapped",
    ),
    "Romance & Drama": (
        "elegant evening gown with open back",
        "casual summer dress in soft cotton",
        "sharp tailored suit with pocket square",
        "oversized knit sweater and jeans",
        "silk blouse with flowing wide-leg trousers",
        "vintage 1950s tea dress",
        "linen shirt open at the collar",
        "bridal white with simple veil",
    ),
    "Action & Thriller": (
        "tactical cargo pants and moisture-wicking shirt",
        "all-black operative gear with kevlar panels",
        "distressed leather jacket and dark jeans",
        "military BDU uniform with patches",
        "plain undercover civilian clothes",
        "wetsuit with equipment harness",
        "suit and tie with concealed holster",
        "desert camouflage with load-bearing vest",
    ),
    "Fantasy & Mythic": (
        "plate armor with embossed crest and flowing cape",
        "elven ceremonial robes with constellation embroidery",
        "barbarian furs and leather bracers",
        "silk mage robes with runic trim",
        "forest ranger cloak in earth tones",
        "royal coronation gown with jeweled bodice",
        "dark lord armor in black iron with red trim",
        "priestess ceremonial white with gold sash",
    ),
    "Noir & Crime": (
        "double-breasted pinstripe suit and fedora",
        "silk evening gown and long gloves",
        "worn detective mac coat and loosened tie",
        "1940s tea dress with seamed stockings",
        "sharp three-piece suit with pocket watch chain",
        "diner waitress uniform",
        "newsboy cap and suspenders over rolled sleeves",
        "fur stole over cocktail dress",
    ),
    "Documentary & Realism": (
        "everyday casual wear — jeans, T-shirt, trainers",
        "workwear — hi-vis vest and hard hat",
        "medical scrubs and stethoscope",
        "field researcher vest with multiple pockets",
        "school uniform",
        "traditional cultural dress",
        "athletic sportswear",
        "rough-worn clothes of a manual laborer",
    ),
    "Comedy & Satire": (
        "ill-fitting business suit two sizes too big",
        "superhero costume visibly homemade",
        "absurd matching couple outfits",
        "formal tuxedo with novelty accessories",
        "gym clothes worn inappropriately",
        "full medieval armor in a modern setting",
        "party outfit with visible wardrobe mishap",
        "mascot costume unzipped mid-torso",
    ),
    "Historical & Period": (
        "Victorian corset gown with bustle and gloves",
        "samurai mon-crested kimono and hakama",
        "Roman toga with laurel wreath",
        "1920s flapper dress with fringe and headband",
        "Regency-era pelisse coat over muslin dress",
        "medieval plate armor with heraldic surcoat",
        "pirate coat, tricorn hat, and sash",
        "WWI officer's tunic with campaign ribbons",
    ),
    "Anime & Stylized": (
        "school uniform with customized accessories",
        "magical girl outfit with ribbon and wand",
        "futuristic military uniform with anime silhouette",
        "fantasy RPG adventurer ensemble",
        "idol stage costume with light sticks motif",
        "casual streetwear with oversized hoodie",
        "demon lord robe with dramatic shoulder horns",
        "maid or butler uniform with stylized details",
    ),
    "Nature & Landscape": (
        "lightweight hiking gear and trail boots",
        "wetsuit and fins for underwater footage",
        "field naturalist vest and wide-brim hat",
        "mountaineering base layer and down jacket",
        "beachwear and bare feet in sand",
        "winter parka and snow boots",
        "yoga activewear in natural setting",
        "minimal athleisure for outdoor sport",
    ),
    "Racing & Motorsport": (
        "racing firesuit with sponsor patches and HANS device",
        "motorcycle leathers with armor inserts and full-face helmet",
        "rally co-driver suit with helmet and HANS collar",
        "pit crew uniform with team branding",
        "cycling skinsuit with aerodynamic helmet",
        "speedboat captain polo with life vest",
        "vintage Le Mans driver overalls and goggles",
        "karting helmet and rib protector over suit",
    ),
    "Aviation & Aerial": (
        "fighter pilot G-suit with helmet and oxygen mask",
        "wingsuit with helmet and altimeter rig",
        "hot air balloon pilot casual wear with radio",
        "parachute rig over athletic gear",
        "commercial pilot uniform with epaulettes",
        "vintage leather flight jacket and goggles",
        "base jumping helmet and container rig",
        "paragliding harness over outdoor layers",
    ),
    "_default": (
        "casual everyday clothing",
        "formal business attire",
        "athletic sportswear",
        "smart casual — dark jeans and blazer",
        "minimal plain white T-shirt and neutral trousers",
    ),
}

MATURE_CLOTHING_GLOBAL: tuple[str, ...] = (
    "sheer lace negligee with minimal coverage",
    "open-front shirt with bare chest",
    "bikini / swimwear with minimal coverage",
    "silk robe loosely draped open",
    "lingerie — satin and lace bra and briefs",
    "low-cut dress with deep neckline",
    "form-fitting bodycon dress",
    "topless with strategic minimal coverage",
)


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def get_clothing_options(genre: str, rating_key: str) -> list[str]:
    base = list(GENRE_CLOTHING.get(genre, GENRE_CLOTHING["_default"]))
    if rating_key == "mature":
        base = _dedupe([*list(MATURE_CLOTHING_GLOBAL), *base])
    return base


def build_character_desc(
    gender: str,
    age_range: str,
    body_type: str,
    ethnicity: str,
    skin_tone: str,
    hair_style: str,
    hair_color: str,
    eye_color: str,
    facial_features: str,
    clothing: str,
    action: str,
) -> str:
    U = "Unspecified"

    def _v(s: str) -> str:
        return s.strip() if s and s.strip() and s.strip() != U else ""

    age_word   = CHAR_AGE_WORDS.get(age_range, "")
    body       = _v(body_type)
    eth        = _v(ethnicity)
    skin       = _v(skin_tone)
    h_style    = _v(hair_style)
    h_color    = _v(hair_color)
    eye        = _v(eye_color)
    face       = _v(facial_features)
    cloth      = _v(clothing)
    act        = _v(action)
    gender_set = gender not in (U, "")

    if not gender_set and not any([age_word, body, eth, skin, h_style, h_color, eye, face, cloth, act]):
        return ""

    # Core noun phrase
    core: list[str] = []
    if age_word:
        core.append(age_word)
    if body:
        core.append(body.lower())
    core.append({"Male": "man", "Female": "woman", "Non-binary": "non-binary person"}.get(gender, "person"))
    if eth:
        core.append(f"of {eth.lower()} heritage")
    desc = "a " + " ".join(core)

    # Appearance clause
    appearance: list[str] = []
    if skin:
        appearance.append(f"{skin.lower()} skin")
    hair = [p for p in [h_style.lower() if h_style else "", h_color.lower() if h_color else ""] if p]
    if hair:
        appearance.append(" ".join(hair) + " hair")
    if eye:
        appearance.append(f"{eye.lower()} eyes")
    if face:
        appearance.append(face.lower())
    if appearance:
        desc += " with " + ", ".join(appearance)

    if cloth:
        desc += f", wearing {cloth}"
    if act:
        desc += f", {act}"

    return desc


def get_option_lists(genre: str, theme: str, rating_key: str) -> dict[str, list[str]]:
    pack = GENRE_PACKS[genre]
    lists: dict[str, list[str]] = {
        "shots": list(pack.shots),
        "subjects": list(pack.subjects),
        "environments": list(pack.environments),
        "lighting": list(pack.lighting),
        "atmospheres": list(pack.atmospheres),
    }

    theme_layer = THEME_OVERLAYS.get(theme, {})
    for category, extras in theme_layer.items():
        lists[category] = _dedupe([*extras, *lists[category]])

    if rating_key == "mature":
        for category, extras in MATURE_OVERLAYS.get("_global", {}).items():
            lists[category] = _dedupe([*extras, *lists[category]])
        for category, extras in MATURE_OVERLAYS.get(genre, {}).items():
            lists[category] = _dedupe([*extras, *lists[category]])

    return lists


def _format_environment(environment: str) -> str:
    env = environment.strip()
    if not env:
        return ""
    lower = env.lower()
    if lower.startswith(("in ", "at ", "on ", "inside ", "within ", "set in ", "against ")):
        return env
    return f"set in {env}"


def _format_lighting(lighting: str) -> str:
    light = lighting.strip()
    if not light:
        return ""
    lower = light.lower()
    if lower.startswith(("the scene is lit", "lit by", "lighting:", "illuminated")):
        return light[0].upper() + light[1:] if light and light[0].islower() else light
    return f"The scene is lit by {light}"


def build_prompt(
    genre: str,
    theme: str,
    rating_label: str,
    shot: str,
    subject: str,
    environment: str,
    lighting: str,
    atmosphere: str,
    character_desc: str = "",
) -> str:
    """
    Assemble a Veo 3.1 / Google Flow prompt:
    [Cinematography + Subject] + [Context] + [Lighting] + [Style & ambiance].
    """
    effective_subject = character_desc.strip() if character_desc.strip() else subject.strip()
    cinematography = f"{shot.strip()} {effective_subject}".strip()
    context = _format_environment(environment)
    lighting_line = _format_lighting(lighting)

    rating_key = CONTENT_RATINGS[rating_label]
    style_parts = [
        atmosphere.strip(),
        GENRE_STYLE.get(genre, "cinematic realism"),
        THEME_MOOD.get(theme, ""),
    ]
    if rating_key == "mature":
        style_parts.append("mature R-rated cinematic tone")
        exclusions = PRO_EXCLUDE_MATURE
    else:
        style_parts.append("broadcast-safe family-friendly tone")
        exclusions = PRO_EXCLUDE_SAFE

    opening = cinematography
    if context:
        opening = f"{cinematography}, {context}"

    sentences = [f"{opening}."]
    if lighting_line:
        sentences.append(f"{lighting_line}.")
    style_clause = ", ".join(part for part in style_parts if part)
    sentences.append(f"{style_clause}. {PRO_BASELINE} {exclusions}")
    return " ".join(sentences)


def resolve(selected: str, custom: str) -> str:
    return custom.strip() if selected == CUSTOM else selected.strip()


_CHAR_PLAIN_KEYS = ("c_gender", "c_age", "c_body", "c_skin", "c_eye")


def clear_picker_state() -> None:
    for key in list(st.session_state.keys()):
        if key.endswith("_sel") or key.endswith("_txt"):
            st.session_state.pop(key, None)


def clear_character_state() -> None:
    for key in _CHAR_PLAIN_KEYS:
        st.session_state.pop(key, None)
    st.session_state.pop("char_enabled", None)


def picker(label: str, help_text: str, options: list[str], key: str, index: int = 0) -> str:
    safe_index = min(index, max(len(options) - 1, 0))
    choice = st.selectbox(label, [*options, CUSTOM], index=safe_index, help=help_text, key=f"{key}_sel")
    custom = ""
    if choice == CUSTOM:
        custom = st.text_input(f"Custom {label.lower()}", key=f"{key}_txt", placeholder="Enter your own…")
    return resolve(choice, custom)


def render_copy_button(text: str, label: str = "Copy Prompt") -> None:
    payload = json.dumps(text)
    components.html(
        f"""
        <button id="copy-prompt-btn" style="
            width: 100%;
            padding: 0.45rem 1rem;
            border-radius: 0.5rem;
            border: 1px solid rgba(49, 51, 63, 0.2);
            background: rgb(255, 255, 255);
            color: rgb(49, 51, 63);
            font-size: 0.875rem;
            font-weight: 500;
            cursor: pointer;
        ">{label}</button>
        <script>
        document.getElementById("copy-prompt-btn").onclick = function() {{
            navigator.clipboard.writeText({payload}).then(function() {{
                var btn = document.getElementById("copy-prompt-btn");
                var original = {json.dumps(label)};
                btn.textContent = "Copied!";
                setTimeout(function() {{ btn.textContent = original; }}, 1500);
            }});
        }});
        </script>
        """,
        height=48,
    )


def apply_preset(
    genre: str,
    theme: str,
    rating_label: str,
    indices: tuple[int, int, int, int, int],
    preset_name: str,
) -> None:
    opts = get_option_lists(genre, theme, CONTENT_RATINGS[rating_label])
    s, sub, env, light, atm = indices
    shot = opts["shots"][min(s, len(opts["shots"]) - 1)]
    subject = opts["subjects"][min(sub, len(opts["subjects"]) - 1)]
    environment = opts["environments"][min(env, len(opts["environments"]) - 1)]
    lighting = opts["lighting"][min(light, len(opts["lighting"]) - 1)]
    atmosphere = opts["atmospheres"][min(atm, len(opts["atmospheres"]) - 1)]
    st.session_state["prompt"] = build_prompt(genre, theme, rating_label, shot, subject, environment, lighting, atmosphere)
    st.session_state["breakdown"] = {
        "Genre": genre,
        "Theme": theme,
        "Content": rating_label,
        "Shot + Camera Move": shot,
        "Subject": subject,
        "Environment": environment,
        "Lighting": lighting,
        "Atmosphere": atmosphere,
    }
    st.session_state["preset_name"] = preset_name


def main() -> None:
    st.set_page_config(page_title="Google Flow Prompt Generator", page_icon="🎬", layout="wide")

    st.markdown(
        """
        <style>
        .title { font-size: 2rem; font-weight: 700; }
        .formula {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border-left: 4px solid #e94560;
            padding: 1rem 1.25rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if "genre" not in st.session_state:
        st.session_state["genre"] = GENRES[0]
        st.session_state["theme"] = THEMES[0]
        st.session_state["rating_label"] = list(CONTENT_RATINGS.keys())[0]

    if "prompt" not in st.session_state:
        apply_preset(
            st.session_state["genre"],
            st.session_state["theme"],
            st.session_state["rating_label"],
            (0, 0, 0, 0, 0),
            "Default",
        )

    st.session_state.pop("out", None)

    st.markdown('<p class="title">🎬 Google Flow Prompt Generator</p>', unsafe_allow_html=True)
    st.caption("Genre · theme · content rating drive cinematographic option libraries")

    with st.sidebar:
        st.header("Workflow")
        st.markdown(
            "0. **Genre · Theme · Rating**\n"
            "↳ **Character Profile** _(optional)_\n"
            "1. **Shot + Camera**\n"
            "2. **Subject** _(or character overrides it)_\n"
            "3. **Environment**\n"
            "4. **Lighting**\n"
            "5. **Atmosphere**"
        )
        st.divider()
        st.subheader("Expert example")
        st.code(
            "Low-angle tracking shot, tracking a chrome android with exposed servo joints, "
            "set in smog-choked megacity rooftop with drone traffic lanes. "
            "The scene is lit by neon magenta and cyan cross-lighting with wet reflections. "
            "volumetric fog, cinematic ultra-realism, sci-fi cinematic realism, dystopian tension, "
            "broadcast-safe family-friendly tone. Photorealistic cinematic video…"
        )
        st.divider()
        if st.button("Reset all to defaults", use_container_width=True):
            st.session_state["genre"] = GENRES[0]
            st.session_state["theme"] = THEMES[0]
            st.session_state["rating_label"] = list(CONTENT_RATINGS.keys())[0]
            clear_picker_state()
            clear_character_state()
            apply_preset(
                st.session_state["genre"],
                st.session_state["theme"],
                st.session_state["rating_label"],
                (0, 0, 0, 0, 0),
                "Default",
            )
            st.rerun()

    st.markdown(
        '<div class="formula"><strong>Veo 3.1 formula:</strong> '
        "<code>[Cinematography + Subject]</code> → <code>[Context / Environment]</code> → "
        "<code>[Lighting]</code> → <code>[Style + Genre + Theme + Quality]</code><br><br>"
        "<em>Genre, theme, and rating shape options and the closing style line.</em></div>",
        unsafe_allow_html=True,
    )

    st.subheader("Primary direction")
    g1, g2, g3 = st.columns(3)
    with g1:
        genre = st.selectbox("Genre", GENRES, index=GENRES.index(st.session_state["genre"]), key="genre_pick")
    with g2:
        theme = st.selectbox("Theme", THEMES, index=THEMES.index(st.session_state["theme"]), key="theme_pick")
    with g3:
        rating_options = list(CONTENT_RATINGS.keys())
        rating_label = st.selectbox(
            "Content rating",
            rating_options,
            index=rating_options.index(st.session_state["rating_label"]),
            key="rating_pick",
            help="Censored keeps broadcast-safe options. Uncensored 18+ adds mature cinematography choices.",
        )

    profile_key = f"{genre}|{theme}|{rating_label}"
    if st.session_state.get("profile_key") != profile_key:
        st.session_state["profile_key"] = profile_key
        st.session_state["genre"] = genre
        st.session_state["theme"] = theme
        st.session_state["rating_label"] = rating_label
        clear_picker_state()
    else:
        st.session_state["genre"] = genre
        st.session_state["theme"] = theme
        st.session_state["rating_label"] = rating_label

    opts = get_option_lists(genre, theme, CONTENT_RATINGS[rating_label])

    if CONTENT_RATINGS[rating_label] == "mature":
        st.warning("18+ mode: mature themes enabled. You are responsible for complying with Google Flow policies.")
    else:
        st.caption("Censored mode: family-safe phrasing; mature-only options hidden.")

    st.caption(f"**{len(opts['shots'])}** shot · **{len(opts['subjects'])}** subject · **{len(opts['environments'])}** env · "
               f"**{len(opts['lighting'])}** lighting · **{len(opts['atmospheres'])}** atmosphere options")

    genre_presets = CONTEXT_PRESETS.get(genre, {})
    if genre_presets:
        st.subheader(f"Quick presets · {genre}")
        pcols = st.columns(len(genre_presets))
        for col, (name, idx) in zip(pcols, genre_presets.items()):
            with col:
                if st.button(name, use_container_width=True, key=f"preset_{genre}_{name}"):
                    clear_picker_state()
                    apply_preset(genre, theme, rating_label, idx, name)
                    st.rerun()

    # ── Character Profile ─────────────────────────────────────────────────────
    rating_key_now = CONTENT_RATINGS[rating_label]
    with st.expander("👤 Character Profile  ·  optional  —  overrides the Subject picker when active"):
        char_enabled = st.toggle("Enable character profile", key="char_enabled", value=False)

        character_desc = ""
        if char_enabled:
            if rating_key_now == "mature":
                st.caption("18+ mode active: mature body options and clothing included. Teen age hidden.")

            cp1, cp2, cp3 = st.columns(3)

            with cp1:
                st.markdown("**Identity**")
                c_gender = st.selectbox(
                    "Gender", CHAR_GENDERS, index=0, key="c_gender",
                    help="Character's gender presentation for the scene.",
                )
                age_opts = [a for a in CHAR_AGE_RANGES if not (a == "Teen (13–17)" and rating_key_now == "mature")]
                c_age = st.selectbox("Age range", age_opts, index=0, key="c_age")
                body_opts = list(CHAR_BODY_TYPES) + (list(CHAR_BODY_TYPES_MATURE) if rating_key_now == "mature" else [])
                c_body = st.selectbox("Body type", body_opts, index=0, key="c_body")
                c_ethnicity = picker(
                    "Ethnicity / Appearance", "Casting look and heritage.",
                    list(CHAR_ETHNICITY), "c_eth", 0,
                )

            with cp2:
                st.markdown("**Appearance**")
                c_skin = st.selectbox("Skin tone", CHAR_SKIN_TONES, index=0, key="c_skin")
                c_hair_style = picker(
                    "Hair style", "Cut, length, and structure.",
                    list(CHAR_HAIR_STYLES), "c_hstyle", 0,
                )
                c_hair_color = picker(
                    "Hair color", "Natural or dyed color.",
                    list(CHAR_HAIR_COLORS), "c_hcolor", 0,
                )
                c_eye = st.selectbox("Eye color", CHAR_EYE_COLORS, index=0, key="c_eye")
                c_facial = picker(
                    "Facial features", "Distinguishing face details.",
                    list(CHAR_FACIAL_FEATURES), "c_face", 0,
                )

            with cp3:
                st.markdown("**Styling & Action**")
                clothing_opts = get_clothing_options(genre, rating_key_now)
                c_clothing = picker(
                    "Clothing", "Outfit and costume — genre-matched options.",
                    clothing_opts, "c_cloth", 0,
                )
                c_action = picker(
                    "Action / Pose", "What the character is doing in frame.",
                    list(CHAR_ACTIONS), "c_act", 0,
                )

            character_desc = build_character_desc(
                c_gender, c_age, c_body, c_ethnicity, c_skin,
                c_hair_style, c_hair_color, c_eye, c_facial,
                c_clothing, c_action,
            )

            if character_desc:
                st.success(f"**Character:** {character_desc}")
            else:
                st.caption("Set at least one field above to activate. When active, this replaces the Subject picker.")

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("1 · Shot + Camera")
        shot = picker(
            "Shot type & camera move",
            "Camera composition and movement (dolly, tracking, close-up, etc.).",
            opts["shots"],
            "shot",
            0,
        )
        st.subheader("2 · Subject")
        if char_enabled and character_desc:
            st.info(f"**Character profile active** — Subject overridden. See expander above to adjust.")
            subject = character_desc
        else:
            subject = picker(
                "Subject + action",
                "Who/what — include a visible action or gesture for stronger motion in Flow.",
                opts["subjects"],
                "subject",
                0,
            )
        st.subheader("3 · Environment")
        environment = picker("Environment / setting", "Location and world context.", opts["environments"], "env", 0)
    with c2:
        st.subheader("4 · Lighting")
        lighting = picker("Lighting architecture", "Sources, quality, contrast.", opts["lighting"], "light", 0)
        st.subheader("5 · Atmosphere")
        atmosphere = picker("Atmospheric style", "Film look, texture, mood.", opts["atmospheres"], "atm", 0)

        st.markdown("")
        st.markdown("")
        if st.button("✨ Generate Prompt", type="primary", use_container_width=True):
            parts = [shot, subject, environment, lighting, atmosphere]
            if not all(parts):
                st.error("Complete all sections (including custom text fields).")
            else:
                st.session_state["prompt"] = build_prompt(
                    genre, theme, rating_label, shot, subject, environment, lighting, atmosphere,
                    character_desc=character_desc,
                )
                breakdown: dict[str, str] = {
                    "Genre": genre,
                    "Theme": theme,
                    "Content": rating_label,
                    "Shot + Camera Move": shot,
                    "Subject": subject,
                    "Environment": environment,
                    "Lighting": lighting,
                    "Atmosphere": atmosphere,
                }
                if char_enabled and character_desc:
                    breakdown["Character Profile"] = character_desc
                st.session_state["breakdown"] = breakdown
                st.session_state.pop("preset_name", None)
                st.rerun()

    st.divider()
    st.subheader("Generated prompt")

    if st.session_state.get("preset_name"):
        st.success(f"Preset loaded: **{st.session_state['preset_name']}** — edit sections or regenerate.")

    prompt = st.session_state["prompt"]
    st.text_area("Copy into Google Flow", value=prompt, height=180)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Characters", len(prompt))
    m2.metric("Words", len(prompt.split()))
    with m3:
        render_copy_button(prompt)
    m4.download_button("Download .txt", prompt, "google_flow_prompt.txt", use_container_width=True)

    with st.expander("Prompt breakdown"):
        bd = st.session_state.get("breakdown", {})
        for section, value in bd.items():
            st.markdown(f"**{section}:** {value}")

    st.info(
        "Pick **genre**, **theme**, and **content rating** first — options below adapt. "
        "Choose subjects with clear **action** when possible. "
        "Then **Generate Prompt** → paste into Google Flow (Veo 3.1). "
        "Use **ingredients** or **start/end frames** in Flow when you need character consistency."
    )


if __name__ == "__main__":
    main()
