import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)

page = int(input('Enter page number that you want to extract  : '))
glassdoor_data=[]

for i in range(1,page):

    url=f'https://www.glassdoor.co.in/Reviews/index.htm?overall_rating_low=3&page={i}&filterType=RATING_OVERALL'

    print('Page is extracting : ',i)

    r = session.get(url)

    soup = BeautifulSoup(r.content,'html.parser')

    n = soup.find_all('div',class_='mt-0 mb-std p-std css-1ax1pfu css-errlgf')

    for d_name in n:
        name = d_name.find('h2').text.strip()
        industry = d_name.find('div',class_='col-lg-4 mt-sm mt-sm-std order-4')
        industry_name = industry.find('span',class_="d-block mt-0 css-56kyx5").text.strip()
            
        company_siz = d_name.find('div',class_="col-lg-4 mt-sm mt-sm-std order-3")
        company_size = company_siz.find('span',class_="d-block mt-0 css-56kyx5").text.strip()

        try:
            locati = d_name.find('div',class_="col-lg-4 mt-xsm mt-sm-std order-2")
            location_link = locati.find('a')['href']
            base_location_link = f"https://www.glassdoor.co.in{location_link}"
        except:
            base_location_link="None"

        rating = d_name.find('span',class_="pr-xsm ratingsWidget__RatingsWidgetStyles__rating").text
            
        try:
            descriptio = d_name.find('div',class_="col-12 my-0 mt-sm mt-sm-std order-5")
            description = descriptio.find('p').text.strip()

        except:
            description='None'
                 
        l = d_name.find('a')['href']
        link_of_Review = l
        link_of_Sal = l.replace('Reviews','Salary',1)
        link_of_Salary = link_of_Sal.replace('Reviews','Salaries')
        link_of_Jobs = l.replace('Reviews','Jobs')
        link_of_Benifits = l.replace('Reviews','Benefits')
        link_of_Pho = l.replace('Reviews','Photos',1)
        link_of_Photos = link_of_Pho.replace('Reviews','Office-Photos')
        link_of_Interv = l.replace('Reviews','Interview',1)
        Link_of_Interview = link_of_Interv.replace('Reviews','Interview-Questions')
        link_of_FA = l.replace('Reviews','FAQ',1)
        Link_of_FAQ = link_of_FA.replace('Reviews','Questions')
        link_of_Over = l.replace('Reviews/','Overview/Working-at-',1)
        Link_of_Overview = link_of_Over.replace('Reviews-','EI_I')

              
        base_Review_link = f"https://www.glassdoor.co.in{link_of_Review}"
        base_Salary_link = f"https://www.glassdoor.co.in{link_of_Salary}"      
        base_Job_link = f"https://www.glassdoor.co.in{link_of_Jobs}"      
        base_Benifit_link = f"https://www.glassdoor.co.in{link_of_Benifits}"      
        base_Photo_link = f"https://www.glassdoor.co.in{link_of_Photos}"      
        base_Interview_link = f"https://www.glassdoor.co.in{Link_of_Interview}"   
        base_FAQ_link = f"https://www.glassdoor.co.in{Link_of_FAQ}"   
        base_Overview_link = f"https://www.glassdoor.co.in{Link_of_Overview}"   

        req1 = requests.get(base_Review_link,headers=headers)
        soup1 = BeautifulSoup(req1.content,'html.parser')

        General_count = soup1.find_all('div',class_='count')
        for k,mixed in enumerate(General_count):
            if k==4:
                Reviews_count=mixed.text
            elif k==5:
                Jobs_count=mixed.text
            elif k==6:
                Salaries_count=mixed.text
            elif k==7:
                Interviews_count=mixed.text
            elif k==8:
                Benefits_count=mixed.text
            elif k==9:
                Photos_count=mixed.text
        
        req2 = requests.get(base_Overview_link,headers=headers)
        soup2 = BeautifulSoup(req2.content,'html.parser')

        Revb = soup2.find_all('text',class_='text css-xsmmgf')
        for m,mixed_1 in enumerate(Revb):
            if m==0:
                Recommend_to_a_friend=mixed_1.text
            elif m==1:
                Approve_of_CEO =mixed_1.text

        try:
            Web = soup2.find('div',class_="d-flex align-items-center").text
        except:
            Web='None'
        print(Web)

        try:
            Web = soup2.find('a',class_="css-1hg9omi css-1cnqmgc")['href']
        except:
            Web='None'
        try:
            Com = soup2.find('p',class_="d-flex flex-column flex-md-row css-dwl48b css-1cnqmgc")
            Comp = Com.find('span').text
        except:
            Comp="None"

        General_info = soup2.find_all('div',class_='css-19hiur5 css-dwl48b css-1cnqmgc')
        
        for j,general in enumerate(General_info):
            if j==0:
                HQ_h=general.text
            elif j==1:
                company_size=general.text
            elif j==2:
                Founded=general.text
            elif j==3:
                Company_type=general.text
            elif j==4:
                Revenue=general.text

        req3 = requests.get(base_Interview_link,headers=headers)
        soup3 = BeautifulSoup(req3.content,'html.parser')
        try:
            Diff_level = soup3.find('div',class_='align-self-center').text
        except:
            Diff_level = 'None'

        glassdoor_d ={
            'Name':name.strip(),
            'Industry':industry_name.strip(),
            'Location Link':base_location_link.strip(),
            'Size (Employees)':company_size.strip(),
            'HQ':HQ_h.strip(),
            'Founded':Founded.strip(),
            'Typr of Company':Company_type.strip(),
            'Revenue':Revenue.strip(),
            'Website':Web.strip(),
            'Competitors':Comp.strip(),
            'Overall Rating':rating.strip(),
            'Reviews Count':Reviews_count.strip(),
            'Jobs Count':Jobs_count.strip(),
            'Salaries Count':Salaries_count.strip(),
            'Interviews Count':Interviews_count.strip(),
            'Benefits Count':Benefits_count.strip(),
            'Photos Count':Photos_count.strip(),
            'Reviews URL':base_Review_link.strip(),
            'Salaries URL':base_Salary_link.strip(),
            'Jobs URL':base_Job_link.strip(),            
            'Benifits URL':base_Benifit_link.strip(),            
            'Photos URL':base_Photo_link.strip(),            
            'Interview URL':base_Interview_link.strip(),            
            'FAQ URL':base_FAQ_link.strip(),            
            'Overview URL':base_Overview_link.strip()            
        }
        glassdoor_data.append(glassdoor_d)

df = pd.DataFrame(glassdoor_data)
df.to_csv('Glassdoor_data_sample.csv')
