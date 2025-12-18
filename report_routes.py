from flask import Flask, jsonify, request, abort

app = Flask(__name__)

reports_db = {}

@app.route('/reports', methods=['POST'])
def create_report():
    data = request.get_json()
    if not data or 'file_name' not in data:
        abort(400, description="Invalid input: 'file_name' is required")

    report_id = (max(reports_db.keys()) + 1) if reports_db else 1
    reports_db[report_id] = {
        "id": report_id,
        "file_name": data.get("file_name"),
        "status": data.get("status", "pending"),
        "summary": data.get("summary", "")
    }
    return jsonify({"message": "Report created successfully", "report": reports_db[report_id]}), 201


@app.route('/reports', methods=['GET'])
def get_all_reports():
    return jsonify(list(reports_db.values())), 200

    
@app.route('/reports/<int:report_id>', methods=['GET'])
def get_report(report_id):
    report = reports_db.get(report_id)
    if not report:
        abort(404, description="Report not found")
    return jsonify(report), 200


@app.route('/reports/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    report = reports_db.get(report_id)
    if not report:
        abort(404, description="Report not found")

    data = request.get_json()
    if not data:
        abort(400, description="Invalid input: no JSON payload")

    report["file_name"] = data.get("file_name", report["file_name"])
    report["status"] = data.get("status", report["status"])
    report["summary"] = data.get("summary", report["summary"])

    return jsonify({"message": "Report updated successfully", "report": report}), 200


@app.route('/reports/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    if report_id not in reports_db:
        abort(404, description="Report not found")
    del reports_db[report_id]
    return jsonify({"message": f"Report {report_id} deleted successfully"}), 200


# ---------------------------------------------------------
# 🔥 New Endpoints Added
# ---------------------------------------------------------

# 1️⃣ Patch only the report status
@app.route('/reports/<int:report_id>/status', methods=['PATCH'])
def update_report_status(report_id):
    report = reports_db.get(report_id)
    if not report:
        abort(404, description="Report not found")

    data = request.get_json()
    if not data or "status" not in data:
        abort(400, description="Missing required field: 'status'")

    new_status = data["status"]
    valid_statuses = {"pending", "in_progress", "completed", "failed"}
    if not isinstance(new_status, str) or new_status not in valid_statuses:
        abort(400, description=f"Invalid status: '{new_status}'. Must be one of {list(valid_statuses)}.")
    report["status"] = new_status

    return jsonify({"message": "Status updated", "report": report}), 200


# 2️⃣ Get reports by status
@app.route('/reports/status/<string:status>', methods=['GET'])
def get_reports_by_status(status):
    filtered = [r for r in reports_db.values() if r["status"] == status]
    return jsonify(filtered), 200


# 3️⃣ Search reports by keyword in filename or summary
@app.route('/reports/search', methods=['GET'])
def search_reports():
    keyword = request.args.get("q", "").lower()
    if not keyword:
        abort(400, description="Query parameter 'q' is required")

    results = [
        r for r in reports_db.values()
        if keyword in r["file_name"].lower() or keyword in r["summary"].lower()
    ]
    return jsonify(results), 200


# 4️⃣ Delete all reports (requires confirm=true)
@app.route('/reports', methods=['DELETE'])
def delete_all_reports():
    confirm = request.args.get("confirm", "false").lower()
    if confirm != "true":
        abort(400, description="Add '?confirm=true' to delete all reports")

    reports_db.clear()
    return jsonify({"message": "All reports deleted"}), 200


# 5️⃣ Count reports (total + by status)
@app.route('/reports/count', methods=['GET'])
def count_reports():
    total = len(reports_db)
    status_counts = {}

    for r in reports_db.values():
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1

    return jsonify({
        "total_reports": total,
        "by_status": status_counts
    }), 200


if __name__ == '__main__':
    app.run()
