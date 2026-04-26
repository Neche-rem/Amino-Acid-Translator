from flask import Flask, render_template, request, jsonify
import csv
import io

app = Flask(__name__)

CODON_TABLE = {
    "AUG": "M", "UUU": "F", "UUC": "F",
    "UUA": "L", "UUG": "L",
    "UAA": "STOP", "UAG": "STOP", "UGA": "STOP"
}

def dna_to_rna(seq):
    return seq.replace("T", "U")

def translate(seq):
    protein = []

    for i in range(0, len(seq), 3):
        codon = seq[i:i+3]
        if len(codon) < 3:
            break

        amino = CODON_TABLE.get(codon, "?")

        if amino == "STOP":
            break

        protein.append(amino)

    return "".join(protein)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate_route():
    if "file" in request.files:
        file = request.files["file"]
        content = file.read().decode("utf-8")

        reader = csv.reader(io.StringIO(content))
        sequence = "".join([row[0] for row in reader])

    else:
        data = request.get_json()
        sequence = data.get("sequence", "")

    sequence = sequence.upper().strip()

    if "T" in sequence:
        sequence = dna_to_rna(sequence)

    protein = translate(sequence)

    return jsonify({
        "protein": protein
    })

if __name__ == "__main__":
    app.run(debug=True)
