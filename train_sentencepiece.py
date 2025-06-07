import sentencepiece as spm

# Path to the training data (a text file containing Tamil text for training)
input_file = 'path_to_your_input_corpus.txt'  # Replace with your corpus path
model_prefix = 'tamil_model'

# Train the SentencePiece model
spm.SentencePieceTrainer.train(f'--input={input_file} --model_prefix={model_prefix} --vocab_size=8000')

print("Model training complete.")
