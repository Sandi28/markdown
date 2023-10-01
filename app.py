
from flask import Flask, render_template,request,session, redirect, url_for
import requests
import sys
import webbrowser
import json
from bs4 import BeautifulSoup
import urllib.request
import secrets
from replit import db
secret_key = secrets.token_hex(24)

# Set the secret key for your Flask application
app = Flask(__name__)
app.secret_key = secret_key
class DataStore():
    my_va=None

data = DataStore()




@app.route("/")



def home():
  return render_template('home.html')
@app.route('/', methods = ['POST'])

def get_data_from_html():
  global my_va
  q = request.form['q']
 # TRYING FOR SNAPDEAL.COM
  url = "https://www.snapdeal.com/search?keyword={}".format(q)
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  product_divs = soup.find_all('div', {'class': 'product-tuple-description'})

  for product_div in product_divs:
    name = product_div.find('p', {'class': 'product-title'}).text.strip()
    price = product_div.find('span', {'class': 'product-price'}).text.strip()
    link = product_div.find('a', {'class': 'dp-widget-link noUdLine'})['href']
    print("Product Name: {name} - Price: {price} - Link: {link}")

  prices = [product_div.find('span', {'class': 'product-price'}).text.strip() for product_div in product_divs]
  lowest_price = min(prices)
  print("Lowest price:",lowest_price)
  



# TRYING ALL WEBSITES

  res=requests.get("http://www.pricetree.com/search.aspx?q="+q)
  link=("http://www.pricetree.com/search.aspx?q="+q)





  page=requests.get(link)
  soup=BeautifulSoup(page.text,"html.parser")


  last_links = soup.find(class_='data-container')
  last_links.decompose()




  artist_name_list = soup.find(class_='items-wrap')
  artist_name_list_items = artist_name_list.find_all('a')


# Create for loop to print out all artists' names
  for artist_name in artist_name_list_items:
    print(artist_name.get('href'))
    plink=artist_name.get('href')
    temp=plink.rfind("-")
    priceid=plink[temp+1:]

  print(priceid)


  with urllib.request.urlopen("http://www.pricetree.com/dev/api.ashx?pricetreeId={}&apikey=7770AD31-382F-4D32-8C36-3743C0271699".format(priceid)) as url:
    s = url.read()
    # I'm guessing this would output the html source code ?
    print(s)
    my_string =s.decode("utf-8")
    data.my_va=my_string
    my_dict = json.loads(my_string)

    print(my_dict)

    #session['userin']="hello"
  
    





  
  return render_template("result.html")

@app.route('/templates/result.html')
def get_variable():
 
  y=data.my_va
  return render_template('result.html',p=y)


  
if __name__=="__main__":
  app.run('0.0.0.0',debug=True)












