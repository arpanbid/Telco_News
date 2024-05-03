from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
import filter_data



country_list = filter_data.country_lists()
country_list.sort()
country_list.insert(0,'All')
dropdown_options = []

for country in country_list:
    dropdown_options.append((country, country))







app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        keywords = request.form.get('keywords')
        dropdown = request.form.get('dropdown')
        end_date = request.form.get('end_date')
        
        filtered_df = filter_data.read_data(str(start_date), str(end_date), (keywords), (dropdown))
        filtered_df = filtered_df.iloc[:50, :] 
        
        filtered_df.to_excel("filtered_news.xlsx", index=False)
      
        return render_template('table.html', count = len(filtered_df), tables=[filtered_df.to_html(classes='data')], titles=filtered_df.columns.values)
        
        
        
    # Generate the form
    return render_template('page.html',
                           date1= '2018-01-01', 
                           string1='',
                           string2='',
                           dropdown_options = dropdown_options,
                           dropdown='',
                           date2= datetime.today().strftime('%Y-%m-%d'))

@app.route('/updatenews', methods=['GET'])
def update_news():
    if request.method == 'GET':
        import update_TP
        count = update_TP.news_added
    return render_template('update_success.html', count=str(count))

@app.route('/download', methods=['GET'])
def download():
    return send_file('filtered_news.xlsx', as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
