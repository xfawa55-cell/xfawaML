-- Lua 运行器脚本
if #arg < 1 then
    io.stderr:write("Usage: lua lua_runner.lua <script>\n")
    os.exit(1)
end

local script = arg[1]

-- 加载并执行Lua脚本
local status, err = pcall(dofile, script)
if not status then
    io.stderr:write("Lua execution error: " .. tostring(err) .. "\n")
    os.exit(1)
end
