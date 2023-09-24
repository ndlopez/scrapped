# Scrapped data repository

Better to update this repo and JS will request from here.

## Batch help

<code>
FOR %%? IN ("C:\somefile\path\file.txt") DO (
   ECHO File Name Only       : %%~n?
   ECHO File Extension       : %%~x?
   ECHO Name in 8.3 notation : %%~sn?
   ECHO File Attributes      : %%~a?
   ECHO Located on Drive     : %%~d?
   ECHO File Size            : %%~z?
   ECHO Last-Modified Date   : %%~t?
   ECHO Drive and Path       : %%~dp?
   ECHO Drive                : %%~d?
   ECHO Fully Qualified Path : %%~f?
   ECHO FQP in 8.3 notation  : %%~sf?
   ECHO Location in the PATH : %%~dp$PATH:?
)
</code>

