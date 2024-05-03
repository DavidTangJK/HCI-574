# Step 4 code in one single cell
from flask import Flask, request, render_template   
import requests # this is the requests (with s!) module
import bs4 # BeautifulSoup parser for html

def get_links(anchors_tags):
    links = []
    for a in anchors_tags:
        l = a.get('href')
        if l != None and l.startswith("http"): # only collect external (internet) links
            links.append(str(l))    # convert to string and append to list
    return links

app = Flask("step4")
@app.route("/") 
def main_page():
    html_str = render_template('step4.html', title="Step 4 - get a URL, scrape for links and display them")
    return html_str  # give it to the browser 

@app.route('/result/', methods=["GET"])
def result_page():
    
    # request.args is a dict with the name and the value of the select and 
    url = request.args["URL"]  # value for name = "URL"  in input part of form
    print("Downloading page from", url)
    
    # if url doesn't start with http://, put it in front, otherwise requests.get() gets confused
    if not url.startswith("http://") and not url.startswith("https://"):
         url = "https://" + url
    
    # if url doesn't end with / add that
    if url[-1] != "/": url += '/'
    
    # GET webpage from the url, 
    wp = requests.get(url)  
    wp.raise_for_status()  # raises an exception if there was a problem when getting the url
    
    # create a BeautifulSoup html parser object 
    # wp.text contains the web page text we want to analyse
    soup = bs4.BeautifulSoup(wp.text, "html.parser")  
    
    # pull out all link URLs  (the <a> or anchor tag)
    anchor_tags = soup.find_all('a')
    links = get_links(anchor_tags)
    print ("found", len(links), "links in", url)
    
    # make a long string with all URLs wrapped into anchor tags
    link_URLs_string = ""
    for l in links:
        link_URLs_string = link_URLs_string + "<a href=\"" + l + "\"> " + l + " </a><br>"
    
    # wrap HTML body around the links and add a back to main button   
    html = """
        <html>
          <body>
            These links were found in """ + url + """
            <form action="/" method="get">
              <input type="submit" value="Back to Main page"> 
            </form>""" + link_URLs_string + """
          </body>
        </html>"""
    return html # show finished web page

@app.errorhandler(500)
def page_not_found(error):
    print(error) 
    s = "Error with " + str(request.args["URL"]) + "<br>" + str(error)   
    s = s + "<br>Hit the Back button and try something else ...)"
    return s

app.run(debug=False, port=8080)
