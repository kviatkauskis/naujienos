import os
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from google import genai
from google.genai import types

def main():
    client = genai.Client()
    now = datetime.now(ZoneInfo("Europe/Vilnius"))
    date_lt = now.strftime("%Y-%m-%d")

    prompt = f"""
Šiandienos data: {date_lt}.
Naudodamasis Google paieška surask realias pastarosios paros technologijų, mokslo pasiekimų, pramonės inovacijų ir sutelktinio finansavimo (pvz., Kickstarter) naujienas.
Sugeneruok PILNĄ, vieno failo HTML5 dokumentą (nuo <!DOCTYPE html> iki </html>) lietuvių kalba, paruoštą atidaryti tiesiogiai „Google Pixel 10 Pro XL“ telefono naršyklėje.

DIZAINO IR TECHNINIAI REIKALAVIMAI:
1. Maketas: vieno stulpelio vertikaliai slenkamas dizainas (max-width: 480px centruotas, 100% mobiliajame), jokio horizontalaus slankiojimo ar poreikio artinti tekstą.
2. Tema: tamsusis OLED režimas įjungtas pagal nutylėjimą (fonas #0D0E12, kortelės #16181F, pagrindinis tekstas #EAECEF, antrinis #A0A6B1). Žurnalinė bordo (#8B2635 / #6E1D29) ir alyvuogių žalios (#4A5D3F) spalvų akcentų paletė.
3. Viršutinė juosta (sticky):
   - Skaitymo progreso juosta pačiame viršuje.
   - Leidinio pavadinimas, data ({date_lt}), tamsaus/šviesaus režimo mygtukas, šrifto dydžio mygtukai (A- / A+).
   - Horizontaliai slenkami greitosios navigacijos mygtukai (TL;DR, Technologijos, Mokslas, Pramonė, Kickstarter, Suvestinė).
4. Vizualai: prie KIEKVIENOS naujienos įterpk originalią, tvarkingą, inline SVG vektorinę techninę iliustraciją (viewBox="0 0 400 200", pritaikytą tamsiam fonui, su aiškiais lietuviškais žymėjimais ir parašu po iliustracija).
5. Nuorodos: prie kiekvienos naujienos pridėk tiesioginę vieno paspaudimo mygtuko stiliaus nuorodą (<a href="REALUS_URL" target="_blank" rel="noopener noreferrer">Atverti šaltinį ↗</a>) į tikrą pirminį šaltinį. Jokių modalinių langų ar kopijavimo skydelių.

TURINIO REIKALAVIMAI:
1. Viršuje – išskirtas bordo spalvos TL;DR blokas su 3–4 aiškiais dienos akcentais.
2. 4 skyriai: Technologijos, Mokslas, Pramonė, Sutelktinis finansavimas (po 2 svarbiausias pastarosios paros naujienas; sutelktiniame finansavime rinkis tik projektus su veikiančiu fiziniu prototipu).
3. Stilius: išsamus, inžinerinis, analitinis (nesistenk sutilpti į 3 minutes). Nenaudok rinkodaros žargono (jokių „revoliucinis“, „stulbinantis“). Pateik tikslius skaičius, techninius parametrus, medžiagas, kainas.
4. Po KIEKVIENOS naujienos teksto pridėk du atskirus vizualiai išskirtus blokus:
   - „DI akimis: perspektyvos, tendencijos ir poveikis“
   - „Realių ekspertų vertinimas“ (inžinierių, mokslininkų ar rinkos praktikų požiūris, skeptiški niuansai ir ribotumai)
5. Pabaigoje pridėk techninių parametrų suvestinę mobiliųjų kortelių formatu (ne plačia lentele).

SVARBU: Grąžink TIK gryną HTML kodą, be jokių paaiškinimų prieš ar po jo.
"""

response = client.models.generate_content(
        model="gemini-4-carbon",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            max_output_tokens=65536,
        ),
    )

    html = response.text or ""
    html = re.sub(r"^```(?:html)?\s*", "", html.strip(), flags=re.IGNORECASE)
    html = re.sub(r"\s*```$", "", html.strip())

    if "<html" not in html.lower():
        raise ValueError("Sugeneruotas atsakymas neatrodo kaip pilnas HTML dokumentas.")

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    os.makedirs("archive", exist_ok=True)
    with open(f"archive/{date_lt}.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Naujienlaiškis sėkmingai sugeneruotas: {date_lt}")

if __name__ == "__main__":
    main()
