# EnergieID Webhook - Izen

Geautomatiseerd de opbrengst van uw zonnepanelen (geïnstalleerd door Izen) upload naar EnergieID.be

Deze tool maakt gebruik van de *Incoming Webhook*-integratie van EnergieID.

## BELANGRIJK

**Izen maakt sinds 2022 gebruik van een [nieuw platform][PVmonitor] waardoor dit script niet langer werkt.**
**Dit script kan dus niet langer gebruikt worden om data uit het platform te halen en op te laden in EnergieID, HomeAssistant, ...**

Gelukkig kan je de data [rechtstreeks uitlezen uit de Solis omvormer][blogpost].
Zo kan je deze alsnog via de EnergieID webhook opladen :)

## Opzet

1. Op het EnergieID-platform - [https://www.energieid.be][EnergieID]
    1. Activeer de [*Incoming Webhook*-integratie][integraties]
    2. Koppel de integratie aan het juiste dossier en vul de App-naam in: `EnergieID Webhook - Izen`
    3. Kopieer de *Webhook URL*  
       Deze dien je te gebruiken met parameter `-u`
    4. Kopieer de *meter-ID* die naast de meter voor jouw PV-installatie staat  
       Deze dien je te gebruiken met parameter `-m`
2. Op het IZEN-platform - [https://izen-monitoring.be][IzenMonitoring]
    1. Login op het platform
    2. Kopieer de guid uit de adresbalk (alles na `?guid=`)  
       Deze dien je te gebruiken met de parameter `-g`


## Gebruik

```bash
$ ./energieid_webhook_izen.py -h
    
usage: energieid_webhook_izen.py [-h] [-c CONFIG] [-u URL] [-m METERID]
                                 [-g GUID] [-d]

Automatically post IZEN solar info via WebHook

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        config.json file containing url, meter and guid
  -u URL, --url URL     EnergieID Webhook url
  -m METERID, --meter METERID
                        EnergieID MeterID
  -g GUID, --guid GUID  Izen GUID
  -d, --debug           Enable debugging
```

## Config bestand

```json
{
    "url":"https://hooks.energyid.eu/services/WebhookIn/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/xxxxxxxxxxxx",
    "meter":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "guid":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

[PVmonitor]: https://izen-pvmonitoring.be/ "PV Dashboard"
[blogpost]: https://sequr.be/blog/2021/08/reading-ginlong-solis-inverter-over-serial-and-importing-in-home-assistant-over-mqtt/ "Reading Ginlong Solis inverter over serial and importing in Home Assistant over MQTT"
[EnergieID]: https://www.energieid.be
[integraties]: https://www.energieid.be/integrations
[IzenMonitoring]: https://izen-monitoring.be
