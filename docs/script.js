document.addEventListener('DOMContentLoaded', (event) => {
    hljs.highlightAll();

    renderMathInElement(document.body, {
        delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false},
            {left: '\\(', right: '\\)', display: false},
            {left: '\\[', right: '\\]', display: true}
        ],
        throwOnError: false
    });

    const heroElements = document.querySelectorAll("#hero .text-fade-in");
    const heroDelay = 100; 

    heroElements.forEach((el, index) => {
        setTimeout(() => {
            el.classList.add('visible');
        }, heroDelay + (index * 100)); 
    });

    const scrollAnimatedElements = document.querySelectorAll(
        ".title-fade-in, .subtitle-fade-in, .scroll-fade-in, .scroll-zoom-in"
    );

    const observerOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    };

    const scrollObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    scrollAnimatedElements.forEach(el => {
        scrollObserver.observe(el);
    });

    // === 文档页面的 ScrollSpy (滚动监听) ===
    const sections = document.querySelectorAll('.docs-content section');
    const navLinks = document.querySelectorAll('.sidebar-nav .nav-link');

    // 只有在文档页面存在 section 时才运行
    if (sections.length > 0) {
        const observerOptions = {
            root: null,
            rootMargin: '-100px 0px -70% 0px', // 调整触发线，让高亮更自然
            threshold: 0
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // 移除所有 active 类
                    navLinks.forEach(link => link.classList.remove('active'));
                    
                    // 找到对应的链接并添加 active 类
                    const id = entry.target.getAttribute('id');
                    const activeLink = document.querySelector(`.sidebar-nav a[href="#${id}"]`);
                    if (activeLink) {
                        activeLink.classList.add('active');
                    }
                }
            });
        }, observerOptions);

        sections.forEach(section => {
            observer.observe(section);
        });
    }
});