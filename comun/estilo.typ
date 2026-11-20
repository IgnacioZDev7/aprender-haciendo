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

// Página oscura de apertura de capítulo, con el estilo de la portada.
// La llama el filtro comun/aperturas.lua antes de cada capítulo numerado.
#let apertura(acento, volumen, num, titulo, codigo) = {
  pagebreak(to: "even", weak: true)
  page(fill: rgb("#0D1117"), margin: 0pt, header: none, footer: none)[
    #set text(font: "DejaVu Sans Mono")
    #show raw.where(block: true): set block(fill: none, inset: 0pt, radius: 0pt)
    #show raw.where(block: true): set text(size: 6.4pt, fill: acento.transparentize(50%))
    #set par(leading: 0.55em, spacing: 0pt)
    #place(top + left, dx: 5mm, dy: 6mm, raw(codigo, block: true))
    #place(top + left, dx: 10mm, dy: 10mm, block(fill: rgb("#0D1117"), inset: (x: 2mm, y: 1.5mm),
      text(size: 6.5pt, weight: "bold", tracking: 1.5pt, fill: rgb("#C9D1CC"))[SERIE APRENDER HACIENDO · VOLUMEN #volumen]))
    #place(bottom + left, dx: 10mm, dy: -14mm, block(width: 128mm - 20mm, fill: rgb("#0D1117"), inset: 2mm)[
      #text(size: 8pt, weight: "bold", tracking: 2pt, fill: rgb("#F2F4F3"))[CAPÍTULO]
      #v(6pt)
      #text(size: 72pt, weight: "bold", fill: acento, top-edge: "cap-height", bottom-edge: "baseline")[#num]
      #v(16pt)
      #par(leading: 0.45em, text(size: 18pt, weight: "bold", fill: rgb("#F2F4F3"), hyphenate: false)[#titulo#text(fill: acento)[\_]])
    ])
  ]
}

// Contraportada oscura, al final del libro. La agrega comun/aperturas.lua.
#let contraportada(acento, volumen, texto, puntos) = {
  pagebreak(to: "even", weak: true)
  page(fill: rgb("#0D1117"), margin: (x: 14mm, top: 16mm, bottom: 14mm), header: none, footer: none)[
    #set text(font: "DejaVu Sans Mono", fill: rgb("#F2F4F3"), size: 8.6pt)
    #set par(leading: 0.62em, spacing: 0.9em, justify: false)
    #text(size: 6.5pt, weight: "bold", tracking: 1.5pt, fill: rgb("#C9D1CC"))[SERIE APRENDER HACIENDO · VOLUMEN #volumen]
    #v(10mm)
    #text(size: 10pt)[#texto]
    #v(6mm)
    #text(size: 7pt, weight: "bold", tracking: 1.5pt, fill: acento)[EN ESTE LIBRO]
    #v(1mm)
    #for p in puntos [#text(fill: acento)[✓] #p \ ]
    #v(1fr)
    #line(length: 100%, stroke: (paint: rgb("#3A4048"), thickness: 0.6pt, dash: "dashed"))
    #v(2mm)
    #grid(columns: (1fr, auto), align: (left + bottom, right + bottom),
      [#text(size: 7pt, fill: rgb("#9AA7A0"))[VOLUMEN 1 · Programar desde cero \ VOLUMEN 2 · Del programa al producto] \
       #v(2mm) #text(size: 11pt, weight: "bold")[Ignacio Zarate]],
      text(size: 40pt, weight: "bold", fill: acento)[#volumen])
  ]
}
