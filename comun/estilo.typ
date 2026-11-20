// Estilo de la serie «Aprender Haciendo» para el PDF
#let azul = rgb("#1F3A5F")
#let caja(color, titulo, cuerpo) = block(
  width: 100%, breakable: true, fill: color.lighten(93%),
  stroke: (left: 2.5pt + color), inset: (x: 8pt, y: 7pt), radius: (right: 3pt),
  above: 1.2em, below: 1.2em,
)[
  #set par(first-line-indent: 0pt)
  #if titulo != [] [#text(weight: "bold", fill: color, size: 0.95em)[#titulo] #v(0.1em)]
  #set text(size: 0.94em)
  #cuerpo
]
#show raw.where(block: true): set block(width: 100%, fill: rgb("#F4F6F8"), inset: 6pt, radius: 3pt, breakable: false)
#show raw.where(block: true): set text(size: 7.4pt)
#show raw: set text(font: "DejaVu Sans Mono")
