from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/excel", methods=['GET', 'POST'])
def excel():
    table = ""
    head = ""
    img = ""
    head_title = ""
    table_title = ""
    img_title = ""
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            df = pd.read_excel(file)
            table = df.describe().to_html()
            head = df.head().to_html()
            head_title = "First five Rows"
            table_title = "Descriptive Statistics"

            # Plot histogram
            plt.figure(figsize=(10,8))
            df.hist()
            plt.tight_layout()  # Adjusts subplot params so that the subplot fits in the figure area

            # Save it to a BytesIO object
            buf = BytesIO()
            plt.savefig(buf, format="png")

            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            img = f"data:image/png;base64,{data}"
            img_title = "Histogram"
    return render_template('xlsx.html', table=table, head=head, img=img, head_title=head_title, table_title=table_title, img_title=img_title)

@app.route("/csv", methods=['GET', 'POST'])
def csv():
    table = ""
    head = ""
    img = ""
    head_title = ""
    table_title = ""
    img_title = ""
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            df = pd.read_csv(file)
            table = df.describe().to_html()
            head = df.head(5).to_html()
            head_title = "First five Rows"
            table_title = "Descriptive Statistics"

            # Plot histogram
            plt.figure(figsize=(8,6))
            df.hist()
            plt.tight_layout()  # Adjusts subplot params so that the subplot fits in the figure area

            # Save it to a BytesIO object
            buf = BytesIO()
            plt.savefig(buf, format="png")

            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            img = f"data:image/png;base64,{data}"
            img_title = "Histogram"
    return render_template('csv.html', table=table, head=head, img=img, head_title=head_title, table_title=table_title, img_title=img_title)

if __name__=="__main__":
    app.run(debug=True, port=8000)