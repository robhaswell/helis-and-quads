-------------------------------------------------------------------------------
-- FM2M ToolBox
-- version: 0.80
-- release date: 2022-12
-- author: Robert Janiszewski JimB40
-- http://fm2m.jimb40.com
-------------------------------------------------------------------------------
local toolName = "TNS|FM2M ToolBox 0.80|TNE"
local SP = '/FM2M/TOOLBOX/'
return {run=(loadScript(SP..'loader','bx')('SA',SP,'bx')).run}
