"""
Google Flow Video Prompt Generator
Cinematographic prompt builder for Google Flow video generation.
"""

import json
from dataclasses import dataclass

import streamlit as st
import streamlit.components.v1 as components

CUSTOM = "✏️ Custom (type below)"

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
            "two lovers sharing a umbrella in drizzle",
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
            "a avalanche survivor sprinting from a collapsing ridge",
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
            "a silver-armored knight on a armored warhorse",
            "a elven archer with glowing arrow nock",
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
            "a elder teaching traditional weaving",
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
            "a office worker covered in Post-it notes",
            "a dog wearing sunglasses driving a tiny car prop",
            "a influencer failing a viral dance challenge",
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
            "a idol singer on stadium stage with light sticks sea",
            "a isekai hero with oversized sword and cloak",
            "a villain monologuing on throne with cape billow",
            "a catgirl barista with bell collar charm",
            "a sports captain mid-impossible spike leap",
            "a alchemist drawing transmutation circle glow",
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
            "Intimate shallow rack-focus drifting across",
            "Unflinching close-up hold on",
        ),
        "lighting": (
            "moody boudoir practical with deep shadow falloff",
            "single-source bedroom lamp with warm skin tones",
        ),
        "atmospheres": (
            "raw intimate grain, adults-only tone",
            "unflinching vérité texture, mature audience",
        ),
    },
    "Horror & Supernatural": {
        "subjects": (
            "a visceral creature with exposed muscle and sinew",
            "a victim silhouette splattered with practical blood mist",
        ),
        "atmospheres": ("crushed blacks, disturbing practical gore haze",),
    },
    "Romance & Drama": {
        "subjects": (
            "lovers in silk-sheet silhouette behind gauze curtain",
            "a passionate embrace in steam-fogged bathroom mirror",
        ),
        "lighting": ("silhouette backlight through sheer fabric, mature tone",),
    },
    "Action & Thriller": {
        "subjects": ("a bruised antihero wiping blood with a sleeve",),
        "atmospheres": ("practical squib mist, R-rated impact texture",),
    },
    "Noir & Crime": {
        "subjects": (
            "a femme fatale adjusting stocking in shadowed motel room",
            "an interrogation sweat close-up under bare bulb",
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
}


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


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


def build_prompt(
    genre: str,
    theme: str,
    rating_label: str,
    shot: str,
    subject: str,
    environment: str,
    lighting: str,
    atmosphere: str,
) -> str:
    core = f"{shot} {subject}, {environment}, {lighting}, {atmosphere}"
    tone = "mature 18+ cinematic tone" if CONTENT_RATINGS[rating_label] == "mature" else "broadcast-safe cinematic tone"
    return f"[{genre} · {theme} · {tone}] {core}"


def resolve(selected: str, custom: str) -> str:
    return custom.strip() if selected == CUSTOM else selected.strip()


def clear_picker_state() -> None:
    for key in list(st.session_state.keys()):
        if key.endswith("_sel") or key.endswith("_txt"):
            st.session_state.pop(key, None)


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
            "1. **Shot + Camera**\n"
            "2. **Subject**\n"
            "3. **Environment**\n"
            "4. **Lighting**\n"
            "5. **Atmosphere**"
        )
        st.divider()
        st.subheader("Expert example")
        st.code(
            "[Sci-Fi & Cyberpunk · Dystopian Future · broadcast-safe] "
            "Low-angle tracking shot, tracking a chrome android with exposed servo joints, "
            "smog-choked megacity rooftop with drone traffic lanes, "
            "neon magenta and cyan cross-lighting, volumetric fog, cinematic ultra-realism.",
        )
        st.divider()
        if st.button("Reset all to defaults", use_container_width=True):
            st.session_state["genre"] = GENRES[0]
            st.session_state["theme"] = THEMES[0]
            st.session_state["rating_label"] = list(CONTENT_RATINGS.keys())[0]
            clear_picker_state()
            apply_preset(
                st.session_state["genre"],
                st.session_state["theme"],
                st.session_state["rating_label"],
                (0, 0, 0, 0, 0),
                "Default",
            )
            st.rerun()

    st.markdown(
        '<div class="formula"><strong>Formula:</strong> '
        "<code>[Genre · Theme · Tone]</code> + "
        "<code>[Shot + Camera]</code> → <code>[Subject]</code> → "
        "<code>[Environment]</code> → <code>[Lighting]</code> → "
        "<code>[Atmosphere]</code><br><br>"
        "<em>Primary selections reshape every dropdown below.</em></div>",
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

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("1 · Shot + Camera")
        shot = picker("Shot type & camera move", "Angle, movement, framing.", opts["shots"], "shot", 0)
        st.subheader("2 · Subject")
        subject = picker("Subject core details", "Who/what — specific visual details.", opts["subjects"], "subject", 0)
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
                    genre, theme, rating_label, shot, subject, environment, lighting, atmosphere
                )
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
                st.session_state.pop("preset_name", None)
                st.rerun()

    st.divider()
    st.subheader("Generated prompt")

    if st.session_state.get("preset_name"):
        st.success(f"Preset loaded: **{st.session_state['preset_name']}** — edit sections or regenerate.")

    prompt = st.session_state["prompt"]
    st.text_area("Copy into Google Flow", value=prompt, height=120)

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
        "Then **Generate Prompt** → **Copy Prompt** or the text area → Google Flow."
    )


if __name__ == "__main__":
    main()
