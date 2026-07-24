import re
import streamlit as st


def alphabet_to_num(char):
    """Converts a-z / A-Z to 1-26."""
    if "a" <= char <= "z":
        return ord(char) - ord("a") + 1
    elif "A" <= char <= "Z":
        return ord(char) - ord("A") + 1
    return None


def num_to_alphabet(num, is_upper):
    """Converts a 1-26 mapped integer back to a character."""
    idx = (num - 1) % 26
    base = ord("A") if is_upper else ord("a")
    return chr(base + idx)


def int_to_roman(n):
    """Converts integer (1-26) to Roman numerals."""
    mapping = [
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]
    result = []
    for val, roman in mapping:
        while n >= val:
            result.append(roman)
            n -= val
    return "".join(result)


def transform_word(word):
    """Reflects letters in a word around the first letter's position value R:

    new_val = 2 * R - L
    """
    if not word or not word.strip():
        return word

    chars = list(word)
    ref_idx = -1
    for i, c in enumerate(chars):
        if c.isalpha():
            ref_idx = i
            break

    if ref_idx == -1:
        return word

    ref_char = chars[ref_idx]
    result = list(chars)

    R = alphabet_to_num(ref_char)
    for i in range(ref_idx + 1, len(chars)):
        c = chars[i]
        if c.isalpha():
            L = alphabet_to_num(c)
            new_val = 2 * R - L
            result[i] = num_to_alphabet(new_val, c.isupper())

    return "".join(result)


def process_sentence(sentence):
    """Transforms words in a sentence, reverses them, converts letters to Roman

    numerals, and records the numeral length count for each letter.
    """
    words = re.findall(r"\b\w+\b", sentence)

    numeral_counts = []
    sentence_roman_tokens = []

    for word in words:
        transformed = transform_word(word)

        # Reverse word for tokenization
        rev_word = transformed[::-1]

        # Convert each letter to Roman numerals & record length of each numeral token
        for char in rev_word:
            if char.isalpha():
                roman_str = int_to_roman(alphabet_to_num(char))
                sentence_roman_tokens.append(roman_str)
                numeral_counts.append(str(len(roman_str)))
            else:
                sentence_roman_tokens.append(char)
                numeral_counts.append("1")

    connected_string = "".join(sentence_roman_tokens)
    length_pattern = "".join(numeral_counts)

    return connected_string, length_pattern


def encode_full(text):
    """Splits text into sentences and encodes each sentence individually."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

    results = []
    for sentence in sentences:
        connected_str, length_pat = process_sentence(sentence)
        results.append(
            {
                "sentence": sentence,
                "connected": connected_str,
                "pattern": length_pat,
            }
        )
    return results


# --- Streamlit UI ---
st.set_page_config(page_title="Reflection Cipher App", page_icon="🏛️")
st.title("🏛️ Symmetrical Roman Cipher (Sentence Connected)")

text_input = st.text_area("Enter your message:", height=100)

if text_input:
    sentence_results = encode_full(text_input)

    # Build the combined multi-line block for easy copying
    combined_output = []
    for item in sentence_results:
        combined_output.append(item["connected"])
        combined_output.append(item["pattern"])

    full_copy_text = "\n".join(combined_output)

    st.subheader("Encoded Output (Click copy icon at top right):")
    st.code(full_copy_text, language="text")

    st.markdown("---")
    st.subheader("Sentence Breakdown:")
    for idx, item in enumerate(sentence_results, 1):
        st.markdown(f"**Sentence {idx}:** `{item['sentence']}`")
        st.write(f"Roman String: `{item['connected']}`")
        st.write(f"Pattern: `{item['pattern']}`")
