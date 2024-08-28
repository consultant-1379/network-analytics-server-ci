@echo off

for /D %%A IN ("C:\Users\EBAMURP\Desktop\Results\*") do (
 for /D %%B IN ("%%A\*") do (
  FORFILES /P "%%B" /D -15 /C "cmd /C if @isdir==TRUE rmdir /S /Q @path"
 )
)
pause

