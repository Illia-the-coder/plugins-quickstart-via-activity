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

## Visualizing Request Data with Gradio

You can visualize the request data logged to the Gist using Gradio. To do this:

1. Install Gradio by running `pip install gradio`.
2. Run the Gradio interface code provided in the `show_data` function.
3. Replace the `url` in the `show_data` function with the raw URL of your Gist's CSV file.

You can now visualize your request data in a Gradio interface!

## Setup remotely

### Cloudflare workers

### Code Sandbox

### Replit

## Getting help

If you run into issues or have questions building a plugin, please join our [Developer community forum](https://community.openai.com/c/chat-plugins/20).
