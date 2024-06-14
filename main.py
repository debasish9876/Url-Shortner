import random 
import string
import json

from flask import Flask,render_template,redirect,url_for,request

app=Flask(__name__,template_folder='template')
shortended_urls={}

def generate_short_urls(length=6):
    chars=string.ascii_letters+string.digits
    short_url="".join(random.choice(chars)for _ in range(length))
    return short_url

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        long_url=request.form['long_url']
        short_url=generate_short_urls()
        while short_url in shortended_urls:
            short_url=generate_short_urls()

        shortended_urls[short_url]=long_url
        with open("urls.json","w") as f:
            json.dump(shortended_urls,f)
        return f"Shortended URL: {request.url_root}{short_url}"
    return render_template("index.html")

@app.route("/<short_url>")
def redirect_urls(short_url):
    long_url=shortended_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "url not found ",404

if __name__=="__main__":
    
    app.run(debug=True)