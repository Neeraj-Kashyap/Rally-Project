<?php
    $PID = $_GET['pid'];
?>
<html>
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" type="text/css" href="style.css" />

        <title>CAR driven by the voice </title>
    </head>

    <body>
    	<div data-role="page">
            <div id="wrapper">
                <div id="wrapper-inner">
                    <header data-role="header">
                        <div id="logo">
                            <h1>
                                <a href="#"> START WITH COMMANDS </a>
                            </h1>
                            <span> speak on the microphone </span>
                        </div>
                    </header>
                    <div id="content">
                        <div class="container">
                            <div id="row">
                                <p> Press STOP to come back to the main window</p>
                            </div>

                            <a href="end.php?pid=<?php echo $PID ?>">
                                <div id="row" class="tasto">
                                    STOP
                                </div>
                            </a>
                        </div>
                    </div>
                </div> <!-- end wrapper inner -->
            </div> <!-- end wrapper -->
        </div> <!-- end data role -->
    </body>
</html>