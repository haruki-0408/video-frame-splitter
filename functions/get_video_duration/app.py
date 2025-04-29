import boto3
import tempfile
import subprocess
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print(f"イベント: {event}")

    bucket = event["detail"]["bucket"]["name"]
    key = event["detail"]["object"]["key"]

    print(f"対象バケット: {bucket}")
    print(f"対象オブジェクトキー: {key}")

    with tempfile.NamedTemporaryFile() as tmpfile:
        s3.download_file(bucket, key, tmpfile.name)

        result = subprocess.run(
            [
                "/opt/python/ffprobe",
                "-v", "error",
                "-show_format",
                "-show_streams",
                "-print_format", "json",
                tmpfile.name
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )

        metadata = json.loads(result.stdout)
        duration = float(metadata['format']['duration'])
        video_stream = next((stream for stream in metadata['streams'] if stream.get('codec_type') == 'video'), None)
        if video_stream is None:
            raise Exception("動画ストリームが見つかりません")
        r_frame_rate = video_stream.get('r_frame_rate', '0/1')
        numerator, denominator = map(int, r_frame_rate.split('/'))
        fps = round(numerator / denominator) if denominator != 0 else 0

    duration_seconds = int(duration)
    print(f"動画の長さ（秒）: {duration_seconds}")
    print(f"動画のフレームレート（fps）: {fps}")

    return {
        'bucket': bucket,
        'key': key,
        'duration': duration_seconds,
        'fps': fps
    }
