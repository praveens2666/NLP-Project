from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer
import sqlite3
import sentencepiece as spm
import os

app = Flask(__name__)
tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")

# Load SentencePiece model
sp = spm.SentencePieceProcessor()
sp.load("tamil_tokenizer.model")  # make sure the model is in the same folder

# creating tokens

def tokenize(inplines):
  res={}
  for i in range(len(inplines)):
    line=inplines[i]
    line=line.replace("\n","")
    line=line.replace("\t"," ")
    if line[0]=='#':
      continue
    elif line[1]=='-':
      a=line
      a=a.replace("\n","")
      a=a.replace("\t"," ")
      a=a.replace(" ","")
      dif=int(line[2])-int(line[0])+i
      en=dif+1
      split=[]
      while(i<en):
        i+=1
        split.append(inplines[i][2:].replace("\n",""))
      res[a[3:]]=split
      #res[inplines[i-1][2:]]=[inplines[i-1][2:]]
      i-=1
    else:
      res[line[2:]]=[line[2:]]
  return res






def getTokens(file_path):
  with open(file_path,"r",encoding="utf-8") as file:
      inplines=file.readlines()
      return tokenize(inplines)
tokens=getTokens("filtered_output_file.txt")





special_splits = {
    "நாடாளுமன்றமும்": ["நாடாளுமன்றம்", "உம்"],
    "நீட்டிஉள்ளே":['நீட்டி', 'உள்ளே']
}

special_splits=tokens

# Tokenizer class for SentencePiece
class TamilTokenizer:
    def __init__(self, sp_model, special_splits):
        self.sp = sp_model
        self.special_splits = special_splits

    def tokenize(self, text):
        for punct in ['.', ',', '!', '?', ';', ':', '"', "'", '(', ')', '[', ']']:
            text = text.replace(punct, f" {punct}")
        words = text.split()
        segmented_words = []
        for word in words:
            if word in self.special_splits:
                segmented_words.extend(self.special_splits[word])
            else:
                pieces = self.sp.encode_as_pieces(word)
                filtered = [p for p in pieces if len(p) > 1]
                segmented_words.extend(filtered if filtered else [word])
        return segmented_words

tamil_tokenizer = TamilTokenizer(sp, special_splits)

# SQLite DB for saving corrections
def init_db():
    conn = sqlite3.connect("tokenizer.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS corrections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original TEXT,
            corrected TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/tokenize', methods=['POST'])
def tokenize():
    algo = request.form.get("algorithm")
    text = request.form.get("text")
    file = request.files.get("file")

    if file:
        text = file.read().decode("utf-8").strip()

    if not text or not algo:
        return jsonify({"error": "Missing input"}), 400

    if algo == "xlmr":
        tokens = tokenizer.tokenize(text)
    elif algo == "sentencepiece":
        tokens = tamil_tokenizer.tokenize(text)
    else:
        return jsonify({"error": "Unknown algorithm"}), 400

    return jsonify({"tokens": tokens})

@app.route('/save_correction', methods=['POST'])
def save_correction():
    data = request.json
    original = " ".join(data.get("original", []))
    corrected = " ".join(data.get("corrected", []))

    if not original or not corrected:
        return jsonify({"message": "Invalid correction data"}), 400

    conn = sqlite3.connect("tokenizer.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO corrections (original, corrected) VALUES (?, ?)", (original, corrected))
    conn.commit()
    conn.close()

    return jsonify({"message": "Correction saved successfully"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
