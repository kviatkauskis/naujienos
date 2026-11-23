import os
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from google import genai
from google.genai import types

# ==============================================================================
# NUSTATYMAI (Čia lengvai keiskite skaitymo trukmę ir temas)
# ==============================================================================

SKAITYMO_TRUKME = "~7 min."

# Norėdami pridėti naują temą, tiesiog nukopijuokite vieną { ... } bloką žemiau.
# Kiekviena tema automatiškai gaus atskirą skyrių, navigacijos mygtuką ir rėmus.
TEMOS = [
    {
        "nav": "01 Tech",
        "pavadinimas": "01 Technologijos ir skaičiavimai",
        "kiekis": 2,
        "aprasymas": "Svarbiausios pastarosios paros technologijų ir skaičiavimų naujienos.",
    },
    {
        "nav": "02 Mokslas",
        "pavadinimas": "02 Mokslo pasiekimai",
        "kiekis": 2,
        "aprasymas": "Svarbiausi pastarosios paros mokslo atradimai ir tyrimai.",
    },
    {
        "nav": "03 Pramonė",
        "pavadinimas": "03 Pramonės inovacijos ir gamyba",
        "kiekis": 2,
        "aprasymas": "Pramonės inovacijos, gamybos technologijos ir inžineriniai sprendimai.",
    },
    {
        "nav": "04 Kickstarter",
        "pavadinimas": "04 Sutelktinis finansavimas",
        "kiekis": 2,
        "aprasymas": "Rinkis tik tuos Kickstarter ar panašius projektus, kurie turi veikiantį fizinį prototipą.",
    },
    {
        "nav": "05 ROL",
        "pavadinimas": "05 ROL Lithuania ir ROL Group",
        "kiekis": 2,
        "aprasymas": "Naujienos, susijusios su įmonėmis „ROL Lithuania“ ir „ROL Group“ (rolgroup). Jei per pastarąją parą naujienų nebuvo, pateik naujausias aktualijas iš pastarųjų savaičių.",
    },
    {
        "nav": "06 Lietuva",
        "pavadinimas": "06 Lietuva: verslo finansavimas, subsidijos ir įstatymai",
        "kiekis": 3,
        "aprasymas": "Skirk daugiau dėmesio ir tikslumo. Nebūtina žiūrėti per technologijų prizmę – pateik aktualijas apie dabar vykstančius verslo finansavimo, subsidijų, valstybės verslo skatinimo projektus žmonėms, bandantiems susikurti sau darbo vietas arba verslą, bei naujausius susijusius įstatymus.",
    },
]

# ==============================================================================
# PAGRINDINIS KODAS (Žemiau esančios dalies keisti nebereikia)
# ==============================================================================

