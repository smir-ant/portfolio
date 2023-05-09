const headerShort = document.querySelector(".header_short");  // укороченная шапка
const headerFull = document.querySelector(".header_full");  // полная шапка
const headerLogos = document.querySelectorAll(".header_logo");

cards_rules = {
    "red": "старшая",
    "orange": "одно число",
    "yellow": "один цвет",
    "green": "четные",
    "lightblue": "разные цвета",
    "blue": "по порядку",
    "purple": "меньше 4"
}

// ====================== Смена шапки при нажатии ======================
headerLogos.forEach(logo => {
    logo.addEventListener('click', () => {
        headerFull.classList.toggle('hidden');
        headerShort.classList.toggle('hidden');
    });
});


// ====================== ЗАПОЛНЕНИЕ КАРТ ======================
let cards = document.querySelectorAll(".card");  // каждая карта игрока (в руке)
cards.forEach(card => {

    // Сперва накидываем 5 div'ов с классами для наполнения дальше в каждую из карт
    let p_cardInfo = document.createElement('p');  // создаём p
    p_cardInfo.classList = ('card-text main-num');  // главное число
    card.append(p_cardInfo);  // добавляем <p> в <div class='card'>
    p_cardInfo = document.createElement('p');
    p_cardInfo.classList = ('card-text up-num');  // верхнее число
    card.append(p_cardInfo);
    p_cardInfo = document.createElement('p');
    p_cardInfo.classList = ('card-text down-num');  // нижнее число
    card.append(p_cardInfo);
    p_cardInfo = document.createElement('p');
    p_cardInfo.classList = ('card-text rule left');  // левое правило
    card.append(p_cardInfo);
    p_cardInfo = document.createElement('p');
    p_cardInfo.classList = ('card-text rule right');  // правое правило
    card.append(p_cardInfo);


    // Пилим класс: "card card-num-3 card-color-lightblue" на цвет и номинал
    const cardColor = card.className.split(' ')[2].split('-')[2]; // например: red 
    const cardValue = card.className.split(' ')[1].split('-')[2]  // например: 2

    // ===== Подстановка правил =====
    card.querySelector(".rule.left").innerHTML = cards_rules[cardColor]; 
    card.querySelector(".rule.right").innerHTML = cards_rules[cardColor];
    
    // ===== Подстановка числа =====
    card.querySelector(".main-num").innerHTML = cardValue;
    card.querySelector(".up-num").innerHTML = cardValue;
    card.querySelector(".down-num").innerHTML = cardValue;
})


