#import "@preview/orange-book:0.7.1": book, part, chapter, appendices

#show: book.with(
// La portada (imagen) ya contiene título, subtítulo y autor.
  title: [],
  subtitle: [],
  author: "",
  cover-background: none,
  copyright: [
    *$title$* \
    $subtitle$ \
    Serie «Aprender Haciendo» \
    #v(0.6em)
    © 2026 $for(by-author)$$it.name.literal$$sep$, $endfor$. Esta obra se distribuye con licencia Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0). \
    #v(0.6em)
    Versión web, código y soluciones: #link("https://ignaciozdev7.github.io/aprender-haciendo/")[ignaciozdev7.github.io/aprender-haciendo] \
    Generado el $date$ con Quarto y Typst.
  ],
  lang: "es",
  paper-size: "a5",
  margin: (inside: 18mm, outside: 14mm, top: 18mm, bottom: 18mm),
  main-color: rgb("#1F3A5F"),
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
