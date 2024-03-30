import torch

def extract_encoder_decoder(filename: str) -> tuple:
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    print("length of dataset in characters: ", len(text))
    chars = sorted(list(set(text)))
    vocab_size = len(chars)
    print(''.join(chars))
    print(f"Vocab Size: {vocab_size}")

    char_to_int = {ch:i for i, ch in enumerate(chars)}
    int_to_char = {i:ch for i, ch in enumerate(chars)}

    encode = lambda s: [char_to_int[c] for c in s]
    decode = lambda l: [int_to_char[i] for i in l]

    return (encode, decode, text)


def test_encoder_decoder(filename):
    test_str = "This is a test"
    encoder, decoder = extract_encoder_decoder(filename)
    
    print(f"Encoded: {encoder(test_str)}")
    print(f"Decoded: {decoder(encoder(test_str))}")
    assert test_str == "".join(decoder(encoder(test_str)))