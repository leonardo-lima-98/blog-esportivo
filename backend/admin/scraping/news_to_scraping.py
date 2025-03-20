import sys
sys.path.append('/home/admin-serverlab/blog-esportivo/backend')

from app.models import News, Time
from bs4 import BeautifulSoup as bs
from sqlalchemy import insert
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models import Time
from app.schemas import TimeResponse
import pandas as pd
import requests

@app.get("/", response_model=List[TimeResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Time).all()

url = 'https://ge.globo.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}

html_content = requests.get(url, headers=headers)
bs_page = bs(html_content.text, 'html.parser')

# Create lists to store data
name = []
slug_name = []
category = []
slug_category = []
content_link = []
image_url = []

# Find all category tabs
category_tabs = bs_page.find_all('label', class_='mosaico__equipe-nome')

# For each category
for tab in category_tabs:
    category_name = tab.text.strip()
    
    # Find the corresponding tab content by ID
    tab_id = tab.get('for')
    tab_content = bs_page.find('div', id=f'tab-content-{tab_id.split("-")[1]}')
    
    # Find all teams in this category
    teams = tab_content.find_all('a', class_='mosaico__escudo')
    
    for team in teams:
        team_name = team.get('title')
        team_link = team.get('href')
        team_img = team.find('img').get('data-src')
        
        # Append to lists
        name.append(team_name)
        slug_name.append(str(team_name).lower().replace('á', 'a').replace('à', 'a').replace('ã', 'a')
                         .replace('â', 'a').replace('é', 'e').replace('ê', 'e').replace('í', 'i')
                         .replace('ó', 'o').replace('ô', 'o').replace('õ', 'o').replace('ú', 'u')
                         .replace('ü', 'u').replace('ç', 'c').replace(' ', '-'))
        category.append(category_name)
        slug_category.append(str(category_name).lower().replace('é','e').replace(' ','-'))
        content_link.append(team_link)
        image_url.append(team_img)

# Create a DataFrame
df = pd.DataFrame({
    'Team': name,
    'Team Slug': slug_name,
    'Category': category,
    'Category Slug': slug_category,
    'Link': content_link,
    'Image URL': image_url
},index=None)

new_list = []
for n in range(len(name)):
    new_list.append({'name':name[n], 'slug_name':slug_name[n], 'category':category[n],
                     'slug_category':slug_category[n], 'content_link':content_link[n], 'image_url':image_url[n]})
    

db = next(get_db())
try:
    db.execute(insert(Time), new_list)
    db.commit()
finally:
    db.close()