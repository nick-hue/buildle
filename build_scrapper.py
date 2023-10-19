import requests
from bs4 import BeautifulSoup

def convert_name(name, item):
    result = ''
    if str(item.text) == "LeBlanc":
        return "Leblanc"
    if str(item.text) == "Renata Glasc":
        return "Renata"
    if str(item.text) == "Wukong":
        return "MonkeyKing"
    
    for i, char in enumerate(name):
        
        if char == "'":
            result = name[:i]+name[i+1].lower()+name[i+2:]
    return result

def filter_names(items):
	champion_names = []
	weird_names = ["Bel'Veth", "Cho'Gath", "Kai'Sa", "Kha'Zix", "LeBlanc", "Renata Glasc", "Vel'Koz", "Wukong"]
	for item in items:
	    if str(item.text) in weird_names:
	        champion_names.append(convert_name(str(item.text), item))
	        #print(convert_name(str(item.text)))
	        continue
	        
	    champion_names.append(str(item.text).replace(' ', '').replace('.', '').replace("'",''))
	return champion_names

def get_original_champion_names(items):
	return [x.text for x in items]

def get_build(data_list):
    build = []
    data_list = list(data_list[3])
    for item in data_list:
        build_info = {
            "name":item.img['alt'], 
            "image":item.img['src']
        }
        build.append(build_info)
    return build

def get_all_champ_data(champion_names):
	all_data = []
	for champion_name in champion_names:
	    headers = {
	        'authority': 'static.bigbrain.gg',
	        'accept': '*/*',
	        'accept-language': 'en-US,en;q=0.9',
	        'origin': 'https://u.gg',
	        'referer': 'https://u.gg/',
	        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Opera GX";v="102"',
	        'sec-ch-ua-mobile': '?0',
	        'sec-ch-ua-platform': '"Windows"',
	        'sec-fetch-dest': 'empty',
	        'sec-fetch-mode': 'cors',
	        'sec-fetch-site': 'cross-site',
	        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0',
	    }
	    url = f'https://static.bigbrain.gg/assets/lol/riot_static/13.18.1/data/en_US/champion/{champion_name}.json'
	    
	    response = requests.get(url,headers=headers)
	    response.raise_for_status()  # raises exception when not a 2xx response
	    if response.status_code != 204:
	        result = response.json()
	       
	    url = f'https://mobalytics.gg/lol/champions/{champion_name}/build'
	    response = requests.get(url)
	    soup = BeautifulSoup(response.content, 'html.parser')
	    build_data = soup.find_all('div', class_="m-1q4a7cx")
	    
	    # name title image
	    # hint1 tags 
	    # hint2 partytype 
	    # hint3 passive passive_description

	    champ_info = {
	        'name':result['data'][champion_name]['name'],
	        'title':result['data'][champion_name]['title'],
	        'image':f'https://static.bigbrain.gg/assets/lol/riot_static/13.19.1/img/champion/{champion_name}.png',
	        'tags':result['data'][champion_name]['tags'],
	        'partype':result['data'][champion_name]['partype'],
	        'passive_name':result['data'][champion_name]['passive']['name'],
	        'passive_description':result['data'][champion_name]['passive']['description'],
	        'build':get_build(build_data)
	    }
	    
	    
	    all_data.append(champ_info)
	    print(champion_name+' done.')

	return all_data

def get_one_champ_data(champion_name):
	headers = {
	        'authority': 'static.bigbrain.gg',
	        'accept': '*/*',
	        'accept-language': 'en-US,en;q=0.9',
	        'origin': 'https://u.gg',
	        'referer': 'https://u.gg/',
	        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Opera GX";v="102"',
	        'sec-ch-ua-mobile': '?0',
	        'sec-ch-ua-platform': '"Windows"',
	        'sec-fetch-dest': 'empty',
	        'sec-fetch-mode': 'cors',
	        'sec-fetch-site': 'cross-site',
	        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0',
	}

	url = f'https://static.bigbrain.gg/assets/lol/riot_static/13.18.1/data/en_US/champion/{champion_name}.json'

	response = requests.get(url,headers=headers)
	response.raise_for_status()  # raises exception when not a 2xx response
	if response.status_code != 204:
	    result = response.json()
	
	url = f'https://mobalytics.gg/lol/champions/{champion_name}/build'
	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')
	build_data = soup.find_all('div', class_="m-1q4a7cx")

	# name title image
	# hint1 tags 
	# hint2 partytype 
	# hint3 passive passive_description

	champ_info = {
	    'name':result['data'][champion_name]['name'],
	    'title':result['data'][champion_name]['title'],
	    'image':f'https://static.bigbrain.gg/assets/lol/riot_static/13.19.1/img/champion/{champion_name}.png',
	    'tags':result['data'][champion_name]['tags'],
	    'partype':result['data'][champion_name]['partype'],
	    'passive_name':result['data'][champion_name]['passive']['name'],
	    'passive_description':result['data'][champion_name]['passive']['description'],
	    'build':get_build(build_data)
	}

	#print(f"Build successfully retrieved for {champion_name}.")	    
	return champ_info

def get_one_champ_image(champion_name):
	headers = {
	'authority': 'static.bigbrain.gg',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://u.gg',
    'referer': 'https://u.gg/',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Opera GX";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0',
	}

	url = f'https://static.bigbrain.gg/assets/lol/riot_static/13.18.1/data/en_US/champion/{champion_name}.json'

	response = requests.get(url,headers=headers)
	response.raise_for_status()  # raises exception when not a 2xx response
	if response.status_code != 204:
	    result = response.json()

	champ_info = {
	'name':result['data'][champion_name]['name'],
	'image':f'https://static.bigbrain.gg/assets/lol/riot_static/13.19.1/img/champion/{champion_name}.png',
	}

	return champ_info
	    

url = 'https://www.metasrc.com/lol'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
items = soup.find_all('div', class_ = '_9581uw') # champions 
champion_names = filter_names(items)
original_champion_names = get_original_champion_names(items)
#print(original_champion_names)