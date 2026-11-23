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
Parenk glaustą, bet techniškai tikslų technologijų, mokslo pasiekimų, pramonės inovacijų, sutelktinio finansavimo  naujienlaiškį iš pastarosios paros įvykių bei įtrauk į naujienas šias įmones atskirai: ROL Lithuania, rolgroup. Dar įdėk naujienas susijusias su Lietuva .Į Lietuvą sutelk daugiau dėmesio ir varbu tikslumas bei nebūtina į tai žiūrėti per technologijų prizmę, o tiesiog pateik aktualijas apie tai kokie dabar vyksta verslo finasavimo, subsidijų projektai, valstybės verslo skatinimo projektai žmonėms bandantiems susikurti sau darbo vietas arba verslą bei naujausi įstatymai Šį naujienlaiškį pateik jį kaip vieno failo HTML5 dokumentą (nuo <!DOCTYPE html> iki </html>) lietuvių kalba, optimizuotą skaitymui „Google Pixel 10 Pro XL“ telefone bei kompiuterio naršyklėje.

TURINIO IR KOKYBĖS REIKALAVIMAI (~7 MIN. SKAITYMO TRUKMĖ):
1. Pradėk nuo trumpos 3–4 punktų greitosios santraukos (TL;DR) išskirtame bordo bloke (po 1 sakinį kiekvienam punktui).
2. Pateik 4 skyrius: „01 Technologijos ir skaičiavimai“, „02 Mokslo pasiekimai“, „03 Pramonės inovacijos ir gamyba“, „04 Sutelktinis finansavimas“ (po 2 svarbiausias naujienas, iš viso 8; sutelktiniame finansavime rinkis tik tuos Kickstarter ar panašius projektus, kurie turi veikiantį fizinį prototipą).
3. Glaustas naujienų stilius (bendra skaitymo trukmė ~5 min.):
   - Jokių rinkodaros klišių („revoliucinis“, „stulbinantis“).
   - Kiekvienoje naujienoje pateik: 3 parametrų žymas (badge), tikslų pavadinimą ir **trumpą, konkrečią 1–2 pastraipų santrauką (apie 50–80 žodžių)** su pagrindiniais skaičiais, techniniais parametrais, medžiagomis ir kainomis.
   - Po tekstu pateik **du išsamius, pilnavertiškus analizės blokus** (jų netrumpink):
     * „DI akimis: perspektyvos, tendencijos ir poveikis“ (bordo kairės kraštinės akcentas).
     * „Realių ekspertų vertinimas“ (alyvuogių žalios kairės kraštinės akcentas – inžinierių, mokslininkų ar rinkos praktikų požiūris, skeptiški niuansai ir ribotumai).
4. Griežti šaltinių ir nuorodų reikalavimai (KRITIŠKAI SVARBU):
   - Prieš rašant kiekvieną naujieną, atlik Google paiešką ir remkis tik realiais, patikrintais pastarosios paros šaltiniais.
   - Prie kiekvienos naujienos pateik VISAS nuorodas, iš kurių buvo imta informacija (pirminius straipsnius, tyrimus, oficialius pranešimus ar konkrečius Kickstarter projektų puslapius).
   - Kiekviena nuoroda PRIVALO būti veikianti ir vesti tiesiogiai į konkretų polapį / straipsnį. Griežtai draudžiama pateikti bendrus svetainių pagrindinius ar kategorijų adresus (pvz., vien nature.com, kickstarter.com/discover/..., ieee.org).
5. Pabaigoje (Skyrius 05) pridėk trumpą techninių parametrų suvestinę 8 kortelių formatu (ne plačia lentele): pagrindinis rodiklis, 1 sakinio aprašymas ir tiesioginės nuorodos į šaltinius.
6. FORMULIŲ TAISYKLĖ: GRIEŽTAI DRAUDŽIAMA naudoti LaTeX sintaksę (jokių `$ ... $`, `\\to`, `\\mu`, `^`, `_`). Visas matematines, fizikos ir chemines formules rašyk TIK naudojant HTML žymes (`<sup>`, `<sub>`) ir Unicode simbolius (pvz., `B<sup>0</sup> → μ<sup>+</sup>μ<sup>−</sup>`, `CO<sub>2</sub>`, `σ`).

