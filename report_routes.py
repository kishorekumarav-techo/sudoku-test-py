from flask import Flask, jsonify, request, abort
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

reports_db = {}

# ---------------------------------------------------------
# 📌 Configure Logging
# ---------------------------------------------------------
handler = RotatingFileHandler("app.log", maxBytes=5000000, backupCount=3)
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.before_request
def log_request_info():
    app.logger.info(
        f"Incoming Request → {request.method} {request.path} | Body: {request.get_json(silent=True)}"
    )

@app.errorhandler(Exception)
def log_error(e):
    app.logger.error(f"Error occurred → {str(e)}")
    raise e


# ---------------------------------------------------------
# CRUD Endpoints (Existing)
# ---------------------------------------------------------

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

    app.logger.info(f"Report created: ID={report_id}")
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

    app.logger.info(f"Report updated: ID={report_id}")
    return jsonify({"message": "Report updated successfully", "report": report}), 200


@app.route('/reports/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    if report_id not in reports_db:
        abort(404, description="Report not found")
    del reports_db[report_id]

    app.logger.info(f"Report deleted: ID={report_id}")
    return jsonify({"message": f"Report {report_id} deleted successfully"}), 200


# ---------------------------------------------------------
# 🔥 Extra Endpoints You Added
# ---------------------------------------------------------

@app.route('/reports/<int:report_id>/status', methods=['PATCH'])
def update_report_status(report_id):
    report = reports_db.get(report_id)
    if not report:
        abort(404, description="Report not found")

    data = request.get_json()
    if not data or "status" not in data:
        abort(400, description="Missing required field: 'status'")

    report["status"] = data["status"]
    return jsonify({"message": "Status updated", "report": report}), 200


@app.route('/reports/status/<string:status>', methods=['GET'])
def get_reports_by_status(status):
    filtered = [r for r in reports_db.values() if r["status"] == status]
    return jsonify(filtered), 200


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


@app.route('/reports', methods=['DELETE'])
def delete_all_reports():
    confirm = request.args.get("confirm", "false").lower()
    if confirm != "true":
        abort(400, description="Add '?confirm=true' to delete all reports")

    reports_db.clear()
    app.logger.warning("All reports deleted!")
    return jsonify({"message": "All reports deleted"}), 200


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


# ---------------------------------------------------------
# 🌟 NEW ENDPOINTS ADDED BELOW
# ---------------------------------------------------------

# 6️⃣ Update only the summary
@app.route('/reports/<int:report_id>/summary', methods=['PATCH'])
def update_summary(report_id):
    report = reports_db.get(report_id)
    if not report:
        abort(404, description="Report not found")

    data = request.get_json()
    if not data or "summary" not in data:
        abort(400, description="Missing field: summary")

    report["summary"] = data["summary"]
    return jsonify({"message": "Summary updated", "report": report}), 200


# 7️⃣ Reset all reports to a given status
@app.route('/reports/reset-status/<string:status>', methods=['PATCH'])
def reset_status(status):
    for r in reports_db.values():
        r["status"] = status

    app.logger.info(f"All reports status set to {status}")
    return jsonify({"message": f"All reports updated to status '{status}'"}), 200


# 8️⃣ Paginated results
@app.route('/reports/paginated', methods=['GET'])
def get_paginated_reports():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    start = (page - 1) * limit
    end = start + limit

    data = list(reports_db.values())[start:end]

    return jsonify({
        "page": page,
        "limit": limit,
        "results": data
    }), 200


# 9️⃣ Advanced stats
@app.route('/reports/stats', methods=['GET'])
def report_stats():
    summaries = [len(r["summary"]) for r in reports_db.values()]

    if not summaries:
        return jsonify({"message": "No reports available"}), 200

    return jsonify({
        "total_reports": len(summaries),
        "min_summary_length": min(summaries),
        "max_summary_length": max(summaries),
        "average_summary_length": sum(summaries) / len(summaries)
    }), 200


# 🔟 Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200


if __name__ == '__main__':
    app.run(debug=True)
