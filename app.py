from flask import Flask, request, render_template, send_file
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    page_content = None

    if request.method == 'POST':
        url = request.form['url']

        try:
            response = requests.get(url)
            if response.status_code == 200:
                page_content = response.text
                # Save the content to a file in memory
                file = BytesIO(page_content.encode())
                file.seek(0)

                # Send the content as a file download
                return send_file(file, as_attachment=True, download_name='downloaded_page.txt', mimetype='text/plain')
            else:
                page_content = f"Failed to download the web page. Status code: {response.status_code}"
        except Exception as e:
            page_content = f"An error occurred: {str(e)}"

    return render_template('index.html', page_content=page_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
