# Mouvement accéléré

Un véhicule démarre à l’arrêt et accélère uniformément. Quelle est la relation entre la durée du trajet et la distance parcourue ?

$$
s(t) = \frac{1}{2} a t^2
$$

Modifie l’accélération avec le curseur et observe le graphique.

**Interactive graphic — authored input declaration.**

Control defaults are author-specified initial values, not learner input. Parameter names bind the controls to the symbolic geometry. For a select control, the parameter is the zero-based option index used by its piecewise expression; all alternatives are retained. A checkbox parameter is 1 when checked and 0 when unchecked; its declared default is Boolean. No learner attempt or result is implied.

```json
{
  "attributes": {
    "id": "muweave-homepage:accelerated-motion",
    "parameters": [
      {
        "continuous": false,
        "default": "1.5",
        "kind": "slider",
        "label": "a",
        "maximum": "3",
        "minimum": "0.5",
        "name": "a",
        "step": "0.5",
        "unit": "\\frac{\\text{m}}{\\text{s}^{2}}"
      }
    ],
    "static_fallback": "control defaults"
  },
  "children": [
    {
      "attributes": {
        "axes": "both",
        "grid": true,
        "numbers": true,
        "summary": "Coordinate system with x from 0 to 6 and y from 0 to 60",
        "ticks": true,
        "x_grid_step": "1",
        "x_label": "t",
        "x_range": [
          "0",
          "6"
        ],
        "x_step": "1",
        "x_unit": "\\text{s}",
        "y_grid_step": "10",
        "y_label": "s",
        "y_range": [
          "0",
          "60"
        ],
        "y_step": "10",
        "y_unit": "\\text{m}"
      },
      "children": [
        {
          "attributes": {
            "colors": {
              "stroke": {
                "name": "teal",
                "srgb": "#008080"
              }
            },
            "domain": [
              "0",
              "6"
            ],
            "expression": "a*t**2/2",
            "variable": "t"
          },
          "type": "graphic_function_plot"
        }
      ],
      "type": "coordinate_system"
    }
  ],
  "type": "interactive_graphic"
}
```

1\. Lis la distance après 2 secondes et après 4 secondes. Quel facteur obtiens-tu en doublant le temps ?

2\. Double l’accélération de 1.5 à 3 mètres par seconde au carré. Comment la distance change-t-elle pour une même durée ?

La version imprimée utilise l’accélération initiale de 1.5 mètre par seconde au carré. Calcule les valeurs pour d’autres accélérations à l’aide de la formule.
