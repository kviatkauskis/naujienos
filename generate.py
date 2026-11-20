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
Parenk išsamų technologijų, mokslo pasiekimų, pramonės inovacijų ir sutelktinio finansavimo naujienlaiškį iš pastarosios paros įvykių ir pateik jį kaip vieno failo HTML5 dokumentą (nuo <!DOCTYPE html> iki </html>) lietuvių kalba, pritaikytą patogiam skaitymui tiek „Google Pixel 10 Pro XL“ telefono naršyklėje, tiek kompiuterio ekrane.

TURINIO IR KOKYBĖS REIKALAVIMAI:
1. Pradėk nuo trumpos 3–4 punktų greitosios santraukos (TL;DR) išskirtame bordo bloke.
2. Pateik 4 skyrius: „01 Technologijos ir skaičiavimai“, „02 Mokslo pasiekimai“, „03 Pramonės inovacijos ir gamyba“, „04 Sutelktinis finansavimas“ (po 2 svarbiausias naujienas, iš viso 8; sutelktiniame finansavime rinkis tik tuos Kickstarter ar panašius projektus, kurie turi veikiantį fizinį prototipą).
3. Naujienas aprašyk plačiai ir išsamiai (nesistenk sutilpti į 3 minutes, skaitymo trukmė ~12–15 min.), nenaudok rinkodaros žargono (jokių „revoliucinis“, „stulbinantis“). Kiekvienoje naujienoje pateik:
   - 3 parametrų žymas (badge), tikslų pavadinimą, techninius parametrus, medžiagas, kainas ir skaičius.
   - Atskirus du analizės blokus po tekstu: „DI akimis: perspektyvos, tendencijos ir poveikis“ (bordo kairės kraštinės akcentas) bei „Realių ekspertų vertinimas“ (alyvuogių žalios kairės kraštinės akcentas – inžinierių, mokslininkų ar rinkos praktikų požiūris ir ribotumai).
4. Griežti šaltinių ir nuorodų reikalavimai (KRITIŠKAI SVARBU):
   - Prieš rašant kiekvieną naujieną, atlik Google paiešką ir remkis tik realiais, patikrintais pastarosios paros šaltiniais.
   - Prie kiekvienos naujienos pateik VISAS nuorodas, iš kurių buvo imta informacija (ne vieną bendrą nuorodą, o visus panaudotus pirminius straipsnius, tyrimus, oficialius pranešimus ar konkrečius Kickstarter projektų puslapius).
   - Kiekviena nuoroda PRIVALO būti veikianti ir vesti tiesiogiai į konkretų polapį / straipsnį, kuriame aprašoma ta naujiena. Griežtai draudžiama pateikti bendrus svetainių pagrindinius ar kategorijų adresus (pvz., vien nature.com, kickstarter.com/discover/..., ieee.org ir pan.).
5. Pabaigoje (Skyrius 05) pridėk techninių parametrų suvestinę 8 kortelių formatu (ne plačia lentele) su pagrindiniu rodikliu, trumpu aprašymu ir tiesioginėmis nuorodomis į konkrečius tų naujienų šaltinių polapius.

DIZAINO IR ADAPTYVAUS MAKETO REIKALAVIMAI:
1. Vieno failo HTML (`<html lang="lt" class="dark scroll-smooth">`), naudojant Tailwind CSS CDN ir Google Fonts („Inter“ tekstui, „Plus Jakarta Sans“ antraštėms).
2. Adaptyvus maketas (Mobile + Desktop):
   - Mobiliuosiuose įrenginiuose (iki 1024px): vieno stulpelio vertikaliai slenkamas dizainas (`max-w-[480px] mx-auto px-4`), pritaikytas valdymui viena ranka be jokio horizontalaus slankiojimo (`overflow-x-hidden`).
   - Kompiuterio naršyklėje (`lg:` ir plačiau): pagrindinis konteineris išsiplečia (`lg:max-w-6xl lg:px-8`), kad būtų tvarkingai išnaudotas ekrano plotas:
     * Kiekvieno straipsnio viduje pagrindinis tekstas ir techninė SVG iliustracija išdėstomi greta arba tvarkingame 2 stulpelių tinklelyje (`lg:grid lg:grid-cols-12 lg:gap-8`, pvz., 7 stulpeliai tekstui ir 5 iliustracijai), o du analizės blokai („DI akimis“ ir „Realių ekspertų vertinimas“) – šalia vienas kito (`lg:grid-cols-2 lg:gap-6`).
     * TL;DR punktai kompiuteryje išdėstomi 2 stulpeliais (`lg:grid-cols-2`), o Skyriaus 05 suvestinės kortelės – 2 arba 4 stulpelių tinklelyje (`md:grid-cols-2 lg:grid-cols-4 gap-4`).
