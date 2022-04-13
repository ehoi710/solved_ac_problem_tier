import requests

from flask import Flask, send_file, Response

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

tier_levels = [
    ('Unlanked', 0),
    ('Bronze', 5),
    ('Bronze', 4),
    ('Bronze', 3),
    ('Bronze', 2),
    ('Bronze', 1),
    ('Silver', 5),
    ('Silver', 4),
    ('Silver', 3),
    ('Silver', 2),
    ('Silver', 1),
    ('Gold', 5),
    ('Gold', 4),
    ('Gold', 3),
    ('Gold', 2),
    ('Gold', 1),
    ('Platinum', 5),
    ('Platinum', 4),
    ('Platinum', 3),
    ('Platinum', 2),
    ('Platinum', 1),
    ('Diamond', 5),
    ('Diamond', 4),
    ('Diamond', 3),
    ('Diamond', 2),
    ('Diamond', 1),
    ('Ruby', 5),
    ('Ruby', 4),
    ('Ruby', 3),
    ('Ruby', 2),
    ('Ruby', 1),
]

colors = {
    'Unlanked': ('#AAAAAA', '#666666', '#000000'),
    'Bronze': ('#F49347', '#984400', '#492000'),
    'Silver': ('#939195', '#6B7E91', '#1F354A'),
    'Gold': ('#FFC944', '#FFAF44', '#FF9632'),
    'Platinum': ('#8CC584', '#45B2D3', '#51A795'),
    'Diamond': ('#96B8DC', '#3EA5DB', '#4D6399'),
    'Ruby': ('#E45B62', '#E14476', '#CA0059'),
}

def generate_svg(res):
    id = res['problemId']
    title = res['titleKo']
    level = res['level']
    tier, level = tier_levels[level]
    color0, color1, color2 = colors[tier]

    res = {
        'id': id,
        'title': title,
        'tier': tier,
        'level': level,
        'color0': color0,
        'color1': color1,
        'color2': color2
    }

    with open('svg_template.svg', 'r', encoding='utf-8') as f:
        template = f.read()

    with open('log.txt', 'w') as f:
        f.write(repr(res))
    return (template % res).replace('%%', '%')

def get_tier(id):
    url = f'https://solved.ac/api/v3/problem/show?problemId={id}'
    hea = {
        'Content-Type': 'application/json'
    }

    try:
        res = requests.get(url, hea)
        res = res.json()
    except:
        return -1

    # return res['level']
    return generate_svg(res)

@app.route('/<id>')
def home(id):
    level = get_tier(id)
    if level == -1:
        return send_file('test.jpg', mimetype='image/jpeg')

    return Response(level, mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=True)