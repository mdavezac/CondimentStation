local homedir="{{homedir}}"

family("project")
setenv("CURRENT_FUN_WITH_HOMEDIR", homedir)

{% if srcdir -%}
local srcdir="{{srcdir}}"
setenv("CURRENT_FUN_WITH_DIR", srcdir)
{% endif -%}

prepend_path("CMAKE_PREFIX_PATH", homedir)
prepend_path("DYLD_FALLBACK_LIBRARY_PATH", pathJoin(homedir, "lib"))
prepend_path("PATH", pathJoin(homedir, "bin"))

{% if julia_package_dir -%}
setenv("JULIA_PKGDIR", "{{julia_package_dir}}")
{% endif -%}

{% for package in modules -%}
load("{{package}}")
{% endfor %}

{% if virtualenv -%}
setenv("VIRTUAL_ENV", "{{virtualenv}}")
set_alias("pydoc", pathJoin("{{virtualenv}}", "bin", "python")  .. " -m pydoc")
{%     if virtualenv != homedir -%}
prepend_path("PATH", pathJoin("{{virtualenv}}", "bin"))
{%     endif -%}
{% endif -%}


setenv("CURRENT_FUN_WITH", "{{project}}")
setenv("HISTFILE", pathJoin(homedir, ".zhistory"))

{% if cc is not none -%}
setenv('CC', "{{cc}}")
{% endif -%}
{% if cxx is not none -%}
setenv('CXX', "{{cxx}}")
{% endif -%}
{% if fc is not none -%}
setenv('FC', "{{fc}}")
{% endif -%}
{% if f77 is not none -%}
setenv('F77', "{{f77}}")
{% endif -%}

{% if footer -%}
{{footer}}
{% endif -%}
