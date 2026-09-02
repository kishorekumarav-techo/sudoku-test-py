from flask import Flask, jsonify, request, abort

app = Flask(__name__)

reports_db = {}

@app.route('/reports', methods=['POST'])
def create_report():
    data = request.get_json()
    if not data or 'file_name' not in data:
        abort(400, description="Invalid input: 'file_name' is required")

    report_id = len(reports_db) + 1
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

@app.route('/reports/v2/<int:report_id>', methods=['DELETE'])
def delete_report_v2(report_id):
    if report_id not in reports_db:
        abort(404, description="Report not found")
    del reports_db[report_id]
    return jsonify({"message": f"Report {report_id} deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
