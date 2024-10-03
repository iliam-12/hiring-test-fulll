<?php
function fizzbuzz($n) {
    for ($i = 1; $i <= $n; $i++) {
        $res = "";
        if ($i % 3 === 0) {
            $res .= "Fizz";
        }
        if ($i % 5 === 0) {
            $res .= "Buzz";
        }
        echo $res ?: $i;
        echo "\n";
    }
}

if ($argc > 1) {
    if (in_array($argv[1], ['-h', '--help'])) {
        echo "Usage: python fizzbuzz.py\n\n";
        echo "  Example:\n";
        echo "  php Algo/fizzbuzz.php\n";
        echo "  > Enter a number: 15\n";
        exit(0);
    }
} else {
    while (true) {
        echo "Entrez un nombre: ";
        $input = fgets(STDIN);
        fizzbuzz($input);
    }
}
?>