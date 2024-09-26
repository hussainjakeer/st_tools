# import os
# import pandas as pd
# from flask import Flask, render_template, request, session, redirect, url_for, jsonify
# import requests
# from flask_socketio import SocketIO, emit
# from bs4 import BeautifulSoup
# import threading
# import time


# app = Flask(__name__)
# app.secret_key = 'your_secret_key_shdvcfjbsdjcfiuswerhtfjkk#%^%^%JKNKJBKIVNdnfkgkjdnfgvk'  # Replace with a strong secret key
# # csv_file = 'data.csv'
# socketio = SocketIO(app)


# # Initialize the data frame
# df = pd.DataFrame(columns=["URLS", 'Tricker symbol', 'Stock type',
#                            'Stock name', 'Current price', 'Buy price',
#                            'target price', 'Review'])




# # Global list to track unique string inputs
# # unique_urls = df["URLS"].tolist()


# # Function to fetch stock data from a URL
# def fetch_data(url):
#     response = requests.get(url)
#     if response.status_code != 200:
#         print("Error fetching data")
#         return None

#     soup = BeautifulSoup(response.text, "html.parser")

#     ticker_symbol = url.split("/")[-1].split(":")[0]
#     stock_type = url.split("/")[-1].split(":")[1].split("?")[0]
#     stock_name = soup.find("div", {"class": "zzDege"}).text
#     price = soup.find("div", {"class": "YMlKec fxKbKc"}).text.strip()

#     if "₹" in price:
#         price = price.split("₹")[-1]
#     price = price.replace(',', "")
#     price = float(price.strip())

#     return (ticker_symbol, stock_type, stock_name, price)

# # Function to periodically update stock prices
# def update_stock_prices():
#     while True:
#         print("-----------")
#         print(time.ctime())
#         print("-----------")
#         print("1")
        
        
#         for index in range(len(df)):
#             print(index)
#             url = df.iloc[index]['URLS']
#             new_data = fetch_data(url)
#             if new_data:
#                 df.at[index, 'Current price'] = new_data[3]
#                 socketio.emit('update_table', df.to_dict(orient='records'))
#                 current_price = float(new_data[3])
#                 print(current_price)

#                 buy_price = float(df.iloc[index]['Buy price'])
#                 target_price = float(df.iloc[index]['target price'])
#                 # Emit the updated data to clients
#                 # socketio.emit('update', {'index': index, 'current_price': new_data[3]})
                
#                 # Check for price conditions and notify if met
#                 if current_price <= buy_price:
#                     socketio.emit('notify', {
#                         'title': f"{new_data[2]} is ready to buy!",
#                         'body': f"{new_data[2]} ({new_data[1]}) has dropped to {new_data[3]}."
#                     })
#                 if current_price >= target_price:
#                     socketio.emit('notify', {
#                         'title': f"{new_data[2]} is ready to sell!",
#                         'body': f"{new_data[2]} ({new_data[1]}) has risen to {new_data[3]}."
#                     })
        
#         time.sleep(10)  # Wait for 10 sec before the next update

# # Start the background thread for updating stock prices
# threading.Thread(target=update_stock_prices, daemon=True).start()

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     global df
#     if request.method == 'POST':
#         url_input = request.form['url_input']
#         buy_input = request.form['buy_input']
#         target_input = request.form['target_input']
#         text_input = request.form['text_input']
        
#         # Check if the string input already exists
#         if url_input in df['URLS'].values:
#             session['message'] = 'String input already exists!'
#             return redirect(url_for('home'))
        
#         data_ = fetch_data(url_input)
#         if data_:
#             tricker_symbol, stock_type, stock_name, price = data_

#             # Save to CSV
#             new_data = pd.DataFrame([[url_input, tricker_symbol, stock_type, stock_name,
#                                     price, buy_input, target_input, text_input]],
#                                     columns=["URLS", 'Tricker symbol', 'Stock type', 
#                             'Stock name', 'Current price', 'Buy price',
#                             'target price', 'Review'])
#             df = pd.concat([df, new_data], ignore_index=True)
           