DIZAINO IR TECHNINIAI REIKALAVIMAI:
1. Vieno failo HTML (`<html lang="lt" class="dark scroll-smooth">`), naudojant Tailwind CSS CDN ir Google Fonts („Inter“ tekstui, „Plus Jakarta Sans“ antraštėms).
2. Adaptyvus maketas:
   - Telefone (iki 1024px): vieno stulpelio vertikaliai slenkamas dizainas (`max-w-[480px] mx-auto px-4`, `overflow-x-hidden`), pritaikytas valdymui viena ranka.
   - Kompiuteryje (`lg:`): konteineris išsiplečia (`lg:max-w-6xl lg:px-8`), straipsnio tekstas ir SVG iliustracija išdėstomi greta (`lg:grid lg:grid-cols-12 lg:gap-8`), analizės blokai – šalia vienas kito (`lg:grid-cols-2 lg:gap-6`), o Skyriaus 05 suvestinės kortelės – 4 stulpeliais (`md:grid-cols-2 lg:grid-cols-4 gap-4`).
3. Spalvų paletė:
   - Numatytasis tamsusis OLED režimas: `#0D0E12` fonas, `#16181F` kortelės, `#1D202A` vidiniai blokai, `#262936` kraštinės, `#F3F4F6` tekstas, `#B4BAC8` prislopintas tekstas.
   - Šviesusis žurnalinis režimas: `#FAF9F6` fonas, `#FFFFFF` kortelės, `#F3F1EC` vidiniai blokai, `#E5E1D8` kraštinės.
   - Akcentai: bordo (`#6B212A`, `#8E2E3D`, `#A8384A`, `#D97B8A`) ir alyvuogių žalia (`#4D6140`, `#6F8560`, `#8AA379`).
4. Viršuje: fiksuota 3 px skaitymo progreso juosta (gradientas nuo bordo iki alyvuogių žalios), lipni valdymo juosta (`sticky top-0 z-50 backdrop-blur-md`) su antrašte **„Naujienos!“**, šrifto dydžio valdymu (`A-` / `17` / `A+`, ribos 15–21 px), tamsaus/šviesaus režimo jungikliu ir horizontaliai slenkama skyrių navigacija (TL;DR, 01 Tech, 02 Mokslas, 03 Pramonė, 04 Kickstarter, Suvestinė).
5. SLINKIMO KLAIDOS PREVENCIJA (JS):
   - Slenkant puslapį (scroll / IntersectionObserver), GRIEŽTAI DRAUDŽIAMA kviesti `scrollIntoView()` ant navigacijos mygtukų arba keisti `window.location.hash` / `history.replaceState`.
   - Horizontalią navigaciją stumk TIK su `navContainer.scrollTo({{ left: btn.offsetLeft - navContainer.offsetWidth / 2 + btn.offsetWidth / 2, behavior: 'smooth' }})`.
   - Skyriams pridėk `scroll-mt-32`.
6. Žurnalinis viršelis (masthead) su alyvuogių žalios kairės kraštinės juosta, data ({date_lt}), antrašte ir skaitymo trukme (~5 min.).
7. Vizualai: prie kiekvienos iš 8 naujienų įterpk švarią, minimalistinę, techninę vektorinę iliustraciją (`<svg viewBox="0 0 640 400" class="w-full h-auto">`) tamsiame fone (`#0B0D14`) su lietuviškais žymėjimais, `FIG. 01`–`FIG. 08` etiketėmis ir `<figcaption>` parašu.
8. Nuorodos: tiesioginės vieno paspaudimo HTML nuorodos (`<a href="..." target="_blank" rel="noopener noreferrer">`, min. 48 px aukščio mygtukai) be modalų ar JS perėmimo.
9. Poraštė su pastaba apie veikimą be interneto ir „Grįžti į pradžią“ mygtuku.

SVARBU: Grąžink TIK gryną HTML kodą, be jokių paaiškinimų prieš ar po jo.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            max_output_tokens=32768,
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
