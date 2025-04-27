from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
JSON_PATH = 'detected.json'

def load_detections():
    with open(JSON_PATH, 'r') as f:
        return json.load(f)['detections']

def save_detections(detections):
    with open(JSON_PATH, 'w') as f:
        json.dump({'detections': detections}, f, indent=4)

@app.route('/')
def dashboard():
    detections = load_detections()
    detections.sort(key=lambda x: x['fixed'])  # Unfixed first
    return render_template('dashboard.html', detections=detections)

@app.route('/view/<int:detection_id>')
def view_detection(detection_id):
    detections = load_detections()
    detection = next((d for d in detections if d['id'] == detection_id), None)
    if not detection:
        return redirect(url_for('dashboard'))
    return render_template('view.html', detection=detection)

@app.route('/map')
def show_map():
    detections = load_detections()
    pending_detections = [d for d in detections if not d['fixed']]
    return render_template('map.html', detections=pending_detections)

@app.route('/fix/<int:detection_id>', methods=['POST'])
def mark_fixed(detection_id):
    detections = load_detections()
    found = False
    for d in detections:
        if d['id'] == detection_id and not d['fixed']:
            d['fixed'] = True
            found = True
            break
    save_detections(detections)
    if request.is_json:
        return jsonify({"success": found})
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:detection_id>', methods=['POST'])
def delete_detection(detection_id):
    detections = [d for d in load_detections() if d['id'] != detection_id]
    save_detections(detections)
    if request.is_json:
        return jsonify({"success": True})
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