#             # # Update the global list
#             # unique_urls.append(url_input)


#             # Store a message in session to confirm submission
#             session['message'] = 'Data submitted successfully!'
#             return redirect(url_for('home'))

    
    
#     if len(df) < 1:
#         return render_template('form.html', length_ = len(df))

#     return render_template('form.html', length_ = len(df),  
#                             message=session.pop('message', None))

# @app.route('/get_data')
# def get_data():
#     return jsonify(df.to_dict(orient='records'))

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')



# if __name__ == '__main__':
#     socketio.run(app, debug=True)




import os
import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import requests
from flask_socketio import SocketIO, emit
from bs4 import BeautifulSoup
import threading
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
socketio = SocketIO(app)

# Initialize the DataFrame to store stock data
df = pd.DataFrame(columns=["URLS", 'Tricker symbol', 'Stock type',
                           'Stock name', 'Current price', 'Buy price',
                           'target price', 'Review'])

# Function to fetch stock data from a given URL
def fetch_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching data")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    ticker_symbol = url.split("/")[-1].split(":")[0]
    stock_type = url.split("/")[-1].split(":")[1].split("?")[0]
    stock_name = soup.find("div", {"class": "zzDege"}).text
    price = soup.find("div", {"class": "YMlKec fxKbKc"}).text.strip()

    if "₹" in price:
        price = price.split("₹")[-1]
    price = price.replace(',', "").strip()
    price = float(price)

    return (ticker_symbol, stock_type, stock_name, price)

# Function to periodically update stock prices
def update_stock_prices():
    while True:
        for index in range(len(df)):
            url = df.iloc[index]['URLS']
            new_data = fetch_data(url)
            if new_data:
                df.at[index, 'Current price'] = new_data[3]
                socketio.emit('update_table', df.to_dict(orient='records'))
                
                current_price = float(new_data[3])
                buy_price = float(df.iloc[index]['Buy price'])
                target_price = float(df.iloc[index]['target price'])

                # Notify if current price meets buy/sell conditions
                if current_price <= buy_price:
                    socketio.emit('notify', {
                        'title': f"{new_data[2]} is ready to buy!",
                        'body': f"{new_data[2]} ({new_data[1]}) has dropped to {new_data[3]}."
                    })
                if current_price >= target_price:
                    socketio.emit('notify', {
                        'title': f"{new_data[2]} is ready to sell!",
                        'body': f"{new_data[2]} ({new_data[1]}) has risen to {new_data[3]}."
                    })
        
        time.sleep(10)  # Wait for 10 seconds before the next update

# Start the background thread for updating stock prices
threading.Thread(target=update_stock_prices, daemon=True).start()

@app.route('/', methods=['GET', 'POST'])
def home():
    global df
    if request.method == 'POST':
        url_input = request.form['url_input']
        buy_input = request.form['buy_input']
        target_input = request.form['target_input']
        text_input = request.form['text_input']
        
        # Check for duplicate URL entries
        if url_input in df['URLS'].values:
            session['message'] = 'String input already exists!'
            return redirect(url_for('home'))
        
        data_ = fetch_data(url_input)
        if data_:
            tricker_symbol, stock_type, stock_name, price = data_
            new_data = pd.DataFrame([[url_input, tricker_symbol, stock_type, stock_name,
                                       price, buy_input, target_input, text_input]],
                                    columns=["URLS", 'Tricker symbol', 'Stock type', 
                                             'Stock name', 'Current price', 'Buy price',
                                             'target price', 'Review'])
            df = pd.concat([df, new_data], ignore_index=True)
            session['message'] = 'Data submitted successfully!'
            return redirect(url_for('home'))

    return render_template('form.html', length=len(df),  
                           message=session.pop('message', None))

@app.route('/get_data')
def get_data():
    return jsonify(df.to_dict(orient='records'))

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
