import yt_dlp
import os

def list_formats(video_url):
    ydl_opts = {'listformats': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(video_url, download=False)



def download_video(video_url, format_code):
    # Specify the output directory
    output_dir = os.path.join(os.getcwd(), "public")
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

    # Set yt-dlp options to save the file in the specified directory
    ydl_opts = {
        'format': f"{format_code}+bestaudio/best",
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s')  # Save with video title as name
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(video_url, download=True)
        file_path = ydl.prepare_filename(result)
        return file_path
        return result['title']  # Return video title for later reference

def extractTypes(info):
    result=[]
    for fmt in info['formats']:
        ext = fmt['ext']
        if ext in ('mp4', 'mp3'):
            format_id = fmt['format_id']
            resolution = fmt.get('resolution', 'audio-only')
            filesize = fmt.get('filesize')
            filesize_mb = f"{filesize // (1024 * 1024)} MB" if isinstance(filesize, int) else 'N/A'
            has_audio = 'Yes' if fmt.get('acodec') != 'none' else 'No'
            stream_type = "Audio/Video" if has_audio == 'Yes' else "Video-only"
            result.append({
                'ID': format_id,
                'Ext': ext,
                'Resolution': resolution,
                'Type': stream_type,
                'Size': filesize_mb
            })
            # print(f"{format_id:<5} | {ext:<3} | {resolution:<10} | {stream_type:<10} | {filesize_mb:<8}")
    return result


