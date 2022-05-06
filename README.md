# KIV/PSI - úkol 3 (REST client)

## Popis fungování
Aplikace nejprve zjistí pozici ISS (International Space Station) z API dostupného na adrese 
http://api.open-notify.org/iss-now.json. Dotaz je vytvořen pomocí knihovny **requests**

Pro takto získané souřadnice aktuální polohy ISS je následně zjištěn východ a západ Slunce pomocí API https://api.sunrise-sunset.org/json.
Díky tomu je poté možné určit, zda se ISS nachází na osvětlené, nebo neosvětlené straně Země.

Nakonec je zjištěno, zda jsou aktuálně na daném místě ideální podmínky pro pozorování - tedy 1-2 hodiny před východem Slunce,
nebo 1-2 hodiny po západu Slunce.

Pro sjednocení je vše počítáno v UTC.

## Spuštění
Spusťte soubor `main.py`, žádné atributy nejsou vyžadovány (ani očekávány).
Aplikace výstup napíše do standardního výstupu (konzole/terminálu)

## Verze Pythonu
Pro spuštění doporučuji Python verzi 3.8 (a novější), aplikace využívá funkci `datetime.fromisoformat`, která ve
starších verzích nemusí být dostupná.