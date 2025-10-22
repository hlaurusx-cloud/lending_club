// EncodeCraft - Advanced Encoding Tool
// Main JavaScript functionality

class EncodeCraft {
    constructor() {
        this.currentAlgorithm = 'base64';
        this.history = JSON.parse(localStorage.getItem('encodecraft_history') || '[]');
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeAnimations();
        this.setupParticleBackground();
        this.loadHistory();
        this.updateAlgorithmInfo();
        this.setupThemeToggle();
    }

    setupEventListeners() {
        // Input handling
        const inputText = document.getElementById('inputText');
        const outputText = document.getElementById('outputText');
        const algorithmSelect = document.getElementById('algorithmSelect');
        const encodeBtn = document.getElementById('encodeBtn');
        const decodeBtn = document.getElementById('decodeBtn');
        const copyBtn = document.getElementById('copyBtn');

        // Real-time encoding/decoding
        inputText.addEventListener('input', () => {
            this.updateCharacterCount();
            this.autoConvert();
        });

        // Algorithm selection
        algorithmSelect.addEventListener('change', (e) => {
            this.currentAlgorithm = e.target.value;
            this.updateAlgorithmInfo();
            this.autoConvert();
        });

        // Encode/Decode buttons
        encodeBtn.addEventListener('click', () => this.encode());
        decodeBtn.addEventListener('click', () => this.decode());

        // Copy functionality
        copyBtn.addEventListener('click', () => this.copyToClipboard());

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case 'Enter':
                        e.preventDefault();
                        this.encode();
                        break;
                    case 'Shift':
                        e.preventDefault();
                        this.decode();
                        break;
                    case 'c':
                        if (e.shiftKey) {
                            e.preventDefault();
                            this.copyToClipboard();
                        }
                        break;
                }
            }
        });
    }

    initializeAnimations() {
        // Animate hero title
        const heroTitle = document.querySelector('.hero-title');
        if (heroTitle) {
            anime({
                targets: heroTitle,
                opacity: [0, 1],
                translateY: [50, 0],
                duration: 1000,
                easing: 'easeOutExpo',
                delay: 300
            });
        }

        // Animate panels
        anime({
            targets: '.panel',
            opacity: [0, 1],
            translateY: [30, 0],
            duration: 800,
            easing: 'easeOutExpo',
            delay: anime.stagger(100, {start: 500})
        });

        // Setup text splitting for animations
        Splitting();
    }

    setupParticleBackground() {
        // p5.js particle background
        new p5((p) => {
            let particles = [];
            const numParticles = 50;

            p.setup = () => {
                const canvas = p.createCanvas(p.windowWidth, p.windowHeight);
                canvas.parent('particle-canvas');
                
                // Create particles
                for (let i = 0; i < numParticles; i++) {
                    particles.push({
                        x: p.random(p.width),
                        y: p.random(p.height),
                        vx: p.random(-0.5, 0.5),
                        vy: p.random(-0.5, 0.5),
                        size: p.random(2, 6),
                        opacity: p.random(0.1, 0.3)
                    });
                }
            };

            p.draw = () => {
                p.clear();
                
                // Update and draw particles
                particles.forEach(particle => {
                    // Update position
                    particle.x += particle.vx;
                    particle.y += particle.vy;
                    
                    // Wrap around edges
                    if (particle.x < 0) particle.x = p.width;
                    if (particle.x > p.width) particle.x = 0;
                    if (particle.y < 0) particle.y = p.height;
                    if (particle.y > p.height) particle.y = 0;
                    
                    // Draw particle
                    p.fill(74, 158, 255, particle.opacity * 255);
                    p.noStroke();
                    p.circle(particle.x, particle.y, particle.size);
                });
            };

            p.windowResized = () => {
                p.resizeCanvas(p.windowWidth, p.windowHeight);
            };
        });
    }

    setupThemeToggle() {
        const themeToggle = document.getElementById('themeToggle');
        const html = document.documentElement;
        
        // Check for saved theme preference
        const savedTheme = localStorage.getItem('encodecraft_theme') || 'dark';
        html.setAttribute('data-theme', savedTheme);
        
        themeToggle.addEventListener('click', () => {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('encodecraft_theme', newTheme);
            
            // Update icon
            const icon = themeToggle.querySelector('i');
            icon.className = newTheme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
        });
    }

    // Encoding Algorithms
    encodeBase64(text) {
        try {
            return btoa(unescape(encodeURIComponent(text)));
        } catch (e) {
            throw new Error('Invalid text for Base64 encoding');
        }
    }

    decodeBase64(text) {
        try {
            return decodeURIComponent(escape(atob(text)));
        } catch (e) {
            throw new Error('Invalid Base64 string');
        }
    }

    encodeURL(text) {
        return encodeURIComponent(text).replace(/[!'()*]/g, (c) => {
            return '%' + c.charCodeAt(0).toString(16).toUpperCase();
        });
    }

    decodeURL(text) {
        try {
            return decodeURIComponent(text.replace(/\+/g, ' '));
        } catch (e) {
            throw new Error('Invalid URL encoded string');
        }
    }

    encodeHex(text) {
        return text.split('').map(char => 
            char.charCodeAt(0).toString(16).padStart(2, '0')
        ).join('').toUpperCase();
    }

    decodeHex(text) {
        try {
            return text.match(/.{2}/g).map(hex => 
                String.fromCharCode(parseInt(hex, 16))
            ).join('');
        } catch (e) {
            throw new Error('Invalid hexadecimal string');
        }
    }

    encodeHTMLEntities(text) {
        const entities = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;',
            '/': '&#x2F;'
        };
        return text.replace(/[&<>"'\/]/g, char => entities[char]);
    }

    decodeHTMLEntities(text) {
        const textarea = document.createElement('textarea');
        textarea.innerHTML = text;
        return textarea.value;
    }

    encodeROT13(text) {
        return text.replace(/[a-zA-Z]/g, char => {
            const start = char <= 'Z' ? 65 : 97;
            return String.fromCharCode(((char.charCodeAt(0) - start + 13) % 26) + start);
        });
    }

    decodeROT13(text) {
        return this.encodeROT13(text); // ROT13 is symmetric
    }

    encodeBinary(text) {
        return text.split('').map(char => 
            char.charCodeAt(0).toString(2).padStart(8, '0')
        ).join(' ');
    }

    decodeBinary(text) {
        try {
            return text.trim().split(/\s+/).map(binary => 
                String.fromCharCode(parseInt(binary, 2))
            ).join('');
        } catch (e) {
            throw new Error('Invalid binary string');
        }
    }

    // Core Functions
    encode() {
        const input = document.getElementById('inputText').value;
        if (!input.trim()) {
            this.showNotification('Please enter text to encode', 'error');
            return;
        }

        try {
            const encoded = this.performEncoding(input, this.currentAlgorithm);
            document.getElementById('outputText').value = encoded;
            this.updateCharacterCount();
            this.addToHistory(input, encoded, 'encode', this.currentAlgorithm);
            this.animateOutput();
            this.showNotification('Text encoded successfully!', 'success');
        } catch (error) {
            this.showNotification(`Encoding error: ${error.message}`, 'error');
        }
    }

    decode() {
        const input = document.getElementById('inputText').value;
        if (!input.trim()) {
            this.showNotification('Please enter text to decode', 'error');
            return;
        }

        try {
            const decoded = this.performDecoding(input, this.currentAlgorithm);
            document.getElementById('outputText').value = decoded;
            this.updateCharacterCount();
            this.addToHistory(input, decoded, 'decode', this.currentAlgorithm);
            this.animateOutput();
            this.showNotification('Text decoded successfully!', 'success');
        } catch (error) {
            this.showNotification(`Decoding error: ${error.message}`, 'error');
        }
    }

    performEncoding(text, algorithm) {
        switch (algorithm) {
            case 'base64': return this.encodeBase64(text);
            case 'url': return this.encodeURL(text);
            case 'hex': return this.encodeHex(text);
            case 'html': return this.encodeHTMLEntities(text);
            case 'rot13': return this.encodeROT13(text);
            case 'binary': return this.encodeBinary(text);
            default: throw new Error('Unknown encoding algorithm');
        }
    }

    performDecoding(text, algorithm) {
        switch (algorithm) {
            case 'base64': return this.decodeBase64(text);
            case 'url': return this.decodeURL(text);
            case 'hex': return this.decodeHex(text);
            case 'html': return this.decodeHTMLEntities(text);
            case 'rot13': return this.decodeROT13(text);
            case 'binary': return this.decodeBinary(text);
            default: throw new Error('Unknown encoding algorithm');
        }
    }

    autoConvert() {
        const input = document.getElementById('inputText').value;
        if (input.trim() && document.getElementById('autoConvert')?.checked) {
            try {
                const encoded = this.performEncoding(input, this.currentAlgorithm);
                document.getElementById('outputText').value = encoded;
                this.updateCharacterCount();
            } catch (error) {
                // Silently fail for auto-convert
            }
        }
    }

    updateCharacterCount() {
        const input = document.getElementById('inputText');
        const output = document.getElementById('outputText');
        const inputCount = document.getElementById('inputCount');
        const outputCount = document.getElementById('outputCount');
        
        inputCount.textContent = input.value.length;
        outputCount.textContent = output.value.length;
    }

    copyToClipboard() {
        const output = document.getElementById('outputText');
        if (!output.value.trim()) {
            this.showNotification('No text to copy', 'error');
            return;
        }

        navigator.clipboard.writeText(output.value).then(() => {
            this.showNotification('Copied to clipboard!', 'success');
            this.animateCopyButton();
        }).catch(() => {
            this.showNotification('Failed to copy text', 'error');
        });
    }

    addToHistory(input, output, operation, algorithm) {
        const historyItem = {
            id: Date.now(),
            input: input.substring(0, 50) + (input.length > 50 ? '...' : ''),
            output: output.substring(0, 50) + (output.length > 50 ? '...' : ''),
            fullInput: input,
            fullOutput: output,
            operation,
            algorithm,
            timestamp: new Date().toLocaleString()
        };

        this.history.unshift(historyItem);
        this.history = this.history.slice(0, 10); // Keep only last 10 items
        
        localStorage.setItem('encodecraft_history', JSON.stringify(this.history));
        this.loadHistory();
    }

    loadHistory() {
        const historyList = document.getElementById('historyList');
        if (!historyList) return;

        historyList.innerHTML = '';
        
        if (this.history.length === 0) {
            historyList.innerHTML = '<div style="color: var(--text-secondary); font-size: 0.9rem; text-align: center; padding: 1rem;">No history yet</div>';
            return;
        }

        this.history.forEach(item => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            historyItem.innerHTML = `
                <div class="history-item-title">
                    <i class="fas fa-${item.operation === 'encode' ? 'arrow-down' : 'arrow-up'}"></i>
                    ${item.algorithm.toUpperCase()} ${item.operation}
                </div>
                <div class="history-item-preview">${item.output}</div>
            `;
            
            historyItem.addEventListener('click', () => {
                document.getElementById('inputText').value = item.fullInput;
                document.getElementById('outputText').value = item.fullOutput;
                document.getElementById('algorithmSelect').value = item.algorithm;
                this.currentAlgorithm = item.algorithm;
                this.updateCharacterCount();
                this.updateAlgorithmInfo();
            });
            
            historyList.appendChild(historyItem);
        });
    }

    updateAlgorithmInfo() {
        const algorithmInfo = {
            base64: {
                description: 'Base64 is a binary-to-text encoding scheme that represents binary data in ASCII format. Commonly used for data transmission and storage.',
                example: 'Hello → SGVsbG8='
            },
            url: {
                description: 'URL encoding replaces unsafe ASCII characters with a "%" followed by two hexadecimal digits. Essential for web development.',
                example: 'Hello World → Hello%20World'
            },
            hex: {
                description: 'Hexadecimal encoding represents binary data in base-16 format. Each byte is represented by two hexadecimal digits.',
                example: 'Hello → 48656C6C6F'
            },
            html: {
                description: 'HTML entity encoding converts special characters to HTML entities, preventing XSS attacks and ensuring proper rendering.',
                example: '<div> → &lt;div&gt;'
            },
            rot13: {
                description: 'ROT13 is a simple letter substitution cipher that replaces each letter with the letter 13 positions later in the alphabet.',
                example: 'Hello → Uryyb'
            },
            binary: {
                description: 'Binary encoding converts text to binary representation, showing the raw binary data of each character.',
                example: 'Hi → 01001000 01101001'
            }
        };

        const info = algorithmInfo[this.currentAlgorithm];
        const descriptionEl = document.getElementById('algorithmDescription');
        const exampleEl = document.getElementById('algorithmExample');
        const exampleTextEl = document.getElementById('exampleText');

        if (descriptionEl) descriptionEl.textContent = info.description;
        if (exampleTextEl) exampleTextEl.textContent = info.example;
        if (exampleEl) exampleEl.style.display = 'block';
    }

    animateOutput() {
        const outputPanel = document.querySelector('.output-textarea').parentElement;
        
        anime({
            targets: outputPanel,
            scale: [0.98, 1],
            duration: 300,
            easing: 'easeOutExpo'
        });
    }

    animateCopyButton() {
        const copyBtn = document.getElementById('copyBtn');
        
        anime({
            targets: copyBtn,
            scale: [1, 1.1, 1],
            duration: 200,
            easing: 'easeOutExpo'
        });
    }

    showNotification(message, type = 'success') {
        const notification = document.getElementById('notification');
        notification.textContent = message;
        notification.className = `notification ${type}`;
        
        // Show notification
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Hide notification after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new EncodeCraft();
});

// Add some utility functions for enhanced functionality
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Enhanced keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + E for encode
    if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
        e.preventDefault();
        document.getElementById('encodeBtn').click();
    }
    
    // Ctrl/Cmd + D for decode
    if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        document.getElementById('decodeBtn').click();
    }
    
    // Ctrl/Cmd + Shift + C for copy
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'C') {
        e.preventDefault();
        document.getElementById('copyBtn').click();
    }
});
