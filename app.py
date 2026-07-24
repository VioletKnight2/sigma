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
    mapping = [(10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    result = []
    for val, roman in mapping:
        while n >= val:
            result.append(roman)
            n -= val
    return "".join(result)

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

def process_sentence(sentence):
    # Extract only words (alphanumeric sequences)
    words = re.findall(r'\b\w+\b', sentence)
    
    word_lengths = []
    sentence_roman_tokens = []
    
    for word in words:
        transformed = transform_word(word)
        # Reverse word for tokenization
        rev_word = transformed[::-1]
        
        # Convert alphabetic characters into Roman numeral tokens
        roman_tokens = []
        for char in rev_word:
            if char.isalpha():
                roman_tokens.append(int_to_roman(alphabet_to_num(char)))
            else:
                roman_tokens.append(char)
                
        word_lengths.append(str(len(roman_tokens)))
        sentence_roman_tokens.append("".join(roman_tokens))
        
    connected_string = "".join(sentence_roman_tokens)
    length_pattern = "".join(word_lengths)
    
    return connected_string, length_pattern

def encode_full(text):
    # Split text by sentence delimiters (. ! ?) while keeping delimiters
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    
    results = []
    for sentence in sentences:
        connected_str, length_pat = process_sentence(sentence)
        results.append({
            "sentence": sentence,
            "connected": connected_str,
            "pattern": length_pat
        })
    return results

# Streamlit App UI
st.set_page_config(page_title="Reflection Cipher App", page_icon="🏛️")
st.title("🏛️ Symmetrical Roman Cipher (Sentence Connected)")

text_input = st.text_area("Enter your message:", height=100)

if text_input:
    sentence_results = encode_full(text_input)
    st.subheader("Results by Sentence:")
    
    for idx, item in enumerate(sentence_results, 1):
        st.markdown(f"**Sentence {idx}:** `{item['sentence']}`")
        st.write(**Connected Roman String:**)
        st.code(item['connected'])
        st.write(**Word Length Pattern:**)
        st.code(item['pattern'])
        st.markdown("---")
