#import "@preview/orange-book:0.7.1": book, part, chapter, appendices

// Colores de cada libro (definidos en _quarto.yml sin «#», porque Pandoc lo escapa)
#let acento = rgb("#$color-acento$")
#let color-texto = rgb("#$color-texto$")
#let volumen = "$volumen$"
// Blanco hueso, el mismo color del recibo de la portada
#set page(fill: rgb("#FBFAF5"))

#show: book.with(
// La portada (imagen) ya contiene título, subtítulo y autor.
  title: [],
  subtitle: [],
  author: "",
  cover-background: none,
  copyright: [
    #set par(spacing: 0.75em)
    *$title$* \
    $subtitle$ \
    Serie «Aprender Haciendo» · Volumen $volumen$ \
    $version$ · $date$
    #v(0.7em)
    *Autor:* $for(by-author)$$it.name.literal$$sep$, $endfor$ \
    Producción intelectual de la asignatura $materia$, $universidad$.$if(docente)$ \
    *Docente:* $docente$$endif$
    #v(0.7em)
    *Diseño de portada e interior:* elaboración propia, con HTML, CSS y Typst. Las figuras y diagramas también son de elaboración propia. No se usaron imágenes de terceros. \
    *Tipografías:* Libertinus Serif y JetBrains Mono (SIL Open Font License) y DejaVu Sans Mono (licencia libre de DejaVu). \
    *Uso de inteligencia artificial:* declarado en «Antes de empezar».
    #v(0.7em)
    © 2026 $for(by-author)$$it.name.literal$$sep$, $endfor$. El texto se distribuye con licencia Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0). El código de MiTienda se distribuye con licencia MIT.
    #v(0.7em)
    Versión web, código y soluciones: #link("https://ignaciozdev7.github.io/aprender-haciendo/")[ignaciozdev7.github.io/aprender-haciendo] \
    Generado con Quarto y Typst.
  ],
  lang: "es",
  paper-size: "a5",
  margin: (inside: 18mm, outside: 14mm, top: 18mm, bottom: 18mm),
  main-color: color-texto,
  heading-style: 2,
  font-size: 9.5pt,
  first-line-indent: false,
  outline-small-width: 8cm,
$if(cover-typst)$
  cover: image("$cover-typst$", width: 100%, height: 100%, fit: "cover"),
$endif$
$if(toc-depth)$
  outline-depth: $toc-depth$,
$endif$
  supplement-chapter: "Capítulo",
  supplement-part: "Parte",
)

// Separación entre párrafos (el libro no usa sangría de primera línea)
#set par(spacing: 0.9em)
