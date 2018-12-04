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
            return int(stream['nb_frames'])

def get_duration(path):
    for stream in _get_json(path)['streams']:
        if stream['codec_type'] == 'video':
            return float(stream['duration'])
