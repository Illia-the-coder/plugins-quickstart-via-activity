import json
import quart
import quart_cors
from quart import request
from github import Github, InputFileContent
import logging
import datetime

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Define the Gist ID and filename
GIST_ID = "YOUR_GIST_ID"
FILENAME = "requests_log.csv"

# Create a Github instance:
g = Github("YOUR_GITHUB_TOKEN")

# Keep track of todo's. Does not persist if Python session is restarted.
_TODOS = {}

def save_request_to_gist(request_type):
    try:
        now = datetime.datetime.now().isoformat()
        row = ['"' + now + '"', '"' + request_type + '"']

        # Get the Gist
        gist = g.get_gist(GIST_ID)

        # Get the current content of the Gist
        current_content = gist.files[FILENAME].content

        # Add the new row to the content
        new_content = current_content + "\n" + ",".join(row)

        # Update the Gist
        try:
            rate_limit_remaining = int(g.rate_limiting[0])
        except ValueError:
            rate_limit_remaining = 0

        if rate_limit_remaining > 0:
            gist.edit(files={FILENAME: InputFileContent(new_content)})
            logging.info("Gist updated successfully.")
        else:
            logging.warning("Rate limit exceeded. Gist edit not performed.")
    except Exception as e:
        logging.error(f"Error while updating Gist: {e}")

@app.post("/todos/<string:username>")
async def add_todo(username):
    request = await quart.request.get_json(force=True)
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(request["todo"])
    save_request_to_gist("add_todo")
    return quart.Response(response='OK', status=200)

@app.get("/todos/<string:username>")
async def get_todos(username):
    save_request_to_gist("get_todos")
    return quart.Response(response=json.dumps(_TODOS.get(username, [])), status=200)

@app.delete("/todos/<string:username>")
async def delete_todo(username):
    request = await quart.request.get_json(force=True)
    todo_idx = request["todo_idx"]
    # fail silently, it's a simple plugin
    if 0 <= todo_idx < len(_TODOS[username]):
        _TODOS[username].pop(todo_idx)
    save_request_to_gist("delete_todo")
    return quart.Response(response='OK', status=200)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
