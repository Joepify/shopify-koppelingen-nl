# Shopify koppelingen voor Nederlandse webshops

Een neutraal overzicht van de koppelingen die Nederlandse Shopify-winkels het vaakst nodig hebben: **Exact Online, Moneybird, Sendcloud, PostNL, bol.com en betalen met iDEAL en Wero**. Per koppeling lees je hoe de verbinding werkt (app of API), wat je vooraf moet beslissen en waar het in de praktijk misgaat.

Dit is geen vergelijking van apps en geen advies voor een merk. Prijzen en functies van apps veranderen vaak, dus kijk voor de actuele stand altijd bij de leverancier.

## Voor wie

- Webshopeigenaren die willen weten of ze een app nodig hebben of maatwerk.
- Webbouwers die een koppeling plannen en de risico's willen kennen.

## Wat zit erin

| Bestand | Doel |
|---|---|
| `README.md` | Het overzicht en de valkuilen |
| `intake-vragen.md` | Vragen om te stellen voor je een koppeling kiest of laat bouwen |
| `verify_shopify_webhook.py` | Werkend voorbeeld: Shopify-webhooks controleren met HMAC (met test) |

## Hoe werkt een koppeling bij Shopify?

Een koppeling gebruikt een van drie routes:

1. **App uit de Shopify App Store.** Je installeert, logt in bij beide systemen en stelt in welke gegevens waarheen gaan. Snel en goedkoop te starten. Je krijgt de logica die de appmaker heeft gekozen.
2. **Koppeling via de Shopify Admin API.** Een stukje software dat orders, producten en voorraad leest en schrijft, meestal met GraphQL en webhooks. Je bepaalt zelf de regels, maar het moet gebouwd en bijgehouden worden.
3. **Een tussenplatform of connector**, bijvoorbeeld voor marktplaatsen, die een andere kant weer met een eigen API aansluit.

Een **webhook** is een bericht dat Shopify naar jouw systeem stuurt bij een gebeurtenis (nieuwe order, betaling, terugbetaling). Controleer altijd de handtekening, zie `verify_shopify_webhook.py`.

## Boekhouding

