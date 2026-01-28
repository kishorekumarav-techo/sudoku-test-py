from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for notes
notes = []
note_id_counter = 1


@app.route("/notes", methods=["POST"])
def create_note():
    global note_id_counter
    data = request.get_json()

    if not data or "content" not in data:
        return jsonify({"error": "Note content is required"}), 400

    note = {
        "id": note_id_counter,
        "content": data["content"]
    }
    notes.append(note)
    note_id_counter += 1

    return jsonify(note), 201


@app.route("/notes", methods=["GET"])
def get_notes():
    return jsonify(notes), 200


@app.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    for note in notes:
        if note["id"] == note_id:
            return jsonify(note), 200
    return jsonify({"error": "Note not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