3. Spalvų paletė:
   - Numatytasis tamsusis OLED režimas: `#0D0E12` fonas, `#16181F` kortelės, `#1D202A` vidiniai blokai, `#262936` kraštinės, `#F3F4F6` tekstas, `#B4BAC8` prislopintas tekstas.
   - Šiltas žurnalinis šviesusis režimas: `#FAF9F6` fonas, `#FFFFFF` kortelės, `#F3F1EC` vidiniai blokai, `#E5E1D8` kraštinės.
   - Akcentai: žurnalinė bordo (`#6B212A`, `#8E2E3D`, `#A8384A`, `#D97B8A`) ir alyvuogių žalia (`#4D6140`, `#6F8560`, `#8AA379`).
4. Viršutinė juosta:
   - Fiksuota 3 px skaitymo progreso juosta pačiame viršuje (gradientas nuo bordo iki alyvuogių žalios).
   - Lipni valdymo juosta (`sticky top-0 z-50 backdrop-blur-md`) su pavadinimu **„Naujienos!“** kairėje, šrifto dydžio valdymu (`A-` / rodiklis `17` / `A+`, ribos 15–21 px), tamsaus/šviesaus režimo jungikliu (saulės/mėnulio ikonos) ir horizontaliai slenkama skyrių navigacija (TL;DR, 01 Tech, 02 Mokslas, 03 Pramonė, 04 Kickstarter, Suvestinė), kur aktyvus skyrius paryškinamas slenkant.
5. KRITIŠKAS JAVASCRIPT REIKALAVIMAS (SLINKIMO KLAIDOS PREVENCIJA):
   - Slenkant puslapį žemyn (scroll / IntersectionObserver), GRIEŽTAI DRAUDŽIAMA kviesti `scrollIntoView()` ant navigacijos mygtukų arba keisti `window.location.hash` / `history.replaceState` – tai priverčia naršyklę šokinėti atgal į viršų!
   - Norint horizontaliai pastumti aktyvų mygtuką viršutinėje navigacijos juostoje, naudok TIK `navContainer.scrollTo({ left: btn.offsetLeft - navContainer.offsetWidth / 2 + btn.offsetWidth / 2, behavior: 'smooth' })`.
   - Visiems skyriams pridėk `scroll-mt-32`, kad paspaudus navigacijos nuorodą antraštė nepalįstų po lipnia juosta.
6. Žurnalinis viršelis (masthead) su alyvuogių žalios kairės kraštinės juosta, pavadinimu „Naujienos!“, aktualia data ({date_lt}), dienos santraukos antrašte ir skaitymo trukme (~12–15 min.).
7. Vizualai: prie kiekvienos iš 8 naujienų įterpk originalią, faile integruotą techninę vektorinę iliustraciją (`<svg viewBox="0 0 640 400" class="w-full h-auto">`) tamsiame fone (`#0B0D14`) su lietuviškais žymėjimais, `FIG. 01`–`FIG. 08` etiketėmis ir `<figcaption>` parašu.
8. Nuorodos: prie kiekvienos naujienos ir suvestinės kortelėse pateik tiesiogines vieno paspaudimo HTML nuorodas (`<a href="..." target="_blank" rel="noopener noreferrer">`, min. 48 px aukščio mygtukai) į visus konkrečius pirminius šaltinius be jokių modalų, iššokančių langų ar JS perėmimo.
9. Poraštė su pastaba apie veikimą be interneto (išskyrus išorines nuorodas) ir sklandžiu „Grįžti į pradžią“ mygtuku.

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
