import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Crawler:
        
    def __init__(self , state="br" , ddd = "" , region = ""):

        self.loop = True
        self.ads = []
        self.state_ok = {
            "sp": "https://sp.olx.com.br/" ,
            "rj": "https://rj.olx.com.br/" ,
            "mg": "https://mg.olx.com.br/" ,
            "pr": "https://pr.olx.com.br/" ,
            "rs": "https://rs.olx.com.br/" ,
            "es": "https://es.olx.com.br/" ,
            "ba": "https://ba.olx.com.br/" ,
            "pe": "https://pe.olx.com.br/" ,
            "df": "https://df.olx.com.br/" ,
            "ce": "https://ce.olx.com.br/" ,
            "ms": "https://ms.olx.com.br/" ,
            "go": "https://go.olx.com.br/" ,
            "am": "https://am.olx.com.br/" ,
            "rn": "https://rn.olx.com.br/" ,
            "pb": "https://pb.olx.com.br/" ,
            "pa": "https://pa.olx.com.br/" ,
            "mt": "https://mt.olx.com.br/" ,
            "al": "https://al.olx.com.br/" ,
            "se": "https://se.olx.com.br/" ,
            "ma": "https://ma.olx.com.br/" ,
            "ac": "https://ac.olx.com.br/" ,
            "ro": "https://ro.olx.com.br/" ,
            "to": "https://to.olx.com.br/" ,
            "pi": "https://pi.olx.com.br/" ,
            "ap": "https://ap.olx.com.br/" ,
            "rr": "https://rr.olx.com.br/" ,
        }.get(state.lower() , "https://olx.com.br/")
        self.url_ini = f"{self.state_ok}{ddd}{region}"

    def status(self , url):
        req = requests.get(url)
        return True if (req.status_code == 200 and (req.url == url or req.url == url.replace("o=1&",""))) else False

    def get_ads(self , itempesquisa , ult_anuncio = "" , limit_pag = ""):

        i = 1
        
        while self.loop:
            URL = f"{self.url_ini}?o={i}&q={itempesquisa}&sf=1"
            print(URL)
            if i <= limit_pag:
                # ^ "https://www.olx.com.br/brasil?o=2&q=guitarra&sf=1"  o=pagina | q=query | sf= ordenação da pagina 1>> mais recente
                if self.status(URL):
                    request = requests.get(URL)
                    soup = BeautifulSoup(request.content, 'html.parser')
                    links = soup.find_all("a" , class_="OLXad-list-link")
                    print(f"Pagina : {i}")

                    for link in links:                
                        if link.attrs['id'] > ult_anuncio :
                            self.ads.append(self.get_ad(link.attrs['href']))
                            # print(link.attrs['href'])
                        else:
                            self.loop = False
                            break

                    i += 1
                else:
                    break
            else:
                self.loop = False

        return self.ads

    def get_ad(self , url):
        if self.status(url):
            request = requests.get(url)
            soup = BeautifulSoup(request.content, 'html.parser')
            imgs = []
            tmp = soup.find_all('img' , class_='image')

            for x in tmp:
                imgs.append(x.attrs['src'])
            
            ad = {
                "value":  soup.find('h2' , class_='sc-bZQynM sc-1wimjbb-0 dSAaHC').get_text() ,
                "publication": self.correct_time(soup.find('span' , class_='sc-bZQynM sc-1oq8jzc-0 dxMPwC').get_text()) ,
                "description": soup.find('p' , class_='sc-1kv8vxj-0 hAhJaI').get_text() ,
                "cod": soup.find('span' , class_='sc-bZQynM sc-16iz3i7-0 cPAPOU').get_text().replace('cód. ' , '') ,
                "category": soup.find('a' , class_='sc-57pm5w-0 sc-1f2ug0x-2 dBeEuJ').get_text() ,
                "images": imgs ,
                "state": request.url[8:10].upper() ,
                "region": request.url.split('/')[3] ,
                "sub-region": soup.find('a' , class_="sc-jKJlTe sc-1aze3je-1 clkGwd").get_text() ,
                "url": request.url
            }

            return ad

        else:
            return False
            
    def correct_time(self , str):

        t = str.replace("Publicado em ","").replace(" às ", f"/{datetime.now().year} ")
        # t = datetime.strptime(t ,"%d/%m/%Y %H:%M")
        return t

# print(Crawler(state="sp").get_ads(local=0 , itempesquisa="guitarra+explorer" , ult_anuncio="" , limit_pag=2))
print(Crawler(state="SP").url_ini)
# print(Crawler().get_ad("https://sp.olx.com.br/sao-paulo-e-regiao/instrumentos-musicais/guitarra-explorer-handmade-luthier-703236712?xtmc=guitarra+explorer&xtnp=1&xtcr=1"))

# ========================================================== ALERTAS ==========================================================

# os dados geograficos são passados na classe , para que seja formado a url inicial. Futuramente isso vai ser passado para um sql , para deixar o codigo mais limpo.

# Até aqui consultamos todas as paginas até o limite de ult_anuncio e limite de pagina , verificando sempre se o limite de pagina confere com o solicitado ex: linha 14.

# Como esta ordenado por mais recente , enviado-se o ult_anuncio pegará apenas os novos , caso contrario todos podendo ser limitado por qtd pagina >>>> IMPORTANTE: SE O ULT_ANUNCIO FOR PASSADO SENDO ELE DE FORA DA UF PESQUISADA ANTERIORMENTE PODE DAR MERDA <<<<<<. 

# Sempre que encontra um novo entra na url e pesquisa os dados , no final retorna um array com varios dicionarios.

# Correct time ajusta o time do anuncio para date time para salvar em banco e talz.

#  Em local , vai ter que ser feito futuramente um depara de municipios e estados ... PQP.
