"""
Google Flow Video Prompt Generator
Cinematographic prompt builder for Google Flow video generation.
"""

import streamlit as st

SHOT_CAMERA_OPTIONS = [
    "Low-angle tracking shot, tracking",
    "High-angle crane shot, descending on",
    "Eye-level dolly shot, pushing in on",
    "Over-the-shoulder handheld shot, following",
    "Wide establishing aerial shot, orbiting",
    "Dutch-angle steadicam shot, circling",
    "Macro close-up, rack-focusing on",
    "Slow-motion bullet-time orbit around",
    "FPV drone fly-through, weaving past",
    "Static locked-off medium shot of",
    "Whip-pan transition into close-up of",
    "Jib arm rising reveal of",
    "Steadicam walk-and-talk alongside",
    "Top-down God's-eye view of",
    "Snorricam body-mounted shot of",
]

SUBJECT_OPTIONS = [
    "a matte black 1969 Mustang fastback",
    "a weathered samurai in lacquered armor",
    "a lone astronaut in a scuffed EVA suit",
    "a ballerina in flowing ivory silk",
    "a vintage leather-clad motorcyclist",
    "a cybernetic detective in a trench coat",
    "a golden retriever sprinting through surf",
    "a medieval knight on a armored warhorse",
    "a street food vendor flipping noodles",
    "a jazz pianist at a grand piano",
    "a falcon in mid-dive with wings tucked",
    "a haute couture model in avant-garde gown",
    "a deep-sea diver with bioluminescent gear",
    "a child releasing a sky lantern at dusk",
    "a Formula 1 car at full throttle",
]

ENVIRONMENT_OPTIONS = [
    "neon-lit rainy cyberpunk alleyway",
    "misty bamboo forest at dawn",
    "abandoned Art Deco ballroom",
    "sun-baked Moroccan medina marketplace",
    "frozen Arctic tundra under aurora",
    "underwater coral reef cathedral",
    "brutalist concrete megastructure interior",
    "dusty Wild West ghost town main street",
    "Tokyo Shibuya crossing at rush hour",
    "Victorian greenhouse overrun with vines",
    "volcanic black-sand beach at golden hour",
    "zero-gravity space station corridor",
    "rain-soaked noir city rooftop",
    "Saharan dunes at blue hour",
    "bioluminescent cave with stalactites",
]

LIGHTING_OPTIONS = [
    "intense anamorphic lens flare",
    "soft Rembrandt key light with deep shadows",
    "harsh overhead fluorescent practicals",
    "warm golden-hour rim lighting",
    "cool moonlight with silver fill",
    "neon magenta and cyan cross-lighting",
    "single bare bulb chiaroscuro",
    "diffused overcast skylight",
    "firelight flicker with orange bounce",
    "strobing club lights with haze",
    "backlit silhouette with blown highlights",
    "motivated window light with dust motes",
    "LED panel matrix with specular highlights",
    "candlelit warmth with deep amber tones",
    "high-contrast noir venetian-blind shadows",
]

ATMOSPHERE_OPTIONS = [
    "volumetric fog, cinematic ultra-realism",
    "film grain, Kodak Vision3 500T aesthetic",
    "dreamy bokeh, shallow depth of field",
    "heat shimmer, documentary vérité",
    "particle dust, epic blockbuster scale",
    "lens breathing, indie arthouse intimacy",
    "chromatic aberration, retro VHS nostalgia",
    "rain streaks on lens, melancholic mood",
    "snow flurries, fairy-tale wonder",
    "smoke wisps, tense thriller atmosphere",
    "lens distortion at edges, surreal unease",
    "clean clinical sharpness, commercial polish",
    "motion blur trails, kinetic energy",
    "double-exposure ghosting, ethereal memory",
    "anamorphic oval bokeh, prestige drama",
]

CUSTOM = "✏️ Custom (type below)"

PRESETS = {
    "Cyberpunk Chase": (0, 0, 0, 0, 0),
    "Samurai Dawn": (4, 1, 1, 3, 4),
    "Space Odyssey": (7, 2, 11, 4, 0),
    "Noir Rooftop": (1, 5, 12, 14, 8),
    "Underwater Wonder": (6, 12, 5, 11, 1),
}


def build_prompt(shot: str, subject: str, environment: str, lighting: str, atmosphere: str) -> str:
    return f"{shot} {subject}, {environment}, {lighting}, {atmosphere}"


def resolve(selected: str, custom: str) -> str:
    return custom.strip() if selected == CUSTOM else selected.strip()


