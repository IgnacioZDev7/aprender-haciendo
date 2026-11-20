-- Cajas de la serie «Aprender Haciendo» para el PDF (Typst).
-- En HTML los callouts quedan como los dibuja Quarto (colores en estilos.css).
local colores = {
  objetivos = "1F3A5F", problema = "E07A2E", error = "C0392B", consejo = "2F6DB5",
  ["reto-basico"] = "4F9D69", ["reto-intermedio"] = "2E7D6B", ["reto-desafio"] = "1F3A5F",
  ia = "6C4AB6", resumen = "2E7D6B", nota = "7A7A7A", plantilla = "E07A2E",
}
local por_tipo = { note = "1F3A5F", tip = "2F6DB5", warning = "C0392B",
  caution = "7A7A7A", important = "6C4AB6" }

local function a_typst(t)
  if not t then return "" end
  local txt = pandoc.utils.stringify(t)
  return (txt:gsub("([%[%]#%*_`$<>@\\])", "\\%1"))
end

function Callout(el)
  if not quarto.doc.is_format("typst") then return nil end
  local color = por_tipo[el.type] or "1F3A5F"
  for _, c in ipairs(el.attr.classes) do
    if colores[c] then color = colores[c] end
  end
  local titulo = a_typst(el.title)
  local res = { pandoc.RawBlock("typst",
    '#caja(rgb("#' .. color .. '"), [' .. titulo .. '])[') }
  local cont = el.content
  if cont and cont.t then cont = { cont } end
  table.insert(res, pandoc.Div(cont or {}))
  table.insert(res, pandoc.RawBlock("typst", "]"))
  return res
end
