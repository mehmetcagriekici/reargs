import markdown
from bs4 import BeautifulSoup

def markdown_processor(md: str) -> str:
    # convert markdown to html
    markup = markdown.markdown(temp_html)
    soup = BeautifulSoup(markup, 'html.parser')
    return soup.get_text()
