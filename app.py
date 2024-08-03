import yaml
import flask
import markdown

app = flask.Flask(__name__)

with open('configs.yaml', 'r') as stream:
    configs = yaml.safe_load(stream)

for i in configs['articles']:
    i['docname_html'] = i.get('docname_html', i['docname'].replace('.md', '.html'))

@app.route('/')
def index():
    article_info = [ 
        {
            'name': article['name'],
            'url': flask.url_for('article', article=article['docname_html']),
        } for article in configs['articles']
    ]
    return flask.render_template('index.html.jinja', articles=article_info, my_websites=configs['my_websites'], cool_websites=configs['cool_websites'])

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
        previous_article = flask.url_for("article", article=configs['articles'][article_id - 1]['docname_html'])
    except IndexError:
        previous_article = None

    try:
        next_article = flask.url_for("article", article=configs['articles'][article_id + 1]['docname_html'])
    except IndexError:
        next_article = None

    return flask.render_template(
        'article.html.jinja', 
        name=article_to_render["name"], 
        rendered_markdown=rendered_markdown, 
        previous_article=previous_article, 
        next_article=next_article
    )