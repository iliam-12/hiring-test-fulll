function fizzbuzz(n) {
    for (let i = 1; i <= n; i++) {
        let res = "";
        if (i % 3 === 0) res += "Fizz";
        if (i % 5 === 0) res += "Buzz";
        console.log(res || i);
    }
}

if (process.argv.length > 2) {
    let arg = process.argv[2];
    if (arg === '-h' || arg === '--help') {
        console.log("Usage: node fizzbuzz.js\n");
        console.log("   Example:");
        console.log("   node fizzbuzz.js");
        console.log("   > Enter a number: 15");
        process.exit(0);
    }
} else {
    const readline = require('readline');
    const std = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    const numberInput = () => {
        std.question('Enter a number: ', (input) => {
            let number = parseInt(input.trim(), 10);
            if (isNaN(number) || number < 1) {
                console.log("Please enter a valid positive number");
                return numberInput();
            }
            fizzbuzz(number);
            numberInput();
        });
    };
    numberInput();
}