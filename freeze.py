from flask_frozen import Freezer, walk_directory
from app import app
import argparse


app.config['FREEZER_DESTINATION'] = 'docs'
app.config['FREEZER_RELATIVE_URLS'] = True
freezer = Freezer(app)


@freezer.register_generator
def assets_url_generator():
    for path in walk_directory('vite/dist/client/assets'):
        yield ('assets', {"path": path})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--run', action="store_true")
    parser.add_argument('-s', '--serve', action="store_true")
    args = parser.parse_args()

    if args.serve:
        freezer.serve()
    elif args.run:
        freezer.run()
    else:
        freezer.freeze()
    