# AUT_Database

Für den zweiten Teil des Autoatisierungskurses soll ein System entwickelt werden, welches Daten von einem MQTT-Server abholt und in einer Datenbank speichert. Diese Daten sollen dann in einem Report visualisiert werden.

## Aufgabenstellung
Umfang fürs bestehen der Aufgabe:

- [ ] Einfache Lösung mit CSV-Datei als Datenbank
- [ ] Daten aller relevanten (siehe unten) Topics werden vollständig und korrekt gespeichert
- [ ] Python-Programm, welches eine beliebige Zeitreihe aus der Datenbank visualisiert
- [ ] Der Report im Markdown enthält einen Plot einer Ausgewählten Zeitreihe für die Sie die Daten gespeichert haben
- [ ] Mindestens 15 Minuten Daten sind gespeichert

Durch folgende Aufgaben kann die Punktzahl erhöht werden:

- [ ] Datenbank wird durch tinyDB, SQLite oder InfluxDB ersetzt
- [ ] Plots werden durch Dashboard mit z.B. mit Grafana oder Plotly ersetzt
- [ ] System ist durch config-Datei konfigurierbar (z.B. MQTT-Server)
- [ ] Sinnvolle Fehlerbehandlung z.B. bei Verbindungsabbruch zum MQTT-Server
- [ ] Daten oder Informationen über die Daten können einfach aus anderen Systemen abgerufen werden (auch während das System läuft), z.B. durch eine REST-API oder SQL-Abfragen