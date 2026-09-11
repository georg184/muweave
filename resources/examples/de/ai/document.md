# Beschleunigte Bewegung

Ein Fahrzeug startet aus dem Stand und beschleunigt gleichmässig. Wie hängen Fahrzeit und zurückgelegter Weg zusammen?

$$
s(t) = \frac{1}{2} a t^2
$$

Verändere die Beschleunigung am Schieberegler und beobachte den Graphen.

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

1\. Lies den Weg nach 2 Sekunden und nach 4 Sekunden ab. Welchen Faktor erhältst du, wenn du die Zeit verdoppelst?

2\. Verdopple die Beschleunigung von 1.5 auf 3 Meter pro Sekunde zum Quadrat. Wie verändert sich der Weg bei gleicher Fahrzeit?

In der Druckfassung gilt die vorgegebene Beschleunigung von 1.5 Metern pro Sekunde zum Quadrat. Berechne die Werte für andere Beschleunigungen mit der Formel.
