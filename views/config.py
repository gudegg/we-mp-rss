import os
class Config:
    base_path= "./public"
    #模板路径 
    public_dir = f"{base_path}/templates/"
    home_template = f"{base_path}/templates/home.html"
    mps_template = f"{base_path}/templates/mps.html"
    tags_template = f"{base_path}/templates/tags.html"
    tag_detail_template = f"{base_path}/templates/tag_detail.html"
    article_template = f"{base_path}/templates/article.html"
    article_detail_template = f"{base_path}/templates/article_detail.html"
    articles_template = f"{base_path}/templates/articles.html"
base = Config()