def picker(label: str, help_text: str, options: list[str], key: str, index: int = 0) -> str:
    choice = st.selectbox(label, [*options, CUSTOM], index=index, help=help_text, key=f"{key}_sel")
    custom = ""
    if choice == CUSTOM:
        custom = st.text_input(f"Custom {label.lower()}", key=f"{key}_txt", placeholder="Enter your own…")
    return resolve(choice, custom)


def apply_preset(indices: tuple[int, ...]) -> None:
    s, sub, env, light, atm = indices
    st.session_state["prompt"] = build_prompt(
        SHOT_CAMERA_OPTIONS[s],
        SUBJECT_OPTIONS[sub],
        ENVIRONMENT_OPTIONS[env],
        LIGHTING_OPTIONS[light],
        ATMOSPHERE_OPTIONS[atm],
    )
    st.session_state["breakdown"] = {
        "Shot + Camera Move": SHOT_CAMERA_OPTIONS[s],
        "Subject": SUBJECT_OPTIONS[sub],
        "Environment": ENVIRONMENT_OPTIONS[env],
        "Lighting": LIGHTING_OPTIONS[light],
        "Atmosphere": ATMOSPHERE_OPTIONS[atm],
    }


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

    if "prompt" not in st.session_state:
        apply_preset((0, 0, 0, 0, 0))

    st.markdown('<p class="title">🎬 Google Flow Prompt Generator</p>', unsafe_allow_html=True)
    st.caption("Professional cinematographic prompts for Google Flow video generation")

    with st.sidebar:
        st.header("Prompting formula")
        st.markdown(
            "1. **Shot Type + Camera Move**\n"
            "2. **Subject Core Details**\n"
            "3. **Environment / Setting**\n"
            "4. **Lighting Architecture**\n"
            "5. **Atmospheric Style**"
        )
        st.divider()
        st.subheader("Expert example")
        st.code(
            "Low-angle tracking shot, tracking a matte black 1969 "
            "Mustang fastback, neon-lit rainy cyberpunk alleyway, "
            "intense anamorphic lens flare, volumetric fog, "
            "cinematic ultra-realism.",
        )
        st.divider()
        if st.button("Reset to Cyberpunk default", use_container_width=True):
            apply_preset((0, 0, 0, 0, 0))
            st.rerun()

    st.markdown(
        '<div class="formula"><strong>Formula:</strong> '
        "<code>[Shot + Camera]</code> → <code>[Subject]</code> → "
        "<code>[Environment]</code> → <code>[Lighting]</code> → "
        "<code>[Atmosphere]</code><br><br>"
        "<em>Avoid vague prompts. Use specific cinematographic language.</em></div>",
        unsafe_allow_html=True,
    )

    st.subheader("Quick presets")
    pcols = st.columns(len(PRESETS))
    for col, (name, idx) in zip(pcols, PRESETS.items()):
        with col:
            if st.button(name, use_container_width=True, key=f"preset_{name}"):
                apply_preset(idx)
                st.session_state["preset_name"] = name
                st.rerun()

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("1 · Shot + Camera")
        shot = picker("Shot type & camera move", "Angle, movement, framing.", SHOT_CAMERA_OPTIONS, "shot", 0)
        st.subheader("2 · Subject")
        subject = picker("Subject core details", "Who/what — specific visual details.", SUBJECT_OPTIONS, "subject", 0)
        st.subheader("3 · Environment")
        environment = picker("Environment / setting", "Location and world context.", ENVIRONMENT_OPTIONS, "env", 0)
    with c2:
        st.subheader("4 · Lighting")
        lighting = picker("Lighting architecture", "Sources, quality, contrast.", LIGHTING_OPTIONS, "light", 0)
        st.subheader("5 · Atmosphere")
        atmosphere = picker("Atmospheric style", "Film look, texture, mood.", ATMOSPHERE_OPTIONS, "atm", 0)

        st.markdown("")
        st.markdown("")
        if st.button("✨ Generate Prompt", type="primary", use_container_width=True):
            parts = [shot, subject, environment, lighting, atmosphere]
            if not all(parts):
                st.error("Complete all sections (including custom text fields).")
            else:
                st.session_state["prompt"] = build_prompt(*parts)
                st.session_state["breakdown"] = {
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
    st.text_area("Copy into Google Flow", value=prompt, height=110, key="out")

    m1, m2, m3 = st.columns(3)
    m1.metric("Characters", len(prompt))
    m2.metric("Words", len(prompt.split()))
    m3.download_button("Download .txt", prompt, "google_flow_prompt.txt", use_container_width=True)

    with st.expander("Prompt breakdown"):
        bd = st.session_state.get("breakdown", {})
        for section, value in bd.items():
            st.markdown(f"**{section}:** {value}")

    st.info("Select options above → **Generate Prompt** → copy the text into Google Flow.")


if __name__ == "__main__":
    main()
