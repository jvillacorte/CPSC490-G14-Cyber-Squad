--[[
to-word.lua: proposal/proposal.md → the course Word template, in one command.

    pandoc proposal/proposal.md -o proposal/proposal.docx --reference-doc=proposal/reference.docx --lua-filter=proposal/to-word.lua --resource-path=proposal

What it does:
  1. Cover page: the template's own cover table (its own page), filled from the
     header block at the top of proposal.md: title, group, authors,
     repository, date. Emails are left for you to type in Word.
  2. Sections: "## 1. Introduction" becomes Word's numbered "1. Introduction"
     (the typed "1." / "1.1" is dropped so Word numbers it, as the template
     does); "## 0. Abstract" is the unnumbered, centred Abstract heading, on
     its own page. Everything before Abstract in proposal.md is skipped, and
     so are the quote blocks (the template's guidance).
  3. Issue references: [epic:#12](https://github.com/OWNER/REPO/issues/12),
     likewise story / feature / enhancement / bug / task / sub-task. A full
     issue URL in a sentence breaks the Word layout, so the text keeps only
     "[epic:#12]" and the URLs go to "Appendix A. Issue References" at the
     end, in order of first citation, the way §8 lists references.
Font, size, spacing and indentation come from proposal/reference.docx (the
template with its formatting turned into styles).
]]

local KINDS = {
  epic = "epic", story = "story", ["user-story"] = "story",
  feature = "feature", features = "feature", enhancement = "enhancement",
  bug = "bug", task = "task", ["sub-task"] = "sub-task", subtask = "sub-task",
}

local function esc(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end
local function str(v) return v and pandoc.utils.stringify(v) or "" end
local function raw(xml) return pandoc.RawBlock("openxml", xml) end

-- ── 1. Issue references ─────────────────────────────────────────────────────
local refs, seen = {}, {}
local function parse_ref(text)
  local kind, num = text:match("^%[?%s*([%a%-]+)%s*:%s*#(%d+)%s*%]?$")
  kind = kind and KINDS[kind:lower()]
  if kind then return kind, num end
end
local function ref_link(el)
  local kind, num = parse_ref(pandoc.utils.stringify(el.content))
  if not kind then return nil end
  local tag = "[" .. kind .. ":#" .. num .. "]"
  local key = tag .. " " .. el.target
  local r = seen[key]
  if not r then
    -- bookmark on the appendix entry; the tag in the text jumps to it
    r = { tag = tag, url = el.target, title = "", anchor = "issue_" .. kind:gsub("%-", "") .. "_" .. num .. "_" .. (#refs + 1) }
    seen[key] = r
    refs[#refs + 1] = r
  end
  if r.title == "" and el.title and el.title ~= "" then r.title = el.title end
  -- internal link (blue, underlined) to the entry in Appendix A
  return pandoc.RawInline("openxml", '<w:hyperlink w:anchor="' .. r.anchor .. '" w:history="1"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">'
    .. tag .. "</w:t></w:r></w:hyperlink>")
end

-- ── 2. Cover page from the reference doc's own cover table ─────────────────
local function read_cover()
  local path = PANDOC_WRITER_OPTIONS and PANDOC_WRITER_OPTIONS.reference_doc
  if not path then return nil end
  local f = io.open(path, "rb")
  if not f then return nil end
  local bytes = f:read("a"); f:close()
  local files = {}
  for _, e in ipairs(pandoc.zip.Archive(bytes).entries) do files[e.path] = e end
  if not files["word/document.xml"] then return nil end
  local xml = files["word/document.xml"]:contents()
  local rels = files["word/_rels/document.xml.rels"] and files["word/_rels/document.xml.rels"]:contents() or ""
  local body = xml:match("<w:body>(.*)")
  local stop = body and body:find(">Abstract</w:t>", 1, true)
  if not stop then return nil end
  -- cut at the start of the paragraph that holds the Abstract heading
  local cut, i = nil, 1
  while true do
    local s = body:find("<w:p[ >]", i)
    if not s or s > stop then break end
    cut, i = s, s + 1
  end
  if not cut then return nil end
  -- Word 2010+ attributes (w14:paraId …) aren't declared in pandoc's document root.
  local cover = body:sub(1, cut - 1):gsub(' w1%w*:%w+="[^"]*"', "")
  -- A picture on the cover (the logo) points at the template's own image
  -- relationship; hand it to pandoc as an image so it gets one in this file.
  local image_for = function(rid, style)
    local target = rels:match('Id="' .. rid .. '"[^>]-Target="([^"]+)"') or rels:match('Target="([^"]+)"[^>]-Id="' .. rid .. '"')
    local e = target and files["word/" .. target]
    if not e then return nil end
    local name = "cover-" .. target:gsub(".*/", "")
    pandoc.mediabag.insert(name, nil, e:contents())
    local attr = {}
    local w, h = style:match("width:([%d%.]+)pt"), style:match("height:([%d%.]+)pt")
    if w then attr.width = string.format("%.3fin", tonumber(w) / 72) end
    if h then attr.height = string.format("%.3fin", tonumber(h) / 72) end
    return pandoc.Div({ pandoc.Para({ pandoc.Image({}, name, "", pandoc.Attr("", {}, attr)) }) }, pandoc.Attr("", {}, { ["custom-style"] = "Normal" }))
  end
  return cover, image_for
end

-- Split cover XML into raw blocks, turning each picture paragraph into an image.
-- Only top-level picture paragraphs are swapped; one inside a table stays raw.
local function cover_blocks(cover, image_for)
  local blocks, pos, s = pandoc.List(), 1, 1
  while true do
    local ps = cover:find("<w:p[ >]", s)
    if not ps then break end
    local _, pe = cover:find("</w:p>", ps, true)
    if not pe then break end
    local p = cover:sub(ps, pe)
    local before = cover:sub(1, ps - 1)
    local _, opened = before:gsub("<w:tbl>", "")
    local _, closed = before:gsub("</w:tbl>", "")
    local rid = opened == closed and (p:match('<v:imagedata r:id="([^"]+)"') or p:match('r:embed="([^"]+)"'))
    local img = rid and image_for(rid, p:match('<v:shape [^>]-style="([^"]+)"') or "")
    if img then
      if ps > pos then blocks:insert(raw(cover:sub(pos, ps - 1))) end
      blocks:insert(img)
      pos = pe + 1
    end
    s = pe + 1
  end
  if pos <= #cover then blocks:insert(raw(cover:sub(pos))) end
  return blocks
end

-- Value cells of the cover table, counted across the table in order:
-- row 1 title | row 2 semester, date | row 3 team | row 4 repository |
-- rows 5–9 member name, email | row 10 advisor, reviewer.
local function fill_cover(cover, f)
  local values = { [2] = f.title, [6] = f.date, [8] = f.team, [10] = f.repository, [34] = f.reviewer }
  if f.semester ~= "" then values[4] = f.semester end
  for k = 1, math.min(#f.members, 5) do
    values[12 + 4 * (k - 1)] = f.members[k].name
    values[14 + 4 * (k - 1)] = f.members[k].email
  end
  local n = 0
  return (cover:gsub("<w:tc>(.-)</w:tc>", function(cell)
    n = n + 1
    local v = values[n]
    if not v or v == "" then return nil end
    local rpr = cell:match("<w:pPr>.-(<w:rPr>.-</w:rPr>)") or ""
    local run = "<w:r>" .. rpr .. '<w:t xml:space="preserve">' .. esc(v) .. "</w:t></w:r>"
    -- drop whatever the template had in the cell's text runs, then add ours
    local p_open, p_body = cell:match("^(.-<w:p[^>]*>)(.*)$")
    if not p_open then return nil end
    local ppr = p_body:match("^%s*(<w:pPr>.-</w:pPr>)") or ""
    local tail = cell:match("</w:p>(.*)$") or ""
    return "<w:tc>" .. p_open .. ppr .. run .. "</w:p>" .. tail .. "</w:tc>"
  end))
end

-- Cover fields, from the header block at the top of proposal.md:
--   # Project Proposal — Secure Member Portal
--   **Group 5 — Example Team** · Sponsor: …
--   Authors: Doe, Jane (jdoe), Roe, Richard (rroe)
--   Repository: https://github.com/OWNER/REPO
--   Date: October 11, 2026
-- A YAML front-matter key of the same name (title, team, repository, date,
-- reviewer, semester, members: [{name, email}]) wins over the header line.
-- A value still holding a 〈placeholder〉 is left blank.
local function lines_of(inlines)
  local lines, cur = {}, pandoc.List()
  for _, il in ipairs(inlines) do
    if il.t == "SoftBreak" or il.t == "LineBreak" then lines[#lines + 1] = pandoc.utils.stringify(cur); cur = pandoc.List()
    else cur:insert(il) end
  end
  lines[#lines + 1] = pandoc.utils.stringify(cur)
  return lines
end
local function clean(s) s = (s or ""):gsub("^%s+", ""):gsub("%s+$", ""); return s:find("〈", 1, true) and "" or s end

local function cover_fields(blocks, meta)
  local f = { title = "", date = "", team = "", repository = "", reviewer = "", semester = "", members = {} }
  for _, b in ipairs(blocks) do
    if b.t == "Header" and b.level >= 2 then break end
    if b.t == "Header" and b.level == 1 then
      local t = pandoc.utils.stringify(b.content)
      f.title = clean(t:match("^[Pp]roject [Pp]roposal%s*[—–%-:]+%s*(.+)$") or t)
    elseif b.t == "Para" or b.t == "Plain" then
      for _, line in ipairs(lines_of(b.content)) do
        local grp = line:match("^(Group%s.-)%s*·") or line:match("^(Group%s.+)$")
        if grp then f.team = clean(grp) end
        local authors = line:match("^Authors?:%s*(.+)$")
        if authors then
          for name in authors:gmatch("([^,()]+,%s*[^,()]-)%s*%b()") do
            name = clean(name)
            if name ~= "" then f.members[#f.members + 1] = { name = name, email = "" } end
          end
        end
        f.repository = clean(line:match("^Repository:%s*(.+)$")) ~= "" and clean(line:match("^Repository:%s*(.+)$")) or f.repository
        f.date = clean(line:match("^Date:%s*(.+)$")) ~= "" and clean(line:match("^Date:%s*(.+)$")) or f.date
        f.reviewer = clean(line:match("^Reviewer:%s*(.+)$")) ~= "" and clean(line:match("^Reviewer:%s*(.+)$")) or f.reviewer
      end
    end
  end
  for _, k in ipairs({ "title", "date", "team", "repository", "reviewer", "semester" }) do
    if meta[k] then f[k] = clean(str(meta[k])) end
  end
  if meta.members then
    f.members = {}
    for _, m in ipairs(meta.members) do
      local tbl = type(m) == "table" and m.name
      f.members[#f.members + 1] = { name = clean(tbl and str(m.name) or str(m)), email = clean(tbl and str(m.email) or "") }
    end
  end
  return f
end

-- ── 3. Headings ─────────────────────────────────────────────────────────────
-- "1." / "1.1" / "0." typed in the markdown heading → (number, rest)
local function split_number(h)
  local first = h.content[1]
  if first and first.t == "Str" and first.text:match("^%d+[%.%d]*$") then
    local rest = pandoc.List(h.content):clone()
    rest:remove(1)
    if rest[1] and rest[1].t == "Space" then rest:remove(1) end
    return first.text, rest
  end
  return nil, h.content
end

local function unnumbered_heading(text, align, new_page)
  return raw('<w:p><w:pPr><w:pStyle w:val="Heading1"/>' .. (new_page and "<w:pageBreakBefore/>" or "")
    .. '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>'
    .. '<w:ind w:left="0"/><w:jc w:val="' .. align .. '"/></w:pPr><w:r><w:t xml:space="preserve">'
    .. esc(text) .. "</w:t></w:r></w:p>")
end

-- The template separates sections with one empty body line before each heading
-- (no space before/after on the headings themselves).
local function blank_line() return raw('<w:p><w:pPr><w:pStyle w:val="BodyText"/></w:pPr></w:p>') end

function Pandoc(doc)
  doc = doc:walk({ Link = ref_link })

  local out, started, first_section, in_refs = pandoc.List(), false, true, false
  local function ref_entry(b)
    return pandoc.Div({ b }, pandoc.Attr("", {}, { ["custom-style"] = "Reference Entry" }))
  end
  local function add(b)
    -- quote blocks are the template's guidance ("delete before submitting"): never exported
    if b.t == "BlockQuote" then return
    elseif in_refs and b.t == "Para" then out:insert(ref_entry(b))
    else out:insert(b) end
  end
  for _, b in ipairs(doc.blocks) do
    if b.t == "Header" and b.level == 2 then started = true end
    if started then
      if b.t == "Header" and b.level <= 3 then
        local num, rest = split_number(b)
        local text = pandoc.utils.stringify(rest)
        if b.level == 2 then in_refs = text:lower() == "references" end
        if b.level == 2 and text:lower() == "abstract" then
          -- the cover is its own page, and so is the Abstract
          out:insert(unnumbered_heading("Abstract", "center", true))
        elseif b.level == 2 then
          if first_section then
            -- the template starts "1. Introduction" on a new page
            out:insert(raw('<w:p><w:pPr><w:pStyle w:val="Heading1"/><w:pageBreakBefore/></w:pPr><w:r><w:t xml:space="preserve">'
              .. esc(text) .. "</w:t></w:r></w:p>"))
            first_section = false
          else
            out:insert(blank_line())
            out:insert(pandoc.Header(1, rest, b.attr))
          end
        else
          -- "### 1.1 Related Work" → numbered 1.1; "### Planned activities" → unnumbered bold
          out:insert(blank_line())
          out:insert(pandoc.Header(num and 2 or 3, rest, b.attr))
        end
      else
        add(b)
      end
    end
  end

  if #refs > 0 then
    out:insert(blank_line())
    out:insert(unnumbered_heading("Appendix A. Issue References", "left"))
    out:insert(pandoc.Para({ pandoc.Str("Issues cited in the text by their tag, in order of first citation.") }))
    for k, r in ipairs(refs) do
      local id = tostring(90000 + k) -- clear of the bookmark ids pandoc numbers from 0
      local line = pandoc.List({
        pandoc.RawInline("openxml", '<w:bookmarkStart w:id="' .. id .. '" w:name="' .. r.anchor .. '"/>'),
        pandoc.Str(r.tag),
        pandoc.RawInline("openxml", '<w:bookmarkEnd w:id="' .. id .. '"/>'),
        pandoc.Space() })
      if r.title ~= "" then line:extend({ pandoc.Str(r.title .. "."), pandoc.Space() }) end
      line:insert(pandoc.Link(r.url, r.url))
      out:insert(ref_entry(pandoc.Para(line)))
    end
  end

  -- leftover 〈placeholders〉 would be printed in the Word file: say so
  local left = {}
  pandoc.Pandoc(out):walk({ Str = function(s) if s.text:find("〈", 1, true) and #left < 5 then left[#left + 1] = s.text end end })
  if #left > 0 then
    io.stderr:write("to-word.lua: proposal still has 〈placeholders〉 (e.g. " .. table.concat(left, " ") .. "): replace them before submitting\n")
  end

  local cover, image_for = read_cover()
  if cover then
    local blocks = cover_blocks(fill_cover(cover, cover_fields(doc.blocks, doc.meta)), image_for)
    for k = #blocks, 1, -1 do out:insert(1, blocks[k]) end
  else
    io.stderr:write("to-word.lua: no cover page: pass --reference-doc=proposal/reference.docx\n")
  end
  -- the cover shows these; keep pandoc from printing its own title block
  for _, k in ipairs({ "title", "subtitle", "author", "date", "abstract" }) do doc.meta[k] = nil end
  doc.blocks = out
  return doc
end
