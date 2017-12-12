<?php
    $PID = shell_exec('nohup python ../provaSpeech.py 1 > /dev/null & echo $!');
    header('location: mainEnd.php?pid='.$PID.'');
?>

<!-- <html>
    <head>
        <link rel="stylesheet" type="text/css" href="style.css" />
    	<title>Start listening </title>
	</head>

	<body>
    	<div data-role="page">
            <div id="wrapper">
                <div id="wrapper-inner">
                    <header data-role="header">
                        <div id="logo">
                            <h1>
                                <a href="#"> SPAKER ACTIVE, GO AWAY WITH YUOR FUCK'IN CAR</a>
                            </h1>
                        </div>
                    </header>
                </div>
            </div>
        </div>
    </body>
</html> -->
