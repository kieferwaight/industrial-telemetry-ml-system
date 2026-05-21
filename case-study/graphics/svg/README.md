# State Overlay SVG Generation

Use this folder to generate scenario graphs by mutating `base-graph.svg` so the output keeps the same style and group naming conventions.

## Files

- `base-graph.svg` - canonical style/template with axis, legend, and group IDs.
- `empty_vs_full_state_overlay.svg` - older handcrafted overlay reference.
- `generate_state_overlay_svg.py` - JSON-to-SVG generator script (template-driven).
- `sample_state_overlay_data.json` - sample input payload.

## Generate a graph

Run from this folder:

```bash
python3 generate_state_overlay_svg.py \
  --input sample_state_overlay_data.json \
  --output generated_state_overlay.svg
```

The resulting SVG preserves key IDs from `base-graph.svg` and updates dynamic nodes:

- `Data`
- `Baseline-Empty-State-Chart`
- `High-Resistance-Full-State-Chart`
- `Graph`
- `X-Axis-Label`
- `Y-Axis-Label`
- `Legend`
- `Legend-Item-1` (empty)
- `Legend-Item-2` (full)
- `Focus`
- `Focus-Line`
- `Focus-Sign`

## Input JSON notes

- `empty_points` and `full_points` must have the same number of points.
- Each point is `[x, y]` normalized to `[0, 1]`.
- `x` maps left-to-right across the plot.
- `y=1` is top of the plot, `y=0` is bottom.

## Mode switching

The generated SVG has `data-mode` on the root element:

- `overlay`
- `empty`
- `full`

You can switch mode from JavaScript:

```js
svgElement.setAttribute("data-mode", "empty");
svgElement.style.setProperty("--accent", "#69b37b");
svgElement.style.setProperty("--ink", "#0a1d57");
```
