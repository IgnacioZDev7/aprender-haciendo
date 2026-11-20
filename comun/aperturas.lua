-- Agrega la contraportada al final e inserta una página oscura de apertura antes de cada capítulo numerado
-- (encabezados con id sec-capN, N >= 1). Solo en el PDF (Typst).
-- El fondo de cada apertura es un trozo distinto del código real de MiTienda,
-- indicado en _quarto.yml con la clave codigo-fondo.

local function escapar_str(s)
  return (s:gsub("\\", "\\\\"):gsub('"', '\\"'):gsub("\n", "\\n"))
end
local function escapar_contenido(s)
  return (s:gsub("([%[%]#%*_`$<>@\\])", "\\%1"))
end

function Pandoc(doc)
  if not quarto.doc.is_format("typst") then return nil end
  local ruta = doc.meta["codigo-fondo"] and pandoc.utils.stringify(doc.meta["codigo-fondo"])
  local volumen = doc.meta["volumen"] and pandoc.utils.stringify(doc.meta["volumen"]) or ""
  local lineas = {}
  if ruta then
    local base = quarto.project.directory or "."
    local f = io.open(pandoc.path.join({ base, ruta }), "r")
    if f then
      for l in f:lines() do if l:match("%S") then table.insert(lineas, l) end end
      f:close()
    end
  end
  local nuevos = {}
  for _, b in ipairs(doc.blocks) do
    if b.t == "Header" and b.level == 1 then
      local n = tonumber((b.identifier or ""):match("^sec%-cap(%d+)$"))
      if n and n >= 1 then
        local trozo = {}
        local inicio = ((n - 1) * 13) % math.max(#lineas, 1)
        for i = 1, 70 do
          local l = lineas[((inicio + i - 1) % math.max(#lineas, 1)) + 1]
          if l then table.insert(trozo, l) end
        end
        local titulo = escapar_contenido(pandoc.utils.stringify(b.content))
        table.insert(nuevos, pandoc.RawBlock("typst", string.format(
          '#apertura(acento, "%s", "%02d", [%s], "%s")',
          volumen, n, titulo, escapar_str(table.concat(trozo, "\n")))))
      end
    end
    table.insert(nuevos, b)
  end
  -- Contraportada
  local cp = doc.meta["contraportada"]
  if cp then
    local texto = escapar_contenido(pandoc.utils.stringify(cp.texto or ""))
    local puntos = {}
    for _, p in ipairs(cp.puntos or {}) do
      table.insert(puntos, "[" .. escapar_contenido(pandoc.utils.stringify(p)) .. "]")
    end
    table.insert(nuevos, pandoc.RawBlock("typst", string.format(
      '#contraportada(acento, "%s", [%s], (%s,))', volumen, texto, table.concat(puntos, ", "))))
  end
  doc.blocks = nuevos
  return doc
end
