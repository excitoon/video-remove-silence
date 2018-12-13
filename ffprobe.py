import json
import subprocess


def _get_json(path):
    result = subprocess.run(['ffprobe', path, '-loglevel', 'quiet', '-print_format', 'json', '-show_streams'], stdout=subprocess.PIPE)
    result.check_returncode()
    return json.loads(result.stdout)

def get_resolution(path):
    for stream in _get_json(path)['streams']:
        if stream['codec_type'] == 'video':
            return stream['width'], stream['height']

def get_frames(path):
    for stream in _get_json(path)['streams']:
        if stream['codec_type'] == 'video':
            if 'nb_frames' in stream:
                return int(stream['nb_frames'])

def get_duration(path):
    for stream in _get_json(path)['streams']:
        if stream['codec_type'] == 'video':
            if 'duration' in stream:
                return float(stream['duration'])
            else:
                parts = stream['tags']['DURATION'].split(':')
                assert len(parts) == 3
                return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])

def get_frame_rate(path):
    for stream in _get_json(path)['streams']:
        if stream['codec_type'] == 'video':
            if 'avg_frame_rate' in stream:
                assert stream['avg_frame_rate'].count('/') <= 1
                parts = stream['avg_frame_rate'].split('/')
                result = float(parts[0])
                if len(parts) == 2:
                    result /= float(parts[1])
                return result
