from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=800))

print("name:", wiki.name)
print("description:", wiki.description)
print("args:", wiki.args)

result = wiki.invoke({"query": "Python (programming language)"})
print(result[:300])
