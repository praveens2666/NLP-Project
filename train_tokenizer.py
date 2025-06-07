import sentencepiece as spm

spm.SentencePieceTrainer.train(
    input='tamil_corpus.txt',
    model_prefix='tamil_tokenizer',
    vocab_size=800,
    model_type='bpe',  # You can also try 'unigram'
    character_coverage=1.0,
    pad_id=0,
    unk_id=1,
    bos_id=2,
    eos_id=3,
    user_defined_symbols=[]
)

print("✅ Tokenizer trained successfully!")
