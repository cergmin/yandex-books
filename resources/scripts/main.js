function caruselScrollHandler(e) {
    let prevButton = e.target.parentElement.querySelector(
        '.carusel__control-prev'
    );
    let nextButton = e.target.parentElement.querySelector(
        '.carusel__control-next'
    );

    let containerWidth = e.target.offsetWidth;
    let containerScroll = e.target.scrollLeft;

    let items = e.target.querySelectorAll('.carusel__item');
    let itemWidth = items[items.length - 1].offsetWidth;
    let itemMargin = parseFloat(
        window.getComputedStyle(items[items.length - 1]).marginLeft
    );
    let itemSize = itemWidth + itemMargin;
    
    let visibleItemsAmount = Math.floor(containerWidth / itemSize);
    let prevItemIndex = Math.round(containerScroll / itemSize) - 1;
    let nextItemIndex = Math.round(
        containerScroll / itemSize
    ) + visibleItemsAmount;
    
    for (let i = 0; i < items.length; i++) {
        if (i > prevItemIndex && i < nextItemIndex) {
            items[i].classList.add("visible");
        }
        else {
            items[i].classList.remove("visible");
        }
    }

    if (prevItemIndex + 1 === 0) {
        prevButton.classList.add("hidden");
    }
    else{
        prevButton.classList.remove("hidden");
    }

    if (nextItemIndex >= items.length) {
        nextButton.classList.add("hidden");
    }
    else{
        nextButton.classList.remove("hidden");
    }
}

function createCaruselResizeHandler(carusels) {
    return (e) => {
        console.log('carusels resized');
    }
}

function caruselControlsHandler(e) {
    let controlAction = e.target.getAttribute("data-action");
    let caruselContainer = e.target.parentElement.querySelector(
        ".carusel__container"
    );
    let caruselContainerWidth = caruselContainer.offsetWidth;

    let item = caruselContainer.querySelector('.carusel__item:last-child');
    let itemWidth = item.offsetWidth;
    let itemMargin = parseFloat(
        window.getComputedStyle(item).marginLeft
    );
    let itemSize = itemWidth + itemMargin;
    
    let visibleItemsAmount = Math.floor(
        caruselContainerWidth / itemSize
    );

    switch (controlAction) {
        case "goNext":
            caruselContainer.scrollBy({
                left: visibleItemsAmount * itemSize,
                behavior: "smooth"
            });
            break;
        case "goPrev":
            caruselContainer.scrollBy({
                left: -visibleItemsAmount * itemSize,
                behavior: "smooth"
            });
            break;
    }
}

function caruselInitializator(carusel) {
    let container = carusel.querySelector('.carusel__container');
    let controlNext = carusel.querySelector('.carusel__control-next');
    let controlPrev = carusel.querySelector('.carusel__control-prev');

    container.addEventListener('scroll', caruselScrollHandler);
    controlNext.addEventListener('click', caruselControlsHandler);
    controlPrev.addEventListener('click', caruselControlsHandler);

    let containerWidth = container.offsetWidth;

    let items = container.querySelectorAll('.carusel__item');
    let itemWidth = items[items.length - 1].offsetWidth;
    let itemMargin = parseFloat(
        window.getComputedStyle(items[items.length - 1]).marginLeft
    );
    let itemSize = itemWidth + itemMargin;
    
    let visibleItemsAmount = Math.floor(containerWidth / itemSize);

    controlPrev.classList.add('hidden');
    if (items.length < visibleItemsAmount) {
        controlNext.classList.add('hidden');
    }
    
    for (let i = 0; i < items.length; i++) {
        if (i < visibleItemsAmount) {
            items[i].classList.add("visible");
        }
        else {
            items[i].classList.remove("visible");
        }
    }
}

window.onload = () => {
    let carusels = document.querySelectorAll('.carusel, .carusel-book');

    window.addEventListener(
        'resize',
        createCaruselResizeHandler(carusels)
    );

    for (let i = 0; i < carusels.length; i++) {
        caruselInitializator(carusels[i]);
    }
};