### Exact Online
- **Hoe:** via een app, of maatwerk via de Exact Online REST API (OAuth 2.0).
- **Wat gaat over:** orders als verkoopboeking of factuur, btw-codes, betalingen, terugbetalingen, klanten, soms voorraad terug naar Shopify.
- **Valkuilen:** btw per land en voor OSS, grootboekrekeningen per betaalmethode, uitbetalingen van de PSP die niet 1 op 1 aansluiten op orders (kosten en inhoudingen), afronding op regelniveau, en de limieten van de Exact-API (zie hun documentatie).
- Meer uitleg: [Shopify Exact Online koppeling](https://www.joepify.nl/shopify-exact-online-koppeling?utm_source=github&utm_medium=readme&utm_campaign=shopify-koppelingen-nl).

### Moneybird
- **Hoe:** app of maatwerk via de Moneybird REST API.
- **Wat gaat over:** facturen, contacten, betalingen en creditnota's.
- **Valkuilen:** btw-tarieven en OSS, dubbele contacten bij gastbestellingen, creditnota's bij gedeeltelijke retouren, en het koppelen van betalingen aan de juiste factuur.

## Verzenden

### Sendcloud
- **Hoe:** de Shopify-integratie van Sendcloud, of via hun API.
- **Wat gaat over:** orders naar het verzendplatform, labels, trackingnummers terug naar Shopify, verzendregels per vervoerder.
- **Valkuilen:** gewichten en afmetingen ontbreken in de producten, verzendmethoden in de checkout die niet overeenkomen met de vervoerder, deelzendingen en adresvelden (huisnummer-toevoeging).

### PostNL
- **Hoe:** via een eigen app of integratie van PostNL, of via een verzendplatform. Directe API-koppelingen zijn mogelijk maar vragen een zakelijke overeenkomst.
- **Valkuilen:** pakketpunten en bezorgopties tonen in de checkout, adresvalidatie, handtekening-bij-aflevering en brievenbuspakjes (afmeting en gewicht).

## Marktplaatsen

### bol.com
- **Hoe:** via de Retailer API van bol.com, of via een connector die producten, voorraad en orders synchroniseert met Shopify.
- **Wat gaat over:** aanbod (EAN, prijs, levertijd), voorraad, orders en verzendbevestigingen.
- **Valkuilen:** een EAN per product of variant is verplicht, prijzen en voorraad lopen uit de pas als synchronisatie te traag is, annuleringen en retouren die twee kanten op moeten, en eigen regels van bol.com voor productinformatie. Check altijd de actuele voorwaarden van bol.com.

## Betalen

### iDEAL en Wero
- **Hoe:** via Shopify Payments (waar beschikbaar, met een Nederlands KvK-nummer) of via een betaalprovider zoals Mollie of Adyen.
- **Wat verandert:** iDEAL gaat stap voor stap over naar iDEAL | Wero. Je betaalprovider regelt veel; vraag hem wat jij moet aanpassen en test een echte betaling.
- **Valkuilen:** terugbetalingen die niet terugkomen in je boekhouding, dubbele orders bij een betaling die te laat wordt bevestigd, en het juiste logo in je checkout en footer.
- Zie ook het stappenplan in [joepify-kennisbank](https://github.com/Joepify/joepify-kennisbank/blob/main/gidsen/ideal-naar-wero-overstappen.md).

## Veelvoorkomende valkuilen bij elke koppeling

1. **Geen duidelijke bron van waarheid.** Spreek af welk systeem leidend is voor voorraad, prijs en klantgegevens.
2. **Geen herstelplan.** Wat gebeurt er als de koppeling een uur uitvalt? Webhooks kunnen te laat of dubbel aankomen. Bouw met idempotentie: dezelfde order twee keer ontvangen mag niet twee keer boeken.
3. **API-limieten.** Shopify beperkt GraphQL-verzoeken op basis van kosten per query. Plan zware synchronisaties buiten de piekuren.
4. **Btw en afronding.** Verschillen van een cent tussen systemen leiden tot afstemproblemen. Spreek af op welk niveau je afrondt.
5. **Terugbetalingen en deelzendingen.** De happy flow werkt altijd. Test deelretouren, geannuleerde orders en kortingscodes.
6. **Variantennamen en SKU's.** Als SKU's niet uniek zijn, raakt alles in de war.
7. **Geen monitoring.** Zonder melding bij een fout merk je het pas als een klant belt.
8. **Persoonsgegevens.** Zorg voor een verwerkersovereenkomst met elke partij die klantgegevens ontvangt.

## Kies je een app of maatwerk?

| Situatie | Meestal |
|---|---|
| Standaardproces, gangbaar systeem | App |
| Eigen boekingsregels of bijzondere btw | Maatwerk |
| Meer dan twee systemen die elkaar nodig hebben | Maatwerk of tussenplatform |
| Laag aantal orders, snel starten | App |
| Gevoelige koppeling die je niet kunt missen | Maatwerk met monitoring |

Vergelijk een app op: wat doet hij met terugbetalingen, wat kost hij per maand bij jouw volume, wat gebeurt er bij een storing, en wie helpt je als iets niet klopt.

## Webhooks veilig ontvangen

```bash
python3 verify_shopify_webhook.py --test
```

Het script toont hoe je de `X-Shopify-Hmac-Sha256` header controleert met de ruwe request body en het app-geheim, en bevat een zelftest. Gebruik de ruwe bytes van de body, niet een opnieuw geserialiseerde versie.

## Laat het mij doen

Ik bouw of installeer de koppeling tussen je Shopify-winkel en je boekhouding of verzending. Vaste prijs op offerte na een korte intake, beheer daarna vanaf €25 per maand (excl. btw). [Meer over koppelingen](https://www.joepify.nl/shopify-koppelingen?utm_source=github&utm_medium=readme&utm_campaign=shopify-koppelingen-nl) of [stuur een WhatsApp-bericht](https://wa.me/31687195043?text=Hoi%20Ayoub%2C%20ik%20kom%20via%20GitHub%20%28shopify-koppelingen-nl%29%20en%20wil%20hulp%20met%20shopify%20koppeling.).

## Over Joepify

[Joepify](https://www.joepify.nl?utm_source=github&utm_medium=readme&utm_campaign=shopify-koppelingen-nl) is een webbureau aan de Metaalhof 27 in Rotterdam. Ayoub Assaidi bouwt Shopify-winkels en koppelingen voor een vaste prijs vooraf. Een overzicht van de mogelijkheden staat op [Shopify koppelingen](https://www.joepify.nl/shopify-koppelingen?utm_source=github&utm_medium=readme&utm_campaign=shopify-koppelingen-nl), en voor maatwerk kun je een [Shopify developer inhuren](https://www.joepify.nl/shopify-developer?utm_source=github&utm_medium=readme&utm_campaign=shopify-koppelingen-nl).

## English

A neutral overview of common Dutch Shopify integrations (Exact Online, Moneybird, Sendcloud, PostNL, bol.com, iDEAL/Wero): how each connects (app or API), what to decide up front and the typical pitfalls. Includes `verify_shopify_webhook.py`, a standard-library Python 3 example of verifying Shopify webhook HMAC signatures, with a self-test.

## Licentie

Tekst: CC BY 4.0. Code: MIT. Zie [LICENSE](LICENSE).
