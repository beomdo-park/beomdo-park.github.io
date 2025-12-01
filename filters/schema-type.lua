local utils = require("pandoc.utils")

local DEFAULT_SITE_URL = "https://beomdo-park.github.io"

local function to_string(value)
  if value == nil then
    return nil
  end
  local result = utils.stringify(value)
  if result == nil or result == "" then
    return nil
  end
  return result
end

local function as_list(value)
  if value == nil then
    return {}
  end
  if value.t == "MetaList" then
    local items = {}
    for i = 1, #value do
      items[#items + 1] = value[i]
    end
    return items
  end
  return { value }
end

local function has_portfolio_category(meta)
  local categories = as_list(meta.categories)
  for _, item in ipairs(categories) do
    local label = to_string(item)
    if label then
      local lower = label:lower()
      if lower:find("portfolio") or lower:find("포트폴리오") then
        return true
      end
    end
  end
  return false
end

local function collect_authors(author_meta)
  local names = {}
  for _, entry in ipairs(as_list(author_meta)) do
    local name = to_string(entry)
    if name then
      names[#names + 1] = name
    end
  end
  return names
end

local escape_map = {
  ["\b"] = "\\b",
  ["\f"] = "\\f",
  ["\n"] = "\\n",
  ["\r"] = "\\r",
  ["\t"] = "\\t",
  ["\\"] = "\\\\",
  ['"'] = '\\"',
}

local function json_escape(str)
  return str
    :gsub('[\\"%z\001-\031]', function(char)
      local mapped = escape_map[char]
      if mapped then
        return mapped
      end
      return string.format("\\u%04x", char:byte())
    end)
end

local function is_array(tbl)
  local count = 0
  for key, _ in pairs(tbl) do
    if type(key) ~= "number" then
      return false
    end
    count = count + 1
  end
  for index = 1, count do
    if tbl[index] == nil then
      return false
    end
  end
  return true
end

local function json_encode(value)
  local value_type = type(value)
  if value_type == "string" then
    return '"' .. json_escape(value) .. '"'
  elseif value_type == "number" or value_type == "boolean" then
    return tostring(value)
  elseif value == nil then
    return "null"
  elseif value_type == "table" then
    if is_array(value) then
      local encoded = {}
      for index = 1, #value do
        encoded[#encoded + 1] = json_encode(value[index])
      end
      return "[" .. table.concat(encoded, ",") .. "]"
    else
      local encoded = {}
      for key, inner_value in pairs(value) do
        encoded[#encoded + 1] = '"' .. json_escape(key) .. '":' .. json_encode(inner_value)
      end
      table.sort(encoded)
      return "{" .. table.concat(encoded, ",") .. "}"
    end
  end
  return '""'
end

local function build_schema(meta)
  local schema_type = to_string(meta["schema-type"]) or to_string(meta.schema_type)
  if schema_type == nil then
    schema_type = has_portfolio_category(meta) and "Dataset" or "Article"
  end

  meta["schema-type"] = pandoc.MetaString(schema_type)

  local schema = {
    ["@context"] = "https://schema.org",
    ["@type"] = schema_type,
    headline = to_string(meta.title) or "",
  }

  local description = to_string(meta.description) or to_string(meta.subtitle)
  if description then
    schema.description = description
  end

  local authors = collect_authors(meta.author)
  if #authors == 0 then
    authors = { "Beomdo Park" }
  end

  if #authors == 1 then
    schema.author = {
      ["@type"] = "Person",
      name = authors[1],
    }
  else
    schema.author = {}
    for _, name in ipairs(authors) do
      schema.author[#schema.author + 1] = {
        ["@type"] = "Person",
        name = name,
      }
    end
  end

  local published = to_string(meta.date)
  if published then
    schema.datePublished = published
  end

  local modified = to_string(meta["date-modified"])
  if modified then
    schema.dateModified = modified
  end

  local canonical = to_string(meta["canonical-url"]) or to_string(meta.canonical_url)
  if canonical then
    schema.url = canonical
  else
    schema.url = DEFAULT_SITE_URL
  end

  local keywords = {}
  for _, item in ipairs(as_list(meta.categories)) do
    local label = to_string(item)
    if label then
      keywords[#keywords + 1] = label
    end
  end
  if #keywords > 0 then
    schema.keywords = keywords
  end

  local image = to_string(meta.image)
  if image then
    if not image:match("^https?://") then
      image = DEFAULT_SITE_URL .. "/" .. image:gsub("^/", "")
    end
    schema.image = image
  end

  if schema_type == "Dataset" then
    schema.license = "https://creativecommons.org/licenses/by/4.0/"
    schema.creator = schema.author
  end

  return schema
end

function Meta(meta)
  local schema = build_schema(meta)
  local script = '<script type="application/ld+json">' .. json_encode(schema) .. '</script>'

  local script_block = pandoc.MetaBlocks({ pandoc.RawBlock("html", script) })
  local header = meta["header-includes"]

  if header == nil then
    meta["header-includes"] = pandoc.MetaList({ script_block })
  elseif header.t == "MetaList" then
    header[#header + 1] = script_block
  else
    meta["header-includes"] = pandoc.MetaList({ header, script_block })
  end

  return meta
end
