import re
import csv
import io
import requests
import json
import os.path
import sys
from untemplate.untemplate import untemplate_string

DETAILS_URL = "http://iresearch.worldbank.org/PovcalNet/Detail.aspx"

HEADERS_TYPES = [
    ("survey_id",str),
    ("region_wb",str),
    ("region_un",str),
    ("region_income",str),
    ("name",str),
    ("coverage",str),
    ("uknown",bool),
    ("poverty_line",float),
    ("ppp",float),
    ("unknown",bool),
    ("flags",int),
    ("years",lambda x: x.split(","))
]

TEMPLATE_FILES = [
    "untemplate/demo/templates/empirical_modular.txt",
    "untemplate/demo/templates/modelled_modular_robust.txt",    
]

FLAGS_PPP_ESTIMATED = 1
FLAGS_UNAVAILABLE = 4

def initCItem2014_js_to_list(js):
    regex = 'new cItem\(([^\)]+)\),?\n'
    out = list()
    
    for line in js.splitlines(True):
        m = re.search(regex, line)
        if m:
            entry = dict()
            fields = next(csv.reader(io.StringIO(m.group(1))))
            
            for val,(key,typefun) in zip(fields, HEADERS_TYPES):
                entry[key] = typefun(val)
                
            out.append(entry)
            
    return out

def download_details(survey, year):
    params = {
        "Format": "Detail",
        "NumOfCountries": "1",
        "C0": survey['survey_id'],
        "PPP0": survey['ppp'],
        "PL0": survey['poverty_line'],
        "Y0": year
    }

    response = requests.get(DETAILS_URL, params)
    html = response.text
    
    open_pre = "<pre>"
    close_pre = "</pre>"
    
    return html[html.find(open_pre)+len(open_pre):html.find(close_pre)]

if __name__ == "__main__":
    if sys.argv[1] == "-fp":
        force_reparse = True
        print("Will reparse any existing text files")

    with open("initCItem2014.js") as f:
        js = f.read()
        
    surveys = initCItem2014_js_to_list(js)
    
    for s in surveys:
        if not(s['flags'] & FLAGS_UNAVAILABLE):
            for year in s['years']:
                already_downloaded = os.path.isfile("txtcache/{}_{}.txt".format(s['survey_id'], year))
                if already_downloaded and not force_reparse:
                    continue
                
                print(s['survey_id'], year)    
                
                if not already_downloaded:
                    details = download_details(s, year)
                    details = details.replace('\r\n','\n')
                    with open("txtcache/{}_{}.txt".format(s['survey_id'], year), "w") as f_txt:
                        f_txt.write(details) 
                else:
                    with open("txtcache/{}_{}.txt".format(s['survey_id'], year), "r") as f_txt:
                        details = f_txt.read()

                try:
                    details_json = untemplate_string(TEMPLATE_FILES,details)
                    with open("jsoncache/{}_{}.json".format(s['survey_id'], year), "w") as f_json:
                        json.dump(details_json, f_json, indent=4)
                except:
                    with open("jsoncache/unparseable/{}_{}.txt".format(s['survey_id'], year), "w") as f_txt:
                        f_txt.write(details) 
        else:
            with open("txtcache/unavailable/{}_{}.txt".format(s['survey_id'], year), "w") as f_txt:
                f_txt.write("unavailable\n") 
            