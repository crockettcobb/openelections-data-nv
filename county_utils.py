import csv
import requests
from BeautifulSoup import BeautifulSoup

"""
The functions here scrape county-level results from the
Nevada Secretary of State's website and output CSV files with
county-level candidate totals.
"""
# 2012 general county-level results
# http://www.nvsos.gov/silverstate2012gen/_xml/USandNV.xml


def parse_2011_special():
    base_url = "http://www.nvsos.gov/SilverState2011Special/Counties/"
    counties = ['Carson%20City.aspx', 'Churchill.aspx','Clark.aspx','Douglas.aspx','Elko.aspx',
    'Esmeralda.aspx','Eureka.aspx','Humboldt.aspx','Lander.aspx','Lincoln.aspx','Lyon.aspx',
    'Mineral.aspx','Nye.aspx','Pershing.aspx','Storey.aspx','Washoe.aspx','White%20Pine.aspx']
    office = "U.S REPRESENTATIVE IN CONGRESS, DISTRICT 2"
    for county in counties:
        candidates = []
        soup, jurisdiction, filename = fetch_and_parse(base_url+county, '2011', '20110913__nv__special__general__')
        results = soup.find('table', {'class' : 'tableshadow'})
        for candidate in results.findAll('tr')[1:]:
            cands = [td.text.strip() for td in candidate.findAll('td')]
            cands.append(office)
            candidates.append(cands)
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            writer.writerow(['candidate','party','votes','percent','office'])
            [writer.writerow(row) for row in candidates]


def parse_2012_primary():
    base_url = "http://www.nvsos.gov/SilverState2012Pri/Counties/"
    counties = ['Carson%20City.aspx', 'Churchill.aspx','Clark.aspx','Douglas.aspx','Elko.aspx',
    'Esmeralda.aspx','Eureka.aspx','Humboldt.aspx','Lander.aspx','Lincoln.aspx','Lyon.aspx',
    'Mineral.aspx','Nye.aspx','Pershing.aspx','Storey.aspx','Washoe.aspx','White%20Pine.aspx']
    for county in counties:
        soup, jurisdiction, filename = fetch_and_parse(base_url+county, '2012', '20120712__nv__primary__')
        finish = len(soup.findAll('li'))-2
        candidates = []
        for i in xrange(8,finish,2):
            results = soup.findAll('li')[i]
            office = results.find('span').text
            for candidate in results.findAll('tr')[1:len(results.findAll('tr'))-1]:
                cands = [td.text.strip() for td in candidate.findAll('td')]
                cands.append(office)
                candidates.append(cands)
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            writer.writerow(['candidate','party','votes','percent','office'])
            [writer.writerow(row) for row in candidates]

def fetch_and_parse(url, year, name):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    jurisdiction = soup.find('title').text.split(' Results')[0]
    if 'County' in jurisdiction:
        jurisdiction = jurisdiction.split(' County')[0]
    jurisdiction = jurisdiction.lower().replace(' ','_')
    filename = year+'/'+name+jurisdiction+'.csv'
    return [soup, jurisdiction, filename]
