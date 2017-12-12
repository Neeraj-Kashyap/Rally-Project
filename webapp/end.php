<?php
$pid = trim($_GET['pid']);
shell_exec( 'sudo kill '.$pid.'');
?>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="style.css" />
        <title>Stop listening </title>
    </head>

    <body>
        <div data-role="page">
            <div id="wrapper">
                <div id="wrapper-inner">
                    <header data-role="header">
                        <div id="logo">
                            <h1>
                                <a href="index.html"> CAR STOPPED SUCCESFULLY</a>
                            </h1>
                        </div>
                    </header>
                </div>
            </div>
        </div>
    </body>
</html>
