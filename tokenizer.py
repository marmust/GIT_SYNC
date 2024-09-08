from transformers import AutoTokenizer

# load / download tokenizer
tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")

# get misc info aboutt tokenizer
vocab_size = len(tokenizer.vocab.keys())
max_token_size = 8#len(max(tokenizer.vocab.keys(), key=len))
average_token_length = int(sum(len(token) for token in tokenizer.vocab.keys()) / vocab_size)

# wrapper for tokenizing segment
def tokenize_segment(text, tokenizer=tokenizer, space_indicator=("▁", " ")):
    """
    breaks up a string into tokens using provided tokenizer

    Args:
        text (str): The input text to be tokenized.
        
        tokenizer (transformers.PreTrainedTokenizer, optional): The tokenizer to use for tokenizing the text.
            Defaults to the `xlm-roberta-base` tokenizer.
            
        space_indicator (tuple): Element 0 is the char to be replaced, element 1 is the one to replace with.
            the character that the specific tokenizer replaces space with.

    Returns:
        list of str: A list of tokenized words with the "▁" character replaced by a space.
    """
    tokens = tokenizer.tokenize(text)

    # NOTE: this is not an underscore "_" its another UTF-8 character: "▁" side by side: "▁_"
    # remo, ▁ve, the, wie, ▁rd, und, ▁er, score    --->   remo, ve, the, wie, rd, und, er, score
    tokens = [token.replace(*space_indicator) for token in tokens]
    
    return tokens