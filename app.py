from flask import Flask, request, render_template_string, Response
import base64
import os

app = Flask(__name__)
NODES_FILE = 'nodes.txt'

def get_nodes():
    if not os.path.exists(NODES_FILE):
        return []
    with open(NODES_FILE, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def save_nodes(nodes):
    with open(NODES_FILE, 'w') as f:
        for node in nodes:
            f.write(node + "\n")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <title>订阅管理面板</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; }
        .container { background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        .link-box { background-color: #e3f2fd; padding: 15px; border-left: 4px solid #2196F3; margin-bottom: 20px; border-radius: 4px; word-break: break-all;}
        .form-group { display: flex; gap: 10px; margin-bottom: 20px; }
        input[type="text"] { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; color: white; font-weight: bold; }
        .btn-add { background-color: #4CAF50; }
        .btn-delete { background-color: #f44336; padding: 5px 10px; }
        ul { list-style-type: none; padding: 0; }
        li { background-color: #f1f1f1; margin-bottom: 10px; padding: 15px; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; word-break: break-all; gap: 15px;}
        .node-text { flex: 1; }
    </style>
</head>
<body>
    <div class="container">
        <h1>订阅管理面板</h1>
        
        <div class="link-box">
            <strong>您的订阅链接:</strong> <br><br>
            <a href="/sub.txt" target="_blank" id="sublink">http://.../sub.txt</a>
            <script>
                document.getElementById('sublink').href = window.location.protocol + "//" + window.location.host + "/sub.txt";
                document.getElementById('sublink').innerText = window.location.protocol + "//" + window.location.host + "/sub.txt";
            </script>
        </div>

        <form class="form-group" action="/add" method="post">
            <input type="text" name="node" placeholder="在此粘贴新的节点链接 (如 hysteria2://...)" required>
            <button type="submit" class="btn-add">添加节点</button>
        </form>

        <h2>当前节点列表 ({{ nodes|length }})</h2>
        <ul>
            {% for node in nodes %}
            <li>
                <div class="node-text">{{ node }}</div>
                <form action="/delete" method="post" style="margin:0;">
                    <input type="hidden" name="index" value="{{ loop.index0 }}">
                    <button type="submit" class="btn-delete">删除</button>
                </form>
            </li>
            {% else %}
            <li>暂无节点，请添加。</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, nodes=get_nodes())

@app.route('/add', methods=['POST'])
def add_node():
    node = request.form.get('node', '').strip()
    if node:
        nodes = get_nodes()
        nodes.append(node)
        save_nodes(nodes)
    return '<script>window.location.href="/";</script>'

@app.route('/delete', methods=['POST'])
def delete_node():
    try:
        index = int(request.form.get('index', -1))
        nodes = get_nodes()
        if 0 <= index < len(nodes):
            nodes.pop(index)
            save_nodes(nodes)
    except ValueError:
        pass
    return '<script>window.location.href="/";</script>'

@app.route('/sub.txt')
def sub():
    nodes = get_nodes()
    content = "\n".join(nodes)
    encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    return Response(encoded, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8123)