def main():
    client = genai.Client()
    now = datetime.now(ZoneInfo("Europe/Vilnius"))
    date_lt = now.strftime("%Y-%m-%d")

    viso_naujienu = sum(t["kiekis"] for t in TEMOS)
    suvestines_nr = f"{len(TEMOS) + 1:02d}"
    nav_mygtukai = ", ".join(["TL;DR"] + [t["nav"] for t in TEMOS] + ["Suvestinė"])

    temu_blokas = "\n".join(
        f'   - „{t["pavadinimas"]}“ (naujienų kiekis: {t["kiekis"]}): {t["aprasymas"]}'
        for t in TEMOS
    )

    prompt = f"""
Šiandienos data: {date_lt}.
Parenk glaustą, tikslų ir struktūrizuotą naujienlaiškį pagal žemiau nurodytas temas ir pateik jį kaip vieno failo HTML5 dokumentą (nuo <!DOCTYPE html> iki </html>) lietuvių kalba, optimizuotą skaitymui „Google Pixel 10 Pro XL“ telefone bei kompiuterio naršyklėje.

TURINIO IR KOKYBĖS REIKALAVIMAI (SKAITYMO TRUKMĖ: {SKAITYMO_TRUKME}):
1. Pradėk nuo trumpos 3–4 punktų greitosios santraukos (TL;DR) išskirtame bordo bloke (po 1 sakinį kiekvienam punktui).
2. Pateik šiuos {len(TEMOS)} atskirus skyrius (kiekvieną aiškiai atskirk atskiruose skyriaus rėmuose su aiškia antrašte; iš viso {viso_naujienu} naujienų):
{temu_blokas}
3. Glaustas naujienų stilius (bendra skaitymo trukmė {SKAITYMO_TRUKME}):
   - Jokių rinkodaros klišių („revoliucinis“, „stulbinantis“).
   - Kiekvienoje naujienoje pateik: 3 parametrų žymas (badge), tikslų pavadinimą ir **trumpą, konkrečią 1–2 pastraipų santrauką (apie 50–80 žodžių)** su pagrindiniais skaičiais, faktais, parametrais, sumomis ar sąlygomis.
   - Po tekstu pateik **du išsamius, pilnavertiškus analizės blokus** (jų netrumpink):
     * „DI akimis: perspektyvos, tendencijos ir poveikis“ (bordo kairės kraštinės akcentas).
     * „Realių ekspertų vertinimas“ (alyvuogių žalios kairės kraštinės akcentas – inžinierių, mokslininkų, teisininkų ar rinkos praktikų požiūris, skeptiški niuansai ir ribotumai).
4. Griežti šaltinių ir nuorodų reikalavimai (KRITIŠKAI SVARBU):
   - Prieš rašant kiekvieną naujieną, atlik Google paiešką ir remkis tik realiais, patikrintais šaltiniais.
   - Prie kiekvienos naujienos pateik VISAS nuorodas, iš kurių buvo imta informacija (pirminius straipsnius, tyrimus, oficialius pranešimus, teisės aktus ar konkrečius Kickstarter projektų puslapius).
   - Kiekviena nuoroda PRIVALO būti veikianti ir vesti tiesiogiai į konkretų polapį / straipsnį. Griežtai draudžiama pateikti bendrus svetainių pagrindinius ar kategorijų adresus (pvz., vien nature.com, kickstarter.com/discover/..., ieee.org).
5. Pabaigoje (Skyrius {suvestines_nr}) pridėk trumpą parametrų suvestinę {viso_naujienu} kortelių formatu (ne plačia lentele): pagrindinis rodiklis, 1 sakinio aprašymas ir tiesioginės nuorodos į šaltinius.
6. FORMULIŲ TAISYKLĖ: GRIEŽTAI DRAUDŽIAMA naudoti LaTeX sintaksę (jokių `$ ... $`, `\\to`, `\\mu`, `^`, `_`). Visas matematines, fizikos ir chemines formules rašyk TIK naudojant HTML žymes (`<sup>`, `<sub>`) ir Unicode simbolius (pvz., `B<sup>0</sup> → μ<sup>+</sup>μ<sup>−</sup>`, `CO<sub>2</sub>`, `σ`).

DIZAINO IR TECHNINIAI REIKALAVIMAI:
1. Vieno failo HTML (`<html lang="lt" class="dark scroll-smooth">`), naudojant Tailwind CSS CDN ir Google Fonts („Inter“ tekstui, „Plus Jakarta Sans“ antraštėms).
2. Adaptyvus maketas:
   - Telefone (iki 1024px): vieno stulpelio vertikaliai slenkamas dizainas (`max-w-[480px] mx-auto px-4`, `overflow-x-hidden`), pritaikytas valdymui viena ranka.
   - Kompiuteryje (`lg:`): konteineris išsiplečia (`lg:max-w-6xl lg:px-8`), straipsnio tekstas ir SVG iliustracija išdėstomi greta (`lg:grid lg:grid-cols-12 lg:gap-8`), analizės blokai – šalia vienas kito (`lg:grid-cols-2 lg:gap-6`), o Skyriaus {suvestines_nr} suvestinės kortelės – 4 stulpeliais (`md:grid-cols-2 lg:grid-cols-4 gap-4`).
3. Spalvų paletė:
   - Numatytasis tamsusis OLED režimas: `#0D0E12` fonas, `#16181F` kortelės, `#1D202A` vidiniai blokai, `#262936` kraštinės, `#F3F4F6` tekstas, `#B4BAC8` prislopintas tekstas.
   - Šviesusis žurnalinis režimas: `#FAF9F6` fonas, `#FFFFFF` kortelės, `#F3F1EC` vidiniai blokai, `#E5E1D8` kraštinės.
   - Akcentai: bordo (`#6B212A`, `#8E2E3D`, `#A8384A`, `#D97B8A`) ir alyvuogių žalia (`#4D6140`, `#6F8560`, `#8AA379`).
4. Viršuje: fiksuota 3 px skaitymo progreso juosta (gradientas nuo bordo iki alyvuogių žalios), lipni valdymo juosta (`sticky top-0 z-50 backdrop-blur-md`) su antrašte **„Naujienos!“**, šrifto dydžio valdymu (`A-` / `17` / `A+`, ribos 15–21 px), tamsaus/šviesaus režimo jungikliu ir horizontaliai slenkama skyrių navigacija ({nav_mygtukai}).
5. SLINKIMO KLAIDOS PREVENCIJA (JS):
   - Slenkant puslapį (scroll / IntersectionObserver), GRIEŽTAI DRAUDŽIAMA kviesti `scrollIntoView()` ant navigacijos mygtukų arba keisti `window.location.hash` / `history.replaceState`.
   - Horizontalią navigaciją stumk TIK su `navContainer.scrollTo({{ left: btn.offsetLeft - navContainer.offsetWidth / 2 + btn.offsetWidth / 2, behavior: 'smooth' }})`.
   - Skyriams pridėk `scroll-mt-32`.
6. Žurnalinis viršelis (masthead) su alyvuogių žalios kairės kraštinės juosta, data ({date_lt}), antrašte ir skaitymo trukme ({SKAITYMO_TRUKME}).
7. Vizualai: prie kiekvienos iš {viso_naujienu} naujienų įterpk švarią, minimalistinę, techninę ar scheminę vektorinę iliustraciją (`<svg viewBox="0 0 640 400" class="w-full h-auto">`) tamsiame fone (`#0B0D14`) su lietuviškais žymėjimais, `FIG. 01`–`FIG. {viso_naujienu:02d}` etiketėmis ir `<figcaption>` parašu.
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
