from langchain_text_splitters import MarkdownHeaderTextSplitter

def split_markdown(text: str):
    
  headers_to_split_on = [
    ("#", "title"),
    ("##", "section"),
    ("###", "subsection"),
  ] 

  markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
  )
  
  return markdown_splitter.split_text(text)