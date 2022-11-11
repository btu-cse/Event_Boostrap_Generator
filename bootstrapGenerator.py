import requests
from bs4 import BeautifulSoup

# scanned website url
URL = "https://bilgisayar.btu.edu.tr/index.php?page=duyuru"
# count of scanned event
COUNT = 30

# disable warnings
requests.packages.urllib3.disable_warnings()

def get_content():
    x = requests.get(URL, verify=False)
    html = x.content
    print("website request successful")
    return html

def extract_context(html):
    info = []
    links = []
    counter = COUNT
    soup = BeautifulSoup(html, 'html.parser')

    # Gathering links
    is_done = False 
    counter = 1 
    print("Scanning links...")
    while not is_done : 
        link = soup.select(f'.scroll-pane > table:nth-child({counter})') 
        links.append(BeautifulSoup(link.pop().decode_contents(), "html.parser").select("td:nth-child(1) .link1").pop().get("href")) 
        counter += 1 
        if counter == COUNT: 
            is_done = True 
    print("Scan successful")

    # Gathering and extracting contents
    print("Extracting...")
    for item in links: 
        req = requests.request('GET', "https://bilgisayar.btu.edu.tr/" + item, verify=False).content 
        ctx = BeautifulSoup(req, "html.parser")
        strcontent =str( BeautifulSoup(str(ctx.select(".col-md-9 > div:nth-child(1) > div:nth-child(2)")), "html.parser") )
        
        if ctx.select(".col-md-9 > div:nth-child(1) > div:nth-child(2)  img"):

            # extracting text
            text = ctx.select(".col-md-9 > div:nth-child(1) > div:nth-child(2) > p:nth-child(1)").pop().getText(" ") 

            # extracting image link
            img =  ctx.select(".col-md-9 > div:nth-child(1) > div:nth-child(2) img:nth-of-type(1)").pop().get("src") 

            # extracting time
            index = strcontent.index("<br/><br/>")
            strcontent = strcontent[index+10:]
            index = strcontent.index(",")
            time = strcontent[:index]

            # event link
            detail = item 

            info.append( generate_boostrap( (text, img, detail, time) ) ) 
 
    return info

cntr = 1
def generate_boostrap(info_list):
    global cntr 
    template = f""" 
    <!-- Etkinlik {cntr} ---> 
    <div class="container-fluid"> 
    <div class="row"> 
    <div class="col-sm-6" style="background-color:lavender;"><a href="#"><img alt="" src="{info_list[1]}" style="height:146px; width:220px" /></a></div> 
 
    <div class="col-sm-6" style="background-color:lavender;height:146px;"><br /> 
    <strong>[{info_list[3]}]</strong>{info_list[0][0:90]}...<a href="{info_list[2]}"><strong><u>Detaylı bilgi</u></strong></a></div> 
    </div> 
    </div> 
 
    <p>&nbsp;</p> 
    """ 
    print(f"{cntr}.event is generated")

    cntr += 1 
    template = template.encode(encoding='UTF-8',errors='strict') 
    return template 

def save(info):
    print("writing results...")
    file = open("./result.txt", "ab+") 
    for i in info: 
        file.write(i) 
    file.close()
    print("result.txt is ready!")

def app():
    html = get_content()
    info = extract_context(html)
    save(info)

app()






 
 


 
 

 
