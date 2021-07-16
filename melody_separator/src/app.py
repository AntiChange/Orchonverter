from flask import Flask
# from gevent.pywsgi import WSGIServer

from separate_bach10 import main

app = Flask(__name__)

@app.route('/')
def hello_world():
    inputfile = 'input/05-DieNacht_fast.wav'
    outdir = 'output'
    model = 'model_fft_rwc_synth_one_aug_more_4096_blind_nomp_all.pkl'
    main(inputfile, outdir, model)
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(port = 8000, host='0.0.0.0',debug=True)
    # http_server = WSGIServer(('0.0.0.0', 8000), app)
    # http_server.serve_forever()
#     # uvicorn.run(app, port=8000, host='0.0.0.0')
#     # server run on http://127.0.0.1:8000/