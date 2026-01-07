
import streamlit as st
from collections import deque

ALPHABET = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
rotor1 = list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
rotor2 = list("AJDKSIRUXBLHWTMCQGZNPYFVOE")
rotor3 = list("BDFHJLCPRTXVZNYEIWGAKMUSQO")
reflector = list("YRUHQSLDPXNGOKMIEBFZCWVJAT")
plugboard = {
    'A': 'D',
    'D': 'A',
    'B': 'C',
    'C': 'B',
    'E': 'F',
    'F': 'E',
    'G': 'H',
    'H': 'G',
    'I': 'J',
    'J': 'I',
}
rotor_container = st.container()
output_container = st.container()
lamp_container = st.container()
keyboard_container = st.container()
plugboard_container = st.container()
reset_container = st.container()

with plugboard_container:
    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if "plug_pairs" not in st.session_state:
        st.session_state.plug_pairs = []
    pair_cols = st.columns(5)
    for i in range(5):
        with pair_cols[i]:
            pair = st.multiselect(
                f"Steckverbindung {i+1}",
                options=letters,
                default=list(st.session_state.plug_pairs[i]) if i < len(st.session_state.plug_pairs) else [],
                max_selections=2,
                key=f"plug_{i}"
            )
            if len(pair) == 2:
                if i >= len(st.session_state.plug_pairs):
                    st.session_state.plug_pairs.append(tuple(pair))
                else:
                    st.session_state.plug_pairs[i] = tuple(pair)
            elif len(pair) == 0 and i < len(st.session_state.plug_pairs):
                st.session_state.plug_pairs[i] = ()
st.session_state.plug_pairs = [p for p in st.session_state.plug_pairs if len(p) == 2]
plugboard = {}
for a, b in st.session_state.plug_pairs:
    plugboard[a] = b
    plugboard[b] = a

def plugboard_substitution(letter):
    return plugboard.get(letter, letter)

def encipher_forward(rotor, letter, position):
    input_index = (ALPHABET.index(letter) + position) % 26
    subst_letter = rotor[input_index]
    output_index = (ALPHABET.index(subst_letter) - position) % 26
    return ALPHABET[output_index]

def encipher_backward(rotor, letter, position):
    target = ALPHABET[(ALPHABET.index(letter) + position) % 26]
    rotor_index = rotor.index(target)
    output_index = (rotor_index - position) % 26
    return ALPHABET[output_index]

def reflect(letter):
    return reflector[ALPHABET.index(letter)]

def enigma_process(plaintext, rotor1, rotor2, rotor3, pos1=0, pos2=0, pos3=0, encode=True, debug=False):
    ciphertext = ""
    position_rotor1 = pos1 % 26
    position_rotor2 = pos2 % 26
    position_rotor3 = pos3 % 26
    for i, letter in enumerate(plaintext, start=1):
        position_rotor1 = (position_rotor1 + 1) % 26
        if position_rotor1 == 0:
            position_rotor2 = (position_rotor2 + 1) % 26
            if position_rotor2 == 0:
                position_rotor3 = (position_rotor3 + 1) % 26
        letter_in_plug = plugboard_substitution(letter)
        x = encipher_forward(rotor1, letter_in_plug, position_rotor1)
        y = encipher_forward(rotor2, x, position_rotor2)
        z = encipher_forward(rotor3, y, position_rotor3)
        reflected_letter = reflect(z)
        z_back = encipher_backward(rotor3, reflected_letter, position_rotor3)
        y_back = encipher_backward(rotor2, z_back, position_rotor2)
        x_back = encipher_backward(rotor1, y_back, position_rotor1)
        final_letter = plugboard_substitution(x_back)
        ciphertext += final_letter
        if debug:
            print(f"Processing letter {i}: {letter}")
            print(f"  Rotor positions: pos1={position_rotor1}, pos2={position_rotor2}, pos3={position_rotor3}")
            print(f"  Plugboard in: {letter} -> {letter_in_plug}")
            print(f"  Nach Rotor1 vorwärts: {x}")
            print(f"  Nach Rotor2 vorwärts: {y}")
            print(f"  Nach Rotor3 vorwärts: {z}")
            print(f"  Reflektor: {reflected_letter}")
            print(f"  Nach Rotor3 rückwärts: {z_back}")
            print(f"  Nach Rotor2 rückwärts: {y_back}")
            print(f"  Nach Rotor1 rückwärts: {x_back}")
            print(f"  Plugboard out: {x_back} -> {final_letter}")
            print(f"  Zwischenstand ciphertext: {ciphertext}")
            print("---")
    return ciphertext


