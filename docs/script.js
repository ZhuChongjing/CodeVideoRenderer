document.addEventListener('DOMContentLoaded', (event) => {
    // 1. 启用 highlight.js
    hljs.highlightAll();

    // 2. ----------------------------------
    // A. 英雄区文本动画 (只触发一次)
    // ----------------------------------
    const heroElements = document.querySelectorAll("#hero .text-fade-in");

    // 为英雄区设置一个短暂的延时，确保在页面加载后立即触发
    const heroDelay = 200; 

    heroElements.forEach((el, index) => {
        setTimeout(() => {
            el.classList.add('visible');
        }, heroDelay + (index * 150)); // 依次延迟显示
    });

    // 3. ----------------------------------
    // B. 通用滚动动画 (Intersection Observer)
    // ----------------------------------

    // 收集所有需要滚动动画的元素
    const scrollAnimatedElements = document.querySelectorAll(
        ".title-fade-in, .subtitle-fade-in, .scroll-fade-in, .scroll-zoom-in"
    );

    const observerOptions = {
        threshold: 0.1, // 元素 10% 进入视口时触发
        rootMargin: "0px 0px -100px 0px" // 底部提前 100px 触发
    };

    const scrollObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // 如果元素可见，添加 visible 类
                entry.target.classList.add("visible");
                // 停止观察，避免重复触发
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    scrollAnimatedElements.forEach(el => {
        scrollObserver.observe(el);
    });
});