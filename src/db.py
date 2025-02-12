from pymongo import MongoClient

def get_db_client():
    client = MongoClient('mongodb://localhost:27017/')
    return client

def store_invoice_in_db(invoice_data):
    """
    Speichert einen einzelnen Rechnungsdatensatz in der MongoDB-Sammlung.
    
    Args:
        invoice_data (dict): Extrahierte Rechnungsdaten.
    """
    client = get_db_client()
    db = client.invoice_db 
    invoices = db.invoices  

    # Um zu prüfen, ob eine Rechnung mit der gleichen Nummer und dem gleichen Absender bereits existiert.
    duplicate = invoices.find_one({
        "rechnung_nummer": invoice_data.get("rechnung_nummer"),
        "sender": invoice_data.get("sender")
    })
    if duplicate:
        print(f"Doppelte Rechnung gefunden: {invoice_data.get('rechnung_nummer')}, Einfügen überspringen.")
    else:
        invoices.insert_one(invoice_data)
    client.close()
