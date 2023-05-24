function setNumbers(target, min, max){
    console.log(target, min, max);
    if (!target){
        return false;
    }
    else {
        var min = min,
            max = max;
            selectElement = document.getElementById(target);
        for (var num = max; num >= min; num--){
            selectElement.add(new Option(num));
        }
    }
};
