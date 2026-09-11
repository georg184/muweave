# Accelerated motion

A vehicle starts from rest and accelerates uniformly. How are travel time and distance related?

$$
s(t) = \frac{1}{2} a t^2
$$

Change the acceleration with the slider and observe the graph.

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

1\. Read the distance after 2 seconds and after 4 seconds. What factor do you get when you double the time?

2\. Double the acceleration from 1.5 to 3 metres per second squared. How does the distance change for the same travel time?

The print version uses the initial acceleration of 1.5 metres per second squared. Use the formula to calculate values for other accelerations.
