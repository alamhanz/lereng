from dotenv import load_dotenv

import lereng

load_dotenv()

area_llm = lereng.areadb("PROV")
print(area_llm.get_normalize("Yogyakarta")["documents"][0])
print(area_llm.get_normalize("Jogja")["documents"][0])
print(area_llm.get_normalize("Daerah Istimewa Yogyakarta")["documents"][0])
