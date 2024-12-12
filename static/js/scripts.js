document.addEventListener('DOMContentLoaded', function() {
    const splitter = document.querySelector('.q-splitter');
    const MIN_PERCENT = 30; // 最小宽度百分比

    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                const beforePanel = splitter.querySelector('.q-splitter__panel.q-splitter__before');
                const afterPanel = splitter.querySelector('.q-splitter__panel.q-splitter__after');
                
                if (beforePanel && beforePanel.style.width) {
                    const currentPercent = parseFloat(beforePanel.style.width);
                    
                    // 检查左面板是否小于最小百分比
                    if (currentPercent < MIN_PERCENT) {
                        beforePanel.style.width = `${MIN_PERCENT}%`;
                        afterPanel.style.width = `${100 - MIN_PERCENT}%`;
                    }
                    
                    // 检查右面板是否小于最小百分比
                    if ((100 - currentPercent) < MIN_PERCENT) {
                        beforePanel.style.width = `${100 - MIN_PERCENT}%`;
                        afterPanel.style.width = `${MIN_PERCENT}%`;
                    }
                }
            }
        });
    });
    
    observer.observe(splitter, {
        attributes: true,
        subtree: true,
        attributeFilter: ['style']
    });

    // 监听窗口大小变化
    window.addEventListener('resize', function() {
        const beforePanel = splitter.querySelector('.q-splitter__panel.q-splitter__before');
        const afterPanel = splitter.querySelector('.q-splitter__panel.q-splitter__after');
        
        if (beforePanel && beforePanel.style.width) {
            const currentPercent = parseFloat(beforePanel.style.width);
            
            // 如果任一面板小于最小百分比，重置为中间位置
            if (currentPercent < MIN_PERCENT || (100 - currentPercent) < MIN_PERCENT) {
                const middlePercent = 50;
                beforePanel.style.width = `${middlePercent}%`;
                afterPanel.style.width = `${100 - middlePercent}%`;
            }
        }
    });
});