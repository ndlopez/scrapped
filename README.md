# Scrapped data repository

Update this data repo and JS will request from here.

## Output from SIDC.be CSV file 

Date Mon, 04 Dec 2023 11:49:59 GMT<br>
Server Apache/2.4.41 (Ubuntu)<br>
X-Content-Type-Options nosniff<br>
Last-Modified Fri, 01 Dec 2023 11:44:07 GMT<br>
ETag "2b9bd6-60b71492a8fc0"<br>
Accept-Ranges bytes<br>
Content-Length 2857942<br>
Connection close<br>
Content-Type text/csv

## Batch help

Get information about a file:

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

## Matplotlib help: adding CJK chars

By default Matplotlib ignores (does NOT support) CJK chars even if input as strings. To parse such chars it's necessary to add a font that can accept CJK chars (in my case Japanese).

A quick [Duckduckgo](https://duckduckgo.com/?t=ffab&q=noto+sans+font&atb=v320-1&ia=web) search will help to find a font that can support Japanese chars. In any way, a [zip file](https://github.com/ndlopez/assort_opt/blob/44ee47dca32c8462dd39d2455ad37fec68057f61/assets/fonts.zip) is included in the data dir.

To install run the following:

    $ python3.11

    >> print(matplotlib.matplotlib_fname())

To set up:

    fprop = fontManager.FontProperties(fname="NotoSansJP-Regular.otf")


This returns a path, copy the font-file to such path.

Close the IDE, or emacs and run python code again.

If the above doesnt work DEL the following file and run python code again:

    $ rm ~/.matplotlib/fontlist*.json

