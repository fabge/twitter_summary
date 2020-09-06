import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import base64

with open(r"tweet_collection.pickle", "rb") as input_file:
    tweet_collection = pickle.load(input_file)

df = pd.DataFrame([x['user']['screen_name'] for x in tweet_collection])[0].value_counts()[:60]
df.sort_values(inplace=True)
plot = df.plot(kind='barh', figsize=(12,12))
figure = plot.get_figure()
figure.savefig('output.png')

tweet_collection = []

with open(r"tweet_collection.pickle", "wb") as output_file:
    pickle.dump(tweet_collection, output_file)

import time
time.sleep(5)

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

with open("output.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

message = Mail(
    from_email='geiger.fabian@outlook.com',
    to_emails='geiger.fabian93@gmail.com',
    subject='Twitter Analysis',
    html_content=f'<img alt="Twitter Analysis" width="100%" src="data:image/png;base64,{encoded_string}"/>')
try:
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
