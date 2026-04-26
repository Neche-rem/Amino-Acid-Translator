from flask import Flask, render_template, request, jsonify
import csv
import io

app = Flask(__name__)

CODON_TABLE = {
    "UUU":"F","UUC":"F","UUA":"L","UUG":"L",
    "UCU":"S","UCC":"S","UCA":"S","UCG":"S",
    "UAU":"Y","UAC":"Y","UAA":"STOP","UAG":"STOP",
    "UGU":"C","UGC":"C","UGA":"STOP","UGG":"W",

    "CUU":"L","CUC":"L","CUA":"L","CUG":"L",
    "CCU":"P","CCC":"P","CCA":"P","CCG":"P",
    "CAU":"H","CAC":"H","CAA":"Q","CAG":"Q",
    "CGU":"R","CGC":"R","CGA":"R","CGG":"R",

    "AUU":"I","AUC":"I","AUA":"I","AUG":"M",
    "ACU":"T","ACC":"T","ACA":"T","ACG":"T",
    "AAU":"N","AAC":"N","AAA":"K","AAG":"K",
    "AGU":"S","AGC":"S","AGA":"R","AGG":"R",

    "GUU":"V","GUC":"V","GUA":"V","GUG":"V",
    "GCU":"A","GCC":"A","GCA":"A","GCG":"A",
    "GAU":"D","GAC":"D","GAA":"E","GAG":"E",
    "GGU":"G","GGC":"G","GGA":"G","GGG":"G"
}

def dna_to_rna(seq):
    return seq.replace("T", "U")

def translate(seq):
    protein = []
    start = False

    for i in range(0, len(seq), 3):
        codon = seq[i:i+3]

        if len(codon) < 3:
            break

        if codon == "AUG":
            start = True

        if not start:
            continue

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
