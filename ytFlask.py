from flask import Flask, request, render_template, jsonify,send_file
from down import list_formats, download_video, extractTypes
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-formats', methods=['POST'])
def get_formats():
    try:
        data = request.json
        video_url = data.get('url')
        if not video_url:
            return jsonify({'error': 'URL is required'}), 400
        
        info = list_formats(video_url)
        title = info.get('title')
        thumbnail = info.get('thumbnail')
        print(info)
        formats = extractTypes(info)
        return jsonify({'formats': formats,'title':title,'thumbnail':thumbnail})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.json
        video_url = data.get('url')
        format_code = data.get('format_code')
        if not video_url or not format_code:
            return jsonify({'error': 'URL and format code are required'}), 400

        # Call the download_video function to save the file
        file_path = download_video(video_url, format_code)
        print(file_path)
        time.sleep(2)
        # Ensure the file exists before sending
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found after download'}), 500

        # Send the file to the frontend as an attachment
        return send_file(file_path, as_attachment=True, download_name=os.path.basename(file_path))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def cleanup_downloads():
    now = time.time()
    print("Calling clean up",now)
    DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "public")
    for filename in os.listdir(DOWNLOAD_FOLDER):
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        if os.path.isfile(file_path) and now - os.path.getmtime(file_path) > 3600:
            os.remove(file_path)
scheduler= BackgroundScheduler()
scheduler.add_job(cleanup_downloads, 'interval', minutes=1)
scheduler.start()
if __name__ == "__main__":
    
    app.run(debug=False,port=3001)