st.set_page_config(page_title="Enigma", layout="centered")
st.markdown("""
<style>
.stApp { background-color: #000; color:#fff; text-align:center; }
div[data-testid="stButton"] > button {
    border-radius: 50%;
    height:60px;
    width:60px;
    margin:6px;
    background:#333;
    color:#fff;
    font-weight:700;
}
div[data-testid="stButton"] > button:hover {
    background:#ffd500;
    color:#000;
}
.lampboard {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 10px;
    margin-bottom: 25px;
    font-family: 'Courier New', Courier, monospace;
}
.lamprow {
    display: flex;
    justify-content: center;
    gap: 10px;
}
.lamp {
    width:44px;
    height:44px;
    border-radius:50%;
    background:#111;
    color:#fff;
    line-height:44px;
    text-align:center;
    border:2px solid #333;
    font-weight:600;
    font-family: 'Courier New', Courier, monospace;
}
.lamp.on {
    background:#ffd500;
    color:#000;
    box-shadow:0 0 18px #ffd500;
    border-color:#ad8b00;
}
</style>
""", unsafe_allow_html=True)
#st.title("Enigma")
if "ciphertext" not in st.session_state: st.session_state.ciphertext = ""
if "pos1" not in st.session_state: st.session_state.pos1 = 0
if "pos2" not in st.session_state: st.session_state.pos2 = 0
if "pos3" not in st.session_state: st.session_state.pos3 = 0
if "last_lamp" not in st.session_state: st.session_state.last_lamp = None
#st.subheader("")
with rotor_container:
    c1, c2, c3 = st.columns(3)
    with c1:
        s1 = st.slider("Rotor I", 0, 25, st.session_state.pos1)
    with c2:
        s2 = st.slider("Rotor II", 0, 25, st.session_state.pos2)
    with c3:
        s3 = st.slider("Rotor III", 0, 25, st.session_state.pos3)
st.session_state.pos1 = s1
st.session_state.pos2 = s2
st.session_state.pos3 = s3
def rotors():
    st.session_state.pos1 = (st.session_state.pos1 + 1) % 26
    if st.session_state.pos1 == 0:
        st.session_state.pos2 = (st.session_state.pos2 + 1) % 26
        if st.session_state.pos2 == 0:
            st.session_state.pos3 = (st.session_state.pos3 + 1) % 26
def enigma_process_one(letter):
    rotors()
    pos1, pos2, pos3 = st.session_state.pos1, st.session_state.pos2, st.session_state.pos3
    l = plugboard_substitution(letter)
    x = encipher_forward(rotor1, l, pos1)
    y = encipher_forward(rotor2, x, pos2)
    z = encipher_forward(rotor3, y, pos3)
    r = reflect(z)
    x_back = encipher_backward(rotor3, r, pos3)
    y_back = encipher_backward(rotor2, x_back, pos2)
    z_back = encipher_backward(rotor1, y_back, pos1)
    final = plugboard_substitution(z_back)
    
    st.session_state.ciphertext += final
    st.session_state.last_lamp = final
    return final

rows = [list("QWERTZUIO"), list("ASDFGHJK"), list("PYXCVBNML")]
with keyboard_container:
    for row in rows:
        cols = st.columns(len(row), gap="small")
        for i, ch in enumerate(row):
            if cols[i].button(ch, key=f"btn_{ch}"):
                enigma_process_one(ch)
with lamp_container:
    lamp_html = '<div class="lampboard">'
    for row in rows:
        lamp_html += '<div class="lamprow">'
        for ch in row:
            cls = "lamp on" if st.session_state.last_lamp == ch else "lamp"
            lamp_html += f'<div class="{cls}">{ch}</div>'
        lamp_html += '</div>'
    lamp_html += '</div>'
    st.markdown(lamp_html, unsafe_allow_html=True)
with output_container:
    st.text_area("Ausgabe",value=st.session_state.ciphertext, height=120)

with reset_container:
    if st.button("NEU"):
        st.session_state.ciphertext = ""
        st.session_state.pos1 = 0
        st.session_state.pos2 = 0
        st.session_state.pos3 = 0
        st.session_state.last_lamp = None
