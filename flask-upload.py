import os
from flask import Flask, render_template, request, send_file
APP = Flask(__name__)

@APP.route('/upload')
def upload_file():
    return render_template('upload.html')

@APP.route('/uploader', methods=['GET', 'POST'])
def uploader_file():
    if request.method == 'POST':
        source_file = request.files['file']
        source_file_name = source_file.filename
        source_file.save(os.path.join('/mnt/', source_file_name))

        searchquery = 'ERROR'

        with open(os.path.join('/mnt/', source_file_name)) as source_file:
            with open(os.path.join('/mnt/', 'output.txt'), 'a') as output_file:

                lines = source_file.readlines()
                for line in lines:
                    if line.startswith(searchquery):
                        output_file.write(line)

        return_string = ('<html><body>File: ' + source_file_name
                         + ' Success!</br><a href="/download" target="blank"><button class="btn'
                         + 'btn-default">Download output</button></a></p></body></html>')

        return return_string
    return 'POST fail'

@APP.route('/download')
def download_file():
    try:
        return send_file('/mnt/output.txt', attachment_filename='output.txt')
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000, debug=True)
