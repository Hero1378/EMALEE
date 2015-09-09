/*
 *Copyright 2015 Felix Woodhead
 *
 *Licensed under the Apache License, Version 2.0 (the "License");
 *you may not use this file except in compliance with the License.
 *You may obtain a copy of the License at:
 *http://www.apache.org/licenses/LICENSE-2.0
 */


// Get the user's OS and dish out the appropriate executable

function winLink()
{
    document.write("win_Download"); // Sub with download File / Link
}

function macLink()
{
    document.write("mac_Download"); // Sub with download File / Link
}

function unixLink()
{
    document.write("unix_Download"); // Sub with download File / Link
}

// User may 'fluke' their OS name

if (navigator.appVersion.indexOf("Win") != -1)
{
    winLink();
}

if (navigator.appVersion.indexOf("Mac") != -1)
{
    macLink();
}

if ((navigator.appVersion.indexOf("X11") != -1) || 
    (navigator.appVersion.indexOf("Linux") != -1))
{
    unixLink();
}
