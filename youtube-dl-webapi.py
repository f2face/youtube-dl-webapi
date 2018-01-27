from flask import Flask, jsonify, request
from subprocess import call
import youtube_dl

app = Flask(__name__)

ydl_opts = {}

@app.route('/', methods = ['GET'])
def retrieve_video_informations():
    required_params = ['url']
    missing_params = [key for key in required_params if key not in request.args.keys()]

    if len(missing_params) == 0 and len(request.args['url']) > 0:
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(
                    request.args['url'],
                    download=False
                )
                return jsonify(result)
        except Exception as e:
            resp = {
                "status":"failure",
                "error": "missing parameters",
                "message": str(e)
            }
            return jsonify(resp)
    else:
        resp = {
                "status":"failure",
                "error" : "missing parameters",
                "message" : "Provide %s in request" %(missing_params)
            }
        return jsonify(resp)


if __name__ == '__main__':
    # IP address where this web service will be running on.
    host = '0.0.0.0'

    # Port number where this web service will be running on.
    port = 8000

    app.run(host=host, port=port)