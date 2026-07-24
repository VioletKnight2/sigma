import re
import streamlit as st

def alphabet_to_num(char):
    if 'a' <= char <= 'z':
        return ord(char) - ord('a') + 1
    elif 'A' <= char <= 'Z':
        return ord(char) - ord('A') + 1
    return None

def num_to_alphabet(num, is_upper):
    num = (num - 1) % 26 + 1
    if is_upper:
        return chr(num + ord('A') - 1)
    return chr(num + ord('a') - 1)

def int_to_roman(n):
    # Standard Roman numeral mapping (1 to 26 range needed for alphabet)
    mapping = [(10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    result = []
    for val, roman in mapping:
        while n >= val:
            result.append(roman)
            n -= val
    return "".join(result)

def roman_to_int(s):
    # Standard Roman numeral parser handling subtraction logic natively
    roman_map = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    prev_val = 0
    for char in reversed(s):
        val = roman_map.get(char, 0)
        if val < prev_val:
            total -= val
        else:
            total += val
            prev_val = val
    return total

def transform_word(word):
    if not word or not word.strip():
        return word
        
    chars = list(word)
    ref_idx = -1
    for i, c in enumerate(chars):
        if c.isalnum():
            ref_idx = i
            break
            
    if ref_idx == -1:
        return word
         
    ref_char = chars[ref_idx]
    result = list(chars)
    
    if ref_char.isalpha():
        R = alphabet_to_num(ref_char)
        for i in range(ref_idx + 1, len(chars)):
            c = chars[i]
            if c.isalpha():
                L = alphabet_to_num(c)
                new_val = 2 * R - L
                result[i] = num_to_alphabet(new_val, c.isupper())
    return "".join(result)

def encode_full(text):
    # Preserve words and whitespace chunks using regex regex split pattern
    tokens = re.findall(r'\S+|\s+', text)
    ciphered = "".join([transform_word(t) for t in tokens])
    reversed_text = ciphered[::-1]
    
    roman_tokens = []
    for char in reversed_text:
        if char.isalpha():
            roman_tokens.append(int_to_roman(alphabet_to_num(char)))
        else:
            roman_tokens.append(char)
            
    return " ".join(roman_tokens)

# Streamlit App UI
st.set_page_config(page_title="Reflection Cipher App", page_icon="🏛️")
st.title("🏛️ Symmetrical Roman Cipher")

text_input = st.text_area("Enter your message:", height=100)

if text_input:
    result = encode_full(text_input)
    st.subheader("Output:")
    st.code(result)
