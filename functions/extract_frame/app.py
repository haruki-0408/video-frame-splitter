import boto3
import os
import tempfile
import subprocess
import glob

s3 = boto3.client('s3')

OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET')

def lambda_handler(event, context):
    print(f"受信イベント: {event}")

    bucket = event['bucket']
    key = event['key']
    second = event['second']
    fps = event['fps']

    filename = os.path.basename(key)
    base_filename = os.path.splitext(filename)[0]

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, filename)
        s3.download_file(bucket, key, input_path)

        output_pattern = os.path.join(tmpdir, "%03d.jpg")

        subprocess.run(
            [
                "/opt/python/ffmpeg",
                "-ss", str(second),
                "-i", input_path,
                "-t", "1",
                "-vf", f"fps={fps}",
                "-q:v", "2",
                output_pattern
            ],
            check=True
        )

        for filepath in glob.glob(os.path.join(tmpdir, "*.jpg")):
            frame_number = os.path.splitext(os.path.basename(filepath))[0]
            output_key = f"thumbnails/{base_filename}/{second:03d}_{frame_number}.jpg"
            s3.upload_file(filepath, OUTPUT_BUCKET, output_key)
            print(f"保存完了: s3://{OUTPUT_BUCKET}/{output_key}")
