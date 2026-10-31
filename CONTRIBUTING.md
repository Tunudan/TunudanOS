# Contribuer à Tunudan OS

## Branches

| Branche | Rôle |
| --- | --- |
| `main` | Version stable. Chaque push construit les ISO ; on n'y pousse jamais directement. |
| `develop` | Intégration : les nouveautés y arrivent par pull request. |
| `feature/<sujet>` | Une nouveauté, partie de `develop` (ex. `feature/bureau-cosmic`). |
| `fix/<sujet>` | Une correction, partie de `develop`. |
| `release/X.Y.Z` | Préparation d'une version : `VERSION`, `CHANGELOG.md`, derniers correctifs. |
| `hotfix/X.Y.Z` | Correction urgente, partie de `main`. |

```sh
git switch develop && git pull
git switch -c feature/mon-sujet
# … commits …
make lint
git push -u origin feature/mon-sujet   # puis ouvrir une pull request vers develop
```

## Messages de commit

Style [Conventional Commits](https://www.conventionalcommits.org/fr/) :

```text
feat(avance): ajoute Budgie à la page « Bureau »
fix(debutant): renomme le menu de démarrage UEFI
docs: explique la construction sans Docker
ci: met en cache l'ISO de Linux Mint
build(docker): ajoute build-essential à l'image Debian
chore: met à jour le .gitignore
```

Portées utiles : `minimal`, `debutant`, `avance`, `expert`, `theme`, `tools`, `branding`, `docker`.

## Publier une version

1. `git switch -c release/0.5.0 develop`
2. Mettre à jour `VERSION` et `CHANGELOG.md`, puis faire une pull request vers `main`.
3. Après la fusion, depuis `main` :
   ```sh
   git tag -a v0.5.0 -m "Tunudan OS 0.5.0"
   git push origin v0.5.0
   ```
   GitHub Actions construit les ISO et publie la release (le tag doit correspondre à `VERSION`).
4. Ramener `main` dans `develop` : `git switch develop && git merge main && git push`.

## Avant d'ouvrir une pull request

- `make lint` passe ;
- si le changement touche une édition, `make iso EDITION=…` puis `make test EDITION=…` ;
- `CHANGELOG.md` est complété dans la section « Non publié ».
