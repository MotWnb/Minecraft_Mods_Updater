import cloudscraper
from lxml import etree

scraper = cloudscraper.create_scraper()

mod_url = "https://www.curseforge.com/minecraft/mc-mods/autofish"

headers = {
    "User-Agent": "Mozilla/5.0",
}
print(mod_url)
response = scraper.get(mod_url, headers=headers)
if response.status_code == 200:
    html = response.content
    tree = etree.HTML(html)
    version_elements = tree.xpath('//*[@id="project-versions"]/li/a')
    versions = [elem.text for elem in version_elements]
    print(f"Minecraft versions for {mod_url}: {versions}")
else:
    print(f"Error getting HTML for {mod_url}: {response.status_code}")  