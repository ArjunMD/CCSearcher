from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load the Excel file. Replace 'data.xlsx' with your actual file name.
excel_file = 'data.xlsx'

# Read both sheets.
df_mcc = pd.read_excel(excel_file, sheet_name='Complete MCC List', engine='openpyxl', header=None)
df_cc = pd.read_excel(excel_file, sheet_name='Complete CC List', engine='openpyxl', header=None)

@app.route('/', methods=['GET', 'POST'])
def index():
    query = ''
    # Initialize as empty DataFrames instead of lists
    results_mcc = pd.DataFrame()
    results_cc = pd.DataFrame()
    
    if request.method == 'POST':
        query = request.form.get('query', '')
        if query:
            results_mcc = df_mcc[df_mcc.iloc[:, 1].astype(str).str.contains(query, case=False, na=False)]
            results_cc = df_cc[df_cc.iloc[:, 1].astype(str).str.contains(query, case=False, na=False)]
    
    return render_template(
        'index.html',
        query=query,
        results_mcc=results_mcc.to_dict(orient='records'),
        results_cc=results_cc.to_dict(orient='records')
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

