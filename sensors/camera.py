"""Sky camera — capture, analysis, and MJPEG streaming using RPi Camera v1.3 (OV5647)."""
import subprocess
import os
import time
import threading
from datetime import datetime

DEFAULT_PATH = '/tmp/hics_sky_latest.jpg'

# Set to True while MJPEG streaming is active; background capture respects this.
streaming = threading.Event()


def capture_sky(path=DEFAULT_PATH, width=1296, height=972):
    """Capture a still frame with rpicam-still. Returns True on success."""
    try:
        result = subprocess.run(
            ['rpicam-still', '--nopreview', '-n',
             '--width', str(width), '--height', str(height),
             '--quality', '70', '-o', path],
            timeout=15, capture_output=True
        )
        return result.returncode == 0 and os.path.exists(path) and os.path.getsize(path) > 5000
    except Exception:
        return False


def sky_analysis(path=DEFAULT_PATH):
    """
    Return basic sky metrics from a captured JPEG.

    Returns dict with keys: brightness, cloud_cover_pct, condition,
    r_mean, g_mean, b_mean, captured_at.
    Requires Pillow; falls back to stub if unavailable.
    """
    result = {
        'brightness': None,
        'cloud_cover_pct': None,
        'condition': 'unknown',
        'r_mean': None, 'g_mean': None, 'b_mean': None,
        'captured_at': None,
    }
    if not os.path.exists(path):
        return result

    result['captured_at'] = datetime.fromtimestamp(os.path.getmtime(path)).isoformat()

    try:
        from PIL import Image
        img = Image.open(path).convert('RGB')
        # Analyse a 320×240 thumbnail — fast and sufficient
        thumb = img.resize((320, 240), Image.BILINEAR)
        pixels = list(thumb.getdata())
        n = len(pixels)
        r_sum = sum(p[0] for p in pixels)
        g_sum = sum(p[1] for p in pixels)
        b_sum = sum(p[2] for p in pixels)
        r_mean = r_sum / n
        g_mean = g_sum / n
        b_mean = b_sum / n
        brightness = int((r_mean + g_mean + b_mean) / 3)

        # Cloud detection: gray/white pixels have R≈G≈B and high brightness.
        # Blue sky pixels have B significantly > R and G.
        # Count pixels where (R+G)/2 > B + 15 (not dominantly blue → cloud/haze)
        cloud_pixels = sum(1 for p in pixels if (p[0] + p[1]) / 2 > p[2] + 15)
        cloud_cover_pct = int(cloud_pixels / n * 100)

        if brightness < 25:
            condition = 'night'
        elif cloud_cover_pct > 70:
            condition = 'overcast'
        elif cloud_cover_pct > 30:
            condition = 'partly_cloudy'
        else:
            condition = 'clear'

        result.update({
            'brightness': brightness,
            'cloud_cover_pct': cloud_cover_pct,
            'condition': condition,
            'r_mean': round(r_mean, 1),
            'g_mean': round(g_mean, 1),
            'b_mean': round(b_mean, 1),
        })
    except Exception:
        pass

    return result


def stream_frames(width=640, height=480, fps=10):
    """
    Generator yielding MJPEG multipart chunks for Flask Response streaming.
    Sets the module-level `streaming` event while active so background
    capture skips rather than conflicting with the camera.
    """
    streaming.set()
    proc = None
    try:
        cmd = ['rpicam-vid', '--codec', 'mjpeg', '-n',
               '--framerate', str(fps),
               '--width', str(width), '--height', str(height),
               '-t', '0', '-o', '-']
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        buf = b''
        while True:
            chunk = proc.stdout.read(8192)
            if not chunk:
                break
            buf += chunk
            while True:
                start = buf.find(b'\xff\xd8')
                end   = buf.find(b'\xff\xd9', start + 2) if start >= 0 else -1
                if start >= 0 and end >= 0:
                    frame = buf[start:end + 2]
                    buf = buf[end + 2:]
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                else:
                    break
    except GeneratorExit:
        pass
    finally:
        if proc:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
        streaming.clear()
