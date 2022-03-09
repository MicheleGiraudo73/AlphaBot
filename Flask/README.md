# Comandare un Alphabot con un sito web tramite freccie direzionali o comando combinato

Per far funzionare l'Alphabot useremo un WEB Server -> FLASK, il linguaggio python e i database
Si utilizza flask in modo che il web server giri su un raspberry e noi tramite un comune browser ci colleghiamo a questo web server che ci ritorna la pagina/e
Il database viene utilizzato:
                              - Per il login -> si controlla nel database se l'username e la password inseriti nel form ci siamo
                              - Movimento complessi 
                              - Accessi -> ogni persona che accede viene registrato con la data
                              - Registro Movimento -> tramite cookie si registra ci ha fatto quel determinato movimento o movimento complesso in una precisa ora e data

### Struttura dei file
app.py -> file di gestione del web server (logica di backend)
databaseAlphabot.db -> database che contiene le tabelle -> User (Login), Accessi (Registro accessi degli utenti alla pagina), RegistroMovimenti, movimenti(tabella dei movimenti)
Login.html -> pagina di login
index.html -> pagina in cui comanderemo il nostro Alphabot

### Funzionamento
Dopo aver effettuato il Login nella pagina di Login il programma ci reindirizza alla pagina dei comandi
Dalla pagina index.html comanderemo il nostro Alphabot:
                                                        - Tasti -> comandi base
                                                        - Casella di testo -> comandi complessi
