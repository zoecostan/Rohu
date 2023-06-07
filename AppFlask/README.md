## Objectif :

Dans un premier temps, il f&aut créer une application flask qui, à partir de l'API OpenWeatherMap (et d'autres potentiellement), va récupérer les données météorologiques d'un point mais aussi l'élévation du terrain associée à ce point, traiter ces données et donner des instructions au drône sur son comportement en fonction de la météo et d'autres facteurs comme la proximité avec des aéroports ou encore d'autres zones à éviter, dangereuses ou interdites. Les aéroports doivent être évités dans un rayon de 8km. 

### Etapes :

1) Créer une application Flask qui récupère les données météo et l'élévation du terrain à partir de l'API OpenWeatherMap.
2) Créer un point de terminaison (endpoint) dans votre application Flask qui prend les coordonnées d'un point et renvoie la météo de ce point.
3) Récupérer une base de données MySQL contenant tous les aéroports en Espagne de votre tuteur.
4) Ajouter une fonctionnalité à votre application Flask pour vérifier la distance à partir des coordonnées sélectionnées et trouver les aéroports les plus proches (à moins de 8 km).
5) Préparer une réponse avec toutes les données demandées (météo, élévation du terrain et aéroports les plus proches).

### Conseils :

- Dans le fichier Flask, modifier la fonction process_forecast pour effectuer une requête à l'API OpenWeatherMap et récupérer les données météo du point spécifié par les coordonnées lat et lng. - Il est possible de conserver la partie qui renvoie simplement les données météo pour le moment.
- Dans le fichier Flask toujours, créer une nouvelle fonction pour récupérer l'élévation du terrain à partir d'une API appropriée. Utiliser les coordonnées lat et lng pour effectuer cette requête. Il faut trouver une API appropriée pour obtenir ces informations d'élévation du terrain.
- Intégrer la base de données MySQL contenant les aéroports en Espagne dans l'application Flask. Il faut se connecter à la base de données, exécuter des requêtes SQL et récupérer les résultats.
- Ajouter une fonctionnalité pour calculer la distance entre les coordonnées sélectionnées et les aéroports de la base de données. Il est possible d'utiliser la formule de la distance entre deux points sur la sphère (par exemple, la formule de la distance orthodromique) pour calculer la distance en kilomètres.
- Modifier la fonction process_forecast pour renvoyer les données de météo, d'élévation du terrain et les aéroports les plus proches (à moins de 8 km) dans le format souhaité.
- S'assurer de comprendre chaque partie du code fourni et de remplir les sections manquantes, notamment l'accès à la base de données et le calcul de la distance entre les coordonnées.
