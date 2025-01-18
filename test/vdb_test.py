from dotenv import load_dotenv

import lereng

load_dotenv()

area_llm = lereng.areadb("PROV")
print(area_llm.get_normalize("Yogyakarta"))
print(area_llm.get_normalize("Jogja"))
print(area_llm.get_normalize("Daerah Istimewa Yogyakarta"))
