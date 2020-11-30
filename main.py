from markdown2 import markdown as md
from jinja2 import Environment, PackageLoader
import os
from datetime import datetime
import re


a={":smiley:":'&#128512;',":grin:":'&#128513;', ":joy:":'&#128514;', ":smiley:":'&#128515;', ":smile:":'&#128516;', ":laughing:":'&#128518;', ":sweat_smile:":'&#128517;', ":innocent:":'&#128519;', ":smiling_imp:":'&#128520;',":wink:":'&#128521;', ":blush:":'&#128522;',":yum:":'&#128523;',":relieved:":'&#128524;',":heart_eyes:":'&#128525;',":sunglasses:":'&#128526;',":smirk:":'&#128527;'}

def create_temp(template,posts,sidebar_v):
    p=template.render(posts=posts,sidebar_v=sidebar_v)
    if(p == None):
        return 0
    return p
    
def Unicode(q):
     x=re.findall(r":\w+:",q)
     for i in x:
         for j in a:
             if j == i:
                 q=q.replace(i,a[j])
     return q

def Creating():
    with open('content/sidebar.md') as files:
        side=md(files.read(),extras=['metadata'])
    POSTS = {}
    for markdown_post in os.listdir('content/posts'):
        file_path = os.path.join('content/posts', markdown_post)

        with open(file_path, 'r') as file:
            q=Unicode(file.read())
            POSTS[markdown_post] = md(q, extras=['metadata','wiki-tables'])
    env = Environment(loader = PackageLoader('main', 'templates'))
    home_template = env.get_template('index.html')
    post_template = env.get_template('post.html')
    about_template = env.get_template('about.html')
    posts_metadata = [POSTS[post].metadata for post in POSTS]


    text = create_temp(home_template,posts_metadata,side.metadata)

    with open('output/index.html', 'w+') as file:
        file.write(text)

    for post in POSTS:
        post_meta=POSTS[post].metadata
        
        post_data ={   
            'content': POSTS[post],                                                         
            'title': post_meta['title'],
            'data': post_meta['date'],
            'img': post_meta['thumbnail'],          
            'slug':post_meta['slug'],
            'summary':post_meta['summary'],
            }

        text = create_temp(post_template,post_data,side.metadata)
        post_file_path='output/posts/{slug}.html'.format(slug=post_meta['slug'])
        print(post_file_path)
        os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
        with open(post_file_path, 'w') as file:
            file.write(text)
        file.close()
    with open('content/info.md') as file:
        info=md(file.read(),extras=['metadata'])
    info=info.metadata
    text = create_temp(about_template,info,side.metadata)
    with open('output/about.html', 'w+') as file:
        file.write(text)
    

