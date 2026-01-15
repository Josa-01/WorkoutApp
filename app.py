import streamlit as st
import time
import os

# ============================
# PAGE CONFIG (Mobile friendly)
# ============================

st.set_page_config(
    page_title="Workout Trainer",
    layout="wide"
)

# ============================
# SESSION STATE
# ============================

if "day" not in st.session_state:
    st.session_state.day = None

if "muscle" not in st.session_state:
    st.session_state.muscle = None

if "exercise_index" not in st.session_state:
    st.session_state.exercise_index = 0

if "sets_done" not in st.session_state:
    st.session_state.sets_done = 0

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

if "time_left" not in st.session_state:
    st.session_state.time_left = 120


# ============================
# DATA
# ============================

WORKOUTS = {
    "Pierna": ["pierna1.jpg", "pierna2.jpg", "pierna3.jpg"],
    "Tricep": ["tricep1.jpg", "tricep2.jpg", "tricep3.jpg"],
}

IMAGES_PATH = "images"
BEEP_SOUND = "beep.mp3"


# ============================
# HELPERS
# ============================

def start_timer():
    st.session_state.timer_running = True
    st.session_state.time_left = 120


def reset_sets():
    st.session_state.sets_done = 0
    st.session_state.exercise_index = 0


# ============================
# UI
# ============================

st.title("🏋️ Workout Trainer")
st.divider()

# ============================
# DAY SELECTION
# ============================

if st.session_state.day is None:
    st.subheader("Select Training Day")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("Day 1", use_container_width=True):
            st.session_state.day = "Day 1"
            st.rerun()

    with c2:
        if st.button("Day 2", use_container_width=True):
            st.session_state.day = "Day 2"
            st.rerun()

    with c3:
        if st.button("Day 3", use_container_width=True):
            st.session_state.day = "Day 3"
            st.rerun()

    st.stop()

# ============================
# MUSCLE SELECTION
# ============================

if st.session_state.muscle is None:
    st.subheader(f"{st.session_state.day}")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("Pierna", use_container_width=True):
            st.session_state.muscle = "Pierna"
            reset_sets()
            st.rerun()

    with c2:
        if st.button("Tricep", use_container_width=True):
            st.session_state.muscle = "Tricep"
            reset_sets()
            st.rerun()

    st.stop()

# ============================
# WORKOUT SCREEN
# ============================

st.subheader(f"{st.session_state.day} - {st.session_state.muscle}")

images = WORKOUTS[st.session_state.muscle]
current_image = images[st.session_state.exercise_index]
image_path = os.path.join(IMAGES_PATH, current_image)

if os.path.exists(image_path):
    st.image(image_path, use_container_width=True)
else:
    st.error(f"Missing image: {current_image}")

# ============================
# SET COUNTER
# ============================

st.markdown(f"## Sets: {st.session_state.sets_done}/3")

if st.button("✅ Complete Set", use_container_width=True):
    if st.session_state.sets_done < 3:
        st.session_state.sets_done += 1
        start_timer()
        st.rerun()

# ============================
# TIMER
# ============================

if st.session_state.timer_running:
    timer_box = st.empty()

    while st.session_state.time_left > 0:
        mins = st.session_state.time_left // 60
        secs = st.session_state.time_left % 60
        timer_box.markdown(f"## ⏳ Rest Time: {mins:02}:{secs:02}")
        time.sleep(1)
        st.session_state.time_left -= 1

    timer_box.markdown("## ✅ Rest Finished!")
    st.audio(BEEP_SOUND)

    st.session_state.timer_running = False
    st.session_state.time_left = 120

# ============================
# NAVIGATION
# ============================

c1, c2 = st.columns(2)

with c1:
    if st.button("➡ Next Exercise", use_container_width=True):
        if st.session_state.exercise_index < len(images) - 1:
            st.session_state.exercise_index += 1
            st.rerun()

with c2:
    if st.button("🔄 Switch Muscle", use_container_width=True):
        if st.session_state.muscle == "Pierna":
            st.session_state.muscle = "Tricep"
        else:
            st.session_state.muscle = "Pierna"

        reset_sets()
        st.rerun()
