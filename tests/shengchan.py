from lxml import etree
html = etree.parse('index.html')
a = html.xpath('//li/a')
print(a[0].text)