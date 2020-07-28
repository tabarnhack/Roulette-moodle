Roulette Moodle
===============

Une roulette pour donner du suspense sur les notes données à travers une plateforme Moodle.

# Getting started

Il faut lancer une instance en local afin de pouvoir tester la roulette.

Pour configurer l'url de l'instance Moodle, il faut mettre à la racine du dossier api un fichier `.env.local` avec comme contenu :
```
MOODLE_URL = "<url de l'instance Moodle>"
```

De même pour l'url de l'api, il faut un fichier `.env.local` avec le contenu :
```
VUE_APP_ROOT_API=<url de l'api>
```

Note: pour une instance en local avec docker-compose, l'api est exposée sur `localhost:5000`.

## Dépendences

Pour build le projet, il y a besoin des paquets suivants:
- docker
- docker-compose

Il faut ensuite lancer la commande suivante

```
docker-compose up
```

# TODO
- Affichage des résultats
- A voir...