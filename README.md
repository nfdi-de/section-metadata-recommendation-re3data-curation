# Kuratierung der re3data-Empfehlung (Sektion Meta(daten), Terminologien, Provenienz)

Dieses Repository dokumentiert die redaktionelle Überarbeitung der Empfehlung
**„Kennzeichnung von NFDI-Datenrepositorien in re3data"** nach der
Community-Kommentierungsphase (bis 18. Mai 2026). Ziel ist ein für jeden
einzelnen Kommentar nachvollziehbarer Weg von **Beitrag → Diskussion →
Entscheidung → Textänderung**.


# Anleitung für die Schreibgruppe

Diese Anleitung setzt **keine** GitHub-Kenntnisse voraus. Alles geschieht im
Browser. Du brauchst nur ein GitHub-Konto und musst zum Repository eingeladen
sein.

## Drei Begriffe vorab

- **Issue** („Vorgang"): Für **jeden Kommentar** aus der Kommentierungsphase
  gibt es ein eigenes Issue. Man kann es sich wie eine digitale Karteikarte
  vorstellen: oben steht der ursprüngliche Kommentar, darunter wird diskutiert
  und die Entscheidung festgehalten. Alle Issues findest du im Reiter
  **„Issues"** oben im Repository.
- **Label** („Etikett"): farbige Schlagworte, die an einem Issue kleben und den
  Stand anzeigen (z. B. „wird gerade diskutiert"). Labels setzt man mit wenigen
  Klicks.
- **Pull Request** („Änderungsvorschlag", kurz *PR*): So ändert man den Text der
  Empfehlung. Wichtig zum Verständnis: Eine Änderung wird **nicht sofort**
  übernommen, sondern erst vorgeschlagen, von einer zweiten Person angesehen und
  dann bewusst übernommen. Man kann dabei nichts kaputt machen.

## Der Arbeitsablauf Schritt für Schritt

Dieser Ablauf wiederholt sich für jeden Kommentar. Am Anfang wirkt er
ungewohnt — nach dem ersten Mal ist er Routine.

### Schritt 1 — Einen Kommentar (Issue) auswählen

1. Klick oben im Repository auf den Reiter **„Issues"**.
2. Du siehst die Liste aller offenen Kommentare. Such dir einen aus, der noch
   das Etikett **`status:eingegangen`** trägt (= noch unbearbeitet).
3. Klick auf den Titel, um das Issue zu öffnen.

### Schritt 2 — Kommentar und Textstelle lesen

Oben im Issue steht im eingerückten Block der ursprüngliche Kommentar, wer ihn
geschrieben hat, sowie:

> Bezug: „…" · Abschnitt: [Name des Abschnitts](…)

- **„Bezug"** ist die Textstelle, auf die sich der Kommentar bezieht.
- Der **Abschnitt** ist ein anklickbarer Link. Er springt im Dokument
  `recommendation.md` an die richtige Stelle. Die genaue Passage findest du dort,
  indem du im Browser **Strg+F** (Mac: Cmd+F) drückst und das „Bezug"-Zitat
  eingibst.

### Schritt 3 — Bearbeitung beginnen

1. Rechts neben dem Issue gibt es eine Spalte. Klick bei **„Assignees"** auf das
   Zahnrad und wähle dich selbst aus — so sehen alle, dass du dich kümmerst.
2. Klick bei **„Labels"** auf das Zahnrad. Entferne `status:eingegangen` und
   setze stattdessen **`status:in-diskussion`** (anklicken zum Setzen, erneut
   anklicken zum Entfernen, dann irgendwo daneben klicken zum Schließen).

### Schritt 4 — Diskutieren

1. Scroll im Issue nach unten zum Schreibfeld **„Add a comment"**.
2. Schreib deinen Beitrag und klick **„Comment"**.

Jeder Beitrag wird automatisch mit Name und Zeitpunkt gespeichert. So bleibt die
ganze Diskussion dauerhaft nachvollziehbar. Wenn schon eine Antwort aus der
Kommentierungsphase vorlag, steht sie bereits als erster Kommentar im Issue.

### Schritt 5 — Entscheidung festhalten

Wenn die Gruppe sich einig ist:

1. Schreib einen abschließenden Kommentar nach dem Muster:
   **„Entscheidung: … Begründung: …"**
2. Setz unter **„Labels"** das passende Ergebnis-Etikett:
   `ergebnis:accepted` (übernommen), `ergebnis:rejected` (nicht übernommen),
   `ergebnis:partial` (teilweise) oder `ergebnis:deferred` (später).
3. Ändere das Status-Etikett auf **`status:entschieden`**.

Wenn der Kommentar **keine** Textänderung erfordert (z. B. eine reine
Verständnisfrage), bist du hier fertig: Schließ das Issue oben mit dem Button
**„Close issue"**.

### Schritt 6 — Den Text ändern (Pull Request)

Nur nötig, wenn die Entscheidung eine Änderung an `recommendation.md` bedeutet.
Das geschieht komplett im Browser:

1. Öffne die Datei **`recommendation.md`** (im Reiter **„Code"** anklicken).
2. Klick oben rechts auf das **Stift-Symbol** („Edit this file").
3. Ändere den Text an der betreffenden Stelle.
4. Klick oben rechts auf **„Commit changes…"**. Es öffnet sich ein Fenster.
5. **Wichtig:** Wähle die Option **„Create a new branch for this commit and start
   a pull request"** (nicht „Commit directly"). Den vorgeschlagenen Namen kannst
   du lassen. Klick **„Propose changes"**.
6. Auf der nächsten Seite gibt es ein großes Textfeld. Schreib dort hinein, auf
   welches Issue sich die Änderung bezieht, in der Form **`Closes #12`**
   (die Zahl ist die Nummer des Issues — sie steht im Issue-Titel hinter dem `#`).
   Das sorgt dafür, dass sich das Issue später automatisch schließt.
7. Klick **„Create pull request"**.

Damit ist die Änderung **vorgeschlagen**, aber noch nicht übernommen.

8. **Eine zweite Person** schaut den Vorschlag an (im Reiter **„Pull requests"**,
   unter **„Files changed"** sieht man die Änderung grün/rot markiert) und klickt
   dann oben **„Merge pull request"** → **„Confirm merge"**.

Beim Mergen wird die Änderung in das Dokument übernommen und das verknüpfte Issue
schließt sich von selbst.

### Schritt 7 — Abschließen

Setz am Issue (falls es nicht ohnehin automatisch geschlossen wurde) das Etikett
**`status:eingearbeitet`**. Fertig — dieser Kommentar ist vollständig und
nachvollziehbar erledigt.

## Die Etiketten (Labels) im Überblick

**Stand der Bearbeitung:**

| Label | Bedeutung |
|-------|-----------|
| `status:eingegangen` | noch unbearbeitet |
| `status:in-diskussion` | wird gerade besprochen |
| `status:entschieden` | Entscheidung steht, Umsetzung offen |
| `status:eingearbeitet` | im Text umgesetzt |

**Ergebnis:**

| Label | Bedeutung |
|-------|-----------|
| `ergebnis:accepted` | Vorschlag übernommen |
| `ergebnis:rejected` | nicht übernommen (mit Begründung) |
| `ergebnis:partial` | teilweise übernommen |
| `ergebnis:deferred` | vertagt / nicht in diesem Release |

**Thema** (zur Sortierung, wurde beim Import vergeben):

| Label | Inhalt |
|-------|--------|
| `thema:terminologie` | Bezeichnung „NFDI-Repositorium", Definitionen |
| `thema:scope` | Abgrenzung „fachlich zugehörig", wer gehört dazu |
| `thema:workflow` | Governance, Zuständigkeit, Nachhaltigkeit, Prozess |
| `thema:technik-re3data` | re3data-Schema, Schnittstelle, Metriken |
| `thema:redaktion` | sprachliche und redaktionelle Klarstellungen |

## Praktische Hinweise

- **Eine Person ändert, eine andere prüft.** Niemand merged den eigenen Pull
  Request allein — das Vier-Augen-Prinzip ist Teil der Qualitätssicherung.
- **Rein sprachliche Punkte sammeln.** Die Kommentare mit `thema:redaktion`
  müssen nicht einzeln geändert werden. Eine Person kann mehrere davon in *einem*
  Pull Request zusammenfassen und dort alle nennen: `Closes #29, #30, #31`.
- **Zum Üben:** Geht als Gruppe einen einfachen Kommentar einmal gemeinsam von
  Schritt 1 bis 7 durch. Danach sitzt der Ablauf bei allen.

---

## Veröffentlichung

Das Repository ist während der Schreibphase privat. Zum Abschluss:

1. Repository auf **public** schalten.
2. Vorher in **Zenodo** die GitHub-Integration für dieses Repository aktivieren.
3. Einen **Release** (Tag `v3.1`) anlegen — Zenodo vergibt automatisch eine DOI.

Der finale Stand von `recommendation.md`, die geschlossenen Issues und die
Entscheidungsübersicht bilden zusammen den zitierbaren Nachweis der Reaktion auf
die Kommentierungsphase.
