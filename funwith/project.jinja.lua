local homedir="{{homedir}}"

family("project")
setenv("CURRENT_FUN_WITH_HOMEDIR", homedir)

{% if srcdir -%}
local srcdir="{{srcdir}}"
setenv("CURRENT_FUN_WITH_DIR", srcdir)
{% endif -%}

prepend_path("CMAKE_PREFIX_PATH", homedir)
prepend_path("DYLD_FALLBACK_LIBRARY_PATH", pathJoin(os.getenv("HOME"), "/lib"))
prepend_path("DYLD_FALLBACK_LIBRARY_PATH", "/usr/lib")
prepend_path("DYLD_FALLBACK_LIBRARY_PATH", "/usr/local/lib")
prepend_path("DYLD_FALLBACK_LIBRARY_PATH", pathJoin(homedir, "lib"))
prepend_path("PATH", pathJoin(homedir, "bin"))

{% if julia_package_dir -%}
setenv("JULIA_PKGDIR", "{{julia_package_dir}}")
{% endif -%}

{% for package in modules -%}
load("{{package}}")
{% endfor %}

if (mode() == "load") then
  local ldlibpaths=os.getenv("LD_LIBRARY_PATH")
  local fallbacks=os.getenv("DYLD_FALLBACK_LIBRARY_PATH")
  if(fallbacks ~= nil) then
    setenv("_FUNWITH_DYLD_FALLBACK_LIBRARY_PATH", fallbacks)
  end
  if( ldlibpaths ~= nil) then
    prepend_path("DYLD_FALLBACK_LIBRARY_PATH", ldlibpaths)
  end
elseif (mode() == "unload") then
  local fallbacks=os.getenv("_FUNWITH_DYLD_FALLBACK_LIBRARY_PATH")
  if(fallbacks ~= nil) then
    setenv("DYLD_FALLBACK_LIBRARY_PATH", fallbacks)
  else
    unsetenv("DYLD_FALLBACK_LIBRARY_PATH")
  end
  unsetenv("_FUNWITH_DYLD_FALLBACK_LIBRARY_PATH")
end

{% if virtualenv -%}
setenv("VIRTUAL_ENV", "{{virtualenv}}")
set_alias("pydoc", "python -m pydoc")
{%     if virtualenv != homedir -%}
prepend_path("PATH", pathJoin("{{virtualenv}}", "bin"))
prepend_path("LD_LIBRARY_PATH", pathJoin("{{virtualenv}}", "lib"))
prepend_path("LD_LIBRARY_PATH", pathJoin("{{virtualenv}}", "lib64"))
prepend_path("DYLD_FALLBACK_LIBRARY_PATH", pathJoin("{{virtualenv}}", "lib"))
prepend_path("DYLD_FALLBACK_LIBRARY_PATH", pathJoin("{{virtualenv}}", "lib64"))
{%     endif -%}
{% endif -%}


setenv("CURRENT_FUN_WITH", "{{project}}")
setenv("HISTFILE", pathJoin(homedir, ".zhistory"))

{% if cc is not none -%}
setenv('cc', "{{cc}}")
{% endif -%}
{% if cxx is not none -%}
setenv('cxx', "{{cxx}}")
{% endif -%}
{% if fc is not none -%}
setenv('fc', "{{fc}}")
{% endif -%}
{% if f77 is not none -%}
setenv('f77', "{{f77}}")
{% endif -%}

{% if footer -%}
{{footer}}
{% endif -%}
