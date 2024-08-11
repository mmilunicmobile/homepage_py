import yaml
import flask
import flask_frozen
import markdown
# import flask_vite
import json
import re
from bs4 import BeautifulSoup
from bs4 import Comment
import subprocess

app = flask.Flask(__name__)

# vite = flask_vite.Vite(app)

vite_manifest = json.load(open('vite/dist/client/.vite/manifest.json'))

vite_filler_manifest = json.load(open('vite/dist/server/.vite/customElements.json'))

def vite_filler(vite_path):
    def temporary(method):
        if app.debug: 
            return method

        def replace_vite(*args, **kwargs):
            output = method(*args, **kwargs)
            for key, value in vite_filler_manifest[vite_path].items():
                output = output.replace(f'<{key}/>', value)
            return output
        
        replace_vite.__name__ = method.__name__
        
        return replace_vite

    return temporary

@app.context_processor
def utility_processor():
    def get_vite_path(path):
        if app.debug: 
            return f"http://localhost:3000/{path}"
        else:
            next_path = vite_manifest[path]['file'].removeprefix('assets/')
            return flask_frozen.relative_url_for("assets",path=next_path)
    
    return dict(get_vite_path=get_vite_path)

with open('configs.yaml', 'r') as stream:
    configs = yaml.safe_load(stream)

for i in configs['articles']:
    i['docname_html'] = i.get('docname_html', i['docname'].replace('.md', '.html'))

@app.route('/')
def index():
    article_info = [ 
        {
            'name': article['name'],
            'url': flask_frozen.relative_url_for('article', article=article['docname_html']),
        } for article in configs['articles']
    ]
    return flask.render_template('index.html.jinja', articles=article_info, my_websites=configs['my_websites'], cool_websites=configs['cool_websites'])

@app.route('/assets/<path:path>')
def assets(path):
    return flask.send_from_directory('vite/dist/client/assets', path)

def load_vite(content: str, script: str):
    parsed_content = BeautifulSoup(content, 'html.parser')

    for element_name, element_contents in vite_filler_manifest[f"./{script}"].items():
        for node in parsed_content.find_all(element_name):
            p = subprocess.Popen(['/usr/local/bin/node', './vite/dist/server/serverRender.js', f"./{script}", element_name, json.dumps(node.attrs)], stdout=subprocess.PIPE)
            out = p.stdout.read()
            node.clear()
            node.extend(BeautifulSoup(out, 'html.parser').find(element_name).contents)

    # comments = parsed_content.find("vite-code-injection-spot")

    # node.replace_with(BeautifulSoup("<vite-code-injection-spot></vite-code-injection-spot>", 'html.parser'))

    return str(parsed_content)


@app.route('/article/<article>')
def article(article):
    possible_articles = list(filter(lambda art: art[1]['docname_html'] == article, enumerate(configs['articles'])))
    if len(possible_articles) == 0:
        return flask.render_template('pagenotfound.html.jinja')
    
    article_id, article_to_render = possible_articles[0]
    

    markdown_to_render = ""

    if not article_to_render.get('skip_header', False):
        markdown_to_render += f"# {article_to_render['name']}\n"
    
        if "author" in article_to_render:
            markdown_to_render += f"By {article_to_render['author']}\n\n"

        if "date" in article_to_render:
            markdown_to_render += f"{article_to_render['date']}\n\n"
        
        markdown_to_render += "---\n\n"

    markdown_to_render += open(f"articles/{article_to_render['docname']}", 'r').read()

    rendered_markdown = markdown.markdown(markdown_to_render, extensions=['tables'])

    try:
        if (article_id == 0): 
            raise IndexError
        previous_article = flask_frozen.relative_url_for("article", article=configs['articles'][article_id - 1]['docname_html'])
    except IndexError:
        previous_article = None

    try:
        next_article = flask_frozen.relative_url_for("article", article=configs['articles'][article_id + 1]['docname_html'])
    except IndexError:
        next_article = None
    
    description = article_to_render.get("description", "Mathum is a collection of articles written about math programming and anything inbetween. This is an article on it.")

    script = article_to_render.get("script", None)

    use_mathjax = article_to_render.get("use_mathjax", None)

    if use_mathjax is None:
        use_mathjax = False
        
        all_texts = BeautifulSoup(rendered_markdown, 'html.parser').strings
        for text in all_texts:
            # print(text)
            if re.search(r"(?<!\\)((?<!\$)\${1,2}(?!\$))(.*?)(?<!\\)(?<!\$)\1(?!\$)", text, re.X | re.S):
                use_mathjax = True
                break

    output = flask.render_template(
        'article.html.jinja', 
        name=article_to_render["name"], 
        rendered_markdown=rendered_markdown, 
        previous_article=previous_article, 
        next_article=next_article,
        description=description,
        script=script,
        use_mathjax=use_mathjax
    )

    if script:
        return load_vite(output, script)
    else:
        return output