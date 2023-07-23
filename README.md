# ChatGPT plugins quickstart with Gist and Gradio Analytics

Get a todo list ChatGPT plugin up and running in under 5 minutes using Python. This plugin is designed to work in conjunction with the [ChatGPT plugins documentation](https://platform.openai.com/docs/plugins). If you do not already have plugin developer access, please [join the waitlist](https://openai.com/waitlist/plugins).

This version of the plugin includes additional functionality to log requests to a GitHub Gist and visualize the request data using Gradio.

## Setup locally

To install the required packages for this plugin, run the following command:

```bash
pip install -r requirements.txt
```

To run the plugin, enter the following command:

```bash
python main.py
```

Once the local server is running:

1. Navigate to https://chat.openai.com. 
2. In the Model drop down, select "Plugins" (note, if you don't see it there, you don't have access yet).
3. Select "Plugin store"
4. Select "Develop your own plugin"
5. Enter in `localhost:5003` since this is the URL the server is running on locally, then select "Find manifest file".

The plugin should now be installed and enabled! You can start with a question like "What is on my todo list" and then try adding something to it as well!

## Using GitHub Gist for Logging

This plugin logs each request to a GitHub Gist. To set this up:

1. Create a new Gist on GitHub. The Gist should contain a single CSV file (e.g., `requests_log.csv`).
2. Get your GitHub token and add it to the code where it says `YOUR_GITHUB_TOKEN`.
3. Replace `GIST_ID` and `FILENAME` in the code with the ID of your Gist and the name of the CSV file, respectively.

The plugin will now log each request to the Gist.

# Gradio Interface for Visualizing Request Data

This guide will help you set up a Gradio interface to visualize the request data logged to a GitHub Gist. This is a continuation of the ChatGPT plugins quickstart guide with Gist and Gradio Analytics.

## Setup

1. Install Gradio by running `pip install gradio` in your terminal.

2. Use the following template to create a Gradio interface:

```python
import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

def show_data():
    # URL of the raw CSV file in your Gist
    url = "https://gist.githubusercontent.com/YOUR_GITHUB_USERNAME/GIST_ID/raw/requests_log.csv"
    
    # Read the CSV file
    df = pd.read_csv(url)
    
    # Convert the 'Timestamp' column to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Table
    table = df

    # Chart
    fig, ax = plt.subplots()

    # Group the data by date and request type, and count the number of each type per day
    daily_counts = df.groupby([df['Timestamp'].dt.date, 'Request Type']).size().unstack()

    # Plot the data
    daily_counts.plot(kind='bar', stacked=True, ax=ax)

    # Format the x-axis
    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig

iface = gr.Interface(fn=show_data, inputs=[], outputs=["plot"])
iface.launch()
```

3. Replace `YOUR_GITHUB_USERNAME` and `GIST_ID` in the `url` with your GitHub username and the ID of your Gist, respectively.

4. Run the script. This will launch a Gradio interface in your web browser.

You can now visualize your request data in a Gradio interface! The interface displays a bar chart showing the number of each type of request per day. The data is read directly from the CSV file in your Gist.

For a live example of this setup, you can visit [this Gradio interface](https://huggingface.co/spaces/Illia56/Plugin-Analytics) and replace the `url` value with your own Gist URL.

## Setup remotely

### Cloudflare workers

### Code Sandbox

### Replit

## Getting help

If you run into issues or have questions building a plugin, please join our [Developer community forum](https://community.openai.com/c/chat-plugins/20).
