import streamlit as st
import time
from pathlib import Path

# -----------------------
# CONFIG
# -----------------------

st.set_page_config(page_title="Workout Trainer", layout="centered")

BASE_PATH = Path(__file__).parent
IMAGE_PATH = BASE_PATH / "images"

# -----------------------
# SESSION STATE
# -----------------------

if "day" not in st.session_state:
    st.session_state.day = None

if "muscle" not in st.session_state:
    st.session_state.muscle = None

if "image_index" not in st.session_state:
    st.session_state.image_index = 0

if "set_count" not in st.session_state:
    st.session_state.set_count = 0

if "timer_start" not in st.session_state:
    st.session_state.timer_start = None

# -----------------------
# DATA
# -----------------------

workouts = {
    "Day 1": {
        "Pierna": [
            "pierna1.jpg",
            "pierna2.jpg",
            "pierna3.jpg",
            "pierna4.jpg",
            "pierna5.jpg",
            "pierna6.jpg"
        ],
        "Tricep": [
            "tricep1.jpg",
            "tricep2.jpg",
            "tricep3.jpg"
        ]
    },
    "Day 2": {
        "Hombro": [
            "hombro1.jpg",
            "hombro2.jpg",
            "hombro3.jpg"
        ],
        "Pecho": [
            "pecho1.jpg",
            "pecho2.jpg",
            "pecho3.jpg"
        ]
    },
    "Day 3": {
        "Espalda": [
            "espalda1.jpg",
            "espalda2.jpg",
            "espalda3.jpg",
            "espalda4.jpg"
        ],
        "Bicep": [
            "bicep1.jpg",
            "bicep2.jpg",
            "bicep3.jpg",
            "bicep4.jpg"
        ]
    }
}

TIMER_SECONDS = 120  # 2 minutes

# -----------------------
# FUNCTIONS
# -----------------------

def start_timer():
    st.session_state.timer_start = time.time()

def reset_timer():
    st.session_state.timer_start = None

def finish_set():
    if st.session_state.set_count < 3:
        st.session_state.set_count += 1
        reset_timer()
        if st.session_state.set_count < 3:
            start_timer()

def next_image():
    images = workouts[st.session_state.day][st.session_state.muscle]
    if st.session_state.image_index < len(images) - 1:
        st.session_state.image_index += 1
    st.session_state.set_count = 0
    reset_timer()

def prev_image():
    if st.session_state.image_index > 0:
        st.session_state.image_index -= 1
    st.session_state.set_count = 0
    reset_timer()

def switch_muscle():
    muscles = list(workouts[st.session_state.day].keys())
    current = muscles.index(st.session_state.muscle)
    st.session_state.muscle = muscles[(current + 1) % len(muscles)]
    st.session_state.image_index = 0
    st.session_state.set_count = 0
    reset_timer()

def get_timer_remaining():
    if st.session_state.timer_start is None:
        return None
    elapsed = int(time.time() - st.session_state.timer_start)
    remaining = TIMER_SECONDS - elapsed
    return max(0, remaining)

def go_back_to_days():
    st.session_state.day = None
    st.session_state.muscle = None
    reset_timer()

def go_back_to_muscles():
    st.session_state.muscle = None
    reset_timer()

# -----------------------
# UI
# -----------------------

st.title("🏋️ Workout Trainer")

# -----------------------
# DAY SELECTION
# -----------------------

if st.session_state.day is None:
    st.subheader("Select your workout day")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Day 1"):
            st.session_state.day = "Day 1"
            st.rerun()

    with col2:
        if st.button("Day 2"):
            st.session_state.day = "Day 2"
            st.rerun()

    with col3:
        if st.button("Day 3"):
            st.session_state.day = "Day 3"
            st.rerun()

    st.stop()

# -----------------------
# MUSCLE SELECTION
# -----------------------

if st.session_state.muscle is None:
    st.subheader(f"{st.session_state.day} - Select muscle")

    muscles = workouts[st.session_state.day].keys()
    cols = st.columns(len(muscles))

    for col, muscle in zip(cols, muscles):
        with col:
            if st.button(muscle):
                st.session_state.muscle = muscle
                st.session_state.image_index = 0
                st.session_state.set_count = 0
                reset_timer()
                st.rerun()

    st.divider()
    if st.button("⬅ Back to Days"):
        go_back_to_days()
        st.rerun()

    st.stop()

# -----------------------
# WORKOUT VIEW
# -----------------------

images = workouts[st.session_state.day][st.session_state.muscle]
current_image = images[st.session_state.image_index]
image_file = IMAGE_PATH / current_image

st.subheader(f"{st.session_state.day} — {st.session_state.muscle}")

# Back button
if st.button("⬅ Back to Muscles"):
    go_back_to_muscles()
    st.rerun()

# Show image
if image_file.exists():
    st.image(str(image_file), use_container_width=True)
else:
    st.error(f"Missing image: {current_image}")

# Timer display
remaining = get_timer_remaining()

if remaining is None:
    st.markdown("## ⏱ Timer ready")
else:
    minutes = remaining // 60
    seconds = remaining % 60
    st.markdown(f"## ⏱ {minutes:02}:{seconds:02}")

st.markdown(f"### Set {st.session_state.set_count + 1 if st.session_state.set_count < 3 else 3} / 3")

# Buttons always available
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("⬅ Previous Exercise"):
        prev_image()
        st.rerun()

with col2:
    if st.button("➡ Next Exercise"):
        next_image()
        st.rerun()

with col3:
    finish_disabled = st.session_state.set_count >= 3
    if st.button("✅ Finish Set", disabled=finish_disabled):
        finish_set()
        st.rerun()

with col4:
    if st.button("🔁 Switch Muscle"):
        switch_muscle()
        st.rerun()

# Auto refresh timer every second (only if running)
if st.session_state.timer_start is not None:
    time.sleep(1)
    st.rerun()
