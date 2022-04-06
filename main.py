
import csv, zipfile
import requests
import fitz
import os

zip_url = 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2022FD.ZIP'
pdf_url = 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/'

pickone = 'Pelosi'

r = requests.get(zip_url)
thezipfile = '2022.zip'

with open(thezipfile, 'wb') as f:
    f.write(r.content)

with zipfile.ZipFile(thezipfile) as z:
    z.extractall('.')

with open('2022FD.txt') as f:

    for line in csv.reader(f, delimiter='\t'):
        if line[1] == pickone:
            date = line[7]
            doc_id = line[8]

            r = requests.get(f'{pdf_url}{doc_id}.pdf')

            with open("C:/Users/dan/PycharmProjects/CongTrader/pdffolder/"f"{doc_id}.pdf", 'wb') as pdf_file:
                pdf_file.write(r.content)

# doc = fitz.open('pdffolder/'f"{doc_id}.pdf")
doc = fitz.open('pdffolder/20020515.pdf')

page = doc.load_page(page_id=0)

data = page.get_text().split('\n')

data = data

strainer = []

for word in data:
    starttag = '$200?'
    endtag = 'initial public offerings'
    if word == starttag:
        # strainer.append(data[data.index(starttag)+1:data.index(endtag)+1])
        strainer.append(endtag in (word.lower() for word in data))
print(strainer)
doc.close()

sifter = []

for i in strainer:
    for j in i:
        if len(j) > 3:
            sifter.append(j)

bad_words = ('FIlINg STATuS', 'DESCRIPTION')
result=[]
for i in sifter:
    if i.startswith(bad_words) == False:
        result.append(i)

print(result)


# mydir = r'C:\Users\Dan\PycharmProjects\CongTrader\pdffolder'
#
# for f in os.listdir(mydir):
#     if not f.endswith(".pdf"):
#         continue

#     os.remove(os.path.join(mydir,f))
