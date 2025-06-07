import sentencepiece as spm

# Train the tokenizer
spm.SentencePieceTrainer.train(
    input='tamil_corpus.txt',                # Path to your Tamil training corpus
    model_prefix='tamil_tokenizer',          # Output model prefix
    vocab_size=8000,                         # Adjust based on your data
    model_type='unigram',                    # You can also try 'bpe' or 'word'
    user_defined_symbols=['<pad>', '<unk>']  # Optional
)

print("Tokenizer trained and saved as tamil_tokenizer.model and tamil_tokenizer.vocab")
