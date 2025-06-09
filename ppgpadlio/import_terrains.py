import csv
from datetime import timedelta
from reservation_app.models import Terrain, Centre

with open('reservation_app/data/terrains_padel_tunisie.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        centre_nom = row['centre_nom'].strip()
        try:
            centre = Centre.objects.get(nom=centre_nom)
        except Centre.DoesNotExist:
            print(f"Centre non trouvé: {centre_nom}")
            continue
        
        etat = row['etat'].strip()
        prix = float(row['prix'])
        temps = timedelta(minutes=int(row['temps']))
        
        Terrain.objects.create(
            nom=row['nom'].strip(),
            description=row['description'].strip(),
            type=row['type'].strip(),
            prix=prix,
            temps=temps,
            etat=etat,
            centre=centre
        )
print("Import terminé")
